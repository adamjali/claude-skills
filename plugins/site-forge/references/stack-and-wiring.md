# Stack & Wiring — GSAP + Lenis single scroll authority

The proven, dependency-light motion stack for a single-file site: GSAP 3.15 +
ScrollTrigger for animation, Lenis 1.3 for smooth scroll, wired so there is
**one scroll authority** (Lenis drives, ScrollTrigger reads from it). Everything
here is CDN + SRI — nothing to install.

## Contents
- [CDN tags (head + before `</body>`)](#cdn-tags)
- [The single-scroll-authority wiring](#wiring)
- [Reduced-motion (the RM flag)](#reduced-motion)
- [Preloader → hero reveal](#preloader)
- [Header-solid, reveals, parallax, marquee, counters](#common)
- [Scroll-progress bar + circular back-to-top](#progress)

<a id="cdn-tags"></a>
## CDN tags

In `<head>` (Lenis CSS + optional Three.js import map if you use 3D):
```html
<link rel="stylesheet" href="https://example-business.com/npm/lenis@1.3.23/dist/lenis.css" integrity="sha384-gvLq/iOMNnPchdosgVym5huSVkKipHCQaqSw2Eg0V52Mzmlf169ZOsXcNc2cNu8x" crossorigin="anonymous" />
```
Just before `</body>` (order matters — gsap, then ScrollTrigger, then Lenis):
```html
<script src="https://example-business.com/npm/gsap@3.15.0/dist/gsap.min.js" integrity="sha384-XmJ9SoHtVOHoQUcKvFAzVXwdkKo1Ie3bhmSoIAkcdsHGaIrVJIkmozyq0FJeb/Ly" crossorigin="anonymous"></script>
<script src="https://example-business.com/npm/gsap@3.15.0/dist/ScrollTrigger.min.js" integrity="sha384-wl5TeDVvOWt30Pbf8aSo2ZrzsOjddu3avOBvHe+p+OhJt9gP6w9YXmDkN5DK2/dF" crossorigin="anonymous"></script>
<script src="https://example-business.com/lenis@1.3.23/dist/lenis.min.js" integrity="sha384-iiCtod6ZId6zT42Bar9EFXNKZh8X4VliWYWFOuY3/t1AxCvLejXExXcbluoc57CJ" crossorigin="anonymous"></script>
```
SRI hashes pin exact versions — if you bump a version, regenerate the hash
(`curl -s <url> | openssl dgst -sha384 -binary | openssl base64 -A`) or the
browser will refuse to load it. Required CSS so Lenis can own scroll height:
```css
html.lenis,html.lenis body{height:auto}
.lenis.lenis-smooth{scroll-behavior:auto!important}
```

<a id="wiring"></a>
## The single-scroll-authority wiring

The whole point: Lenis runs the scroll, and ScrollTrigger updates *from* Lenis's
ticker — never two systems fighting over the scroll position (the usual cause of
jank and desync). `lagSmoothing(0)` stops GSAP from "catching up" after a frame
drop, which would otherwise jump the scrub.
```js
const RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const gsap = window.gsap;
gsap.registerPlugin(window.ScrollTrigger);
const ST = window.ScrollTrigger;

let lenis;
if (!RM) {
  lenis = new window.Lenis({ duration: 1.1, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)) });
  lenis.on('scroll', ST.update);                 // ScrollTrigger reads Lenis
  gsap.ticker.add(t => lenis.raf(t * 1000));      // Lenis runs on GSAP's ticker
  gsap.ticker.lagSmoothing(0);                    // no post-stall catch-up jump
}

// Anchor links route through Lenis so in-page nav is smooth too
document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
  const id = a.getAttribute('href'); if (id.length < 2) return;
  const el = document.querySelector(id); if (!el) return;
  e.preventDefault();
  lenis ? lenis.scrollTo(el, { offset: -10 }) : el.scrollIntoView({ behavior: 'smooth' });
}));
```

<a id="reduced-motion"></a>
## Reduced motion

`RM` is the master switch. When the user prefers reduced motion, **don't start
Lenis at all** (native scroll), and set every animated element to its final
state instead of animating. Every effect below guards on `RM`. This isn't just
politeness — it's the accessible default and it doubles as your "static
fallback" path.

<a id="preloader"></a>
## Preloader → hero reveal

A short branded preloader that wipes up and hands off to a staggered hero
reveal. `ST.refresh()` after the preloader is removed so ScrollTrigger
remeasures the now-final layout. Replace the selectors/timeline beats to fit the
brief; the *pattern* (one orchestrated load with staggered delays) is what
creates the "designed" feel.
```js
const pre = document.getElementById('pre');
function startHero() {
  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
  tl.to('.h-eyebrow span', { y: 0, duration: .7 })
    .to('.hero h1 .ln>span', { y: 0, duration: 1, stagger: .12 }, '-=.35')
    .to('.hero .sub', { opacity: 1, y: 0, duration: .8 }, '-=.6')
    .to('.hero .cta', { opacity: 1, y: 0, duration: .7 }, '-=.55')
    .to('.scrollcue', { opacity: 1, duration: .6 }, '-=.3');
  gsap.fromTo('.hero .bg img', { scale: 1.18 }, { scale: 1, duration: 2.4, ease: 'power2.out' });
}
function startHeroStatic(){ gsap.set(['.h-eyebrow span','.hero h1 .ln>span'],{y:0}); gsap.set(['.hero .sub','.hero .cta','.scrollcue'],{opacity:1,y:0}); }
function init() {
  if (RM) { pre.style.display = 'none'; startHeroStatic(); return; }
  const tl = gsap.timeline();
  tl.to('#pre .pm', { opacity: 1, scale: 1, duration: .45, ease: 'back.out(1.7)' })
    .to('#pre .pn', { opacity: 1, duration: .35 }, '-=.18')
    .to('#pre .bar i', { width: '100%', duration: .55, ease: 'power1.inOut' }, '-=.22')
    .to('#pre', { yPercent: -100, duration: .6, ease: 'power3.inOut' }, '+=.02')
    .add(() => { pre.style.display = 'none'; ST.refresh(); })
    .add(startHero, '-=.25');
}
window.addEventListener('load', init);
```

<a id="common"></a>
## Header-solid, reveals, parallax, marquee, counters

Bread-and-butter ScrollTrigger patterns. `ST.batch('.reveal', …)` is the
efficient way to reveal many elements (one observer, batched) rather than a
trigger per element.
```js
// Header turns solid after a little scroll
ST.create({ start: 60, end: 99999, onUpdate: self => document.getElementById('hd').classList.toggle('solid', self.scroll() > 60) });

// Reveal-on-enter (give elements class="reveal" + a starting opacity:0;translateY in CSS)
if (RM) gsap.set('.reveal', { opacity: 1, y: 0 });
else ST.batch('.reveal', { start: 'top 86%', onEnter: els => gsap.to(els, { opacity: 1, y: 0, duration: .9, stagger: .08, ease: 'power3.out', overwrite: true }) });

// Parallax (subtle — keep yPercent small)
if (!RM) gsap.to('.parallax img', { yPercent: 14, ease: 'none', scrollTrigger: { trigger: '.parallax', start: 'top bottom', end: 'bottom top', scrub: true } });

// Seamless marquee (duplicate the track once, then loop -50%)
if (!RM) { const t = document.querySelector('#marq .track'); t.innerHTML += t.innerHTML; gsap.to(t, { xPercent: -50, repeat: -1, duration: 22, ease: 'none' }); }

// Count-up (supports one decimal via data-count="4.3" data-suffix="★")
document.querySelectorAll('[data-count]').forEach(el => {
  const raw = el.dataset.count, end = +raw, suf = el.dataset.suffix || '', dec = raw.includes('.') ? 1 : 0;
  if (RM) { el.textContent = end.toFixed(dec) + suf; return; }
  ST.create({ trigger: el, start: 'top 90%', once: true, onEnter: () => {
    const o = { v: 0 }; gsap.to(o, { v: end, duration: 1.4, ease: 'power2.out', onUpdate: () => { el.textContent = o.v.toFixed(dec) + suf; } });
  }});
});
```

<a id="progress"></a>
## Scroll-progress bar + circular back-to-top

The full component — markup, CSS, and the JS (appears only after ~500px, ring
fills with scroll, scroll-to-top through `window.__lenis`) — lives in
`references/scroll-effects.md` → "Scroll UI — progress bar + back-to-top ring".
Read it there; don't duplicate it here. It's cheap and high-signal — a good
default on any page with real length.
