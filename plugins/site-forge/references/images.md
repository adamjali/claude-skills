# Images & media assets

How to place images so they never distort or cause layout shift, plus the ffmpeg
recipes for prepping them.

## Contents
- [The height:auto stretch fix (do this first)](#the-heightauto-stretch-fix)
- [object-fit & aspect-ratio](#object-fit--aspect-ratio)
- [Lazy-loading & CLS](#lazy-loading--cls)
- [ffmpeg: crop / scale / convert](#ffmpeg-crop--scale--convert)
- [Favicons (macOS, no ImageMagick)](#favicons)

---

## The height:auto stretch fix
**Always include this in your base CSS:**

```css
img{display:block;max-width:100%;height:auto}
```

Why it matters (this was a real shipped bug): if an `<img>` has BOTH `width` and
`height` HTML attributes (good — they reserve space and prevent layout shift) and
your CSS sets `width:100%` but **not** `height`, the browser keeps the *attribute*
height fixed while the width scales to the container — so the image renders
stretched (e.g. a 430×320 photo rendered 532×320, squashing faces sideways). The
one-liner `height:auto` lets the height follow the width and preserve the aspect
ratio. Put it on the base `img` rule so it can never recur; elements that truly
need a fixed box (`object-fit` covers, below) override it explicitly.

---

## object-fit & aspect-ratio
For any image that must fill a fixed box (hero background, card thumbnail,
before/after), give it an explicit height (or a sized parent) and `object-fit`:

```css
.hero .bg img{width:100%;height:120%;object-fit:cover}  /* fills, crops, never distorts */
.card img{width:100%;aspect-ratio:4/3;object-fit:cover} /* fixed box via aspect-ratio */
```

`object-fit:cover` scales to fill and crops the overflow — the correct default
for photos in a fixed frame. These rules set height explicitly, so they're immune
to the stretch bug above.

Keep the `width`/`height` **attributes** on the tag matching the file's real
pixels (e.g. `width="430" height="320"`) — the browser uses their ratio to
reserve space and avoid layout shift, even when CSS resizes the element.

---

## Lazy-loading & CLS
```html
<img src="photo.jpg" alt="descriptive alt" width="860" height="646"
     loading="lazy" decoding="async" />
```
- `loading="lazy"` on below-the-fold images; **omit it for the hero/LCP image**
  (lazy-loading the first paint hurts Largest Contentful Paint).
- `decoding="async"` keeps decode off the main thread.
- Real `width`/`height` attributes = reserved space = no Cumulative Layout Shift.

---

## ffmpeg: crop / scale / convert
Prep source images/video at native quality. `-q:v 2` is high-quality JPEG.

```bash
# Uniform upscale to a target width, height auto (even number) — NEVER distorts:
ffmpeg -y -i in.jpg -vf "scale=860:-2" -q:v 2 out.jpg

# Tight crop: crop=W:H:X:Y (region WxH starting at x,y). Native res, no upscale:
ffmpeg -y -i in.jpg -vf "crop=430:320:42:60" -q:v 2 out.jpg

# Match one image's dimensions to another (e.g. before/after pair):
ffmpeg -y -i worn.jpg -vf "scale=1920:1275" -q:v 2 worn-out.jpg

# Extract scroll-scrub frames from a clip (see scroll-effects.md for usage):
mkdir -p seq
ffmpeg -y -i clip.mp4 -vf "fps=12,scale=1200:-2" -q:v 3 "seq/frame_%03d.jpg"
```
Note `scale=W:-2` (uniform, height auto-even) vs `crop=W:H:X:Y` (cut a region).
Use `scale` to resize, `crop` to reframe — mixing them up is the usual cause of a
"stretched" or "cut wrong" image.

---

## Favicons

> **NEVER use a `data:image/svg+xml;base64,...` href.** It renders fine in a browser
> tab, so the bug hides — but Google's [favicon-in-search docs](https://example-business.com/search/docs/appearance/favicon-in-search)
> require that *"Googlebot-Image must be able to crawl the favicon file"* and that
> `href` be a relative or absolute **URL**. A data-URI is neither, so **Google shows a
> generic globe next to the site in search results.** A 2026-07-24 fleet audit found
> 13 of 14 client sites broken this way. Ship real files, always.

Google's requirements: square (1:1), **at least 8x8**, they recommend **>48x48**, any
valid favicon format, and a **stable URL** (don't churn the path).

`magick` (ImageMagick 7) handles SVG fine on this Mac. Generate the full set from one
brand SVG:

```bash
mkdir -p assets
magick -background none icon.svg -resize 512x512 assets/icon-512.png
for s in 192 180 96 48 32 16; do magick assets/icon-512.png -resize ${s}x${s} /tmp/i-$s.png; done
cp /tmp/i-192.png assets/icon-192.png
cp /tmp/i-180.png assets/apple-touch-icon.png
magick /tmp/i-16.png /tmp/i-32.png /tmp/i-48.png favicon.ico   # multi-size .ico
cp icon.svg assets/icon.svg
```
Fallback if `magick` renders a black square (older builds sometimes do), use Quick Look:
```bash
qlmanage -t -s 512 -o /tmp icon.svg      # -> /tmp/icon.svg.png
sips -z 180 180 /tmp/icon.svg.png --out assets/apple-touch-icon.png
```

Link them in `<head>` — `favicon.ico` at the **root**, which is also where Google and
every browser probe by default:
```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#yourbrand">
```

`site.webmanifest` (192 + 512 + a maskable):
```json
{ "name":"Full Business Name", "short_name":"Brand", "start_url":"/",
  "display":"standalone", "background_color":"#bg", "theme_color":"#brand",
  "icons":[{"src":"/assets/icon-192.png","type":"image/png","sizes":"192x192"},
           {"src":"/assets/icon-512.png","type":"image/png","sizes":"512x512"},
           {"src":"/assets/icon-512.png","type":"image/png","sizes":"512x512","purpose":"maskable"}]}
```
**Netlify serves `.webmanifest` as `application/octet-stream`** unless you say otherwise.
Add to `_headers`:
```
/site.webmanifest
  Content-Type: application/manifest+json; charset=utf-8
```

### Site name in Google results (ship with the favicon)
Google's [site-names doc](https://example-business.com/search/docs/appearance/site-names)
says **`WebSite` structured data is the most important** signal, and it also weighs
`og:site_name`, `<title>`, and headings. Ship all four:
```html
<meta name="application-name" content="Brand">
<meta property="og:site_name" content="Brand">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite",
 "name":"Brand","alternateName":"Full Legal Business Name","url":"https://example.com/"}
</script>
```
Only one site name per hostname, and it must match how the home page refers to itself.
