# SVG line work: a scroll-drawn thread that actually behaves

A single line weaving down a page, drawn by scroll, with loops. It looks like a
small ornament and it has more failure modes than anything else in a static
build. Every section below is a defect that shipped.

Performance of the reveal itself lives in `scroll-performance.md` §3 and §7.

---

## 1. One page-height path, not per-gap segments

The first version was 31 separate `<div>` dividers, one in each gap between
sections. Two things were wrong: the line only existed in the gaps, so it
vanished for most of the scroll, and the gaps added **1,853px of empty band** to
one homepage. Generate ONE path in real pixel coordinates for the whole document
and let sections sit on top of it.

```js
svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
main.insertBefore(svg, main.firstChild);
```

Rebuild on resize and on `load`, debounced. The document grows as lazy images
land, so a path built at DOMContentLoaded is the wrong length.

## 2. The stacking trick that puts the line BEHIND content

`position: relative` with **no** `z-index` does not create a stacking context.
That single fact is what makes this work:

```css
main            { position: relative }
.spine          { position: absolute; inset: 0; z-index: 1; pointer-events: none }
main > section  { position: relative }          /* NO z-index */
.band > .wrap   { position: relative; z-index: 2 }
.hero, .phero   { z-index: 2 }                  /* opening frame beats the line */
```

A band paints its background in the background layer, the line paints above it at
1, the band's content paints above that at 2. Give a band a `z-index` and it
becomes a stacking context and swallows the line again.

**Do let the line cross mid-page full-bleed photo panels** (at a lower opacity).
Excluding them meant that on a screen dominated by one, the drawn line was hidden
and all the visitor saw was the faint undrawn track, which reads as "the
animation is not working".

## 3. Per-band colour: gradient with hard stops, not blend modes

One SVG spans the page, so it cannot take a per-band colour the way a component
can. `mix-blend-mode: difference` solves it automatically and costs a full-layer
re-composite every frame (`scroll-performance.md` §5).

Build a `linearGradient` in user space with **two stops per band at identical
offsets**, so the colour flips exactly at the seam instead of fading across it:

```js
bands.forEach(function (b) {
  var col = b.dark ? '#F4F4F2' : '#0B0B0C';
  var o = b.photo ? 0.62 : (b.dark ? 0.92 : 0.9);
  grad.appendChild(stop(b.top / h, col, o));
  grad.appendChild(stop(b.bottom / h, col, o));
});
```
```css
.spine .draw { stroke: url(#spine-grad) }
```

Detect a band's tone from its class AND its computed background luminance, so a
band added later is handled without touching this code.

**Paper needs MORE alpha than ink**, not less: a dark line on a light field reads
quieter than a light line on a dark one at the same value.

## 4. Loops: cubics, never arcs

Two arc attempts both failed, for reasons worth knowing:

- A chord **exactly equal to 2r** is the degenerate case where the large-arc flag
  is ambiguous. Browsers disagree.
- A chord **longer than 2r** makes the spec scale the radii up until they fit, so
  it silently stops being the circle you asked for.

Together they produced a lopsided kink that read as a rendering glitch.

## 5. The loop must be tangent-continuous, in the PATH's frame

The cubic rewrite still glitched, because it hardcoded "the path arrives
travelling straight down": the first control point sat directly below the join.
A weaving path arrives **diagonally**, so the line kinked to enter the loop and
kinked again to leave it.

Build the circle in the path's own frame. Given arrival point P and unit tangent
t, centre `C = P + r*n`, and parametrise so the tangent at theta=0 IS t. Entry and
exit tangents then match by construction, at any arrival angle:

```js
function loopPath(px, py, tx, ty, r, side, adv) {
  var k = 0.5522847498 * r;                    // kappa: quarter circle as a cubic
  var nx = -ty * side, ny = tx * side;
  var cx = px + nx * r, cy = py + ny * r;
  var ux = -nx, uy = -ny;                      // centre -> P
  var vx = -uy * side, vy = ux * side;         // equals t
  // four quarter points, each stepped forward by adv/4 along t so it crosses itself
}
```

Get the arrival tangent from the curve you are actually drawing. For Catmull-Rom
the tangent at `p2` is proportional to `p3 - p1`.

**Verify in isolation before rendering.** Reimplement in Python, assert the entry
and exit tangents equal the arrival tangent to machine precision across a range
of arrival angles and both sides. This catches the bug in seconds; a browser
screenshot takes minutes and only shows you one case.

## 6. Drive the reveal by a MONOTONIC scroll anchor, not by document y

Mapping scroll fraction onto path-length fraction is wrong: a meandering path is
longer than the document (13,709px over 8,480px, a factor of 1.62), so the head
drifts off screen and the drawn end is nowhere near the viewport.

Mapping document `y` to path length fixes that and **breaks at every loop**:
inside a loop the path climbs and comes back down, so ~2πr of path shares one
narrow band of y. "Length at this y" jumps from loop-entry to loop-exit and the
whole loop appears in a single frame. The user description is exact: *it jumps to
that height on the loop then continues.*

Build a third column when you sample the path: `y` forced monotonic, with any
stretch that does not descend given a scroll budget proportional to its own arc
length.

```js
var seg = Math.hypot(pt.x - prevPt.x, pt.y - prevPt.y);
anchor = Math.max(anchor + seg * 0.42, pt.y);
lut.push([pt.x, pt.y, at, anchor]);
```

Descending stretches still track y exactly, so the head stays put on screen. A
loop costs a couple of hundred pixels of scrolling and draws around itself.
Because the anchor column is monotonic, lookup is a binary search that can never
step backwards.

**Measure it**: step the page 12px at a time and record the drawn length. The
worst single-frame advance should be a few tens of pixels. Before the fix it was
the whole loop (~390px at r=62).

## 7. Draw ahead of the reader

Target `pageYOffset + innerHeight * 0.62`, not the top or the centre. The head
sits just below the middle of the screen at every scroll position and is always
slightly ahead of what is being read.

## 8. Marks, not dots

A travelling node that is the same shape everywhere reads as a loading spinner.
Give each section seam a different mark and cycle them. On a photography build
these were the marks that appear on real film and contact sheets: a registration
cross with a gap at the centre, a china-marker ring, a solid stop, a crop corner,
a splice tick, a rebate diamond. The vocabulary should come from the subject.

Build them with `createElementNS` and an attribute helper rather than string
concatenation into `innerHTML`. Same result, no injection sink to argue about.

---

## Checklist

- [ ] One path for the document, rebuilt on resize and load.
- [ ] Bands carry no `z-index`; content does.
- [ ] Colour from a hard-stop gradient, not a blend mode.
- [ ] Loops are cubics, tangent-continuous, verified numerically.
- [ ] Reveal driven by a monotonic anchor, not raw y and not path fraction.
- [ ] Worst single-frame draw advance measured and under ~50px.
- [ ] Head lands in the viewport at every scroll position.
- [ ] Path segmented for the reveal (`scroll-performance.md` §3).

---

## 9. Lock the anchor count, or the line reroutes on every reflow

Every term in the weave should depend on the viewport WIDTH: the edge inset, the
amplitude, the loop radius, the swell. If any term comes from the document
HEIGHT, the route changes whenever the page reflows.

The one that did was the anchor count, `round(h / step)`. At a 661px viewport
`step` is 516, so a document of 8658px gives 17 anchors and anything under about
8510px gives 16. Fonts swapping from the fallback move an eleven-section page by
more than that on their own. Result: the line drew one way on first paint and a
visibly different way a moment later. The user's words: *it switches tracks.*

**Quantising the height was tried first and is worse.** It does not remove the
boundaries, it moves them, and because one quantum spans more than two anchors it
makes the jump bigger when it happens.

Lock it instead, and re-derive only on a real change:

```js
if (lockN === null || w !== lockW || Math.abs(h - lockH) > 1500) {
  lockN = Math.max(3, Math.round(h / step));
  lockW = w; lockH = h;
}
```

Verify by forcing the reflow rather than waiting to catch it: append a 520px
spacer, dispatch resize, and assert the curve count is unchanged. Then append
2600px and assert it DOES change.

## 10. Never give a hidden helper element the same class as the visible ones

The path is generated once and kept, hidden, purely to call `getTotalLength()`
and `getPointAtLength()` on. It was created with `class="draw"`, the same class as
the 40 visible segments.

Every "is the line complete?" check then counted 41 elements, found 40 visible,
and reported the line one segment short. That was investigated twice, and once
"fixed" by scaling the anchors to 0.94 of their range, which made the line
genuinely stop early: a real defect introduced to solve an imaginary one.

Give helper elements their own class (`measure`), always. A hidden element
sharing a class with visible ones poisons every count that will ever be written
against it.

## 11. Mask the line off content, not just text

A hairline crossing a map, a filter bar or a row of buttons is the same defect as
one crossing a paragraph. The mask selector should cover everything the eye has
to read or aim at:

```
h1,h2,h3,h4,p,li,blockquote,figcaption,.lbl,.exif,.lead,.meta,.cap,
.map-c,.map-p,.filt,.btn,.rail-nav,.dgm,.key,.stars,.social,.film,.dl
```

Verify by geometry, not by eye: take the element's rect in document space and
assert some black mask rect fully contains it.
