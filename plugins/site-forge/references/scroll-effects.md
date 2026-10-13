# Scroll Effects — scrub sequences, before/after, and the perf rules

Heavy, high-impact scroll moments. These are **optional capabilities** — use one
as a centerpiece when the brief earns it, not all of them on every site. Read
the [Performance rules](#perf) before adding more than one.

## Contents
- [Canvas image-sequence scrubber (Apple-style)](#scrub)
- [Before / after clip-path wipe](#beforeafter)
- [Scroll UI — progress bar + back-to-top ring](#scrollui)
- [Scroll-driven fill on a TALL section](#tall-fill)
- [Performance rules — read before stacking effects](#perf)

<a id="scrub"></a>
## Canvas image-sequence scrubber

Scrub through a sequence of JPEG frames tied to scroll — the "cinematic" Apple
product-page effect. Key decisions that make it robust:
- **Draw pre-extracted JPEG frames to a canvas — never scrub `video.currentTime`.**
  This is the whole reason the technique exists: mobile browsers (iOS Safari
  especially) stall or render blank on programmatic `currentTime` seeks, so a
  video scrubber that looks fine on desktop ships broken on phones. Frames drawn
  to a canvas scrub reliably everywhere. Export ~60–90 frames from a short clip
  (see `references/images.md` for the ffmpeg extract).
- **Build the ScrollTrigger immediately** and draw the *nearest already-loaded*
  frame, so scrubbing works while frames are still streaming in — never gate the
  build on "all frames loaded" (that race often never fires).
- **Lazy-boot the frame loader** via IntersectionObserver with `rootMargin`
  ~200px so the sequence preloads just before the section arrives, not on page
  load. (A bigger margin like 700px is fine when you want a longer head start;
  200px is the floor that still feels instant.)
- **Re-size the canvas defensively — the boot can win a race with layout.** The
  IntersectionObserver may fire before the section's height settles, so the very
  first `sizeCanvas()` reads a tiny (or zero) `clientWidth` and the backing store
  ends up too small, leaving the frame blurry or absent. Guard for it: re-size
  whenever `canvas.width < canvas.clientWidth * dpr`, and **redraw the current
  frame on every image `onload`** so a late-correct size repaints. Always wire
  `im.onerror` to `console.warn` (a missing frame should surface, not silently
  hold the sequence), and NaN-guard `data-frame-count` (`Number(...) || fallback`)
  so a typo'd attribute degrades to a default instead of looping `NaN` times.
- **If your scrub markup wraps the frames in a track / pinned element, give it a
  dedicated class like `.frames-track` — never the bare `.track`.** That name
  collides with the back-to-top progress ring's faint `.track` circle below, and
  one rule will silently restyle the other.

```js
(() => {
  const section = document.querySelector('.scrub');
  const canvas = document.getElementById('scrubCanvas');
  if (!section || !canvas) return;
  const ctx = canvas.getContext('2d', { alpha: false });
  const COUNT = 80;                                   // number of frames
  const url = i => `seq/frame_${String(i + 1).padStart(3, '0')}.jpg`;
  const frames = [], loaded = [], state = { i: 0 };

  function nearestLoaded(idx) {                        // fallback while streaming
    if (loaded[idx]) return idx;
    for (let d = 1; d < COUNT; d++) { if (loaded[idx - d]) return idx - d; if (loaded[idx + d]) return idx + d; }
    return -1;
  }
  function draw(req) {                                 // cover-fit draw
    const idx = nearestLoaded(Math.max(0, Math.min(COUNT - 1, req | 0)));
    if (idx < 0) return;
    const img = frames[idx], cw = canvas.width, ch = canvas.height;
    const ir = img.naturalWidth / img.naturalHeight, cr = cw / ch;
    let dw, dh, dx, dy;
    if (ir > cr) { dh = ch; dw = ch * ir; dx = (cw - dw) / 2; dy = 0; }
    else { dw = cw; dh = cw / ir; dx = 0; dy = (ch - dh) / 2; }
    ctx.drawImage(img, dx, dy, dw, dh);
  }
  function sizeCanvas() {
    const dpr = Math.min(devicePixelRatio || 1, 1.5);  // cap DPR — perf
    canvas.width = Math.round(canvas.clientWidth * dpr) || 2;
    canvas.height = Math.round(canvas.clientHeight * dpr) || 2;
    draw(state.i);
  }
  let started = false;
  function preload() {
    if (started) return; started = true;
    for (let i = 0; i < COUNT; i++) {
      const img = new Image();
      img.onload = () => { loaded[i] = true; if (i === 0) sizeCanvas(); draw(state.i); };
      img.onerror = () => {};
      img.src = url(i); frames[i] = img;
    }
    sizeCanvas();                                      // build the scrub NOW
    if (!RM) {
      gsap.to(state, { i: COUNT - 1, ease: 'none',
        scrollTrigger: { trigger: section, start: 'top top', end: 'bottom bottom', scrub: 0.4, invalidateOnRefresh: true, onUpdate: () => draw(state.i) } });
      ST.refresh();
    }
  }
  new IntersectionObserver((es, ob) => es.forEach(e => { if (e.isIntersecting) { preload(); ob.disconnect(); } }), { rootMargin: '200px' }).observe(section);  // floor that feels instant; bump toward 700px for a longer head start
  addEventListener('resize', sizeCanvas);
})();
```
The `.scrub` section is tall (e.g. `height:300vh`) with a `position:sticky`
canvas inside, so scroll distance maps to frames. If you have no video, this same
sticky-canvas slot can hold a single image with a Ken-Burns transform instead
(the `auto`-mode fallback).

<a id="beforeafter"></a>
## Before / after clip-path wipe

Two stacked images; scroll wipes the "after" over the "before" via an animated
`clip-path: inset(…)`, with a draggable-looking edge line that tracks the seam.
Pin the section (`height:200vh`, sticky inner) so the wipe spans real scroll.
```js
(() => {
  const after = document.querySelector('.ba-after'), edge = document.querySelector('.ba-edge'), baEl = document.querySelector('.ba');
  if (!after || !baEl) return;
  if (RM) { after.style.clipPath = 'inset(0 0 0 0)'; return; }   // static: show "after"
  let baW = baEl.clientWidth;
  addEventListener('resize', () => { baW = baEl.clientWidth; });
  const s = { p: 0 };
  gsap.to(s, { p: 1, ease: 'none', scrollTrigger: {
    trigger: '.ba-sec', start: 'top top', end: 'bottom bottom', scrub: .5, invalidateOnRefresh: true,
    onUpdate: () => {
      after.style.clipPath = `inset(0 0 0 ${(1 - s.p) * 100}%)`;
      edge.style.transform = `translateX(${(1 - s.p) * baW}px)`;
      edge.style.opacity = (s.p > 0.01 && s.p < 0.99) ? '1' : '0';
    }
  }});
})();
```
This shines when the two images are a genuine transformation (worn→new,
before→after, day→night). Generate the pair with the same-base edit trick in
`references/ai-media.md` so they register perfectly.

<a id="scrollui"></a>
## Scroll UI — progress bar + back-to-top ring

The standard award-site scroll chrome: a thin bar across the top that fills as
you read, and a circular back-to-top button whose ring mirrors the same
fraction. It's cheap, it's expected on a polished site, and it gives the page a
sense of length and place. Two behaviours carry it:
- **The button appears only after you've scrolled** (~500px), never at the very
  top — a back-to-top control at the top is noise. Reveal it by toggling a
  `.show` class, not by animating from zero, so it can't flicker on at `y=0`.
- **Scroll-to-top routes through Lenis when present** so the trip uses the same
  smooth-scroll engine as the rest of the page (`window.__lenis`); fall back to
  native `scrollTo({behavior:"smooth"})` when Lenis isn't on the page.

Precompute the ring circumference once (`2π × r`, with `r=22` here) and set it as
the `stroke-dasharray`; then drive a single `stroke-dashoffset` from full to zero
as progress goes 0→1. Run the whole thing off one **passive** scroll listener —
it only reads `scrollY` and writes transforms, so it must never block scrolling.

```js
(() => {
  const prog = document.querySelector('.scroll-prog');
  const toTop = document.querySelector('.to-top');
  const bar  = toTop && toTop.querySelector('.bar');
  if (!prog || !toTop || !bar) return;
  var C = 2 * Math.PI * 22;                 // ring circumference (r = 22)
  bar.style.strokeDasharray = C;
  addEventListener('scroll', () => {
    var p = Math.min(1, scrollY / (document.documentElement.scrollHeight - innerHeight));
    prog.style.transform = 'scaleX(' + p + ')';
    bar.style.strokeDashoffset = C * (1 - p);
    toTop.classList.toggle('show', scrollY > 500);
  }, { passive: true });
  toTop.addEventListener('click', () => {
    window.__lenis ? __lenis.scrollTo(0) : scrollTo({ top: 0, behavior: 'smooth' });
  });
})();
```

Markup — a fixed bar that scales from its left edge, and a button wrapping an SVG
with two concentric circles (a faint `.track` and an accent `.bar`). Rotate the
SVG `-90deg` so the ring starts filling from 12 o'clock. The button is hidden by
default and revealed only by `.to-top.show`:
```html
<div class="scroll-prog" aria-hidden="true"></div>
<button class="to-top" aria-label="Back to top">
  <svg viewBox="0 0 50 50">
    <circle class="track" cx="25" cy="25" r="22"></circle>
    <circle class="bar"   cx="25" cy="25" r="22"></circle>
  </svg>
</button>
```
```css
.scroll-prog { position: fixed; top: 0; left: 0; right: 0; height: 3px;
  background: var(--accent); transform-origin: 0 50%; transform: scaleX(0); z-index: 60; }
.to-top { position: fixed; bottom: 24px; right: 24px; opacity: 0; pointer-events: none;
  transition: opacity .3s; z-index: 60; }
.to-top.show { opacity: 1; pointer-events: auto; }
.to-top svg { transform: rotate(-90deg); }                  /* ring starts at top */
.to-top .track { fill: none; stroke: rgba(255,255,255,.15); stroke-width: 3; }
.to-top .bar   { fill: none; stroke: var(--accent); stroke-width: 3; stroke-linecap: round; }
```
Note the `.track` class here is the back-to-top ring's faint circle — keep the
canvas scrubber's frames track on a different name (`.frames-track`) so the two
don't collide.

<a id="perf"></a>
<a id="tall-fill"></a>
## Scroll-driven fill on a TALL section, measured against the section not the viewport
A "how it works" flow that fills in as you scroll is a staple. The trap: the
section is a short horizontal row on desktop and a tall vertical stack on mobile,
and a viewport-anchored formula that feels right on desktop finishes on mobile
while step one is still the only thing on screen.

**Wrong** — the whole progress range is a fraction of the viewport, so on a
section three screens tall it completes almost immediately:
```js
var p = (innerHeight * 0.82 - r.top) / (innerHeight * 0.44);
```

**Right** — on narrow screens divide by the SECTION's own height, so progress
tracks how far you have scrolled *through* it and the last step lights up as you
actually reach it:
```js
var r = flow.getBoundingClientRect();
var narrow = innerWidth < 900;
var p = narrow
  ? (innerHeight * 0.66 - r.top) / Math.max(1, r.height * 0.72)   // scales with the stack
  : (innerHeight * 0.82 - r.top) / (innerHeight * 0.44);
p = Math.max(0, Math.min(1, p));
flow.style.setProperty('--fill', (p*100).toFixed(1) + '%');
steps.forEach(function(s,i){ s.classList.toggle('lit', p >= (i+0.55)/steps.length); });
```
`Math.max(1, …)` guards a zero height before layout. Because the divisor is the
element's own height, the timing self-corrects when the stack gets taller (more
steps, longer copy) instead of needing a new magic number.

Always give it a `prefers-reduced-motion` branch that sets the fill to 100% and
lights every step immediately, and a hard-finish safety net so a fill can never
strand half-drawn.

## Performance rules (read before stacking effects)

The fastest way to make a beautiful site feel cheap is to run every heavy effect
at once. Discipline:
- **One heavy effect per viewport.** Stagger the scrubber, the 3D, and the
  before/after down the page so only one is computing at a time. Never put two
  scrubbing canvases on screen together.
- **Lazy-init everything below the fold** with IntersectionObserver — don't
  preload a 90-frame sequence or boot a WebGL context the user may never reach.
- **Cap DPR** (`Math.min(devicePixelRatio, 1.5)`) on canvas/WebGL — retina at
  full DPR quadruples fill cost for little visible gain.
- **`will-change` is a loan, not a gift.** Add it only to elements actively
  transforming; leaving it on everything bloats GPU memory and backfires. Prefer
  toggling it on enter / off on exit.
- **`contain: paint`** on self-contained animated sections to isolate their
  repaints from the rest of the page.
- **Render on demand** for anything you drive yourself (3D, canvas) — only draw
  when visible AND something changed (a `dirty` flag), not every rAF.
- Always provide the **reduced-motion static path** — it's both accessibility
  and your low-power fallback.
