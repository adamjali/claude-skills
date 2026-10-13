# Interactive 3D — Three.js, capability-gated

An optional, **heavy** capability: a small interactive 3D object the user can
orbit, with hovering highlights and floating labels. Use it only for a brief
that earns a centerpiece (a product, an "anatomy/how-it-works" explainer). It is
fully gated and lazy — on weak/unsupported hardware it silently drops to a CSS
fallback, so it never breaks a page.

## Contents
- [Decision: canvas pseudo-3D vs Three.js](#decision)
- [Canvas pseudo-3D (no bundler)](#canvas)
- [Why gated + on-demand](#why)
- [Capability gate + fallback](#gate)
- [Scene, procedural geometry, lights](#scene)
- [Orbit controls + scroll-assemble](#controls)
- [Hover raycasting + tracked labels (anti-collision)](#labels)
- [On-demand render loop](#loop)

<a id="decision"></a>
## Decision: canvas pseudo-3D vs Three.js

Default to **canvas pseudo-3D** for the single-self-contained-HTML / no-build
constraint. Three.js is ~155KB and needs a bundler or an import map; even via the
import map below it's a real dependency that fights the inline-everything goal.
For ONE tasteful 3D moment — a hero point-cloud, a value-field surface, a gentle
rotating mesh of dots — a 2D-canvas projection is ~zero-dependency and ships
inline. Reach for the **Three.js** guidance below only when the brief justifies the
weight: real GLB models, true raycast-picking on solid surfaces, material/lighting
fidelity, or rich orbit interaction. Otherwise, canvas wins.

| Want | Use |
|---|---|
| One ambient/hero 3D moment, no build step, inline everything | Canvas pseudo-3D |
| Real GLB models, solid-mesh hover-pick, PBR lighting/materials | Three.js (gated) |
| Self-contained HTML is a hard constraint | Canvas pseudo-3D |
| Brief explicitly earns a bundler / heavy centerpiece | Three.js (gated) |

<a id="canvas"></a>
## Canvas pseudo-3D (no bundler) — prefer this for self-contained / no-build sites

The trick: you don't need WebGL for one 3D moment — you need **perspective
projection done by hand on a 2D canvas**. Take a grid of points whose height is
some value field (a metric, a surface, a terrain), rotate them by an azimuth + a
tilt, sort back-to-front, and draw each as a filled arc whose radius/alpha scales
with depth. That reads as 3D, costs zero dependencies, and lives entirely inline.

Same perf discipline as the Three.js path — gate it, cap it, throttle it, respect
reduced motion — because a naive canvas loop janks just as badly:

- **DPR-capped** (`Math.min(devicePixelRatio, …)`, min 1.5) — high-DPR screens
  otherwise quadruple the fill cost for no visible gain.
- **~30fps throttled** — a 3D ambience doesn't need 60; halving frames halves CPU.
- **IntersectionObserver-gated** — animate only while the canvas is on-screen; stop
  the rAF work entirely when it scrolls away.
- **`prefers-reduced-motion` → render one static frame** and never start the loop.
- **`aria-hidden="true"`** on the animated canvas — it's decorative; keep it out of
  the accessibility tree.
- **Optional pointer drag-to-rotate** — let azimuth follow the pointer for a little
  agency without the weight of orbit controls.

```js
const cv = document.getElementById('field3d'), ctx = cv.getContext('2d');
const RM2 = matchMedia('(prefers-reduced-motion: reduce)').matches;
const DPR = Math.max(1.5, Math.min(devicePixelRatio || 1, 2));
const N = 26, GAP = 1 / N;                                  // grid resolution
const pts = [];                                             // height = a value field
for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
  const x = i * GAP - 0.5, z = j * GAP - 0.5;
  pts.push({ x, z, y: 0.18 * Math.sin(x * 7) * Math.cos(z * 7) });   // swap in real data
}
let az = 0.6, tilt = 0.5, w = 0, h = 0;
function resize() { w = cv.clientWidth; h = cv.clientHeight; cv.width = w * DPR; cv.height = h * DPR; ctx.setTransform(DPR,0,0,DPR,0,0); }
new ResizeObserver(resize).observe(cv); resize();

function project(p) {                                       // rotate by az+tilt → screen + depth
  const ca = Math.cos(az), sa = Math.sin(az);
  const rx = p.x * ca - p.z * sa, rz = p.x * sa + p.z * ca;
  const ct = Math.cos(tilt), st = Math.sin(tilt);
  const ry = p.y * ct - rz * st, depth = p.y * st + rz * ct;
  const s = 1.9 / (2.4 + depth);                            // perspective foreshortening
  return { sx: w/2 + rx * w * s, sy: h/2 + ry * h * s, d: depth, s };
}
function frame() {
  ctx.clearRect(0, 0, w, h);
  const drawn = pts.map(project).sort((a, b) => a.d - b.d); // depth-sort, back to front
  for (const q of drawn) {
    ctx.globalAlpha = 0.25 + 0.55 * (q.s);
    ctx.beginPath(); ctx.arc(q.sx, q.sy, 2.4 * q.s * 3, 0, 7); ctx.fill();
  }
  ctx.globalAlpha = 1;
}
if (RM2) { frame(); }                                       // one static frame, no loop
else {
  let visible = false, last = 0;
  new IntersectionObserver(es => es.forEach(e => visible = e.isIntersecting), { rootMargin: '120px' }).observe(cv);
  cv.setAttribute('aria-hidden', 'true');
  cv.addEventListener('pointermove', e => { const r = cv.getBoundingClientRect(); az = ((e.clientX - r.left) / r.width - 0.5) * 2.4; });   // optional drag-to-rotate
  (function loop(t) {
    requestAnimationFrame(loop);
    if (!visible || t - last < 33) return;                  // IntersectionObserver-gate + ~30fps
    last = t; az += 0.004; frame();
  })(0);
}
```

The whole thing is ~40 lines and one canvas element — no import map, no probe, no
fallback branch (a 2D context is universally supported). Swap the `pts` height
function for whatever the brief's value field is, and tune `N` down on a busy page.

<a id="why"></a>
## Why gated + on-demand

WebGL can jank or fail on low-power devices. So: (1) **gate** on a real
capability probe before importing Three at all, (2) **lazy-init** via
IntersectionObserver, (3) **render on demand** — only when visible and something
changed (`dirty`) or auto-rotating — never a blind 60fps loop. Three.js loads
via an **import map** (no bundler), so it stays a single-file site.

Import map in `<head>`:
```html
<script type="importmap">
{ "imports": {
  "three": "https://example-business.com/npm/three@0.179.0/build/three.module.min.js",
  "three/addons/": "https://example-business.com/npm/three@0.179.0/examples/jsm/"
}}
</script>
```

<a id="gate"></a>
## Capability gate + fallback

`failIfMajorPerformanceCaveat:true` makes the probe return false on software
renderers / weak GPUs — exactly when you'd want the fallback. If the gate fails,
tag the section so CSS shows a static/CSS-3D version instead.
```js
const sec = document.getElementById('anatomy');
const canvas = document.getElementById('roofCanvas');
const RM2 = matchMedia('(prefers-reduced-motion: reduce)').matches;
function hwWebGL() {
  try { return !!document.createElement('canvas').getContext('webgl', { failIfMajorPerformanceCaveat: true }); }
  catch (e) { return false; }
}
if (!sec || !canvas || !hwWebGL()) {
  if (sec) sec.classList.add('no-webgl');     // CSS handles the fallback
} else {
  const THREE = await import('three');
  const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');
  /* … build scene (below) … */
}
```

<a id="scene"></a>
## Scene, procedural geometry, lights

Build geometry **procedurally** (boxes/cylinders/extrudes) rather than loading a
model file — keeps it single-file and tiny. The example is a stack of labeled
layers (generalize to whatever the brief needs: product parts, strata, modules).
Cap pixel ratio for perf.
```js
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'low-power' });
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.6));
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
camera.position.set(5.4, 3.6, 6.0);
scene.add(new THREE.HemisphereLight(0xcfe0ea, 0x4a3a2a, 1.0));
const key = new THREE.DirectionalLight(0xfff1da, 1.25); key.position.set(6, 9, 5); scene.add(key);
const rim = new THREE.DirectionalLight(0xbcd6ff, 0.4); rim.position.set(-6, 2, -6); scene.add(rim);

const group = new THREE.Group(); group.rotation.z = -0.32; scene.add(group);
const LAYERS = [
  { name: 'Layer A', color: 0x9a7a52, t: 0.34, w: 4.30, d: 3.05, aY: 0.00, eY: 0.0 },
  { name: 'Layer B', color: 0x35657e, t: 0.12, w: 4.12, d: 2.90, aY: 0.32, eY: 1.0 },
  { name: 'Layer C', color: 0xa23d2c, t: 0.24, w: 4.22, d: 3.00, aY: 0.56, eY: 2.1 },
];
const meshes = LAYERS.map(L => new THREE.Mesh(
  new THREE.BoxGeometry(L.w, L.t, L.d),
  new THREE.MeshStandardMaterial({ color: L.color, roughness: 0.85, metalness: 0.02 })
));
meshes.forEach(m => group.add(m));
```
(`aY` = assembled Y, `eY` = exploded Y — used by scroll-assemble below.)

<a id="controls"></a>
## Orbit controls + scroll-assemble

Lock zoom/pan (keep the interaction focused), enable damping for weight, give
**wide vertical freedom** (`minPolarAngle`/`maxPolarAngle`) so it doesn't feel
locked, and stop auto-rotate the moment the user grabs it. Scroll drives an
"assemble/explode" by lerping each layer between `eY` and `aY`.
```js
const controls = new OrbitControls(camera, canvas);
controls.enablePan = false; controls.enableZoom = false; controls.enableDamping = true; controls.dampingFactor = 0.09;
controls.autoRotate = !RM2; controls.autoRotateSpeed = 0.75;
controls.minPolarAngle = 0.2; controls.maxPolarAngle = 2.3;   // wide vertical freedom
controls.target.set(0, 0.4, 0);
controls.addEventListener('start', () => { controls.autoRotate = false; });

let assemble = RM2 ? 1 : 0;
const applyAssemble = () => meshes.forEach((m, i) => { m.position.y = LAYERS[i].eY + (LAYERS[i].aY - LAYERS[i].eY) * assemble; });
applyAssemble();
if (!RM2 && window.ScrollTrigger) {
  window.ScrollTrigger.create({ trigger: sec, start: 'top 82%', end: 'center 45%', scrub: 0.6,
    onUpdate: self => { assemble = self.progress; applyAssemble(); dirty = true; } });
  window.ScrollTrigger.refresh();
}
```

<a id="labels"></a>
## Hover raycasting + tracked labels (anti-collision)

Raycast from the pointer to highlight the hovered mesh (emissive) and sync an
HTML label/legend. Labels are HTML (crisp text), each tracking its mesh's
projected screen position, **pinned to the right edge with vertical
anti-collision** so they never overlap (the bug if you skip it: only the top
label is readable).
```js
const ray = new THREE.Raycaster(), ptr = new THREE.Vector2(2, 2);
let hovered = -1, dirty = true, visible = false;
function setHover(idx) {
  if (idx === hovered) return; hovered = idx;
  meshes.forEach((m, i) => m.material.emissive.setHex(i === hovered ? 0x3a1d0f : 0x000000));
  if (labelsEl) [...labelsEl.children].forEach((el, i) => el.classList.toggle('on', i === hovered));
}
canvas.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); ptr.x = ((e.clientX - r.left) / r.width) * 2 - 1; ptr.y = -((e.clientY - r.top) / r.height) * 2 + 1; dirty = true; });
canvas.addEventListener('pointerleave', () => { ptr.set(2, 2); dirty = true; });

const anchor = new THREE.Vector3();
function updateLabels() {                              // project + de-collide vertically
  if (!labelsEl) return;
  const w = canvas.clientWidth, h = canvas.clientHeight;
  const items = meshes.map((m, i) => { anchor.set(0,0,0); m.localToWorld(anchor); anchor.project(camera); return { i, y: (-anchor.y * 0.5 + 0.5) * h }; });
  const order = [...items].sort((a, b) => a.y - b.y);
  const gap = 48, pad = 26;
  for (let k = 1; k < order.length; k++) if (order[k].y - order[k-1].y < gap) order[k].y = order[k-1].y + gap;
  order.forEach(o => { o.y = Math.max(pad, Math.min(h - pad, o.y)); });
  const x = w - 8;
  items.forEach(o => { const el = labelsEl.children[o.i]; el.style.opacity = '1'; el.style.transform = `translate(-100%,-50%) translate(${x}px, ${o.y}px)`; });
}
```

<a id="loop"></a>
## On-demand render loop

The perf heart: render only when **visible** and (`dirty` or auto-rotating).
Declare `dirty`/`visible` **before** `resize()` references them (a `let`-after-use
ordering bug throws a temporal-dead-zone error — see quality-checklist).
```js
let labelsEl = document.getElementById('r3dLabels');
function resize() { const w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); dirty = true; }
new ResizeObserver(resize).observe(canvas); resize();
new IntersectionObserver(es => es.forEach(e => { visible = e.isIntersecting; if (visible) dirty = true; }), { rootMargin: '150px' }).observe(canvas);
function loop() {
  if (visible && (dirty || controls.autoRotate)) {
    controls.update();
    ray.setFromCamera(ptr, camera);
    const hit = ray.intersectObjects(meshes, false)[0];
    setHover(hit ? meshes.indexOf(hit.object) : -1);
    renderer.render(scene, camera);
    updateLabels();
    dirty = false;
  }
  requestAnimationFrame(loop);
}
loop();
```
Add colored legend dots that map to each layer's color so the hover↔label↔legend
relationship is obvious. Keep the whole thing under ~150 lines — if a brief needs
more than this, it probably wants a real 3D pipeline, which is out of scope for a
single-file site.

---

<a id="debugging"></a>
## Debugging a canvas that renders nothing (read this FIRST)

Learned the expensive way, 2026-07-30: a particle field rendered zero pixels and
six hypotheses about geometry, culling, camera, context loss and the shader were
all wrong. The cause was three missing lines of JavaScript.

**A throw inside a `requestAnimationFrame` callback is swallowed by the browser.**
No red console entry an automation tab can read, no visible failure. The WebGL
context stays alive and uncorrupted, the geometry stays valid, the program stays
linked, `object.visible` stays true. Every value you can inspect afterwards looks
perfectly healthy, because the failure is upstream of all of it.

The specific trigger: a shader declared `uniform float uKick;` but the JS
`uniforms` object never defined it, so `uniforms.uKick.value = kick` in the tick
threw `Cannot set properties of undefined` before `renderer.render()` ever ran.

### The two things that make this impossible to lose hours to again

**1. Never let a render loop throw silently.**

```js
function whileVisible(el, tick) {
  let raf = 0, dead = false;
  const loop = (t) => {
    if (dead) return;
    try { tick(t); }
    catch (err) {
      dead = true;                                  // stop, don't throw 60x/sec
      console.error('[gl] render loop threw, scene stopped:', err);
      el.dataset.glError = String((err && err.message) || err);   // readable from JS
      return;
    }
    raf = requestAnimationFrame(loop);
  };
  raf = requestAnimationFrame(loop);
  /* ...IntersectionObserver pause/resume... */
}
```

`el.dataset.glError` matters as much as the console line: an automation tab that
cannot capture console output *can* read a data attribute.

**2. Expose a frame counter.** `frames === 0` is the single signal that separates
"the loop is dead" from "the loop runs and draws nothing". Without it those two
states are indistinguishable, which is what makes this bug so slow to find.

**3. Check the shader/JS contract in CI, not by eye.**
`python3`-free, no deps: `node ~/.claude/skills/site-forge/scripts/check-shaders.js <file.js>`
cross-checks every `uniform`/`attribute` a shader declares against what the JS
defines, and every `uniforms.uX.value` write against the same list. Non-zero exit
= broken. Verified it catches the original bug.

### Diagnostics that LIE, and must not be trusted

| Tool | Why it lies |
|---|---|
| `drawImage(canvas)` into a 2D context | Returns blank from a WebGL canvas without `preserveDrawingBuffer` |
| `material.program.diagnostics` | `material.program` no longer exists in current Three |
| Automation-tab console capture | Captured nothing at all across many attempts |

### Automation-tab artifacts that look exactly like bugs

The Claude-in-Chrome tab reports `document.hidden === true`. Consequences, all of
which read as broken code:

- **`requestAnimationFrame` never fires.** Frame counters read 0 and the canvas
  looks dead. A screenshot forces a paint and unsticks it.
- **CSS transitions never advance**, so every scroll-reveal element measures
  `opacity: 0` and the page looks blank in JS while screenshotting correctly.
- **IntersectionObserver never fires**, so anything gated on scroll-into-view
  stays uninitialised.
- **`await`ing a rAF hangs the renderer** until the CDP call times out (~45s).
  Never await a frame in that tab.

To inspect a reveal-driven page there: force `.in` on every reveal element,
inject `*{transition:none}`, then screenshot.

<a id="particles"></a>
## Particle fields: making a flock, not noise

Four rebuilds to get a murmuration. The failures are more instructive than the
final code, because each one *looked* like a tuning problem and was structural.

### The progression, and why each step failed

| Attempt | Why it read wrong |
|---|---|
| Flow field added to a fixed home position | An oscillation. Each body swings around its own spot and returns, so the field shimmers and goes nowhere |
| Fixed spherical "knots" of bodies | Density variation, but FROZEN: N lumps sliding across the frame in permanent formation |
| Gradient descent to noise minima | Minima are POINTS, so bodies gather into lumps, and lumps in a volume are indistinguishable from a random field however tightly they clump |
| **Isosurface projection** | Correct. See below |

### The thing that actually works

A murmuration is not lumps. It is an enormous number of birds spread across a
thin, curved, folding **sheet**. Every dense passage is where that sheet is
edge-on to the viewer; every wispy passage is where it is face-on. The organised
look comes from one continuous surface bending.

So put every body ON a surface: the isosurface `n(p) = target` of a noise field,
reached by **Newton iteration**. Same gradient as descent, different question.
Descent asks "which way is downhill" and slides to a point. Newton asks "how far
to the surface and in which direction" and lands on it.

```glsl
const vec3 F = vec3(0.16, 0.34, 0.28);        // per-axis field frequency
vec3 drift = vec3(uTravel * -0.55 * F.x, 0.0, uTime * 0.008);
vec3 nq = pos * F + drift;
vec3 basePos = pos; float moved = 0.0; vec3 gw;
for (int it = 0; it < 3; it++) {
  float n0 = snoise(nq);
  vec3 g = vec3(snoise(nq + vec3(E,0,0)) - n0,
                snoise(nq + vec3(0,E,0)) - n0,
                snoise(nq + vec3(0,0,E)) - n0) / E;
  gw = g * F;                                  // chain rule, MULTIPLY (see below)
  float target = 0.055 * sin(pos.x*0.23 - uTime*0.15)
               + 0.028 * sin(pos.y*0.51 + uTime*0.10);
  vec3 stp = gw * ((n0 - target) / (dot(gw, gw) + 0.02)) * uClump;
  float L = length(stp); if (L > 0.9) stp *= 0.9 / L;
  pos -= stp; moved += L; nq = pos * F + drift;
}
if (moved > 1.5) pos = mix(basePos, pos, 1.5 / moved);   // no sheet-hopping
```

### Six rules that each cost a rebuild

1. **Chain rule direction.** `n_world(p) = snoise(p * F)`, so the world gradient
   is the sample-space gradient **times** F. Dividing sends every body off the
   true direction: uneven density, no structure. This one is easy to get backwards.
2. **Anisotropy works FOR the shape once the direction is right.** A field
   stretched along x has shallow gradients in x and steep ones in y, so bodies
   barely move sideways and collapse hard vertically, gathering onto long
   filaments instead of round blobs.
3. **Step size vs band spacing.** A step larger than half the band spacing jumps
   a body clean over the valley it is falling into and it oscillates between two
   ribbons. Use a decaying step (x0.55 each) across 3 iterations.
4. **Cap CUMULATIVE displacement, not just each step.** Otherwise a body
   converges on a different fold of the surface than last frame: a teleport.
5. **Fade whatever never reached the sheet.** Residual distance drives opacity.
   Strays sit throughout the volume with no relation to the shape, and a correct
   structure plus ~8% random specks still reads as random, because the eye
   grades the picture by its worst part. It also gives wispy edges for free.
6. **Random per-body variance is itself read as noise.** Any term keyed to a
   per-body seed is uncorrelated between neighbours BY CONSTRUCTION. Drive every
   motion term from POSITION and TIME only; two bodies close together then always
   get the same vector and the group banks as one. Keep seed for static size and
   colour jitter, and keep both spreads narrow.

### Travel, not oscillation

Displace the whole flock by an accumulating distance and wrap at the frame edge:

- **Integrate speed, do not set position from a sine.** `travel += dt * speed * surge`.
- The surge must be **global**, not per-body, or bodies drift apart and stop
  being one group.
- **Each body wraps at its own span**, computed from its own depth: the frustum
  is wider further back. Uniform world speed across different spans is what
  produces parallax for free (near crosses in ~20s, far in ~70s).
- **Fade the wrap seam.** `mod()` is a hard jump; a body must be invisible while
  crossing it.
- **Clamp `dt`** (50ms). The loop suspends off-screen, so the first frame back
  otherwise carries the whole absence as one step and teleports the flock.

### Popping: it is arithmetic

If a travelling isovalue reveals/hides bodies, the amplitude of the sweep must be
**smaller than the sheet's own thickness**:

```
ratio = isovalue sweep / distance at which a body fully fades
ratio > 1  =>  the surface sweeps CLEAN PAST bodies: fade out, fade back. popping.
ratio < 1  =>  it breathes and shifts without leaving anyone behind.
```
Measured on the real defect: 3.71 (popping) vs 0.87 (fixed).

Also: **never `discard` on an opacity threshold**. It is a step function, so a
body drifting across the line vanishes between frames. And do not square a
`smoothstep` fade: it steepens the shoulder enough that ordinary drift across it
reads as a blink.

### Two metrics that DO NOT detect popping (do not rebuild these)

- **Total scene luminance.** When one body fades out another fades in, so the sum
  barely moves. Read 0.64% vs 0.56% on a genuine 3.7x defect.
- **Per-pixel frame difference.** Small bright sprites on black produce enormous
  per-pixel deltas from ordinary motion, so it saturates. 36.0% vs 33.6% on the
  same defect.

Neither separates popping from movement. Use the ratio arithmetic above instead.

### Cursor interaction

- **Repulsor, never attractor.** An attractor drags a body toward the pointer on
  approach, then the direction flips 180 degrees the instant the pointer crosses
  it and the same body is dragged back: a visible rebound on everything the
  cursor passes. A repulsor cannot do that; it opens a hole that travels with
  the pointer and closes behind.
- **Local means a hard outer edge.** Inverse-square falloff never reaches zero,
  so the whole field leans toward the pointer and reads as a global tilt. Use
  `pow(1.0 - smoothstep(0.0, R, d), 2.0)`: past R, untouched.
- **Momentum is asymmetric.** Engage fast (~0.35s), release slow (~1.7s). Equal
  rates feel like a switch. Accumulate and decay the pointer velocity rather than
  reading it instantaneously, so it keeps pushing after the hand stops.
- Measure velocity from a **smoothed** cursor position; raw events spike violently
  on the first move after a pause.

### An invisible form revealed by the particles

Cheap and striking: an SDF shape that nothing draws.

- **Carve.** Push bodies inside out to the skin. A hole in a dense field reads
  as a solid.
- **Light the rim.** Bodies grazing the skin brighten, enlarge slightly, and
  bypass whatever opacity gate the field uses. Without the rim there is no sense
  of facing as it rotates; without the bypass the object only appears where the
  field is already dense and flickers in and out of legibility.
- **Round any box SDF.** A hard box has zero gradient across each flat face, so
  the outward normal is undefined there and bodies smear along the face instead
  of leaving it. Subtracting a small radius fixes it and it still reads as a cube
  because the edges dominate the silhouette.
- Keep rotation slow (~50s/turn) so it drifts rather than spins.

### Cost

Cheaper than it sounds. 44,000 bodies at 13 noise samples each measured well
under 1ms/frame against a 16.7ms budget. Measure with a bench method that renders
N frames synchronously rather than guessing.
