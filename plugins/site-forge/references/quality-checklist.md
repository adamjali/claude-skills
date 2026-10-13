# Quality checklist — run before shipping

Every item here is a bug that actually bit on a real build. Walk the list after
the site looks done but before deploy. Each is: **the symptom → why → the fix.**

## Contents
- [SEO + deploy verification, on the LIVE site](#seo-live)
- [Content must exist in the HTML, not only after JS](#crawlable-html)
- [Structured data is not optional](#structured-data)
- [The social card is a staple](#social-card)
- [Deploy from a clean dist/](#clean-publish)
- [Layout & CSS](#layout--css)
- [The "Adam always wants this" audit](#always-wanted)
  - [Before you edit a CSS rule — three greps](#css-collisions)
- [JavaScript](#javascript)
- [Images & media](#images--media)
- [Forms & deploy](#forms--deploy)
- [Local-service conversion](#local-service-conversion-added-2026-07-28)
- [Motion & loading](#motion--loading)
- [Multi-page consistency](#multi-page-consistency)
- [Measure, don't eyeball](#measure)
- [Verifying in an automation browser](#automation-verify)
- [Final sweep](#final-sweep)

## Layout & CSS

**Content touching the screen edge on mobile** — A more-specific rule silently
clobbered the gutter. e.g. `.wrap{padding:0 32px}` gives the gutter, but a
section did `.cta .inner{padding:110px 0}` (note the `0` horizontal) which, being
more specific, won set horizontal padding to 0. On desktop the centered max-width
hid it; on mobile the text jammed the edge.
*Fix:* give every full-bleed inner its own horizontal padding at each breakpoint
(`padding:84px 32px` → `60px 20px` → `52px 16px`), and grep for `padding:.* 0}`
on layout containers.

**Duplicate / overriding rules** — Two rules set the same property on the same
selector; the later one wins by accident. *Fix:* one source of truth per
property; search the stylesheet for the selector before adding a second rule.

**Inconsistent spacing system** — Random px values everywhere read as sloppy.
*Fix:* a small spacing scale (or CSS vars) and reuse it; comfortable mobile
gutters (16–20px) and section rhythm.

**CSS class-name collision across components** — The same class name carries two
unrelated rulesets, and whichever loads/applies last wins. Real failure: an
image-fade helper named `.pre` collided with a preloader `.pre`
(`position:fixed; inset:0`) — loading images briefly rendered as **full-screen
overlays** on first paint, then "fixed itself on reload" because cached images
skip the JS that adds the class, so the collision never re-triggered.
*Fix:* grep every class for use by two different components; namespace component
classes so they can't clash (`.imgfade`, not a generic `.pre`).

**Mobile nav dropdown hides its own links** — Stacking the open menu as two
`position:absolute` blocks pinned at the same `top` overlaps them, so the CTAs
cover the nav links. *Fix:* on open, lay the menu out with flex-wrap and
full-width rows so links stack above CTAs in normal flow
(`.nav.open .container{flex-wrap:wrap}` + full-width children), not two absolute
layers at one offset.

### Before you edit a CSS rule — three greps {#css-collisions}
*Five collisions in one a junk-removal client build. This is the dominant bug class in a
hand-written stylesheet, not an occasional one, and every instance cost more than
the grep would have.*

**1. Is this selector declared more than once, and is my override AFTER the base rule?**
The last one wins, so an edit to the first is dead on arrival. **This includes media
queries: a media rule placed ABOVE the base rule it overrides never fires.** Equal
specificity, earlier position, base wins. `@media(max-width:1320px){.phpill{display:none}}`
written above `.phpill{display:inline-flex}` left the nav overflowing every phone viewport.
```bash
grep -n '^\.hero{\|[ ,]\.hero{' index.html    # expect exactly ONE top-level hit
```
Three competing `.hero{}` rules silently re-added an `overflow:hidden` that had
just been removed; the fix "didn't work" twice before the duplicate was found.

**2. Does a rule exist for a component that no longer exists?**
Delete a component's CSS when you delete the component. A dead `.seal` (an old
badge) kept `height:64px` on a stamp whose SVG rendered at 150px, so every
`getBoundingClientRect()` was against a box less than half the real size and
three position fixes in a row landed wrong.
```bash
# for each generic-sounding class, confirm it still has a user
for c in seal badge stamp card rev pre; do
  echo "$c: $(grep -c "class=\"[^\"]*\b$c\b" *.html) users"
done
```

**3. Does this component have a mobile branch that relies on the property I am changing?**
A fix at one breakpoint can silently break the other. Adding `align-items:center`
to `.menu > li` fixed a caret wrapping on desktop and broke the entire mobile
menu, because the mobile branch collapses submenus with `grid-template-rows` and
that only works on stretched grid items. Both rules read as correct alone.
```bash
grep -n '\.menu > li' index.html     # see EVERY branch before editing one
```
After changing a shared component rule, **re-verify the other breakpoint** before
shipping.

**Symptom → cause, when a CSS fix appears to do nothing:**

| Symptom | Look for |
|---|---|
| Edit has no effect at all | Duplicate selector later in the sheet |
| Measurements disagree with what you see | Dead rule pinning `width`/`height` |
| Works on desktop, broken on mobile (or vice versa) | Shared rule with two breakpoint branches |
| Track collapses but child does not | Grid item not `stretch`-aligned / missing `min-height:0` |
| Element clipped at a container edge | An ancestor `overflow:hidden` you did not write |

---

## JavaScript

**"Cannot access 'X' before initialization"** (temporal dead zone) — A function
defined early referenced a `let`/`const` declared later in the same scope (e.g.
`resize()` used `let dirty` before its line). Hoisting doesn't save `let`/`const`.
*Fix:* declare state (`let dirty=true, visible=false`) **before** any function
that closes over it.

**A ScrollTrigger/effect that never runs** — It was gated on a condition that
never becomes true (e.g. "build only after all frames loaded", which never
fired). *Fix:* build the trigger immediately and degrade gracefully (draw the
nearest-loaded frame), don't gate setup on a load that may not complete.

**Console must be clean** — Open devtools; any red error or repeated warning is a
ship-blocker. Fix the cause, don't silence it.

## Images & media

**Image looks horizontally stretched** — The `<img>` had `width`/`height`
attributes (good for layout-shift) but CSS set `width:100%` with **no**
`height:auto`, so the height stayed pinned at the attribute value while the width
scaled → wrong aspect ratio. *Fix:* a global `img{max-width:100%;height:auto}`
(cover images that need a fixed box override with explicit `height:100%;
object-fit:cover`).

**Soft / warped photo from upscaling** — Scaling a small source way up looks
mushy and "off." *Fix:* crop at native resolution; don't upscale a 512px source
to 860px. See `images.md`.

**Layout shift as images load** — *Fix:* set `width`/`height` (or
`aspect-ratio`) so the browser reserves the box; `loading="lazy"` below the fold,
`decoding="async"`.

**`<video>` won't seek or autoplay locally** — Python `http.server` answers
`200` and ignores HTTP Range requests; `<video>` needs `206 Partial Content` to
seek/buffer, so the clip looks broken on the dev server — but works in production
(Netlify and most hosts honor Range). *Fix:* test video on a Range-capable server
(`npx http-server`, or a tiny Node Range handler). Don't "fix" a video whose only
fault is a Range-blind dev server.

## Forms & deploy

**Netlify form not detected (`Forms: []`)** — New Netlify sites default
`ignore_html_forms:true`, so the build-time form scraper is off and submissions
404. *Fix:* `netlify api updateSite` → `ignore_html_forms:false`, then redeploy.
See `deploy.md`. Also keep the hidden `form-name` input, the honeypot, and the
real `name=` attributes.

**SRI integrity present** — Every CDN `<script>`/`<link>` should carry an
`integrity=` + `crossorigin` so a tampered CDN file can't run. Verify the hashes
match the pinned version. (The Cloudflare Web Analytics beacon is the one
documented no-SRI exception — Cloudflare rotates `beacon.min.js`.)

**Favicon as REAL CRAWLABLE FILES, never a data-URI (hard rule, fixed 2026-07-24)** —
A site with no favicon reads as unfinished, but the bigger trap is shipping one
Google cannot use. Google's favicon-in-search docs require that **Googlebot-Image
can crawl the favicon file** and that `href` is a real URL. A
`data:image/svg+xml;base64,…` href is not a URL, so **Google renders a generic
globe next to the site in search results.** It looks perfect in the browser tab,
which is exactly why it hid on **13 of 14 fleet sites** until an audit caught it.
Ship the full set from one brand SVG:
`/favicon.ico` (multi-size 16/32/48), `/assets/icons/icon.svg`,
`apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png`, plus a
`site.webmanifest` — and add `Content-Type: application/manifest+json` for the
manifest in `_headers`, or Netlify serves it as `application/octet-stream`.
Keep `<meta name="theme-color">` alongside. Google also wants square, >48x48, and
a **stable URL** (don't churn the path). Recipe in `images.md`.

**Designed OG social-share image (default, every build)** — `og:image` is the
picture that appears when someone pastes the link into a text, DM, Slack, or FB.
Leaving it as a **raw job photo looks unfinished and off-brand**. Ship a designed
**1200x630 branded card** (brand-color background + logo/mark + the headline +
phone) and wire `og:image` + `og:image:width/height` + `og:image:alt` +
`twitter:image` + `twitter:card=summary_large_image`. If ImageMagick can't render
text on this machine (no freetype — common on macOS), reuse the **Remotion
promo's final-card frame** as the card:
`ffmpeg -ss <t> -i promo.mp4 -frames:v 1 -vf "scale=1200:-1,crop=1200:630" og.jpg`.
Verify it's reachable (HTTP 200) after deploy.

**No glow, no pulse — grep for it (hard brand rule, every build)** — banned:
colored/tinted `box-shadow` (a shadow carrying the accent color reads as a glow
halo — a gold button with `box-shadow:… rgba(gold,.28)` is the classic slip; use
a **neutral dark** shadow), `filter: blur/brightness/drop-shadow(<color>)` used to
glow, and any `animation … infinite` that pulses/breathes. A dark `text-shadow`
purely for legibility over a photo is fine. Before deploy: `grep -oE
"box-shadow:[^;}]*" index.html` and neutralize any non-black tint; `grep -n
infinite` and remove pulse loops.

**Data-entry pages: the four mobile defects (learned 2026-07-28 on the lead
tracker + meeting sheet)** — any page a human actually fills out on a phone
needs all four, or it is unusable one-handed:

1. **Every `input`/`select`/`textarea` is `font-size:16px` or larger.** Below
   16px iOS Safari auto-zooms on focus and **never zooms back out**, so the user
   is stranded at 1.4x for the rest of the session. This is the single most
   common complaint and it is invisible on desktop. Grep: `grep -nE
   "font-size:\s*1[0-5]px" index.html` and check none of the hits are inputs.
2. **A polling/auto-sync page must not rebuild the DOM under the user's thumb.**
   Gate the re-render: skip it while an input is focused or a form/card/menu is
   open, and restore `pageYOffset` after any rebuild that changes height.
   ```js
   function busy(){ var a=document.activeElement;
     if(a && /^(INPUT|SELECT|TEXTAREA)$/.test(a.tagName)) return true;
     return !!document.querySelector(".addform.open, .cbody.open, .menu-pop.open"); }
   function render(){ var y=window.pageYOffset; renderInner();
     if(window.pageYOffset!==y) window.scrollTo(0,y); }
   ```
   Same rule for incoming sync data: defer the merge while `busy()`, or you
   overwrite what they are mid-way through typing.
3. **Collapsing a section must anchor the heading.** Measure the header's
   `getBoundingClientRect().top` before and after the toggle and `scrollBy` the
   delta, otherwise closing a long section throws the user somewhere random.
4. **`viewport-fit=cover` + `env(safe-area-inset-*)` padding, 44px minimum tap
   targets, `touch-action:manipulation`, and `scroll-padding-top` matching any
   sticky header** so anchors and focused fields don't land underneath it.

A tall fixed header eats the whole viewport on a phone — make it collapsible
rather than sticky-tall.

**CSS brace balance (run this, it is not optional)** — A single stray `}` silently
kills every rule after it. On a junk-removal client this made **every image on the page vanish**
while the HTML, the files and the network were all fine, and it came from
string-replacing a rule while anchoring on the selector WITHOUT its closing brace.
Extract the `<style>` block and assert the count matches and depth never goes negative:

```bash
python3 - <<'EOF'
import re
css = re.search(r'<style>(.*?)</style>', open('index.html').read(), re.S).group(1)
d = 0
for ch in css:
    d += (ch == '{') - (ch == '}')
    assert d >= 0, "stray } before this point"
assert d == 0, f"unclosed rule, depth {d}"
print("css balanced")
EOF
```
When you string-replace a CSS rule, always include its closing brace in the anchor.

**`<picture>` wrappers need `picture{display:contents}`** — Adding WebP `<source>`
elements inserts an inline `<picture>` box between each `img` and its real parent,
which breaks percentage heights (`.marquee img{height:100%}`) and flex/grid behaviour.
`display:contents` removes the wrapper from the layout tree so every existing
`.parent img` rule keeps resolving against the true parent. Check for direct-child
selectors (`.x > img`) first: those break outright and `display:contents` will not
save them.

**Serve images at the size they RENDER, not the size they were shot** — Re-compressing
an already-optimised JPEG buys almost nothing (a junk-removal client: 10MB to 9.5MB). Generating
WebP at the displayed width does (same set: 2.1MB). Ship
`<picture><source type="image/webp" srcset="w700/x.webp 700w" sizes="..."><img src="x.jpg" width= height=></picture>`
and set intrinsic `width`/`height` on every img to kill layout shift.

## Local-service conversion (added 2026-07-28)

Pretty is not the bar. **99.2% of home service websites convert under 1%.** Getting to 4-5%
yields roughly **3x the leads from identical traffic**, before any SEO or ads. Frame:
`value = (dream outcome x perceived likelihood) / (time delay x effort)`. Almost every build
works only the numerator. The denominator is where the compounding is, and it is all
template work, built once.

**Raise value (most builds do this already):**
- **Dream outcome in the H1.** "Lawn care in a nearby town" is a *category*. "Your lawn cut this
  week, flat rate, no contracts" is an *outcome*. Same visitor, different conversion rate.
  Audit every hero for this: if the H1 names the category, rewrite it.
- Reviews on the homepage (real ones only), before/after photos, owner named and pictured,
  named guarantees, licensed and insured, certifications.

**Cut friction (usually missing, ship all of these):**
- **Sticky mobile action bar** that follows the scroll: call / quote / text / book.
- **Address autocomplete** on the form.
- **Photo upload from the phone.** Huge for visual trades (torn screen, flooded basement,
  storm damage). It also pre-qualifies the lead for the owner.
- **Honest price ranges page.** Not exact quotes, ranges. Removes the biggest hesitation.
- **Emergency / after-hours availability on the homepage**, not buried in a footer.
- Online booking with visible availability where the client has a calendar to expose.
- **Phone AND form, both, always.** Some need it now; some will not talk to anyone yet.
  Most local sites offer one.

**Map embeds: the rule depends on the business type, and getting it wrong leaks an address:**
- **Storefront** (barbershop, salon, retail, diner, shop): embed a **street-address pin**, and
  put `streetAddress` in the LocalBusiness schema. People need to find the door.
- **Service-area business** (lawn, junk, window cleaning, plumbing, screen repair): **never
  pin their home address.** Embed a **regional view** instead (`?q=the metro+Bay,+my state&z=9`)
  or no map at all, and use `areaServed` with `"@type": "City"` entries in schema, with **no
  `streetAddress`**. Pinning a SAB's house contradicts the address they hide on their Google
  profile, and it publishes where they live.
- **A map embed is NOT a ranking factor.** Widely repeated, never substantiated. Embed it for
  trust and orientation, not for SEO.
- **Always `loading="lazy"`** on the iframe, and add the frame origin to that site's CSP
  `frame-src` (see `deploy.md`).

*Audited 2026-07-28: all 22 sites already follow this correctly, and all 4 map iframes are
lazy-loaded. Written down so it does not drift.*

**If the business wants COMMERCIAL work, that is a separate page, not a section.** A property
manager needs different proof and a different CTA than a homeowner: name the buyer types in the
copy (property management groups, project managers, superintendents, contractors, HOAs), show
**insurance limits, workers comp, crew count, response-time commitment and property case
studies** instead of homeowner reviews, and make the CTA **"Request a bid"** or **"Get on our
vendor list"**, never "free quote". Add a downloadable capability sheet, because they forward it
internally. Qualify the client first (net-30-to-60 terms and a $1M COI disqualify most
one-truck operators). Method: `~/.claude/skills/site-prospector/references/commercial-b2b.md`

**Full detail, plus the ranking side:**
`~/.claude/explanations/20260724_valstratis-replication/SEO-PLAYBOOK.md`

## The sticky header that dies only on a phone (added 2026-07-30)

**`body { overflow-x: hidden }` breaks `position: sticky` on iOS Safari.** It turns body into a
scroll container, so the sticky nav has nothing to stick to and scrolls away on a phone while
looking perfect in desktop Chrome — which is why it survives every desktop check. Reported by
Adam as "on mobile the header doesn't stay there when i scroll".

**Use `overflow-x: clip` instead.** `clip` contains the same overflow without establishing a
scroll container, so sticky keeps working:

```css
body{ overflow-x:clip; overflow-y:visible }   /* NOT overflow-x:hidden */
```

Verify by walking the scroll and asserting the nav stays pinned, and by listing any ancestor
that is a scroll container:

```js
const nav = document.querySelector('.nav'); const tops = [];
for (const y of [0, 900, 2400, 4800]) { window.scrollTo(0, y);
  await new Promise(r => setTimeout(r, 200)); tops.push(Math.round(nav.getBoundingClientRect().top)); }
tops.every(t => Math.abs(t) < 2)          // must be true
// and nothing above the nav may be a scroll container:
let n = nav.parentElement; while (n) { const cs = getComputedStyle(n);
  if (!['visible','clip'].includes(cs.overflowX)) console.warn('breaks sticky:', n.tagName, cs.overflowX); n = n.parentElement; }
```

`overflow-x:hidden` is usually added defensively against a horizontal-scroll bug. Fix the
overflow at its source instead, then `clip` is only a safety net.

---

## Run the impeccable detector directly, do not wait for the hook (added 2026-07-30)

The write-hook goes quiet after ~6 edits and truncates its list, so late findings are invisible.
Run it yourself over the whole build and read the real output:

```bash
node ~/.claude/plugins/cache/impeccable/impeccable/<ver>/skills/impeccable/scripts/detect.mjs *.html assets/css/site.css
```

**It reports only ONE font per file**, so a second flagged face stays hidden until you fix the
first. On a barber client it flagged `Instrument Sans`; fixing that revealed `Geist Mono` behind
it. Re-run until it prints nothing. Both were replaced (Hanken Grotesk, Spline Sans Mono) after
testing candidates against the detector rather than guessing which faces are on its list.

**Real findings it caught that a screenshot never would:**
- `transition:width` on the scroll progress bar, whose width is set **every scroll frame** —
  layout thrash on the hottest path in the page. Fixed with `translateX` on a full-width
  striped bar (`scaleX` would have distorted the barber-pole stripes).
- Two transitions on properties that **never change** (`.nav .row` min-height, `.brand img`
  width/height) — dead code that also happened to be flagged.
- `border-left:3px solid <accent>` on a callout. The checklist's own rule applies: a side bar
  on a **card** is the tell; on a `blockquote` it is a typographic convention. The callout was
  restyled to a hairline border plus tint; the quote got a hanging quotation mark instead.

---

## Motion & loading

**Loading state** — A preloader (or at least reserved space + reveal-on-load)
prevents a flash of unstyled/janky content and a "pop" as fonts/images arrive.

**`prefers-reduced-motion`** — Honor it: gate scroll-scrub/parallax/3D behind
`gsap.matchMedia()` or a media query and present a static, fully-usable layout.
Some users get motion sick; some are on weak devices.

**Programmatic scroll desyncs Lenis** — Browser-extension or scripted
`scrollTo` can fight Lenis and blank the screen in screenshots/automation. Not a
real-user bug, but don't panic-debug it; verify with native scrolling. Same
applies to reveal-on-scroll: a jump past a `ScrollTrigger.batch` onEnter may not
fire it, leaving content at `opacity:0` — force-reveal to check layout, but trust
a normal wheel-scroll for the real behavior. This IS a real bug, though, for
**in-page nav links** (`<a href="#services">`) — a plain hash-jump with Lenis
active can leave the destination section's `.reveal` content invisible for a
real user too, since no real scroll event fires. Fix it, don't just note it:
route every same-page anchor click through Lenis —
```js
document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
  const t = document.querySelector(a.getAttribute('href')); if (!t) return;
  e.preventDefault();
  window.__lenis ? __lenis.scrollTo(t, { offset: -navHeight }) : t.scrollIntoView({ behavior: 'smooth' });
}));
```

**Mobile nav burger animates but shows nothing** — Toggling `.nav.open` to spin
the icon into an X is not the same as verifying an actual dropdown panel
appears. Check that `.nav.open .nav-links` is a real, fully opaque,
correctly-sized panel — not just that the icon changed. A `position:fixed`
panel with `top` and `bottom` both set does not reliably auto-stretch its
height in every case (seen collapsing to ~20px with no explicit cause); prefer
an explicit `height:calc(100vh - <navheight>px)` (`100dvh` as a fallback line
after it) over relying on top+bottom inference.

**`filter:brightness(0) invert(1)` only works on flat single-color icons** —
applied to a real multi-color raster/photo logo (to force it "white" for a dark
footer), it crushes the whole image to a blank box. Put the real logo on a
small opaque background chip instead of trying to recolor it.

**A canvas frame-scrub reads "broken" in the first screenshot** — the hero
sequence loads asynchronously, so a shot taken in the first moment shows the
canvas's background color, not a frame. Don't chase a non-bug: sample a center
pixel (`getImageData` ≠ the background color) to confirm it drew, then re-shoot.
A hero scrub loads on page load (not lazily), so keep the frame budget lean
(~64 frames, recompressed) — it's the one sequence you can't defer.

**When Claude-in-Chrome isn't connected, don't reach for raw headless-Chrome
CLI flags** — use `puppeteer-core` pointed at the existing Chrome install
instead:
```js
const puppeteer = require('puppeteer-core'); // npm i puppeteer-core --no-save in a scratch dir
const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new',
});
// ...page.goto, page.evaluate(() => window.scrollTo(0,y)) in real increments,
// page.click on nav links, page.screenshot, page.on('console'/'pageerror')...
await browser.close();
```
This gives real scroll events (so `ScrollTrigger.batch` reveals fire correctly,
unlike a hash-jump), reliable console-error capture, and click-testing on nav
links — plus you hold the exact browser handle to close, so no process cleanup
guesswork. The raw CLI (`chrome --headless --window-size=W,H --screenshot=`) is
a trap for anything with `vh`-based CSS: inflating `H` to fake a "full page"
capture also inflates every `vh` rule (a `height:280vh` section balloons to
`280×H`), producing garbage. Use a realistic viewport height and scroll/click
programmatically instead. **Never `pkill` Chrome by a broad pattern** (e.g.
`pkill -f "Google Chrome"`) to clean up test instances — it kills the user's
real running browser too; either scope the match tightly (`--headless` in the
string) or just `browser.close()` the handle you launched.

## Multi-page consistency

**Hand-copied chrome drifts between pages** — On a multi-page site where the
head, nav, footer, and script blocks are copied by hand, edits land on some
pages and not others: a page with a different font setup, a missing dark-mode
toggle, a dead link. This is a real bug — it bit the auth pages on a real build.
*Fix:* hash each shared block (head/nav/footer/scripts) across every page and
confirm they're byte-identical; reconcile any page that differs.

## Final sweep

- [ ] Mobile pass at ~390px: gutters present, nothing edge-touching, headings
      not cramped, tap targets ≥ 44px.
- [ ] Console clean (no red, no repeated warnings).
- [ ] Every image correct aspect (no stretch), lazy below the fold.
- [ ] Form (if any) detected after deploy + a test submission arrives.
- [ ] Reduced-motion gives a clean static experience.
- [ ] No duplicate/overriding CSS; one spacing system; no class-name collisions
      across components.
- [ ] Mobile nav opens and shows all links (no overlapping absolute blocks) — AND the
      link text has contrast against the dropdown background. Trap: a transparent-over-hero
      nav sets links to white; the open mobile dropdown has a light/cream background, so the
      white links vanish until you scroll and the nav flips to its solid dark-text state.
      Force dark link color inside the mobile dropdown regardless of scroll state.
- [ ] Video (if any) seeks/autoplays on a Range-capable server, not just the prod host.
- [ ] Multi-page: shared head/nav/footer/script blocks byte-identical across pages.
- [ ] All CDN tags have SRI integrity (Cloudflare beacon is the one exception).
- [ ] Favicon shipped as REAL FILES (favicon.ico + icon.svg + apple-touch + 192 + 512 + webmanifest with the right Content-Type). NEVER a data-URI, Google shows a globe.
- [ ] Social card: `verify-og.py <host>` exits 0. All 16 tags on every page including
      **twitter:title and twitter:description**, self-referential og:url, jpeg/png not webp.
- [ ] No glow / no pulse: no colored box-shadows, no glow filters, no infinite pulse loops
      (grep the CSS). Neutral dark elevation shadows only.
- [ ] Carousels: native `overflow-x:auto` scroll (NOT hand-rolled transform drag), seamless
      infinite (3 cloned sets), scroll on trackpad/two-finger + horizontal wheel
      (`data-lenis-prevent` on the container), click opens the lightbox (delegated so clones
      work), no photo ghost-drag (`img{-webkit-user-drag:none;pointer-events:none}`), no
      double-tap zoom on arrows (`touch-action:manipulation`). See components.md.

## Design-stack gate

Runs after the list above, before deploy. Full detail in `design-stack.md`.

- [ ] `/impeccable critique` run (UX review), every finding resolved.
- [ ] `/impeccable audit` run (a11y, perf, responsive), every finding resolved.
- [ ] Findings were **fixed or explicitly classified as false positives with a stated
      reason**. No inline `impeccable-disable` comments. Suppressing a real finding
      needs Adam's confirmation first.
- [ ] taste-skill pre-flight (its Section 14) walked, not skimmed. Watch the mechanical
      ones: max 1 eyebrow per 3 sections, no three equal feature cards, no 3+ consecutive
      image-text splits, hero headline ≤ 2 lines, bento cell count matches item count.
- [ ] The override held: no `infinite` animations, no tinted `box-shadow`. taste-skill's
      default motion dial permits perpetual loops and we do not. Grep, do not trust.
- [ ] Icons from one family (Phosphor preferred), one global strokeWidth, no hand-rolled
      icon paths.

**The detector is mechanical.** It cannot tell decoration from function. A 3px accent
border on a callout is a real tell; the same border marking the selected item in a tab
list is doing a job. Read each finding, do not auto-apply.


---

## Measure, don't eyeball {#measure}
*Added 2026-07-28. Every one of these caught something a screenshot did not.*

Design targets stated as numbers can be **verified as numbers**. Run these in the
console on the deployed page, not locally.

### Type ramp — count the distinct sizes
A page should live on 5-6 type levels. Real builds drift to 20+ without anyone
noticing, because each individual size looked fine when it was written.

```js
const RAMP=[11,14,16,21,32,48];   // your ramp
const all=[...document.querySelectorAll('h1,h2,h3,p,li,span,a,label,b,strong')]
  .filter(e=>e.children.length===0&&e.textContent.trim());
const sizes=all.map(e=>Math.round(parseFloat(getComputedStyle(e).fontSize)*100)/100);
console.log({
  onRampPct:Math.round(100*sizes.filter(x=>RAMP.includes(x)).length/sizes.length),
  offRamp:[...new Set(sizes.filter(x=>!RAMP.includes(x)))].sort((a,b)=>a-b)
});
```

**Then build the fix from the LIVE DOM, not from guessed class names.** Writing
`.rev, .svc-body, .tally-lab {…}` from memory silently misses half the elements
and the count barely moves. Dump the real offenders with their selectors first:

```js
const off={};
[...document.querySelectorAll('*')].filter(e=>e.children.length===0&&e.textContent.trim())
 .forEach(e=>{
   const px=Math.round(parseFloat(getComputedStyle(e).fontSize)*100)/100;
   if(RAMP.includes(px))return;
   const own=typeof e.className==='string'&&e.className.trim()
     ? e.tagName.toLowerCase()+'.'+e.className.trim().split(/\s+/).join('.')
     : (e.parentElement?.className||'').split(' ')[0]+' > '+e.tagName.toLowerCase();
   const k=own+'  @'+px; off[k]=(off[k]||0)+1;
 });
console.log(off);
```

**Never let body text go below 16px to buy page height,** and check form inputs
separately (`input,select,textarea` at 16px minimum or iOS zooms on focus).

### Section rhythm — count the distinct paddings
```js
[...new Set([...document.querySelectorAll('body > section')]
  .map(s=>getComputedStyle(s).paddingTop))]
```
More than 2 values (one being the hero's `0`) means the vertical rhythm is
accidental rather than designed **on an article or documentation page**.

**Do NOT apply this to a marketing page.** Collapsing every band to one padding
value is what flattened three fleet builds into spreadsheets. A marketing page
wants deliberate rhythm: a tall hero, a medium split, a tight card grid, a tall
photo band. If every band measures within 10% of the others the page reads flat
no matter how good the content is. See `page-composition.md`.

### Sibling pages — are they a template with the nouns swapped?
The doorway-page test, as a number. Jaccard word overlap between sibling pages:

```python
def jac(a,b):
    A,B=set(a.split()),set(b.split()); return len(A&B)/len(A|B)
```
**>70% = template-y, fix it.** Shared nav/footer/form alone puts a floor around
30-40%, so target under ~55% for area pages and under ~40% for service pages.
Also count repeated `<h2>` text across pages — identical headings on 4+ pages is
boilerplate even when the body copy differs.

### Fixed-element collisions
List everything `position:fixed` and confirm each pair that shares a screen
corner uses the **same breakpoint** and the same height variable. A bar shown at
`800px` and a FAB offset at `760px` overlap in a 40px window nobody tests.

---



## SEO + deploy verification, on the LIVE site {#seo-live}
*Added 2026-07-29. Every item here was wrong or missing on a build that "looked done"
locally. Source of truth is the live response, never the file on disk.*

**The URL itself is a local-SEO asset.** Name the Netlify site `business + city`
(`lawncare-demo`, `smallengine-demo`), not `business-demo`. Do the
rename BEFORE the SEO pass, then rewrite every `canonical`, `og:url`, `sitemap.xml` and
`robots.txt` entry to the new host in one sweep, or half the site points at a dead name.

```bash
netlify api updateSite --data '{"site_id":"<id>","body":{"name":"<business><city>"}}'
```

**Netlify Forms are NOT detected by default.** The parser is off until you turn it on, and a
form that renders perfectly will silently swallow every lead:

```bash
netlify api updateSite --data '{"site_id":"<id>","body":{"processing_settings":{"html":{"ignore_html_forms":false}}}}'
# then REDEPLOY (the parser runs at deploy time), then confirm:
netlify api listSiteForms --data '{"site_id":"<id>"}'      # must list the form name
```

Wire the notification and **submit a real test post**, do not assume:

```bash
netlify api createHookBySiteId --data '{"site_id":"<id>","body":{"type":"email",
  "event":"submission_created","data":{"email":"<inbox>","form_id":"<form-id>"}}}'
curl -X POST https://<host>/ --data-urlencode "form-name=<name>" --data-urlencode "name=Test" ...
netlify api listFormSubmissions --data '{"form_id":"<form-id>"}'   # must show it
```

**Metadata limits, measured not guessed.** Titles ≤ 62 chars, descriptions ≤ 165, exactly one
`<h1>`, no duplicate titles or descriptions across the site. A build shipped with titles up to
79 chars and descriptions up to 189, all of which truncate in results.

```python
for p in pages:
    t=re.search(r'<title>(.*?)</title>',s,re.S).group(1)
    d=re.search(r'<meta name="description" content="(.*?)"',s,re.S).group(1)
    assert len(t)<=62 and len(d)<=165 and s.count('<h1')==1
```

**The 404 must be `noindex,follow` and must not appear in the sitemap.** Set it in the head
server-side; a JS-injected meta is not reliable. Verify the live page returns a real 404
status AND serves the fuzzy matcher:

```bash
curl -s -o /dev/null -w '%{http_code}' https://<host>/nope     # must be 404
curl -s https://<host>/golf-cart | grep -o 'Did you mean'      # matcher present
curl -s https://<host>/nope | grep -o '<meta name="robots"[^>]*>'
```

**Check security headers on the live response, not in `_headers`.** Expect CSP,
`x-frame-options`, `x-content-type-options: nosniff`, `referrer-policy`,
`permissions-policy` and HSTS. A CSP missing `frame-src` silently blanks any map embed and
only shows up live.

```bash
curl -sI https://<host>/ | grep -iE "content-security|x-frame|x-content|referrer|permissions|strict-transport"
```

**Keep build artefacts out of the deploy** with `.netlifyignore` (the stock image library,
research notes, `*.py`), and `Disallow:` them in robots.txt as a backstop.

### Confirm you deployed to the site you think you did {#deploy-target}
`netlify deploy` reports **"Deploy is live!"** whether or not it went where you intended.
Three ways that goes wrong, all seen on 2026-07-30 on one site:

**1. The directory is linked to a different site.** `~/money/adamjali` was linked to
`frolicking-crisp-95ec14`, so four consecutive "successful" deploys published a full copy of
the personal site to a stray URL while `<client>.netlify.app` sat unchanged. Check before
deploying, and pass the ID explicitly:

```bash
netlify status | grep -i "current project"
netlify deploy --prod --dir dist --site <SITE_ID>     # ID, not name; --site <name> 404s
```

**2. A `[build] publish` directive inside the deployed folder.** Deploying `--dir dist` makes
`dist` the site root, so a `publish = "dist"` in the `netlify.toml` you just copied into it
sends Netlify looking for `dist/dist`. It reports success and **quietly keeps serving the
previous deploy.** Omit `[build]` from any toml that ships inside the publish directory.

**3. Headers split across `netlify.toml` and `_headers`.** A `[[headers]]` block in the toml
wins **outright**; `_headers` is then ignored entirely, silently dropping anything only it
defined. On adamjali that meant the CSP, COOP and X-DNS-Prefetch-Control never shipped on a
single response despite being written down. **Put all headers in ONE file.**

**Always confirm against the live host, never the deploy log:**

```bash
curl -sI https://<host>/ | grep -i content-security-policy     # a header only you set
curl -s https://<host>/ | grep -c 'application/ld+json'        # something you just added
```
If the thing you changed is not visible live, the deploy did not land where you think.

---


---


#
## Content must exist in the HTML, not only after JavaScript {#crawlable-html}
*Added 2026-07-29 after an audit found 93 causes of high-intent copy, five service headlines
and four statistics that no crawler could see.*

The common criticism of AI-built sites is that they are JavaScript applications rendering
HTML, so the content only exists once code runs. Our static builds are the opposite by
default. **But the moment you put copy in a JS array and inject it, you have reintroduced
exactly that problem for that block.**

Three real instances, all shipped and all fixed:

| What | Symptom |
|---|---|
| a small-engine client symptom diagnostic | 6 machines x 27 symptoms x 93 causes lived in a `DIAG` object. Raw HTML was 5,023 chars; none of it indexable. Fixed: 14,522 chars. |
| a client rebuild hero slideshow | Only `haul junk.` was in the markup. *Tree work, yard and sod, handyman and demo* were JS-only, so four of the five services the shop sells were invisible. |
| Count-up statistics | Markup said `<b data-count="92">0</b>`. Crawlers indexed **"0 Manufacturer certifications"**. Worse than missing: actively wrong. |

**The rule.** Copy ships in the markup. JavaScript may *filter, toggle or animate* what is
already there; it must not be the only source of it.

```html
<!-- WRONG: JS is the only source -->
<div class="chips" id="dSymptoms"></div>
<b data-count="92">0</b>

<!-- RIGHT: markup is the source, JS enhances -->
<button class="chip" data-m="golf-cart" data-s="golf-cart-wont-hold-a-charge" hidden>Won't hold a charge</button>
<article class="dcase" id="golf-cart-wont-hold-a-charge" hidden>...93 causes ship here...</article>
<b data-count="92" data-suffix="%">92%</b>   <!-- JS blanks it to 0 then animates -->
```

**Generate the markup from one source of truth** so copy cannot drift between the HTML and
the JS. a small-engine client uses `diag_data.json` + `make_diag.py`; a junk-removal client slideshow reads
the headlines back out of the DOM instead of duplicating them in a `SLIDES` array.

**The CSS trap.** `[hidden]` is a UA rule with almost no specificity, so **any** `display`
declaration beats it and every hidden variant renders at once. a junk-removal client hero stacked all five
headlines. Declare the scoped rule AFTER the component rule:

```css
.hero h1 .verb{display:inline-block}        /* 0,2,1 */
.verbs .verb[hidden]{display:none}          /* 0,3,0 — after it, and wins */
```

**Audit any build with this**, comparing what curl returns against what the browser renders:

```bash
curl -s https://<host>/ | sed 's/<script[^>]*>.*<\/script>//g; s/<[^>]*>/ /g' | grep -i "<phrase>"
```
Probe every phrase that lives in a JS array, plus every count-up value. Anything absent is
invisible to Google and to every social scraper, none of which run JavaScript.

**Hidden-behind-a-click content is indexed**, just weighted a little lower than visible copy.
That is vastly better than not being in the document at all.

---

## Structured data is not optional {#structured-data}
A fleet audit on 2026-07-29 found **15 of 23 live sites with no LocalBusiness-family schema
at all**. That is a bigger local-SEO gap than anything JavaScript-related, because
`LocalBusiness` is how you hand Google the name, phone, hours, service area and rating in a
form it can consume without guessing.

Every build ships, minimum:
- One `LocalBusiness` subtype (`AutoRepair`, `MovingCompany`, `HairSalon`, `RoofingContractor`…) with `name`, `telephone`, `url`, `areaServed`, `openingHoursSpecification`, `sameAs`
- `BreadcrumbList` on every inner page
- `Service` on each service page
- `FAQPage` wherever there is a FAQ

**Only assert `aggregateRating` if the rating is verifiable.** a small-engine client shipped
`4.42 / 31 reviews` sourced from an aggregator that marked the profile unclaimed; when the
listing could not be found, the whole block came out.

**Audit the fleet with `@graph` handling** or you will get false negatives: a site can carry a
perfectly good `LocalBusiness` inside `@graph` and a naive `j.get("@type")` reads `None`.

---

## The social card is a staple, not an afterthought {#social-card}
Pointing `og:image` at a hero photo is not a social card, and pointing it at a **WebP** is
worse: the scrapers want JPG or PNG and several ignore WebP entirely. Build a real one.

**Render it with the site's own typography** rather than drawing it in PIL: write a
`ogcard.html` at exactly 1200x630 using the same fonts and palette, then screenshot it.

```
chrome-devtools: resize_page(1200,630) -> navigate(/ogcard.html) -> take_screenshot(filePath: assets/og.jpg)
```

Put on it: logo, business name, the one-line positioning, service towns, the phone, and a
real proof number if there is one. Then ship the FULL tag set on every page, absolute URLs:

```html
<meta property="og:type"           content="website">          <!-- article on inner pages -->
<meta property="og:site_name"      content="Business Name">
<meta property="og:locale"         content="en_US">
<meta property="og:url"            content="https://<host>/this-page.html">  <!-- SELF-referential -->
<meta property="og:title"          content="...">
<meta property="og:description"    content="...">
<meta property="og:image"          content="https://<host>/assets/og.jpg">
<meta property="og:image:width"    content="1200">
<meta property="og:image:height"   content="630">
<meta property="og:image:type"     content="image/jpeg">
<meta property="og:image:alt"      content="...">
<meta name="twitter:card"          content="summary_large_image">
<meta name="twitter:title"         content="...">   <!-- MISSED FLEET-WIDE until 2026-07-30 -->
<meta name="twitter:description"   content="...">   <!-- MISSED FLEET-WIDE until 2026-07-30 -->
<meta name="twitter:image"         content="https://<host>/assets/og.jpg">
<meta name="twitter:image:alt"     content="...">
```

**Ignore SEO tools that demand `og:logo`. It does not exist.** Checked against ogp.me on
2026-07-30: the Open Graph protocol defines exactly 23 properties and **`og:logo` is not one of
them** (zero occurrences in the spec). No scraper consumes it. Cheap audit tools invent it and
report it as "missing", which is a false positive, not a gap.

The logo IS handled, by the mechanism Google actually documents: **`logo` on the
`Organization`/`LocalBusiness` JSON-LD node**, pointing at a square, crawlable raster.
Do not add fake tags to silence a bad validator — that is how markup rots.

```bash
curl -s https://<host>/ | grep -o '"logo":"[^"]*"'    # this is the real one
```

**Verify with the script, not by eye. `curl | grep` on one page is how this stayed broken.**

```bash
python3 ~/.claude/skills/site-forge/scripts/verify-og.py <host>     # non-zero exit = broken
```

It walks every page in `sitemap.xml` (plus 404 and thanks) and asserts: the full 16-tag set,
absolute image URLs, a **self-referential `og:url` per page**, no duplicate `og:title`, the
image resolves as **jpeg or png** (webp is rejected: several scrapers ignore it), and the
declared `og:image:width/height` match the file's **real pixels**.

**A fleet run on 2026-07-30 found the tag set incomplete on every site checked.** The cause was
that the documented list itself omitted `twitter:title` and `twitter:description`, so they were
never written anywhere. `junkremoval-demo` — live in front of a paying client — was additionally
missing `og:image:width`, `og:image:height`, `og:image:type`, `og:image:alt` and `twitter:image`
on all 23 pages. A partial set still renders, just badly and differently per platform, which is
precisely why nobody spots it.

**Keep `ogcard.html` out of the published output** (see below) so the source never indexes.

---

### Deploy from a clean `dist/`, never from the project root {#clean-publish}
**`.netlifyignore` is NOT honoured by `netlify deploy --dir .`.** Deploying the project root
published the build scripts, the 86-image stock library, and `research/BRIEF.md` — which
contained the OWNER'S HOME ADDRESS, the exact thing the whole build was careful never to
print on a page. It was live until caught.

Build an explicit publish directory containing only the pages plus the assets those pages
actually reference, and deploy that:

```python
pages=[p for p in R.rglob('*.html') if 'dist' not in p.parts and p.name!='ogcard.html']
refs=set()                       # parse src/href/content AND every srcset candidate
for p in pages: refs |= extract_asset_urls(p.read_text())
# copy only pages + referenced assets + app.js, sitemap.xml, robots.txt, _headers
```

Then **prove the exclusions on the live host**, because a local check proves nothing:

```bash
for f in /research/BRIEF.md /build.py /STATE.md /ogcard.html /assets/stock/x.jpg; do
  curl -s -o /dev/null -w "$f %{http_code}\n" https://<host>$f      # every one must be 404
done
curl -s https://<host>/ https://<host>/about/ | grep -ic "<owner street name>"   # must be 0
```

Research notes routinely hold exactly what must never ship: home addresses, negative reviews,
unverified claims, passwords. Treat the research directory as private by construction.

**Use the scripts, do not hand-roll it:**

```bash
python3 ~/.claude/skills/site-forge/scripts/make-dist.py .
netlify deploy --prod --dir dist
~/.claude/skills/site-forge/scripts/verify-published.sh <host> [owner-street-name]
```

`verify-published.sh` exits non-zero if ANY private path returns 200, so it can gate a deploy.

**Fleet audit, 2026-07-29.** All 26 live sites were checked. **8 were publishing files they
should not have been.** One was serious: `leadtracker/tracker.py` was world-readable
and hardcoded the tracker password plus its `/api/store` endpoint, which was enough to read and
write the CRM. The other seven exposed `build.py`, `pages.py`, `optimize.py` or `package.json`,
which on inspection contained only the client's public phone number. All 26 now audit clean.

The lesson is not "be careful." It is that **`--dir .` reads as correct on a no-build static
site**, because the directory holding `index.html` is also the directory holding `build.py` and
`research/`. Any recipe that says `--dir <the site directory>` will produce this bug eventually.
Publish a directory that never contained the private files.

---

## The "Adam always wants this" audit {#always-wanted}
*Added 2026-07-29 after a build shipped without a service-area map, without clickable
reviews, and without a preloader, all of which were standing requests. Run this list
BEFORE calling any build done. A missing standing request is a defect, not a variation.*

| Staple | Pass condition |
|---|---|
| Preloader | Logo (INLINED as a data URI, never a network `<img>`), progress bar, SMALL spinner. Homepage only. |
| Reveal | Panel **slides up** (`translateY(-100%)`), never fades. A fade cross-dissolves into the hero and reads as a flash. |
| Nav loading state | Top bar + pending-link spinner. **One at a time**: a new click clears the previous pending link, and a timeout clears it so it can never hang. |
| Service-area map | Interactive SVG, hover + focus + click pins, live info panel. A photo where the map goes is a miss. |
| Review carousel | Seamless-infinite (cloned track, wrap at `scrollWidth/2`), pointer-drag, wheel, AND prev/next buttons. |
| Reviews are links | Every card links out to its source platform, plus a "see all reviews" button. |
| Review count | As many real 4- and 5-star reviews as exist. Not a curated three. |
| Scroll header | Opens with the util strip out of frame; transparent + compact at top over the hero; solid + taller on scroll. Recipe: `components.md#header-scroll`. |
| Social card | Real 1200x630 **JPG/PNG** (never WebP, never a raw hero photo), rendered in the site's own type. **All 16 og:/twitter: tags on every page**, including `twitter:title` and `twitter:description`. Self-referential `og:url`. Gate it with `verify-og.py <host>`. |
| Marquee | Same engine, drift ~0.9px/frame, drag, no buttons. |
| Count-up stats | Real, checkable numbers only. |
| Scroll progress + back to top | Both. |
| Themed form controls | Custom select, label-as-button file input. |
| Every card grid has images | A grid of text boxes is the "empty" failure. Town/area cards included. |

**Verification, not eyeballing:**
```js
// no label in an SVG map may overlap another
const t=[...document.querySelectorAll('.mpin text')].map(e=>{const b=e.getBBox();
  return {n:e.textContent,x1:b.x,x2:b.x+b.width,y1:b.y,y2:b.y+b.height}});
for(let i=0;i<t.length;i++)for(let j=i+1;j<t.length;j++){const a=t[i],b=t[j];
  if(a.x1<b.x2&&b.x1<a.x2&&a.y1<b.y2&&b.y1<a.y2) console.warn('overlap',a.n,b.n)}

// reviews really loop and really link
const track=document.getElementById('revTrack'), rail=document.getElementById('revRail');
rail.scrollLeft = track.scrollWidth/2 - 5; rail.dispatchEvent(new Event('scroll'));
// scrollLeft should snap back near 0
[...track.querySelectorAll('.rev')].every(c=>c.tagName==='A'&&c.href)   // must be true

// mobile, at a REAL viewport (chrome-devtools resize_page, not Claude-in-Chrome)
document.documentElement.scrollWidth > innerWidth   // must be false
[...document.querySelectorAll('a.btn,button')].filter(b=>{const r=b.getBoundingClientRect();
  return Math.min(r.width,r.height)>0 && Math.min(r.width,r.height)<44})   // must be empty
```

---

## Verifying in an automation browser {#automation-verify}
*Claude-in-Chrome and similar report `document.hidden: true`. This fakes a whole
class of bugs and hides real ones. Learned repeatedly; write it down.*

| Symptom in the automation tab | Reality |
|---|---|
| Images render as blank boxes | Compositing artifact. The image is usually fine. |
| `requestAnimationFrame` never fires | `document.hidden` is true. rAF-driven code stalls. |
| Wheel scroll does nothing | Same cause when a rAF-driven smooth-scroll lib (Lenis) is in use. |
| Screenshots identical before/after scroll | Same cause. |

**Never `await` a rAF loop in that tab** — the promise never resolves and the
renderer hangs until the CDP call times out (~45s):

```js
await new Promise(r=>{const l=()=>{...requestAnimationFrame(l)};requestAnimationFrame(l)}); // HANGS
```

**To prove an image is actually fine, read its pixels** rather than trusting the
screenshot. Same-origin images will not taint the canvas:

```js
const img=document.querySelector('.wall img');
const c=document.createElement('canvas'); c.width=c.height=8;
const x=c.getContext('2d'); x.drawImage(img,0,0,8,8);
console.log([...x.getImageData(0,0,8,8).data].slice(0,12));  // real colour = it paints
```
Also check `img.complete && img.naturalWidth>0` and walk the ancestor chain for
`opacity`/`visibility`/`display` before blaming CSS.

**Corollary — do not "verify" smooth scroll with `lenis.scrollTo()`.** That
bypasses the wheel path, which is exactly where the failure lives. Use a real
wheel event or `window.scrollTo` and read `scrollY`.

**Mobile viewports are not reliable here** (fixed ~1440px render regardless of
window size, and `resize_window` does not change the render viewport).

**For a mobile-only bug, switch tools — do not reason from the CSS.** The
chrome-devtools MCP genuinely reflows and fires the mobile media queries:

```
new_page(url) → resize_page(390,844) → evaluate_script(...) → take_screenshot()
```

This is the one carve-out from the Claude-in-Chrome preference, and it earns its
place: it reproduced a completely broken mobile nav on a client rebuild in one shot,
on a page where every desktop check passed and where reading the CSS had already
produced four wrong hypotheses. **When a bug is reported as mobile-only, go here
first.**

Two caveats:
- `resize_page` is floored by the OS window minimum — asking for 390px yielded
  500px. That still trips `max-width:900px` breakpoints, but it is NOT a
  phone-width check. Read back `innerWidth` and say which width you actually
  tested. Below ~500px, confirm on a real phone.
- It cannot tell you about iOS Safari toolbar behaviour, `env(safe-area-inset-*)`,
  or touch/momentum scrolling. Those still need the phone.

Never claim a mobile pass you did not observe; state the width you tested at.

---

## Generated-page build bugs {#generated-pages}
*From the `build.py`/`pages.py` generator pattern.*

- **A concatenated-string page body joined with `,` becomes a tuple.** If
  `blocks` is built as `block(...) + section(...) + ...` and you insert a new
  item with a trailing comma, Python quietly makes a 2-tuple and the rendered
  HTML contains a literal `', '` between the halves. **Assert the type:**
  ```python
  for p in PAGES: assert isinstance(p["blocks"], str), p["slug"]
  ```
- **Never regex-strip a call by bare function name** — the pattern matches the
  `def` too and turns `def steps(items):` into `def:`. Anchor on the call site
  (`+ steps(` / `\n        steps(`) or skip any match preceded by `def `.
- **Grep the built HTML for Python artifacts** before deploy, but exclude
  `<script>`/`<style>` or your own JS string literals produce false positives:
  ```python
  stripped=re.sub(r'<(script|style)[^>]*>.*?</\1>','',html,flags=re.S)
  re.findall(r"', '|\(&#39;|None<|\[\(&", stripped)
  ```
- **Balance-check the CSS after every string surgery** (`{` vs `}`). One stray
  brace silently kills every rule after it — on a junk-removal client it took out every image
  on the page.
- **SVG maps: check label collisions by coordinate,** not by looking. Extract
  every `<text x= y=>` and compare; a county label at `(500,105)` and a town
  label at `(496,115)` overlap. Hide town labels below ~620px where they become
  illegible anyway, and give all map text a dark `paint-order:stroke` halo.

## Third-party widgets (added 2026-07-30, from the BadgerLayer teardown)

**A single third-party widget can undo an otherwise flawless design system, and it does the most
damage exactly where the money is.**

Verified live at a 500px viewport on a competitor agency: a live-chat widget auto-opened a proactive
bubble plus three quick-reply chips that **covered the hero paragraph and part of both hero CTAs**,
then **followed the scroll and permanently obscured the right half of the pricing cards**, hiding
tier feature lists on the single highest-intent section of the page. It was also the only rounded,
animated, off-palette element on a page with radius 0 and one accent colour.

**Rules:**
- Any chat/booking/review widget ships **disabled on mobile by default**, or at minimum with the
  **proactive auto-open turned off** below 900px.
- Test every widget at **≤500px against the pricing and contact sections specifically**, not just
  the hero. Those are the sections it will cover and the ones that cost money.
- Check the widget against the shape and colour system before shipping. A rounded gold pill on a
  square single-accent page reads as a bolt-on because it is one.
- The site's own design can be perfect and still fail this. **Audit what you embed, not just what
  you write.**

## Narrow schema types (added 2026-07-30)

**Use the narrowest schema.org type that fits, never generic `LocalBusiness`.** A competitor's HVAC
client build ships `HVACBusiness`; narrower types are more eligible for rich results.

Common trade types: `HVACBusiness` · `Plumber` · `Electrician` · `RoofingContractor` ·
`HousePainter` · `MovingCompany` · `Locksmith` · `GeneralContractor` · `LandscapingBusiness` ·
`AutoRepair` · `PestControlBusiness` · `SelfStorage` · `DryCleaningOrLaundry`.

For trades with no exact type (junk removal, pressure washing, screen repair), use
`HomeAndConstructionBusiness` or `ProfessionalService` rather than bare `LocalBusiness`.

**Competitor gap worth beating:** their client build had **0 images with `loading="lazy"`, 0 with
`width`/`height`, and 0 in webp/avif** — on a site whose sales page markets "performance-optimized
images". All three are already mandatory on our builds; keep it that way, it is measurable
differentiation.

### Schema: verify the type against the CONTENT, not the business name (added 2026-07-30)

**Narrow to the most specific type that ACTUALLY FITS.** "a small-engine client" reads like
motorcycles; `MotorcycleRepair` looked like an obvious upgrade over `AutoRepair`. The page has
**zero** motorcycle mentions — 48 ATV, 45 UTV, 50 mower, 22 golf cart, plus generators and
chainsaws. `AutoRepair` was already the closest available type and narrowing would have been wrong.
**Grep the copy before changing a schema type.**

**Never ship `FAQPage` without a real, visible FAQ.** Schema has to match what a visitor sees.
Neither a junk-removal client-v2 nor southern-powersports has a true FAQ section, so neither gets FAQPage — the
fix is to build a real FAQ first, not to mark up headings that aren't questions.

**Type arrays are valid and often correct** for multi-service trades:
`"@type": ["LocalBusiness","MovingCompany"]`.

**Pre-deploy schema check:**
```bash
grep -c 'application/ld+json' index.html          # must be >= 1
grep -o '"@type": *"[^"]*"' index.html | sort -u  # must not be ONLY LocalBusiness
```

---

# Checks added after LATENT (2026-07-31)

## Dead features ship silently. Test the interaction, not the markup.

Three features shipped with **complete markup, complete CSS and zero JavaScript**:
an FAQ accordion, four archive filter buttons, and a map panel. Every one of them
looked finished in the source and in a screenshot. Nothing in the build caught it,
because nothing was broken: the handler simply never existed.

**Before calling a build done, click every interactive element in a real browser
and assert a state change.** Cheap and mechanical:

```js
const btns = [...document.querySelectorAll('.faq > div > button')];
const h0 = btns[1].nextElementSibling.getBoundingClientRect().height;
btns[1].click(); await sleep(600);
const h1 = btns[1].nextElementSibling.getBoundingClientRect().height;
// h0 < 4 && h1 > 20  or the accordion is decoration
```

Inventory every `<button>` and every `data-*` attribute the JS reads, and diff
against the handlers that exist. A `data-filt` with no listener is a dead
affordance the visitor will click.

## A JS-contract check belongs in the verifier

`pick()` read `data-img`, `data-t`, `data-m`, `data-d` off elements that carried
only `data-place`, so it assigned a null src on init and the panel shipped
visibly broken. The asset checker could not see it: a src assigned by JS is
invisible to a markup scan.

Assert that every element JS reads from carries the attributes it reads. Exempt
`aria-hidden` copies (decorative clones), and prove the check FAILS when you break
it before trusting it.

## Full-page screenshots lie about anything reveal-gated

A stitched full-page capture does not fire IntersectionObserver, so every
`.rv { opacity: 0 }` element photographs as a blank rectangle. Three separate
"missing image" panics this session were all this artifact: the images were
loaded, complete, and at `opacity: 1`.

**Verify by reading DOM state, or with viewport screenshots at real scroll
positions.** Only trust a full-page capture for layout and rhythm.

## Namespace every modifier class, and let the duplicate-selector check run

`.sel` was introduced for "selected frame, keeps its colour" while `.sel` already
meant the custom `<select>` wrapper. The duplicate-selector check caught it before
it shipped; without it, one of the two silently loses and the failure looks like
three unrelated bugs. Renamed to `.keep`.

## Crop checking is per-frame and blind to rows

`check-crops.py` tests each image against its own frame and has no concept of a
row. It passed clean while a three-card row shipped with two 0.67 portraits and
one 1.50 landscape, visibly ragged. The client caught it, not the tool.

**Card grids enforce ONE shared ratio.** Matching each frame to its own photograph
is right for a standalone image and wrong inside a row.

## Preload must match the srcset the browser resolves

`<link rel=preload as=image href=hero-2400.webp>` with no `imagesrcset` downloads
the 2400 on a phone, where the browser then picks the 1200 from the srcset. 191KB
wasted, and Chrome warns about it in the console if you look.

```html
<link rel="preload" as="image" href="hero-2400.webp"
      imagesrcset="hero-1200.webp 1200w, hero-2400.webp 2400w"
      imagesizes="100vw" fetchpriority="high">
```

## Tap targets fail by fractions

Footer links measured **43.6px** against the 44px floor: `font-size:16px` at
`line-height:1.6` plus `padding-block:9px`. Four tenths of a pixel is invisible to
every visual review and is a real failure. Measure, do not look.

Also worth measuring rather than eyeballing: body copy under 16px (exclude labels
and eyebrows, which legitimately run 12-13px), and horizontal overflow, checking
each element's ancestors for a scroll container before reporting it.

<a id="regression"></a>
## When you REMOVE a section, re-check what it was silently carrying

Deleting a band is never a local edit. Two failures from one removal, 2026-07-30:

- **Cutting a 20-card client grid left the portfolio showing no client work at
  all** until a visitor hovered a catalogue row, and a phone visitor never
  hovers. The grid had been the only always-visible proof; the catalogue's
  hover-reveal was designed as a *second* look at work already seen.
- The catalogue's heading, **"Blank until you look."**, became false the moment
  it was given a resting image. Copy that describes an interaction has to be
  re-read whenever that interaction changes.

Same class, same session: a four-colour legend keyed to a particle map stayed on
the page after the map was replaced by an ambient field, so it pointed at
something that no longer existed.

Checklist after removing or changing any band:
- What did it prove that nothing else now proves?
- Does any copy elsewhere describe the old behaviour? Grep the headings.
- Does any legend, key or count refer to it?
- **Delete its CSS**, and grep the modifier classes it used for collisions.

## `element.click()` does NOT prove a control is clickable

The lightbox close button shipped unclickable. Escape worked, so it read as "the X
is broken" rather than as a stacking problem. It had passed a test that called
`document.querySelector('.lb-x').click()` and saw the lightbox close.

**A synthetic `.click()` dispatches straight at the node and skips hit-testing
entirely.** It cannot tell you whether a real pointer would ever reach the
element. Only `elementFromPoint` at the control's own centre can:

```js
function unreachable(scope) {
  const bad = [];
  scope.querySelectorAll('a[href],button,input,select,textarea,[role="button"]').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    if (r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth) return;
    const hit = document.elementFromPoint(r.left + r.width/2, r.top + r.height/2);
    if (!(hit && (hit === el || el.contains(hit) || hit.contains(el)))) {
      bad.push({ el: el.className || el.tagName,
                 blockedBy: hit ? (hit.className || hit.tagName) : 'nothing' });
    }
  });
  return bad;
}
```

Run it on the page AND inside every overlay, drawer and modal while it is open,
which is where the covering elements live.

**The cause here is worth knowing on its own.** Two positioned siblings with
`z-index: auto` paint in DOM order. The close button sat before the image in the
DOM, so the moment `.lb-img` gained `position: relative` (to fix an unrelated crop
bug) it began painting over the button. Nothing about that change looks like it
touches a button.

> Adding `position` to ANY element can silently bury an earlier sibling that was
> relying on being painted last. After introducing `position` anywhere, hit-test
> the controls near it.

### Clip the rect against every ancestor, or the hit test lies back

The first version of the sweep above flagged five controls that were perfectly
fine: the collapsed mobile menu. A child of a `grid-template-rows:0fr` +
`overflow:hidden` parent still reports its FULL layout rect, so the test looked at
a 435x62 box, hit the hero behind it, and called it unreachable.

Walk the ancestors and intersect the rect with every scrolling or hidden one
before deciding an element is on screen:

```js
if (['hidden','clip','auto','scroll'].includes(c.overflow) || ...) {
  const p = n.getBoundingClientRect();
  const top = Math.max(r.top, p.top), bottom = Math.min(r.bottom, p.bottom);
  if (bottom - top < 2) return null;          // clipped away, not a defect
  r = { top, bottom, ... };
}
```

Run the sweep in both states: menu closed AND menu open. With the menu open,
controls underneath it SHOULD be unreachable, so expect those and ignore them.

## `complete: false` does not mean broken. It often means mid-decode.

Twice in one session a check reported broken images that were fine:

- "36 broken images" was lazy images not yet scrolled into view.
- "1 broken image" reported `complete: false` while simultaneously reporting
  `naturalWidth: 640` and returning HTTP 200. It was mid-decode when sampled.

Before reporting a broken image, do all three:

1. scroll the page fully so nothing is merely un-fetched
2. `await img.decode()` and re-check
3. HEAD the URL and confirm the status

The authoritative check is the third one. Fetch every distinct image the markup
names and assert 200:

```bash
curl -s $H/ | grep -oE 'assets/img/[A-Za-z0-9_-]+\.(webp|jpg|png)' | sort -u |
  while read -r p; do
    code=$(curl -s -o /dev/null -w '%{http_code}' "$H/$p")
    [ "$code" != "200" ] && echo "FAIL $code $p"
  done
```

## A hover-pause is not a freeze

A drifting carousel that pauses on `pointerenter` will read as frozen in any
automated check that just clicked something inside it: the synthetic pointer is
still parked there. Blur, move the pointer away, or measure before clicking. This
produced two false "the gallery is broken" reports.
