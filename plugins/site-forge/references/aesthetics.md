# Aesthetics — derive a fresh look per brief

This is **direction, not a skin to reuse.** The single example below is one
finished palette; the job is to invent a *different* one every time. If two sites
from this skill look related, something went wrong. `frontend-design` (invoke it
in Phase 2) is the authority on the actual aesthetic decision — this file is the
mechanical scaffold for expressing whatever it decides.

`frontend-design` is one of three skills that run on every build. The other two are
`design-taste-frontend` (anti-slop discipline, dials, named bans) and Impeccable
(the detector and the pre-deploy audit). **See `design-stack.md`** for how they
interact, which taste-skill setting is deliberately overridden, and the conflict table.

## The anti-slop rules (non-negotiable, because they're what separates "designed" from "AI default")
- **Never** Inter / Roboto / Arial / system-ui as the display face. Never the
  purple-gradient-on-white cliché. Never the same layout twice.
- Commit to ONE bold aesthetic and execute it precisely — editorial, brutalist,
  luxury/refined, organic, retro-future, industrial, playful, art-deco… Pick an
  extreme; intentionality beats intensity. Minimal can be as striking as
  maximalist — match code complexity to the vision (restraint vs. elaboration).
- Vary the fundamentals across briefs: light vs dark, serif-led vs grotesk-led,
  dense vs airy, symmetric vs asymmetric. Surprise with layout (overlap,
  diagonal flow, grid-breaks) and atmosphere (gradient meshes, grain, layered
  transparency, dramatic shadows) instead of defaulting to flat solid colors.

## Type
Pair a **distinctive display font** with a **clean body font** — both characterful,
neither generic. Load via Google Fonts (or self-host). Derive the pairing from the
brief's tone: a law firm ≠ a skate brand ≠ a bakery.

```html
<link href="https://example-business.com/css2?family=<Display>:wght@...&family=<Body>:wght@...&display=swap" rel="stylesheet" />
```

## Theme as CSS variables
Define the whole palette + type + motion once in `:root`, reference everywhere —
this is what makes a site feel cohesive and makes restyling trivial. Structure
(not the values) is the reusable part:

```css
:root{
  /* ink / surface / lines — derive 3-5 neutrals from the brand */
  --ink:#0f1e28; --ink-soft:#41606e; --surface:#fbf6ee; --line:#e2d4bf;
  /* one dominant accent + a deep + a soft variant (dominant color > timid palette) */
  --accent:#c75d36; --accent-deep:#a8492a; --accent-soft:#e8a578;
  /* type + motion */
  --serif:"<Display>",Georgia,serif; --sans:"<Body>",system-ui,sans-serif;
  --ease:cubic-bezier(.2,.8,.2,1);
  --shadow:0 30px 70px -34px rgba(15,30,40,.6);
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--sans);color:var(--ink);background:var(--surface);-webkit-font-smoothing:antialiased;overflow-x:hidden}
h1,h2,h3{font-family:var(--serif);font-weight:600;line-height:1.02;letter-spacing:-.025em}
img{display:block;max-width:100%;height:auto}
.wrap{max-width:1280px;margin:0 auto;padding:0 32px}     /* tighten on mobile */
```
> The values above are ONE example (a warm Gulf-coast palette w/ Fraunces +
> Hanken Grotesk). For a new brief, replace every value — pick fresh neutrals, a
> fresh accent, a fresh type pairing, a fresh mood. Keep the *structure*.

## Motion
One well-orchestrated page-load (staggered reveals) lands harder than scattered
micro-interactions. Add scroll-triggered reveals and a few surprising hover
states. Always gate motion behind `prefers-reduced-motion` (see
`stack-and-wiring.md`). Hover/transition discipline: transition specific
properties, not `all`; keep `will-change` only on elements that actually animate.

## Mobile
Generous, consistent gutters; lighter vertical rhythm than desktop; watch for
sections whose inner padding overrides `.wrap` (a real bug — a CTA `inner` with
`padding:Npx 0` had zero horizontal padding on phones, jamming text to the edge).
See `quality-checklist.md`.
