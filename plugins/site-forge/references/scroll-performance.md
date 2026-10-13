# Scroll performance: the bugs that make a build feel cheap

`scroll-effects.md` covers how to BUILD scroll effects. This covers why they jank,
and every entry is a real defect that shipped and was then measured, not a
best-practice list. All figures are from a 9,500px photography page on a 2019
Intel MacBook, Chrome, 1440x900.

## Use a PERFORMANCE TRACE, not frame-rate sampling

Read this before the list, because getting it wrong cost a whole session.

Frame-rate sampling under CPU throttling has **plus or minus ten points of
run-to-run variance**, which is wider than most of the effects worth finding. On
one build it scored "GSAP disabled" as WORSE than "GSAP enabled". Two separate
conclusions drawn from it were wrong, and a third was right by luck.

A trace finds the same thing in one pass and names it by file and line:

```
performance_start_trace (reload: false, autoStop: false)
  -> scroll the page for ~4s
performance_stop_trace
performance_analyze_insight (insightName: "ForcedReflow")
```

It returned: *"top function call that caused forced reflow: move @ site.js:729,
total reflow time 197ms"*. That is the answer, immediately, with no ambiguity.

**Sampling still has one job**: confirming a fix moved the number, on the same
machine, several runs. Never use it to choose BETWEEN candidates.

And when you do sample: run three passes and **discard the first** (cold decode),
or you measure loading rather than scrolling.

---

**Then, and only then, isolate.** Remove one candidate at a time and re-measure:

```js
async function frameCost(label) {
  window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 450));
  const times = []; let last = performance.now(), on = true;
  (function tick(t){ times.push(t - last); last = t; if (on) requestAnimationFrame(tick); })(performance.now());
  const t0 = performance.now();
  while (performance.now() - t0 < 2600) {
    window.scrollBy(0, 16);
    await new Promise(r => requestAnimationFrame(r));
  }
  on = false;
  const f = times.slice(5).filter(x => x > 0).sort((a, b) => a - b);
  return { label,
    median: f[Math.floor(f.length / 2)],
    smoothPct: 100 * (1 - f.filter(x => x > 32).length / f.length) };
}
```

Run it three times. **The first pass is always worse** (cold image decode) and
that difference is not your bug. On the build this came from, the first
hypothesis was wrong twice: the scroll-drawn line looked like the obvious
culprit and at steady state it cost nothing at all.

---

## 1. Chrome rounds `scrollLeft` to whole pixels

A per-frame delta under 0.5px rounds back to where it started, every frame, and
the element **never moves** while the rAF loop runs flat out.

Three marquee rows drifting at 0.42, 0.53 and 0.64 px/frame: rows two and three
rounded up to 1px and looked fine, row one rounded down and sat frozen. It reads
as "that row is broken", not as a rounding issue.

```js
// WRONG: silently dead below 0.5px/frame, and quantises every other speed to 60px/s
vp.scrollLeft += speed;

// RIGHT: accumulate in a float, write the sum
r.pos += r.speed * r.dir;
if (r.pos >= r.half) r.pos -= r.half;
else if (r.pos < 0) r.pos += r.half;
r.vp.scrollLeft = r.pos;
```

Any hand-driven move (drag, wheel, keys) must hand the position back:
`function sync(){ r.pos = vp.scrollLeft; }` on `pointerup` and `wheel`.

**Related:** a seamless wrap must never come to rest exactly ON the boundary.
`>= half -> subtract` plus `<= 0 -> add` ping-pongs forever when a row lands on
`half`. Land one pixel inside the interval.

## 2. The rAF guard has to be released inside the callback

```js
var ticking = false;
function onScroll(){ if (!ticking) { ticking = true; requestAnimationFrame(draw); } }
function draw(){
  ticking = false;        // <- omit this and draw() runs ONCE, ever
  ...
}
```

Without it the flag latches true on the first scroll event and nothing is ever
scheduled again. The symptom is not "slow", it is "the effect does not work",
which sends you looking in completely the wrong place.

## 3. `stroke-dasharray` is priced by PATH LENGTH, on every repaint

The browser walks and tessellates the dash pattern along the **entire** path each
time it paints. Measured on one 13,709px path, everything else identical:

| | median frame |
|---|---|
| dashed | 32.4 ms |
| undashed | 16.8 ms |

It got worse the moment the path grew, which is the trap: a change that looks
purely visual (adding loops) doubles the frame cost.

**Fix: split the path into ~40 segments.** Everything before the head is a plain
undashed stroke, everything after is `visibility:hidden`, and exactly ONE segment
is ever mid-reveal. Dash work drops from 13,709px to ~340px.

```js
// state per segment: 0 hidden, 1 revealing, 2 fully drawn. Write only on change.
var want = at >= sg.to ? 2 : (at <= sg.from ? 0 : 1);
if (want === sg.state && want !== 1) continue;
```

Sample at ~11px spacing and emit each segment as a polyline. On a curve whose
tightest radius is 62px that is a quarter-pixel sagitta: invisible, and cheaper
to paint than a bezier.

## 4. Animating `scale` on a large bitmap re-rasterises it every frame

A GSAP scrub doing `scale: 1.09 -> 1` on a 1200px image was one of the largest
single costs in a page. **Pre-scale once in CSS and animate only the transform:**

```css
.plate-media > img { height: 108%; will-change: transform; }
```
```js
gsap.fromTo(m, { yPercent: -4 }, { yPercent: 4, ease: 'none', scrollTrigger: {...} });
```

A translate is composited on the GPU. A scale is not.

## 5. `mix-blend-mode` on a full-page-height layer

Elegant for auto-contrast (`difference` gives near-black on paper and near-white
on ink from one stroke colour) and it forces the browser to re-composite that
entire layer against the page every frame. On an 8,480px-tall SVG that is not
affordable. See `svg-line-work.md` for the gradient-with-hard-stops replacement,
which is computed once and costs nothing.

## 6. `content-visibility: auto` trades frames for scroll-height lies

It genuinely helps (26% -> 83% smooth frames on one page) and it was **reverted**.
An unmeasured band falls back to `contain-intrinsic-size`, so the document
reported 8,598px instead of its real 9,484px and grew as you scrolled. The
scrollbar drifts under the user's thumb.

Fatal here for a second reason: anything measuring `scrollHeight` (a scroll-drawn
line, a progress bar) is now measuring a document that is not the one on screen.

Use it only when nothing reads the document height and you can set
`contain-intrinsic-size` close to the real value.

## 7. Guard every per-frame write

Three unconditional operations per scroll frame is enough to lose 60fps:

- `path.getPointAtLength()` forces the browser to walk SVG geometry. If you
  already sampled the path into a table, lerp between two array entries instead.
- A `strokeDashoffset` write repaints the path. Round it and skip no-ops.
- `classList.toggle()` invalidates style. Toggling 7 stations 60 times a second
  when they change 6 times in a whole page is pure waste. Track the count.

```js
var off = Math.round(at);
if (off !== lastOff) { /* ...writes... */ lastOff = off; }
```

## 8. Layout thrashing: read everything, THEN write everything

The trace's number one finding, twice, on two different functions. The pattern is
always the same and always looks innocent:

```js
rows.forEach(function (row) {
  var r = row.getBoundingClientRect();        // READ
  var over = row._tr.scrollWidth - row.clientWidth;   // READ
  row._tr.style.transform = '...';            // WRITE, invalidates layout
});                                           // next iteration READS again -> reflow
```

Every read after a write forces a synchronous layout. Three instances on one page:

| where | cost |
|---|---|
| a multi-row parallax reading rect + scrollWidth + clientWidth per row | 197 ms |
| a draw loop reading `main.getBoundingClientRect()` every frame | 92-151 ms |
| a progress bar reading `root.scrollHeight` every frame | 92 ms |

Two fixes, applied together:

1. **Cache what does not change while scrolling.** `scrollWidth`, `clientWidth`,
   `scrollHeight` and the document's own offset only change when layout does.
   Measure them on resize and load, never in the scroll callback.
2. **Split the loop.** One pass collecting rects into an array, a second pass
   writing transforms. The browser then lays out once per frame, not once per
   element.

One forced reflow per frame is normal and fine. N of them is the bug.

## 9. GSAP is not free, and four translations do not justify it

117KB of JavaScript (gsap + ScrollTrigger) for four `yPercent` parallax moves,
and **274ms of forced reflow** in the trace: it reads layout for its own
bookkeeping on every update and there is no way to opt out.

Replaced with one batched rAF loop, about 40 lines, same visual result. Also
removed a CSP origin and a third-party dependency.

Keep GSAP when you need what it is actually good at: timelines, pinning,
horizontal scroll-hijack, staggered orchestration. A handful of scroll-linked
translations is not that.

## 10. `loading="lazy"` defers the fetch, which forces decode INTO a scroll frame

The single biggest first-impression win on an image-heavy page, and the symptom
is unmistakable: **rough on the first scroll, fine once you have been all the way
down.** That is decode, and it disappears once everything is decoded.

A 2400px webp is 8.6 million pixels. `loading="lazy"` waits until the image is
near the viewport to fetch it, so it is also decoded near the viewport, which
means inside a scroll frame.

| | smooth frames | worst frame |
|---|---|---|
| lazy, cold first scroll | 58% | 167 ms |
| lazy, warm second pass | 72% | 116 ms |
| no lazy + decode warm-up, cold | **85%** | |

Fix, for sites where scroll quality outranks initial bytes:

- drop `loading="lazy"`, add `fetchpriority="low"` to everything below the fold,
  so it queues after the critical path but starts immediately
- after `load`, decode every image during idle time, in document order

```js
var idle = window.requestIdleCallback || function (cb) {
  return setTimeout(function () { cb({ timeRemaining: function () { return 8; } }); }, 16);
};
(function step(deadline) {
  while (i < imgs.length && deadline.timeRemaining() > 4) imgs[i++].decode().catch(function(){});
  if (i < imgs.length) idle(step);
})({ timeRemaining: function () { return 8; } });
```

**Count the real payload before worrying about it.** Summing every file the
markup names counts every srcset candidate: one page "totalled" 13.6MB and a real
first visit transferred 3.8MB, because the browser picks one candidate per slot.

## 11. Compositor promotion can make it WORSE. Measure, do not assume.

`will-change: transform` + `translateZ(0)` + `contain: paint` on two constantly
moving tracks, on the theory that 28 translating images should move one layer
instead of re-compositing 28 rasters.

A/B, two runs each: **promoted 79.5% smooth, unpromoted 89.5%.** Reverted. The
memory and compositing cost of forcing the layer exceeded the raster work saved.

`will-change: transform` alone was enough. Promotion is a trade, not an upgrade.

## 12. `prefers-reduced-motion` is not a performance lever

It fires only for users who set it at OS level. If it were active you would see no
animation at all, so it cannot be the cause of jank you are watching happen. Never
strip it chasing frames; it is a craft floor item and it costs nothing.

---

## Checklist

- [ ] No `el.scrollLeft += n` with n possibly < 0.5. Float accumulator.
- [ ] Every rAF-guarded callback sets `ticking = false` on entry.
- [ ] No `stroke-dasharray` on a path over ~2000px without segmenting.
- [ ] No `scale` animated on a bitmap in a scroll scrub.
- [ ] No `mix-blend-mode` on an element taller than a viewport or two.
- [ ] `content-visibility` only where nothing reads `scrollHeight`.
- [ ] Every per-frame DOM write guarded by a changed-value check.
- [ ] Measured by isolation, three passes, first pass discarded.
- [ ] No `loading="lazy"` on an image-heavy page; warm the decodes at idle instead.
- [ ] Reads and writes separated into two passes in every per-frame loop.
- [ ] Nothing reads `scrollWidth`/`scrollHeight`/`getBoundingClientRect` per frame that could be cached.
- [ ] Compositor promotion A/B tested, not assumed.
- [ ] Diagnosed with a trace, confirmed with sampling. Never the reverse.
