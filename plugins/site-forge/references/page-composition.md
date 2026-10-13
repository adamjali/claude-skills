# Page composition — why a page feels full or empty

*Written 2026-07-28 after Adam looked at a Terra-structured build next to five of
our own and said the earlier ones "all feel empty." Both halves of that
conversation are recorded here: what he noticed, and what the measurable cause
turned out to be. Read this BEFORE laying out any marketing page.*

---

## The single most useful rule

**No band may be text-only. Never two un-illustrated sections in a row.**

This is the whole diagnosis in one line. Our "empty" builds had entire sections
with zero imagery: a differentiation section, a process section, a stats band, an
FAQ, a features grid. Each was a heading, a paragraph, and four bordered boxes of
text.

> A card containing only text is still a text section wearing a card costume.
> Four of them in a row is where "empty" comes from.

Fix by giving every band one of: a photograph, a masked image, an illustrated
card grid, a diagram, an oversized numeral, or a layered composition. If a band
genuinely has nothing to show, merge it into a neighbouring band rather than
letting it sit as its own screenful of prose.

---

## The four devices that actually do the work

### 1. Layering — the most underrated one
In the flat builds, every element sat in its own lane, in normal flow, nothing
overlapping anything. That reads as a stack of divs because it literally is one.

Give each major section **one deliberate overlap**: a card straddling the edge of
a photo, a badge crossing a section divider, an image breaking its container.

```css
.media{position:relative}
.float-card{position:absolute;left:34%;bottom:6%;z-index:3;
  background:#fff;border-radius:12px;box-shadow:0 16px 40px rgba(0,0,0,.16);padding:16px 20px}
```
Overlap reads as composition. No overlap reads as output.

### 2. Silhouette variety — rotate the mask shapes
When every element is the same rounded rectangle, the eye has nothing to catch
and scrolls straight past. Rotate through four masks across a page:

```css
.m-circle{border-radius:50%;aspect-ratio:1;overflow:hidden}
.m-arch{border-radius:50% 50% 10px 10px / 42% 42% 10px 10px;aspect-ratio:4/5;overflow:hidden}
.m-blob{border-radius:58% 42% 46% 54% / 44% 52% 48% 56%;aspect-ratio:5/4;overflow:hidden}
.m-pair{position:relative;aspect-ratio:1}          /* two overlapping circles */
.m-pair .a{position:absolute;inset:0 0 12% 18%;border-radius:50%;overflow:hidden}
.m-pair .b{position:absolute;left:0;bottom:0;width:46%;aspect-ratio:1;
  border-radius:50%;overflow:hidden;border:7px solid #fff}
```
All masked images need `img{width:100%;height:100%;object-fit:cover}` and, if
wrapped in `<picture>`, `picture{display:contents}`.

### 3. Section transitions — bands must not butt flat together
A flat colour change between bands is the "just lines and grids" feeling. An
organic divider costs one inline SVG:

```html
<div class="wave"><svg viewBox="0 0 1440 110" preserveAspectRatio="none" aria-hidden="true">
  <path fill="#fff" d="M0,54 C220,110 420,6 720,44 C1010,80 1220,18 1440,52 L1440,110 L0,110 Z"/>
</svg></div>
```
```css
.wave{position:absolute;left:0;right:0;bottom:-1px;z-index:2;line-height:0;pointer-events:none}
.wave svg{width:100%;height:clamp(50px,7vw,104px);display:block}
```
Put it at the foot of any photo-background header. Vary the path per project so
it is not the same curve every time.

### 4. Photo-background headers on EVERY page
Not just the homepage. Every inner page gets a reduced-height version of the same
device: photo, directional dark gradient, breadcrumb, serif h1, two CTAs, wave.
This is most of what makes a multipage set feel like one designed site rather
than a homepage plus a pile of documents.

---

## The correction: grids are not the problem

Adam's read was "not square or rectangle or grid, which is boring." The half of
that which is wrong matters, because acting on it would remove a pattern that
works.

**The strongest section on the reference build is a 2x2 grid of rectangles.** It
works because every cell carries a photograph with a gradient scrim, a title and
a circular arrow button. Same geometry as our flat builds, opposite result.

> The rule is not "avoid grids." It is **"a grid needs images in its cells, or it
> should not be a grid."**

---

## The mistake to not repeat: density optimisation flattened the pages

This is on me and it is the uncomfortable half of the diagnosis.

a junk-removal client was compressed from 13.4 screens to 9.4, seven section-padding values
collapsed to one, type snapped to a six-level ramp, and whole sections deleted.
Every move was defensible alone. Together they produced a page that was tighter
and **flatter**.

The metrics being optimised (words per screen, count of distinct paddings,
sibling-page overlap) measure **discipline**, and discipline is not the same
thing as quality. Uniformity is what those numbers reward, and uniformity is
precisely what makes a page feel like a spreadsheet.

The density spec even said `Do not make it uniform. Dense plus flat is the wall.`
That line was read and then walked straight into, and the numbers were reported
as progress.

**Practical resolution:** keep the type ramp and the readability floors, they are
real. But **one section-padding value is a target for a text-heavy article page,
not for a marketing page.** A marketing page wants rhythm: a tall hero, a medium
split, a tight card grid, a tall photo band. Vary it deliberately.

---

## Old-school chrome reads as professional, and here is why

Adam liked the utility bar and the hover dropdowns. They are not nostalgia, they
are a **scope signal**.

A flat nav of five anchor links says "this is one page." A nav with four
dropdowns of three to four children each says "there are nineteen pages behind
this." For a demo site whose job is to make a small operator look established,
that signal is doing more work than any animation.

Include: a slim utility bar above the nav (service areas, reviews, phone), a
sticky white nav with the logo left, hover dropdowns centre, an outlined phone
pill and a solid CTA right.

---

## Pre-ship composition check

Run alongside the quality checklist:

- [ ] Zero text-only bands. Every section has a visual.
- [ ] No two consecutive bands share the same layout shape.
- [ ] At least three different photo mask shapes used across the page.
- [ ] At least two deliberate overlaps (card over photo, badge over divider).
- [ ] Every photo-background header ends in an organic divider.
- [ ] Every inner page has a photo header, not just the homepage.
- [ ] Section heights vary. If every band measures within 10% of the others, the
      page will read flat no matter how good the content is.
- [ ] Nav implies more depth than a single page.
- [ ] Every card grid has images in its cells.

---

## Mandatory interactive staples (every build, no exceptions)

Added 2026-07-29 after Adam listed what was missing. These are not optional
flourishes; a build without them reads as unfinished.

| Staple | Behaviour required |
|---|---|
| **Review carousel** | seamless-infinite, native-scroll, pointer-drag, vertical-wheel, AND prev/next buttons |
| **Sideways marquee** | same engine, gentle autoplay drift, drag + wheel, **no** buttons |
| **Nav loading state** | top progress bar + pending link + spinner on `.btn`; ONE at a time, a new click overrides the last |
| **Service-area map** | interactive SVG, hoverable/focusable/clickable pins, live info panel, coverage radius |
| **Themed form controls** | custom-styled `select` (native arrow removed, SVG chevron) and a **label-as-button file control** showing the chosen filename |
| **Multipage** | hubs + nested children, full SEO and local SEO on every page |

One rail engine drives both the carousel and the marquee: clone the track once,
wrap at `scrollWidth/2`, and cancel a click when the pointer moved more than
~6px so a drag never follows a link.

```js
rail.addEventListener('click', e => { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
```

The native `<input type=file>` is never shown. Hide it and drive it from a
`<label for>` styled as a dashed drop target that swaps to the filename on
change. The UA file button cannot be themed and looks a decade old next to
everything else.

---

## Dividers belong BETWEEN sections, not just under the hero

One wave under the hero and flat joins everywhere else is the giveaway. Vary the
shape and vary where it appears:

- **wave** (organic curve) under photo headers
- **angled cut** — `<polygon points="0,70 1440,10 1440,70">` into a tinted band
- **stepped/notched** — a stair-step `<path>` into a dark band, reads industrial
- **inverted curve** — the same wave rotated 180deg coming *out* of a band

Give each project its own curve values. Reusing the exact same path across
clients is how a template starts to show.

---

## Copy: let it sell itself

Adam, 2026-07-29: *"NO 'this is not a stock photo' like thats not impressive,
stop being so dramatic... to the point is better, let it sell itself."*

Cut every line that congratulates the page on its own contents or announces that
something ordinary is remarkable. Offenders to grep for:

- "this is not a stock photo", "an actual X job"
- "That is the whole advantage", "That is the actual problem", "is the whole product"
- "genuinely annoying", "A striking number", "the maths almost nobody runs"

State the fact and stop. *"A screened lanai, packed wall to wall, cleared and
swept in one visit"* beats the same sentence with *"this is a real job, not a
stock photo"* bolted on. The photograph already proves it.

---

## Bugs this pass surfaced (check for these every time)

- **Ghost button invisible on inner heroes.** The rule was
  `.dark .btn-out, .hero .btn-out{color:#fff}` but inner pages used `.phero`, so
  the button fell back to `currentColor` = dark on a dark photo. **Scope hero
  button colour by every hero class you actually ship.**
- **A mask whose children are ALL absolutely positioned collapses to height 0.**
  `aspect-ratio` has no in-flow content to resolve against, the mask disappears
  and any floating card positioned against it orphans into blank space. Keep one
  child in flow.
- **Masks become enormous when a split collapses.** `aspect-ratio:1` at full
  container width is a giant circle on a phone. Cap with
  `max-width:min(400px,74vw); margin-inline:auto` under the breakpoint.
- **Curved `textPath` inside a square plate clips at the corners.** A circular
  medallion has no corners to clip against; prefer it for seals.
- **Generated pages need a manual pass.** A generator guarantees consistency,
  not quality: it will happily emit a floating card with nothing behind it.
  After generating, open several pages and look.

---

## Band tone must ALTERNATE. Never dark-to-dark.

Adam, 2026-07-29: *"in general alt is better than dark to dark."*

Two photo-backed dark bands in a row merge into one long smear with a visible
seam, and no divider rescues it. Audit the whole page as a tone string before
shipping:

```python
DARK={'statband','faqband','whyband','dark'}   # a red/brand band is its own tone
seq=['R' if 'ctared' in c else ('D' if set(c.split())&DARK else 'L')
     for c in re.findall(r'<section class="([^"]*)"', html)]
assert 'DD' not in ''.join(seq)
```

`LLDLDLLD` is healthy. `LLDDLLDD` is not. Fix by reordering bands (move a light
band between them) or by converting one to a light variant that still carries
imagery, not by adding a divider.

---

## "Staple" means once per SITE, not once per page

Corrected by Adam after the marquee shipped on all 17 pages. A marquee on every
page is repetition, not a staple. Same for reviews: **the same four quotes on
twelve pages is duplicate content, not social proof.** Reviews belong on the
homepage, a dedicated reviews page, and About. Nowhere else.

Place a marquee where the join is otherwise plain, and make it visibly move.
`0.35px/frame` (~22px/s) reads as static; **~0.9px/frame (~56px/s)** is a calm,
visible drift.

---

## Voice: first person, plain, no horn-tooting

Adam, 2026-07-29: *"everything should be in first person please, we and such,
and keep it simple and straight forward, no making a big deal out of nothing or
tooting own horn."*

Write as the business: *"we answer our own phone"*, not *"he answers his own
phone"*. **Customer reviews stay verbatim** even when they refer to the owner in
third person, because they are quotations and editing them would be fabrication.
Convert only our own copy.

---

## A native `<select>` popup cannot be themed

`appearance:none` styles the closed control only. The option list is drawn by the
OS and CSS cannot touch it. If a themed dropdown is required, build a listbox:
keep the real `<select>` in the DOM (so the form still posts and works with JS
off), hide it, and drive it from a `<button aria-haspopup="listbox">` plus a
`<ul role="listbox">`.

---

## Ghost buttons: use a variable, never a class list

`.dark .btn-out, .hero .btn-out {color:#fff}` shipped an invisible button THREE
separate times as new dark bands were added (`.phero`, `.statband`, `.whyband`).
Invert the dependency so new bands opt in automatically:

```css
.btn-out{color:var(--ghost, var(--ink));border-color:currentColor}
.btn-out:hover{background:var(--ghost, var(--ink));color:var(--ghost-ink, var(--paper))}
.hero,.dark,.phero,.statband,.faqband,.whyband,.ctared{--ghost:#fff;--ghost-ink:var(--ink)}
```

---

## More bugs worth grepping for

- **Class-name collisions across unrelated components.** A `.rev` modifier meaning
  "reversed split" collided with `.rev` meaning "review card", so every reversed
  split silently became `display:flex` with a white card background and the photo
  dropped below the text. It looked like a dozen separate layout bugs. **Namespace
  modifiers** (`.split.flip`, not `.split.rev`).
- **`Cache-Control: immutable` on JS means deploys do nothing.** `/assets/*` with
  `max-age=31536000, immutable` served a stale `app.js` for several deploys, so
  every JS fix appeared to fail. Scope immutable to images only and version the
  script (`app.js?v=<hash>`).
- **A `frame-src`-less CSP silently blocks any map embed.** If a map is required,
  add `frame-src https://www.google.com https://example-business.com` and verify on
  the live response header, not in the source file.
- **Map embeds centre on the SERVICE AREA, never the owner's address.** A
  service-area business run from home must not have its street pinned.
- **An absolutely-positioned overlay paints over content** unless the content gets
  `position:relative; z-index`. A stripe texture ended up on top of the buttons.
- **Give each service page a real reference block**, different per page: load
  sizes, doorway widths, mattress dimensions, what the county will not collect.
  Proportional bars beat prose and are genuinely useful rather than filler.

---

## Five more that cost a full review round

**Namespace your modifier classes.** `.split.rev` (reversed split) collided with
`.rev` (review card), so every reversed split silently inherited
`display:flex; background:#fff; padding:26px; border` and rendered as a white card
with the photo dropped below the text. It presented as a dozen unrelated layout
bugs across many pages. Prefix or pick distinct words: `.split.flip`, not `.split.rev`.
Before shipping, grep every modifier against the component classes:

```bash
comm -12 <(grep -oE '^\.[a-z-]+' style.css | sort -u) <(grep -oE '\.[a-z-]+\b' modifiers | sort -u)
```

**One shared chart component across N pages is a template, not a visual.** Feeding
different numbers into the same bar chart on nine service pages reads as filler and
Adam called it immediately. Give each page a diagram that suits *its own question*:
a trailer filling up, doorway widths to scale, mattresses side by side, a donut of
how the visit splits, a garage floor plan, unit footprints, a gantt, a
will-take/won't-take pair, a 24-hour dial.

**Never put a text label inside a data-driven shape.** Bar and zone widths come from
the data; the label does not, so it overflows the moment a value is small or a word
is long. Put labels in a fixed left column (gantt), beneath the shape (scaled
rectangles), or in a legend beside the drawing (floor plan).

**Animate height with `grid-template-rows: 0fr → 1fr`, never `max-height`.**
Animating a layout property thrashes layout every frame. With `li` as the grid
container the markup needs no wrapper:
```css
.menu > li{display:grid;grid-template-rows:auto 0fr;transition:grid-template-rows .26s}
.menu > li.open{grid-template-rows:auto 1fr}
.sub{overflow:hidden;min-height:0}
```

**Check the nav row fits before assuming the menu is at fault.** A reported "menu cut
off" was actually logo + a full-size CTA + burger exceeding the viewport, pushing the
burger off-screen. Below ~600px drop the nav CTA entirely: a sticky bottom action bar
and the open menu already carry it.


## Diagrams and illustrations (a staple on every site)

Every service/topic page gets a visual built for **that page's own question**. One shared
chart fed different numbers is a template, not a visual, and reads as one. If a diagram
could be dropped onto another page unchanged, it is filler.

**Rejected on sight (all of these were shipped once and sent back):**

| Lazy | Build this instead |
|---|---|
| Flat percentage bars | The real object at four states — a trailer at 18/34/58/100% fill, junk stacked in the loaded part |
| Donut "how the day splits" | A plan of the space worked front-to-back: cleared / working / not-seen-yet, which is *why* a packed garage quotes as a range |
| Two facing lists, ticks vs crosses | The kerbside pile drawn once, split down the middle: county takes the vegetation, everything else sits |
| Numbers-only chart | Doorways drawn to a shared scale with the actual sofa laid across them, green where it clears, red where it comes apart |
| Same shape reskinned per page | Palm with the 9-and-3 cut line; soil cross-section showing root depth; tree with cost concentrated at the sectioned takedown |

**Rules that keep them honest**

- **Derive geometry from real numbers.** A 30in door is `30/96` of the garage width. A trunk
  ring narrows as the trunk tapers, or it visibly overhangs the lower trunk.
- **No label may sit over the artwork.** Give it its own gutter above/below the drawing, put a
  plate behind it, or move the fact into the legend. Centring a caption on a fanned canopy
  buries it every time.
- **Tighten the `viewBox` to the content bounding box.** A map authored at `0 0 900 760` whose
  shapes only occupy `x 215..685` renders at ~half size inside its own padding. Tightening it
  was a **1.85x area gain** for one attribute, and flipped the aspect so it finally filled the
  column. Measure the bbox, do not eyeball it.
- **Watch what the aspect ratio does to the row.** After tightening, that same map went
  portrait and ballooned the section to 1272px. Cap the width so the height lands where you
  want it.
- **Validate every SVG parses as XML before shipping** (`ElementTree.fromstring`). A malformed
  path renders as nothing and screenshots of a hidden automation tab will not tell you.
- **Pair every diagram with a plain-words legend.** The colours mean nothing on their own.

**Third-party map embeds:** the keyless Google embed (`?q=...&output=embed`) geocodes and
outlines exactly ONE place.

**That is a FEATURE when the service area IS one place.** a small-engine client serves
an inland rural county, so `?q=an inland rural county+County,+my state&output=embed&z=9` outlines it correctly:
no API key, no billing, no My Maps, no upload step for the user, and no account display name
to hide. **Check the shape of the service area before reaching for My Maps** — the KML route
below exists for MULTI-place areas only, and running it for a single county is wasted work
plus an unnecessary manual upload.

The one-place limit only bites on a MULTI-place area. A red ring around the home city next
to copy that says "four counties" contradicts the copy — drop the `q=` and centre on the region instead. Outline the
full service area on your own SVG map, where you control it, and highlight every county you
actually serve rather than just the base.


## Building the service-area SVG (never hand-draw the polygon)

A hand-drawn county outline reads as exactly what it is. Pull the real geometry:

```python
# US Census cartographic boundary file, keyed by 5-digit FIPS. Land-clipped.
curl -s -o counties.json https://example-business.com/plotly/datasets/master/geojson-counties-fips.json
# ST: an inland rural county 12055, the exurban county 12101, the coastal county 12103, the core metro county 12057, the rural county 12053
```

**Verify the polygon before you draw it.** Shoelace the ring, convert to sq mi, and compare
against the county's published area. an inland rural county came out at 1091 against a published
1,018 land + 88 water = 1,106 total, which confirms the correct inland boundary. The
water-inflation problem in the recipe above is a COASTAL issue (territorial water); an
inland county legitimately contains its own lakes.

Project with a `cos(lat)` correction or the county comes out stretched east to west:

```python
kx = math.cos(math.radians(LAT_CENTRE))
X = PAD + (lon - LON_MIN) * kx / ((LON_MAX-LON_MIN)*kx) * CW
Y = PAD + (LAT_MAX - lat) / (LAT_MAX-LAT_MIN) * CH
```

Then add real geography, not decoration: the major lakes at their true centres sized from
published surface acres, and the highway following the towns it actually connects.

**Label rules, learned the hard way over three rounds:**
- Set each label's side (`L`/`R`/`C`) and vertical offset **explicitly**. An automatic
  "label goes right if x < 62% of width" rule collided *a nearby town* with *an inland town*
  and *Sun 'n Lake* with *a nearby town*.
- **Measure ALL text pairs, not just the town labels.** The second round still shipped a
  *Lake Jackson* / *a nearby town* overlap because the check only compared `.mpin text` against
  each other and ignored the lake and road labels.
- **Do not label every minor feature.** Naming three lakes caused two of the collisions;
  naming only Istokpoga fixed them and reads cleaner. Small lakes are obviously water
  without a name on them.
- Keep the road label in open land, not on the boundary stroke.
- Give labels `paint-order:stroke` with a background-coloured stroke so they stay legible
  wherever they land.

```js
// run this, do not eyeball it
const t=[...svg.querySelectorAll('text')].filter(x=>!x.getAttribute('transform'))
  .map(x=>{const b=x.getBBox();return{n:x.textContent,x1:b.x,x2:b.x+b.width,y1:b.y,y2:b.y+b.height}});
for(let i=0;i<t.length;i++)for(let j=i+1;j<t.length;j++){const a=t[i],b=t[j];
  if(a.x1<b.x2&&b.x1<a.x2&&a.y1<b.y2&&b.y1<a.y2) console.warn('OVERLAP',a.n,b.n)}
```

**A `frame-src`-less CSP silently blocks any map embed.** Add
`frame-src https://www.google.com https://example-business.com` and verify on the live response
header, not in the source file.

---

### Service-area maps on Google My Maps (the repeatable recipe)

**Only for a MULTI-place service area.** For a single county or city, use the keyless
`?q=` embed above and skip all of this.

The keyless `?q=...&output=embed` map outlines exactly ONE geocoded place. For a multi-county
service area, build a **Google My Map** and embed that instead: free, no API key, no billing.

1. Pull county polygons from the Census. **Use the cartographic boundary files, NOT TIGER/Line.**
   TIGER is the *legal* boundary and coastal counties legally own their territorial water, so
   the polygons run out into the Gulf and the bays and the map looks broken. Cartographic
   boundary files are clipped to the shoreline.
   Land-clipped source that works: `https://example-business.com/plotly/datasets/master/geojson-counties-fips.json`
   (keyed by 5-digit FIPS, e.g. ST the exurban county `12101`, the coastal county `12103`, the core metro county `12057`, the rural county `12053`).
2. **Verify before importing: compare polygon area to published land area.** This catches the
   water bug in seconds where eyeballing a coastline does not. the coastal county measured **866 sq mi**
   on TIGER against **274 sq mi** of real land; the cartographic file came in at 334.
   Also point-in-polygon a few known towns to rule out an offset.
3. Emit KML with `<PolyStyle>`/`<LineStyle>` in `aabbggrr` (site lime `#7DC242` -> `7d42C27D`).
   Handle MultiPolygon via `<MultiGeometry>` — the coastal county is mainland + barrier islands and
   collapses into a blob over the water if you only take the first ring.
4. My Maps -> Import -> Browse. **The file picker is a native OS dialog that browser automation
   cannot drive** — prep everything, drop the .kml in ~/Downloads, and hand the user that one click.
5. Share -> "Anyone with this link can view". Without it the embed is blank. Leave "let others
   search for and find this map" OFF; the embed does not need it.
6. Embed `https://www.google.com/maps/d/embed?mid=<MID>` and allow `https://www.google.com`
   in the CSP `frame-src`.

Caveat to tell the client: the free embed shows a header with the map title and the **Google
account display name** of whoever made it, plus "made with Google My Maps". Not removable.
