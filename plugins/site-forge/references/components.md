# Components

Drop-in, framework-free components — each is HTML + CSS + a self-contained JS
IIFE. All guard for missing elements (`if (!el) return`) so you can include the
JS even when the section isn't on the page. Generalize the copy/classes to the
brief; the JS hooks (ids) are what matter.

## Contents
- [Testimonial / review carousel](#testimonial--review-carousel)
- [Video player (autoplay-in-view → click for sound)](#video-player)
- [Animated counters (decimal-aware)](#animated-counters)
- [Netlify Forms — contact/lead form](#netlify-forms)
- [Nav links — growing-underline hover (both states)](#nav-links)
- [Mobile hamburger — animated 3-lines-to-X (all scroll states)](#hamburger)
- [Header: transparent + compact at top, solid + taller on scroll](#header-scroll)
- [Mobile submenu — the `0fr` accordion that will not collapse](#submenu)
- [Preloader — logo, bar, slide-up reveal (static builds)](#preloader-static)
- [Hero stamp / seal that interrupts a divider](#seal)
- [Hero scrim — readable text over a bright photo](#hero-scrim)
- [Ghost button — inverts to solid white on hover](#btn-invert)
- [`<button class="btn">` — the UA `buttonface` trap](#btn-ua)
- [Fixed mobile action bar — iOS + Android safe area](#actionbar)
- [Photo wall — uniform grid, never `column-count`](#photo-wall)
- [Gallery page — filters + spotlight viewer](#gallery)

---

## Testimonial / review carousel
Native scroll-snap track (momentum + accessible) with arrows and generated dots.
No library. Why scroll-snap over a JS slider: it's GPU-smooth, keyboard/touch
native, and degrades gracefully.

> **PREFERRED for infinite + smooth mobile: a NATIVE `overflow-x:auto` scroll
> container with 3 cloned card-sets — do NOT hand-roll a transform drag.** A custom
> pointer-drag / wheel-translate carousel feels glitchy on touch (no native
> momentum) and is a nest of gotchas (photo ghost-drag, pointer-capture eating the
> click, double-tap-zoom). Native scroll gives real momentum on touch, trackpad
> two-finger, and horizontal wheel for free, and clicks Just Work. (Learned the
> hard way on a lawn-care client 2026-07-21 — the transform version below was glitchy on
> mobile and broke the desktop click; the native rebuild fixed all of it.)
>
> Build it: `.car-vp{overflow-x:auto;overflow-y:hidden;scrollbar-width:none;
> -webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}` (+ hide the
> webkit scrollbar); rail = `display:flex;width:max-content`.
> **Seamless infinite:** clone the full card set TWICE so the rail is
> `[clonesL][originals][clonesR]` (3 identical sets); `vp.scrollLeft = setW` to
> start on the real middle set; on `scroll` (throttled with ONE rAF) if
> `scrollLeft < setW*0.5` → `scrollLeft += setW`, else if `> setW*1.5` →
> `scrollLeft -= setW` (invisible jump — content one set over is identical). Strip
> `.reveal`/`.cut` (any hide-until-in-view class) off the clones and
> `aria-hidden`+`tabindex=-1` them. Arrows = `vp.scrollBy({left:±cardW,behavior:'smooth'})`.
> `setW` = sum of the n original card widths + gaps.
>
> **Lenis eats the horizontal wheel** (it hijacks `wheel` for smooth vertical), so
> trackpad/two-finger sideways scroll dies unless you put **`data-lenis-prevent`**
> on the scroll container — then Lenis leaves it to native scroll. (The old "go
> transform-based, Lenis cancels native scrollBy" advice was wrong for a *child*
> overflow container: Lenis only drives the root, so the child's native scroll +
> `scrollBy` are independent once `data-lenis-prevent` is set.)
>
> **Clickable cards → lightbox:** capture the lightbox `shots` from the ORIGINAL
> cards BEFORE cloning, then **delegate** the click on the rail
> (`e.target.closest('.car-card')`, read a `data-*` index) — delegation covers the
> clones automatically, and there's no pointer-capture retarget problem.
>
> **Two must-haves or it looks broken:** `img{-webkit-user-drag:none;
> pointer-events:none}` on card images (else the browser ghost-drags the photo when
> you swipe), and `touch-action:manipulation` on buttons/links (else a double-tap on
> an arrow ZOOMS the whole page on mobile).
>
> (Only hand-roll a transform stepper for a NON-scrollable, non-infinite case; if
> you do, don't `setPointerCapture` on pointerdown — capture only after a real drag
> `|dx|>~6`, or it retargets the desktop click off the card and the lightbox "works
> on mobile, dead on desktop.")

```html
<div class="carousel">
  <button class="car-nav" id="revPrev" aria-label="Previous">‹</button>
  <div class="car-track" id="revTrack">
    <article class="car-card"><!-- one slide --></article>
    <article class="car-card"><!-- … --></article>
  </div>
  <button class="car-nav" id="revNext" aria-label="Next">›</button>
</div>
<div class="car-dots" id="revDots" aria-hidden="true"></div>
```

```css
.car-track{display:flex;gap:24px;overflow-x:auto;scroll-snap-type:x mandatory;
  -webkit-overflow-scrolling:touch;scrollbar-width:none}
.car-track::-webkit-scrollbar{display:none}
.car-card{flex:0 0 min(420px,80%);scroll-snap-align:center}
.car-nav{width:48px;height:48px;border-radius:50%;cursor:pointer;display:grid;place-items:center}
.car-dots{display:flex;gap:8px;justify-content:center;margin-top:24px}
.car-dots button{width:8px;height:8px;border-radius:50%;border:0;background:var(--line);cursor:pointer;transition:all .3s}
.car-dots button.on{width:22px;border-radius:4px;background:var(--accent)}
@media (max-width:760px){.car-card{flex:0 0 100%}}
```

```js
(() => {
  const track = document.getElementById('revTrack');
  if (!track) return;
  const cards = [...track.querySelectorAll('.car-card')];
  const dotsWrap = document.getElementById('revDots');
  const prev = document.getElementById('revPrev'), next = document.getElementById('revNext');
  const step = () => (cards[0] ? cards[0].offsetWidth + 24 : track.clientWidth); // card + gap
  prev && prev.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
  next && next.addEventListener('click', () => track.scrollBy({ left:  step(), behavior: 'smooth' }));
  cards.forEach((c, i) => {
    const b = document.createElement('button');
    b.setAttribute('aria-label', 'Go to item ' + (i + 1));
    b.addEventListener('click', () => track.scrollTo({ left: i * step(), behavior: 'smooth' }));
    dotsWrap.appendChild(b);
  });
  const dots = [...dotsWrap.children];
  const sync = () => {
    const idx = Math.min(dots.length - 1, Math.round(track.scrollLeft / step()));
    dots.forEach((d, i) => d.classList.toggle('on', i === idx));
  };
  track.addEventListener('scroll', sync, { passive: true }); sync();
})();
```

---

## Video player
Muted ambient autoplay while on screen; first click unmutes and hands over the
browser's native controls (scrub/volume/fullscreen).

**Gate autoplay, then actually buffer it.** Autoplay pulls the whole file the
moment the page opens, which on a phone is usually the single slowest thing on
the site. Earn it: wide screen, not `saveData`, not 2g/3g, and only once the
player is on screen. But **`preload="metadata"` plus an immediate `play()` on
intersect fails** — the call lands against an empty buffer. On the autoplay path
set `preload='auto'` so the file is buffering on approach, use a low IO threshold
(~0.15, not 0.35 — a tall player may never reach 35%), and retry once on
`canplay` before giving up:

```js
var conn = navigator.connection || {};
var slow = conn.saveData === true || /^(slow-)?2g$|^3g$/.test(conn.effectiveType || '');
var mayAuto = !reduce && !slow && matchMedia('(min-width:900px)').matches;
if (!mayAuto) { vid.removeAttribute('autoplay'); vid.preload='none'; vid.controls=true; }
else {
  vid.removeAttribute('autoplay'); vid.preload='auto';
  var tryPlay=function(){
    var pr=vid.play();
    if(pr&&pr.catch) pr.catch(function(){
      vid.addEventListener('canplay',function once(){
        vid.removeEventListener('canplay',once);
        var again=vid.play(); if(again&&again.catch) again.catch(function(){});
      });
    });
  };
  new IntersectionObserver(function(es,obs){es.forEach(function(e){
    if(e.isIntersecting){obs.disconnect();tryPlay();}
  });},{threshold:0.15}).observe(vid);
}
```
**A custom overlay must not cover the native control strip.** A play button at `inset:0`
and a sound button at `bottom:14px` both sit on top of the scrubber, so the controls render
but cannot be operated. Adam reported it as "scrub is there but locked i cant move it".

```css
.playbtn{position:absolute;left:0;right:0;top:0;bottom:48px}  /* clears the control strip */
.sndbtn{position:absolute;right:14px;top:14px}                /* not bottom */
```

**Sync the sound button to the ELEMENT, not to its own state.** The native controls can mute
too, and a button tracking its own boolean silently drifts out of sync:

```js
vid.addEventListener('volumechange', function () {
  var m = vid.muted || vid.volume === 0;
  snd.setAttribute('aria-pressed', m ? 'false' : 'true');
  snd.querySelector('b').textContent = m ? 'Sound off' : 'Sound on';
});
```

**Autoplay cannot be verified in an automation tab** — it reports
`document.hidden: true` and Chrome refuses gesture-free playback there, so
`play()` always rejects no matter how correct the code is. Confirm
`vid.readyState === 4` (buffered) as evidence the plumbing works, and say plainly
that playback itself needs a real browser. Why this pattern: muted
autoplay is allowed everywhere, native controls beat any custom UI for
scrub/fullscreen, and there's exactly one play affordance (no double-button
desync). Keep it calm — no glow/pulse on the button.

```html
<div class="vframe">
  <video id="promo" poster="poster.jpg" muted loop playsinline preload="none">
    <source src="promo.mp4" type="video/mp4" />
  </video>
  <button class="play" id="playBtn" aria-label="Play with sound">▶ Play with sound</button>
</div>
```

```css
.vframe{position:relative;border-radius:16px;overflow:hidden}
.vframe video{width:100%;height:100%;object-fit:cover;display:block}
.play{position:absolute;inset:0;margin:auto;width:max-content;height:max-content;cursor:pointer}
.play.hide{opacity:0;pointer-events:none;transition:opacity .4s}
```

```js
(() => {
  const v = document.getElementById('promo'), playBtn = document.getElementById('playBtn');
  if (!v) return;
  let engaged = false;
  // ambient muted autoplay while in view (until the user engages)
  new IntersectionObserver(es => es.forEach(e => {
    if (engaged) return;
    if (e.isIntersecting) v.play().catch(() => {}); else v.pause();
  }), { threshold: .4 }).observe(v);
  // click -> play WITH SOUND and hand over native controls
  playBtn && playBtn.addEventListener('click', () => {
    engaged = true; v.muted = false; v.controls = true; v.currentTime = 0;
    v.play().catch(() => {}); playBtn.classList.add('hide');
  });
})();
```

---

## Animated counters
Counts up when scrolled into view. Decimal-aware (`data-count="4.3"` → one
decimal; `data-count="20"` → integer) and respects reduced motion. Needs GSAP +
ScrollTrigger (see `stack-and-wiring.md`).

```html
<span data-count="20" data-suffix="+">0</span>      <!-- 20+    -->
<span data-count="4.3" data-suffix="★">0</span>     <!-- 4.3★   -->
<span>$<span data-count="0">0</span></span>          <!-- $0     -->
```

```js
document.querySelectorAll('[data-count]').forEach(el => {
  const raw = el.dataset.count, end = +raw, suf = el.dataset.suffix || '';
  const dec = raw.includes('.') ? 1 : 0;                 // decimals only if the source has them
  if (RM) { el.textContent = end.toFixed(dec) + suf; return; }
  ST.create({ trigger: el, start: 'top 90%', once: true, onEnter: () => {
    const o = { v: 0 };
    gsap.to(o, { v: end, duration: 1.4, ease: 'power2.out',
      onUpdate: () => { el.textContent = o.v.toFixed(dec) + suf; } });
  }});
});
```

---

## Netlify Forms
A working contact/lead form with **zero backend** — Netlify captures the POST and
emails the lead to any address (no recipient verification). Three things make
detection work: `data-netlify="true"`, a hidden `form-name` matching the form's
`name`, and (for SPA-style AJAX) posting URL-encoded form data back to `/`. The
honeypot (`netlify-honeypot` + a hidden field) kills bots without a CAPTCHA.

> Deploy gotcha: new Netlify sites default `ignore_html_forms:true`, so the form
> won't be detected until you set it false + redeploy. See `deploy.md`.

```html
<form name="contact" method="POST" data-netlify="true"
      netlify-honeypot="company-website" id="lead-form">
  <!-- honeypot: humans never see it; bots fill it and get dropped -->
  <p hidden><label>Don't fill this out:
    <input name="company-website" tabindex="-1" autocomplete="off" /></label></p>
  <!-- required for AJAX detection: must equal the form's name -->
  <input type="hidden" name="form-name" value="contact" />
  <input type="hidden" name="subject" value="New lead from {{SITE}}" />

  <label>Name<input type="text" name="name" required autocomplete="name" /></label>
  <label>Phone<input type="tel" name="phone" required autocomplete="tel" /></label>
  <label>Email<input type="email" name="email" required autocomplete="email" /></label>
  <label>What do you need?
    <select name="service"><option>Option A</option><option>Option B</option></select>
  </label>
  <label>Message<textarea name="message" rows="3"></textarea></label>

  <button type="submit" class="ef-submit">Send</button>
  <p class="ef-status" id="ef-status" role="status" aria-live="polite" hidden></p>
</form>
```

```js
(() => {
  const form = document.getElementById('lead-form');
  if (!form) return;
  const statusEl = document.getElementById('ef-status');
  const btn = form.querySelector('.ef-submit');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const orig = btn.textContent;
    btn.disabled = true; btn.textContent = 'Sending…';
    statusEl.hidden = true; statusEl.className = 'ef-status';
    try {
      const res = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString()   // includes form-name
      });
      if (!res.ok) throw new Error('bad response');
      form.reset();
      statusEl.textContent = 'Thanks! We got it and will reach out shortly.';
      statusEl.classList.add('ok');
    } catch (err) {
      statusEl.textContent = 'Sorry, something went wrong — please try again.';
      statusEl.classList.add('err');
    } finally {
      statusEl.hidden = false; btn.disabled = false; btn.textContent = orig;
    }
  });
})();
```

```css
.ef-status{margin-top:12px}
.ef-status.ok{color:#1a7f4b}
.ef-status.err{color:#b3402a}
```

### Never collapse success + error (the silent-lost-lead bug)
The submit handler above branches on `res.ok` on purpose — keep it that way. The
tempting one-liner is the trap:

```js
fetch('/', opts).then(done).catch(done);   // WRONG — reports "sent" on a 4xx/5xx
```

`fetch` only rejects its promise on a *network* failure (offline, DNS, CORS). An
HTTP 400/403/404/500 still *resolves* — so a single `.then(done)` (or
`.then(done).catch(done)`) flashes "Thanks, we got it!" while the lead is gone.
For a lead form on a site you're pitching, that's the worst possible failure: it
looks like it works and you never know leads are being dropped. So:

- **Capture the button label first** (`const orig = btn.textContent`) — you need
  it to restore on failure; "Sending…" stuck forever is its own bad signal.
- **Throw on `!res.ok`** so a real HTTP error lands in `.catch`, not the success
  path: `.then(res => { if (!res.ok) throw new Error(res.status); showSuccess(); })`.
- **In `.catch`, recover visibly**: re-enable the button, restore `orig`, and
  show a real `.ef-status.err` message. A silent re-enable looks like a no-op.

### Netlify detection requires all four hooks
For a static form you submit via `fetch` (no full-page POST), Netlify only wires
up capture if the **static HTML** carries every one of these — they can't be
added by JS at runtime, since Netlify scans the deployed HTML at build time:

| Hook | Where | Why |
|---|---|---|
| `name="contact"` | `<form>` attr | names the form in Netlify's dashboard |
| `data-netlify="true"` | `<form>` attr | opts the form into capture |
| `netlify-honeypot="company-website"` | `<form>` attr | bot trap, no CAPTCHA |
| `<input type="hidden" name="form-name" value="contact">` | inside `<form>` | must equal `name`; matches the AJAX POST to the form |

Then the **JS POST body must include `form-name`** too — the
`new URLSearchParams(new FormData(form))` above already does, because the hidden
input is part of the form. If you build the body by hand, add `form-name`
explicitly or detection silently fails. See `deploy.md` for flipping
`ignore_html_forms` so Netlify actually scans the form on deploy.

---

## Nav links — growing-underline hover (both states) {#nav-links}

**Every build's nav links get an animated growing-underline on hover** (an
accent bar that wipes in left→right) plus a color shift. Non-negotiable, and it
must work in BOTH nav states: transparent-over-hero AND scrolled-solid.

```css
.nav-links a{position:relative;color:var(--ink-2);transition:color .22s}
.nav-links a::after{content:"";position:absolute;left:0;right:0;bottom:-6px;height:2px;
  background:var(--accent);transform:scaleX(0);transform-origin:left center;
  transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.nav-links a:hover::after,.nav-links a:focus-visible::after{transform:scaleX(1)}
.nav-links a:hover{color:var(--accent)}                 /* solid-state hover */

/* transparent-over-hero state */
.nav:not(.solid) .nav-links a{color:rgba(255,255,255,.9)}
.nav:not(.solid) .nav-links a:hover{color:#fff}         /* REQUIRED — see gotcha */

/* mobile dropdown: kill the underline so it doesn't clash with divider borders */
@media (max-width:720px){ .nav-links a::after{display:none} }

/* footer/secondary TEXT links get the same growing underline (scope to the link
   lists — NOT social-icon or brand-mark links, which keep their own hover) */
.footer ul a{position:relative;display:inline-block}
.footer ul a::after{content:"";position:absolute;left:0;right:0;bottom:-2px;height:1.5px;
  background:var(--accent);transform:scaleX(0);transform-origin:left center;
  transition:transform .28s cubic-bezier(.2,.7,.2,1)}
.footer ul a:hover::after,.footer ul a:focus-visible::after{transform:scaleX(1)}
```

**Consistency rule:** every TEXT link on the page uses this growing-underline hover
— nav links AND footer column links. Icon-only links (socials) and the brand mark
keep their own hover (bg tint / color). The fleet's older footers only color-shifted;
the standard since 2026-07-22 is the growing underline for both nav + footer text links.

### The specificity gotcha (hit on a lawn-care client, 2026-07-22)
If you only write `.nav-links a:hover{color:…}`, the hover works when the nav is
solid but **does nothing at the very top of the page**. Why: the transparent-state
rule `.nav:not(.solid) .nav-links a` has specificity (0,3,1) and *outranks*
`.nav-links a:hover` (0,2,1), so the base transparent color wins over hover. Fix:
give the transparent hover its OWN rule `.nav:not(.solid) .nav-links a:hover` (0,4,1).
The `::after` underline animates fine regardless because it's a separate property,
not competing on `color`.

### Legibility over a bright hero photo/video
Nav text, eyebrows, and pill badges sitting over a bright hero wash out. Add a
**dark `text-shadow`** for legibility (`0 1px 16px rgba(0,0,0,.6)`), and give pill
badges a **semi-dark background fill** (`background:rgba(14,26,18,.42)`) so the
text pops. That's a readability halo, not a glow — allowed. (a lawn-care client hero eyebrow.)

**An accent-COLORED eyebrow/label (blade-green, gold, etc.) over a bright hero
needs the pill treatment, not just a shadow.** A text-shadow alone is not enough
when the text itself is a mid-tone accent over a light photo — it stays low
contrast, worst on mobile. Wrap it in a semi-dark pill:
`display:inline-block;background:rgba(20,33,26,.55);border:1px solid rgba(<accent>,.4);
padding:8px 15px;border-radius:999px;backdrop-filter:blur(3px)`, and lean the hero
gradient overlay darker when the photo is bright. (a landscaping client "SERVING the metro
SINCE 1998" in blade-green over a beige house was invisible until it got a pill.)

## Mobile hamburger — animated 3-lines-to-X (all scroll states) {#hamburger}
The burger must **morph to an X on open** and stay **visible + tappable in every
state** — including at the very top where the nav is transparent. Two bugs to
avoid (both hit on a landscaping client):

1. **Light-on-light disappearance.** At the top the nav is transparent so the bars
   are the light hero color (`--bone`). When the menu opens over the light/bone
   dropdown, the bars vanish and never form an X. Fix: force the open bars dark
   regardless of nav-solid state — `.burger.open span{background:<ink>}`.
2. **Dropdown covers the burger.** The fixed open dropdown paints over the burger
   so you can't tap it to close. Fix: burger `z-index` above the dropdown
   (e.g. burger 130 / `.nav-links` dropdown 120).

The JS must toggle `.open` on the **burger element itself**, not only the menu.

```css
.burger{background:none;border:0;padding:10px;cursor:pointer;position:relative;z-index:130;width:44px;height:44px}
.burger span{display:block;width:24px;height:2px;background:var(--bone);border-radius:2px;margin:5px auto;
  transition:transform .32s var(--ease),opacity .2s var(--ease),background .25s var(--ease)}
.nav.solid .burger span{background:var(--ink)}      /* dark when scrolled */
.burger.open span{background:var(--ink)}            /* dark when open, ANY scroll pos */
.burger.open span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.burger.open span:nth-child(2){opacity:0}
.burger.open span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
/* in the mobile media query, give the dropdown a lower z-index than the burger */
@media(max-width:900px){ .nav-links{position:fixed;top:0;z-index:120; /* ...slide-down... */ } }
```
```js
burger.addEventListener("click", function(){
  var open = menu.classList.toggle("open");
  burger.classList.toggle("open", open);      // <-- the .open the X transform needs
  burger.setAttribute("aria-expanded", open ? "true" : "false");
});
// close on link tap: also clear the burger's .open
menu.querySelectorAll("a").forEach(function(a){ a.addEventListener("click", function(){
  menu.classList.remove("open"); burger.classList.remove("open"); burger.setAttribute("aria-expanded","false");
}); });
```

---


## Header: transparent + compact at top, solid + taller on scroll {#header-scroll}
*Adam's preferred header, ported from a client rebuild and requested by name since. Ships on every
build.* Three behaviours, and all three are the point:

1. **The page opens with the utility strip just out of frame**, so the nav sits at the very top.
2. **At the top the bar is transparent and compact**, sitting over the hero photo, with white
   text and enough padding that nothing reads cramped.
3. **On scroll it solidifies and grows**, with a border and a soft shadow.

```css
:root{--navh:78px; --navpad:66px}            /* solid height, transparent height */
@media (max-width:900px){:root{--navpad:60px}}

.nav{position:sticky;top:0;z-index:200;background:transparent;border-bottom:1px solid transparent;
  transition:background .28s var(--ease),border-color .28s var(--ease),box-shadow .28s var(--ease)}
.nav .wrap{min-height:var(--navh);transition:min-height .28s var(--ease)}

/* transparent state: smaller, white, slightly shrunken logo and buttons */
.nav:not(.solid) .wrap{min-height:var(--navpad);padding-top:10px}
.nav:not(.solid) .brand b,.nav:not(.solid) .menu > li > a{color:#fff}
.nav:not(.solid) .brand small{color:rgba(255,255,255,.74)}
.nav:not(.solid) .burger span{background:#fff}
.nav:not(.solid) .phpill{color:#fff;border-color:rgba(255,255,255,.62)}
.nav:not(.solid) .brand img{transform:scale(.88);transition:transform .28s var(--ease)}
.nav:not(.solid) .navcta .btn,.nav:not(.solid) .navcta .phpill{padding-top:11px;padding-bottom:11px}
.nav.solid{background:var(--paper);border-bottom-color:var(--line);box-shadow:0 2px 16px rgba(0,0,0,.07)}

/* the hero runs UP under the bar so the photo is edge to edge */
.hero,.phero{margin-top:calc(-1 * var(--navpad))}

/* the open mobile menu is always solid, at any scroll position */
.nav.open{background:var(--paper);border-bottom-color:var(--line)}
.nav.open .brand b,.nav.open .menu > li > a{color:var(--ink)}
.nav.open .burger span{background:var(--ink)}
```

```js
var nav = document.getElementById('nav');
var util = document.querySelector('.util');
var utilH = util ? Math.round(util.getBoundingClientRect().height) : 0;
/* open with the util strip just out of frame. Only on a genuine fresh load at the very
   top, so browser scroll restoration and #anchors still win. */
if (utilH && !location.hash) {
  var nudge = function () { setTimeout(function () { if (scrollY === 0) scrollTo(0, utilH); }, 60); };
  /* the script is deferred, so `load` may ALREADY have fired. Cover both paths. */
  if (document.readyState === 'complete') nudge();
  else addEventListener('load', nudge);
}
var trip = utilH + 70;                       /* transparent through the strip and a little hero */
var set = function () { nav.classList.toggle('solid', scrollY > trip); };
addEventListener('scroll', set, { passive: true });
set();
```

**The trap that costs a round every time.** `margin-top:-var(--navpad)` pulls the hero under
the bar, so the hero's own `padding-top` has to grow by the same amount or the first line of
content sits 6px under the nav. **Declare that padding AFTER the base `.hero .wrap` rule**, and
on generated pages put the `.phero` version in the LATER stylesheet (EXTRA_CSS), or the base
rule wins on equal specificity and you get a cramped header with no obvious cause:

```css
.hero .wrap{padding-top:clamp(56px,8vw,104px)}                       /* base */
.hero .wrap{padding-top:calc(var(--navpad) + clamp(46px,6.4vw,88px))} /* AFTER it, so it wins */
```

**Verify by measurement, both states and both breakpoints:**

```js
// on load
scrollY === utilH && !nav.classList.contains('solid')
firstContent.getBoundingClientRect().top - nav.getBoundingClientRect().bottom   // want 40px+
// after scrolling past the trip
nav.classList.contains('solid') && getComputedStyle(nav).backgroundColor !== 'rgba(0, 0, 0, 0)'
```

---

## Mobile submenu — the `0fr` accordion that will not collapse {#submenu}
Nav items with children need an accordion on mobile. The `grid-template-rows:
auto 0fr → auto 1fr` technique is right (never `max-height`), but it has a
prerequisite that is easy to miss and produces a spectacular failure.

**The bug (a client rebuild, 2026-07-29).** Every submenu rendered permanently open,
overlapping the link beneath it, burying the top three nav items under floating
panels and making the carets unreachable. The JS was fine. Devtools showed
`grid-template-rows: 61.7px 0px` — the track WAS collapsing — while the `.sub`
inside it measured 140px.

**The cause.** `.menu > li` carried `align-items:center` from the desktop nav row.
A grid item that is `center` or `start` aligned is sized to its own content
instead of being stretched to its track, so it overflows a 0px row and the
`overflow:hidden` on it never clips anything. Only `stretch` (the default, but
easily overridden) makes the item adopt the track height.

```css
@media (max-width:1080px){
  .menu > li{display:grid;grid-template-rows:auto 0fr;
    align-items:stretch;                 /* REQUIRED — resets the desktop row's center */
    transition:grid-template-rows .26s var(--ease)}
  .menu > li.sub-open{grid-template-rows:auto 1fr}
  .sub{position:static;min-height:0;overflow:hidden;   /* both REQUIRED */
    box-shadow:none;min-width:0;margin:0;opacity:1;visibility:visible;transform:none}
}
```

Three things must ALL be true or the accordion silently no-ops:
`align-items:stretch` on the parent, `min-height:0` on the child (grid items
default to `min-height:auto` and refuse to shrink below content), and
`overflow:hidden` on the child.

**The caret is its own button, and it must be `position:absolute`.** A separate
`<button>` sibling of the `<a>` is correct for tap targets (the name navigates,
the caret toggles), but as a static sibling it becomes a THIRD grid item and
lands in an implicit auto-sized row, which breaks the two-row layout. Absolute
positioning takes it out of flow so the grid stays `[link, sub]`.

```css
@media (max-width:1080px){
  .menu > li{position:relative}
  .menu > li:has(.sub) > a{padding-right:60px}   /* keep the label clear of the caret */
  .subtoggle{position:absolute;right:0;top:0;width:56px;height:56px;display:grid;
    place-items:center;background:none;border:0;color:var(--ink-2);
    -webkit-tap-highlight-color:rgba(125,194,66,.2)}
  .subtoggle::before{content:"";position:absolute;left:0;top:50%;transform:translateY(-50%);
    width:1px;height:24px;background:var(--line)}   /* hairline so it reads as its own control */
}
.menu > li.sub-open .subtoggle svg{transform:rotate(180deg)}
```
Also give `.subtoggle` an explicit colour for the **transparent** nav state, or
it renders black-on-dark and looks missing: `.nav:not(.solid) .subtoggle{color:#fff}`.

**Verify by measurement, not by eye** (in a real mobile viewport, see the
quality checklist's automation section):
```js
// closed must be 0, open must be >0, and no two links may share a top
const li=document.querySelector('.menu > li');
li.querySelector('.sub').getBoundingClientRect().height        // 0 when closed
const tops=[...document.querySelectorAll('.menu > li > a')].map(a=>a.getBoundingClientRect().top);
tops.some((t,i)=>i>0 && t<=tops[i-1])                          // must be false
document.elementFromPoint(cx,cy)===caret                       // caret is the top hit
```

---

## Preloader — logo, bar, slide-up reveal (static builds) {#preloader-static}
For the GSAP/Lenis variant see `stack-and-wiring.md#preloader`. On a plain static
build, this is the whole thing. Adam's stated preference: **logo plus a progress
bar, with a small spinner — not a big spinning wheel.**

**The logo must be inlined as a data URI.** A normal `<img src="/assets/logo.png">`
is a network request that has not finished when the panel paints, so the mark
visibly pops in a beat after the panel it sits on — which reads as broken.
Shrink it and inline it (a 128px webp is ~1.5KB, ~2KB as base64):
```bash
sips -Z 128 logo.jpg --out /tmp/pl.png && cwebp -q 82 /tmp/pl.png -o /tmp/pl.webp
python3 -c "import base64,pathlib;print('data:image/webp;base64,'+base64.b64encode(pathlib.Path('/tmp/pl.webp').read_bytes()).decode())"
```
Only inline the *preloader's* copy. Inlining full-size art on every page is how
you trade a fast first paint for a fat HTML document.

**Reveal by sliding the panel up, not by fading it.** A fade cross-dissolves into
the hero and reads as a flash; a slide uncovers the hero from underneath.
```css
.preloader{position:fixed;inset:0;background:var(--ink);z-index:200;display:grid;place-items:center;
  transform:translateY(0);transition:transform .62s cubic-bezier(.76,0,.24,1),visibility .62s}
.ready .preloader{transform:translateY(-100%);visibility:hidden}
.pl-in{display:grid;justify-items:center;gap:14px}
.pl-in img{width:64px;height:64px;border-radius:9px;display:block}
.pl-row{display:flex;align-items:center;gap:12px}
.pl-bar{width:150px;height:3px;background:rgba(255,255,255,.16);border-radius:2px;overflow:hidden}
.pl-bar i{display:block;height:100%;width:100%;background:var(--accent);transform-origin:left;
  transform:scaleX(0);animation:plfill 1.1s var(--ease) forwards}
.pl-spin{width:14px;height:14px;flex:none;border-radius:50%;
  border:2px solid rgba(255,255,255,.18);border-top-color:var(--accent);animation:plspin .7s linear infinite}
@keyframes plfill{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes plspin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.preloader{display:none}}
```
```js
var go=function(){
  document.documentElement.classList.add('ready');
  var pl=document.getElementById('preloader');
  if(pl) setTimeout(function(){pl.remove();},600);   /* stop it eating clicks */
};
/* the script is deferred, so `load` may ALREADY have fired — cover both paths */
if(document.readyState==='complete') requestAnimationFrame(go);
else addEventListener('load',function(){requestAnimationFrame(go);});
setTimeout(go,1200);                                  /* never leave the hero hidden */
```
The two loading spinners here (`plspin`, and a form-submit spinner) are the ONLY
sanctioned `animation:…infinite` on a build. They are progress indicators, not
decoration, and are exempt from the no-pulse rule.

**Homepage only, unless asked.** A preloader on every internal click is a tax on
navigation, not a flourish. Adam explicitly reverted a site-wide version.

---

## Hero stamp / seal that interrupts a divider {#seal}
A circular stamp straddling the hero's bottom divider is a cheap, high-value
signature element. Three things make or break it.

**1. Give it a knockout ring in the page background colour** so it reads as
embedded and the divider visually stops against it, rather than the tape running
underneath a floating disc:
```html
<circle cx="100" cy="100" r="100" fill="#FBFAF6"/>   <!-- knockout, page bg -->
<circle cx="100" cy="100" r="88" fill="none" stroke="#16181A" stroke-width="2"/>
```

**2. Anchor it to the DIVIDER, not to the hero's box.** If the divider is a curved
wave, the hero's `bottom` edge and the line you actually see are tens of pixels
apart at the stamp's horizontal position — anchoring to the box put the stamp
almost entirely below the visible tape. Lift it to the curve, then hang a third
of its OWN height below:
```css
.seal{position:absolute;right:clamp(14px,5vw,86px);bottom:clamp(30px,4.6vw,66px);
  transform:translateY(33%);z-index:5;width:clamp(96px,11vw,150px);pointer-events:none}
```
`translateY(%)` resolves against the element's own size, so the 2/3-on / 1/3-off
split holds at every width; a percentage `bottom` would resolve against the hero
and drift. Ensure `.hero` is NOT `overflow:hidden` or the overhang is clipped —
move the clip to the background layer (`.hero-bg{overflow:hidden}`) so photos
still crop.

**3. Curved text needs room on BOTH sides of its band.** Set the `textPath` radius
so the glyph band sits centred between the inner disc and the outer rule. Rotated
glyphs on the diagonals reach further out than the ones at top-centre, so text
that looks clear at 12 o'clock can still touch the ring at 2 o'clock.

**Measuring curved text: `getBBox()` LIES.** On a `<text>` containing a
`<textPath>` it returns the layout box, not where the glyphs land — it will
happily report an unchanged radius after you have moved the arc. Use
`getExtentOfChar(i)` per character (still axis-aligned boxes of rotated glyphs,
so it over-reports the outer radius), and for a real verdict clone the SVG into a
420px box and look at it:
```js
const c=document.querySelector('.seal svg').cloneNode(true);
const w=document.createElement('div');
w.style.cssText='position:fixed;left:40px;top:40px;width:420px;height:420px;z-index:9999;background:#FBFAF6';
c.style.cssText='width:100%;height:100%'; w.appendChild(c); document.body.appendChild(w);
```

---

## Hero scrim, readable text over a bright photo {#hero-scrim}

A bright hero photo (beige house, pale sky, snow, sand) eats hero copy. The wrong
fix is darkening the whole image: it kills the photo you chose the hero for. The
right fix is a **feathered radial-gradient anchored under the text block**, as its
own layer between the photo and the copy, so the text sits on contrast while the
rest of the image stays bright.

a landscaping client hero (2026-07-23) needed two passes before it read cleanly. Once the
scrim carries the contrast, **lighten the base full-bleed overlay** or the hero
goes muddy.

```html
<section class="hero">
  <img class="hero-photo" src="assets/hero.jpg" alt="">
  <div class="hero-scrim" aria-hidden="true"></div>
  <div class="hero-copy"> ... </div>
</section>
```

```css
.hero{position:relative;isolation:isolate}
.hero-photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}

/* base full-bleed overlay: keep it LIGHT once the scrim exists */
.hero::before{content:"";position:absolute;inset:0;background:rgba(20,33,26,.18);z-index:1}

/* the scrim: feathered, anchored under the text block (desktop = left/lower third) */
.hero-scrim{
  position:absolute;inset:0;z-index:2;pointer-events:none;
  background:radial-gradient(145% 108% at 30% 80%,
    rgba(20,33,26,.92) 0%,
    rgba(20,33,26,.30) 56%,
    transparent 80%);
}
.hero-copy{position:relative;z-index:3}

/* mobile: hero text is bottom-anchored, so a full-width bottom ramp beats a radial */
@media (max-width:760px){
  .hero-scrim{
    background:linear-gradient(to top,
      rgba(20,33,26,.94) 0%,
      rgba(20,33,26,.72) 34%,
      rgba(20,33,26,.20) 66%,
      transparent 100%);
  }
}
```

Tune the `at X% Y%` origin to wherever the copy actually sits. Swap `20,33,26` for
the brief's ink. This is a readability layer, not a glow: it must stay a neutral
dark, never an accent tint.

---

## Ghost button, inverts to solid white on hover {#btn-invert}

Adam's stated preference for an outline/ghost button over a dark hero: on hover it
**inverts to a solid white fill with dark text** rather than lightening or glowing.
Clean, high-contrast, and it reads as a real state change on a photo background.

```css
.btn-invert{
  background:transparent;
  color:var(--bone);
  border:1.5px solid rgba(255,255,255,.55);
  transition:background .18s ease,color .18s ease,border-color .18s ease;
}
.btn-invert:hover,
.btn-invert:focus-visible{
  background:#fff;
  color:var(--ink);
  border-color:#fff;
}
```

No colored box-shadow on hover: elevation shadows stay neutral dark, per the
no-glow rule.


---

## `<button class="btn">` — the UA `buttonface` trap {#btn-ua}
*Learned the hard way on a junk-removal client, 2026-07-28. Shipped a white-on-white button.*

A `.btn` class written for `<a>` almost never declares a `background`, because
anchors have none. The moment you reuse it on a real `<button>`, the browser's
own stylesheet fills it with `buttonface` (light grey), and light button text
becomes invisible.

**The symptom is a button that looks white-on-white and only in the one place
you used a real `<button>`.** Every anchor version looks fine, which is why it
survives review.

```css
/* whenever .btn can land on a <button>, not just an <a> */
button.btn{
  background:transparent;              /* kills UA buttonface */
  font-family:inherit;                 /* UA also overrides font */
  cursor:pointer;
  -webkit-appearance:none;appearance:none;
}
button.btn-primary{background:var(--accent);color:var(--ink)}
button.btn-ghost{color:var(--fg);border-color:var(--line)}
```

**Rule:** any shared button class must set `background`, `font-family` and
`appearance` explicitly, or be documented as anchor-only. Grep for
`createElement('button')` and `<button class="btn` before shipping.

---

## Fixed mobile action bar — iOS + Android safe area {#actionbar}
*Two separate bugs, two separate engines. Both present as the bar "hovering".*

A fixed call/text/quote bar is the highest-converting element on a local-service
phone page, and it has three failure modes that all look like a floating bar.

### 1. Content scrolls underneath it
`position:fixed` removes it from flow, so nothing reserves its height and the
last of the page hides behind it.

```css
:root{--actionbar-h:60px}
@media (max-width:800px){
  body{padding-bottom:calc(var(--actionbar-h) + var(--sa-max-bottom))}
}
```

### 2. iOS — the safe-area strip renders in the WRONG COLOUR
On iOS, `env(safe-area-inset-bottom)` is **0 while the browser toolbar is
visible** and jumps to ~34px the moment it hides on scroll. If the bar draws its
dividers from a grid `gap` over a container background, that inset suddenly
paints a 34px band **in the divider colour** under the buttons. It reads exactly
like the bar is floating above a gap.

```css
/* WRONG: container bg shows through the safe-area padding */
.actionbar{background:var(--line);gap:1px;padding-bottom:env(safe-area-inset-bottom)}

/* RIGHT: bar bg matches the buttons; dividers come from borders */
.actionbar{background:var(--surface);gap:0}
.actionbar a + a{border-left:1px solid var(--line)}
```

### 3. Chrome Android — never put a safe-area inset in `padding`
Chrome's [edge-to-edge guide](https://example-business.com/docs/css-ui/edge-to-edge)
states it directly: when Chrome detects `env(safe-area-inset-*)` inside a
`padding`, it drops off its fast path and **will not slide its bottom chin
away**. Use the *static* `safe-area-max-inset-bottom` for padding and let a
negative `bottom` track the live inset.

```css
:root{
  /* nested fallback: Chrome 135+ gets max-inset; iOS falls back to the live
     inset; everything else gets 0 */
  --sa-max-bottom:env(safe-area-max-inset-bottom, env(safe-area-inset-bottom, 0px));
}
.actionbar{
  padding-bottom:var(--sa-max-bottom);
  bottom:calc(env(safe-area-inset-bottom, 0px) - var(--sa-max-bottom));
}
```

### 4. Match the breakpoints of everything that shares the corner
A back-to-top FAB offset at `760px` while the bar appears at `800px` leaves a
40px-wide window where they overlap. **Any two fixed elements that avoid each
other must use the same breakpoint and the same height variable.**

```css
@media (max-width:800px){          /* SAME query as the bar */
  .to-top{bottom:calc(var(--actionbar-h) + var(--sa-max-bottom) + 12px)}
}
```

---

## Photo wall — uniform grid, never `column-count` {#photo-wall}
*a junk-removal client shipped a genuinely ugly section this way.*

CSS multi-column looks like free masonry until real client photos arrive with
wildly different aspect ratios (portrait phone shots next to landscape). Add a
`max-height` clamp to control the height and you get columns of wildly different
lengths with a dead zone below the short ones.

```css
/* WRONG */
.wall{column-count:6;max-height:430px;overflow:hidden}

/* RIGHT — every cell identical, bottom edge always straight */
.wall{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}
.wall figure{margin:0;aspect-ratio:4/5;border-radius:8px;overflow:hidden}
.wall figure picture{display:contents}     /* <picture> would break the fill */
.wall img{width:100%;height:100%;object-fit:cover;display:block}
/* cap the visible rows, reveal the rest via a link to the gallery page */
.wall:not(.all) figure:nth-child(n+13){display:none}
@media (max-width:1000px){.wall{grid-template-columns:repeat(4,1fr)}}
@media (max-width:600px){
  .wall{grid-template-columns:repeat(3,1fr)}
  .wall figcaption{opacity:0}   /* never burn captions over mobile thumbnails */
}
```

**Two rules that came out of client feedback:**
- **Never show captions permanently over mobile thumbnails.** At thumbnail size
  the text covers the photo and the user cannot tell the cell is tappable. Photo
  only; the caption belongs in the opened viewer.
- Past ~15 photos, stop toggling in place and **link to a real gallery page**.

---

## Gallery page — filters + spotlight viewer {#gallery}

When a client has 30+ real job photos, they are the strongest proof asset on the
site and deserve their own indexable page: grouped by trade, filterable, each
opening in a viewer. Self-contained, no library.

```css
.ggrid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.gcell{margin:0;position:relative;aspect-ratio:4/5;overflow:hidden;cursor:zoom-in}
.gcell img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.gcell:hover img,.gcell:focus-visible img{transform:scale(1.06)}
.glb{position:fixed;inset:0;z-index:300;background:rgba(0,0,0,.96);display:none;place-items:center}
.glb.on{display:grid}
@media (max-width:700px){.ggrid{grid-template-columns:repeat(2,1fr)}}
```

```js
(function(){
  var cells=[].slice.call(document.querySelectorAll('.gcell')), live=[], idx=0;
  var lb=document.createElement('div'); lb.className='glb';
  lb.setAttribute('role','dialog'); lb.setAttribute('aria-modal','true');
  lb.innerHTML='<button class="glb-x">&#10005;</button><button class="glb-p">&#8249;</button>'+
               '<button class="glb-n">&#8250;</button><figure><img alt="">'+
               '<figcaption></figcaption><span class="glb-i"></span></figure>';
  document.body.appendChild(lb);
  var im=lb.querySelector('img'), cap=lb.querySelector('figcaption'), cnt=lb.querySelector('.glb-i');
  function show(){
    var c=live[idx], s=c.querySelector('img');
    im.src=s.currentSrc||s.src; im.alt=s.alt;      // currentSrc keeps the <picture> choice
    cap.textContent=c.dataset.cap;
    cnt.textContent=(idx+1)+' / '+live.length;
  }
  function open(i){
    live=cells.filter(function(c){return c.closest('.gsection').hidden!==true}); // respect the filter
    idx=live.indexOf(cells[i]); if(idx<0){live=cells;idx=i;}
    show(); lb.classList.add('on'); document.body.style.overflow='hidden';
    lb.querySelector('.glb-x').focus();
  }
  function close(){lb.classList.remove('on');document.body.style.overflow='';}
  function step(d){idx=(idx+d+live.length)%live.length;show();}
  cells.forEach(function(c,i){
    c.addEventListener('click',function(){open(i)});
    c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open(i)}});
  });
  lb.querySelector('.glb-x').addEventListener('click',close);
  lb.querySelector('.glb-p').addEventListener('click',function(e){e.stopPropagation();step(-1)});
  lb.querySelector('.glb-n').addEventListener('click',function(e){e.stopPropagation();step(1)});
  lb.addEventListener('click',function(e){if(e.target===lb)close()});
  addEventListener('keydown',function(e){
    if(!lb.classList.contains('on'))return;
    if(e.key==='Escape')close();
    if(e.key==='ArrowLeft')step(-1);
    if(e.key==='ArrowRight')step(1);
  });
})();
```

**Details that matter:** `tabindex="0"` + Enter/Space on each cell (keyboard
parity), `currentSrc` so the viewer reuses the already-decoded responsive
source, filter-aware prev/next (the counter must read `1 / 7` when a filter is
on, not `1 / 30`), and `overflow:hidden` on body while open. On mobile the
viewer must clear the fixed action bar: `padding-bottom:calc(var(--actionbar-h) + var(--sa-max-bottom))`.

---

# Components learned on LATENT (2026-07-31)

## Lightbox: `max-height:100%` silently does nothing

A lightbox rendered a 2000x3000 frame at **1360x2040 inside a 661px viewport**.
The user reported it as "a super zoomed in random crop", which is exactly what it
looks like.

Cause: the image's parent was a grid item with an **indefinite height**, and a
percentage `max-height` against an indefinite height resolves to `none`. The rule
was in the stylesheet, looked correct, and had never applied.

```css
/* WRONG: max-height resolves to nothing, image overflows massively */
.lb-img     { display:grid; place-items:center; min-height:0 }
.lb-img img { max-width:100%; max-height:100%; object-fit:contain }

/* RIGHT: size the BOX definitely, let object-fit letterbox inside it */
.lb-img     { position:relative; min-height:0; overflow:hidden }
.lb-img img { position:absolute; inset:0; width:100%; height:100%;
              object-fit:contain; max-width:none; max-height:none }
```

Verify by opening several frames at different native ratios and asserting the
painted box fits inside its container. Do not eyeball one landscape image.

## Film strip: perforations are ROUNDED RECTANGLES

Every CSS film strip on the internet uses `radial-gradient(circle ...)` for the
sprocket holes, and that single wrong shape is most of why they read as clip art.
Real 35mm perfs (Kodak KS-1870) are rounded rects, ~2 x 2.8mm.

Cut them with a mask so the band behind shows through the holes rather than
painting a lighter colour to fake them:

```css
.strip{
  --perf:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://example-business.com/2000/svg' width='34' height='14'%3E%3Crect x='7' y='2' width='20' height='10' rx='2.4' fill='%23000'/%3E%3C/svg%3E");
  -webkit-mask-image:linear-gradient(#000 0 0),var(--perf),var(--perf);
  mask-image:linear-gradient(#000 0 0),var(--perf),var(--perf);
  mask-size:100% 100%,34px 14px,34px 14px;
  mask-position:0 0,0 4px,0 calc(100% - 4px);
  mask-repeat:no-repeat,repeat-x,repeat-x;
  mask-composite:exclude;
}
```

**The film base must contrast with its band.** A near-black base on an ink band
means the rebates, strip edges and perforations are all black on black and simply
cannot be seen. A white base reads as a contact print on a light table.

Frames butt together with a thin rebate (`border-inline`), never a grid `gap`.

## Polaroid: the giveaway is an even border

A real SX-70 print is 88 x 107mm around a 79 x 79mm **square** image: sides and
top ~4.5mm, chin ~24mm. Getting that one ratio right is most of the effect.

```css
.pol            { padding: 5.1% 5.1% 27.3%; transform: rotate(var(--rot,0deg)) }
.pol > .frame   { aspect-ratio: 1 }
```

Set `--rot` per instance so a cluster never lines up, and overlap them on a grid
row rather than laying them out as three equal columns.

**A polaroid can carry meaning, not just texture.** On a page about latent images,
three of them clearing from a flat grey-green at staggered delays as the band
enters the viewport *demonstrates* the paragraph instead of decorating it. A real
SX-70 clears from grey-green, not from black, and it clears unevenly.

## Multi-row marquee: run the middle row backwards

Three rows all drifting the same way reads as a conveyor belt: the eye locks onto
one photograph and rides it. Counter-run the middle row and the wall reads as
moving. Vary the row heights too, or three rows become one striped block, and
seed each row at a different scroll offset so the vertical seams never line up
into a grid.

One rAF loop drives every row. Three loops is three times the per-frame work for
nothing. See `scroll-performance.md` §1 for the `scrollLeft` rounding trap that
will otherwise freeze whichever row you gave the slowest speed.

## Embedded video: match the band and drop the chrome

To make a film read as part of the page rather than an embed sitting on it:
frame it at the video's **exact** aspect ratio, `autoplay muted loop playsinline`,
no `controls`, background matching the band, and a feathered mask on the edges.

```css
.film   { aspect-ratio: 16/9; background: var(--bg) }
.film-v { mask-image: radial-gradient(126% 132% at 50% 50%, #000 66%, transparent 100%) }
```

A frame ratio that does not match the film crops it before it reaches the screen:
a 16:9 film in a 2.4:1 frame under `object-fit:cover` loses 26%.

Sound is opt-in, and the toggle **syncs to the element** via `volumechange`, never
to its own state. Pause the video when it leaves the viewport.

<a id="section-bg"></a>
## A scroll-following section background: sticky, never fixed

A background image that follows the scroll behind a long list (a catalogue where
hovering a row swaps the image) has three candidate positions and two of them are
wrong.

- `absolute` pins it to the top of the section, so it scrolls out of view while
  you are still reading the list.
- `fixed` follows correctly **but is positioned against the VIEWPORT and is not
  clipped by its section at all.** This hides while the element only appears on
  hover. The moment it is given a resting image it covers every band below,
  including the contact section and the footer, and it also shows through above
  the section. Both reported as separate bugs; one cause.
- `sticky` follows the scroll exactly like fixed and is bounded by its parent.

```css
.band{position:relative; overflow:clip}
.band .bg{position:sticky; top:0; height:100vh; margin-bottom:-100vh; z-index:0}
```

The negative margin cancels the 100vh the element would occupy in flow.

**`overflow:clip`, not `overflow:hidden`.** `hidden` creates a scroll container,
which breaks the very stickiness it is meant to bound. `clip` does not, so sticky
still resolves against the viewport and keeps working. Verify BOTH behaviours:
that it stays pinned mid-list, and that it is gone below the section.

Related trap: `getBoundingClientRect()` does not account for clipping by an
ancestor, so a clipped element still reports its full box. Confirm containment
with a screenshot, not a measurement.

<a id="svg-specificity"></a>
## Styling SVG children: match the element or lose to the container rule

`.chart .layer rect { fill:none; stroke:currentColor }` is specificity (0,2,1).
A later `.chart .bar { fill:#333 }` is (0,2,0) and **loses**, so every bar renders
as a hollow outline while the CSS looks correct.

Add the element to tie the specificity so source order decides:
`.chart .layer rect.bar { ... }`. Same family as the duplicate-selector bug: when
a rule that plainly should apply does not, count specificity before rewriting it.
