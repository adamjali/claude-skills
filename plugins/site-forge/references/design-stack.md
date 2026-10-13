# The design stack

Three skills run on every UI build, in this order. This file is the single home for
the detail. Adam's hard rules live in `~/.claude/CLAUDE.md` under
"UI / Frontend Non-Negotiables"; this file never restates them, it only records how
the three skills interact with them.

Installed 2026-07-25. Impeccable v4.0.2 (plugin, user scope), taste-skill
`design-taste-frontend` v2 (experimental).

---

## 1. `frontend-design`: direction

Anthropic's official skill. Ships with Claude Code as a plugin. Handles the part no
detector can: what this specific page should look like and why. Palette as 4-6 named
hex values, display and body typefaces chosen deliberately, a layout concept, and one
signature element the page is remembered by.

Its key instruction, worth keeping in mind: brainstorm and critique the plan *before*
writing code, and if any part of it reads like the generic default you would produce
for any similar brief, revise that part and say what changed.

**Invoke first, always.** Nothing below replaces it.

---

## 2. `design-taste-frontend` (taste-skill): anti-slop discipline

One file, ~1,200 lines, no code. A prompt that loads and changes what you reach for.
Scope is landing pages, portfolios, and redesigns. It explicitly excludes dashboards,
data tables, multi-step forms, and code editors.

### The three dials

Everything downstream is gated on these numbers, so set them before writing markup.

```
DESIGN_VARIANCE   1 symmetry      10 artsy chaos     default 8
MOTION_INTENSITY  1 static        10 cinematic       default 6
VISUAL_DENSITY    1 airy          10 packed          default 4
```

**Use taste-skill's own defaults and its per-brief presets.** Adam's call, 2026-07-25:
where the skill is newer and better informed than the older hand-written rules, it wins.

Rules that reference the dials, so you know what you are actually setting:
- `DESIGN_VARIANCE > 4` bans centered heroes. Forces split, offset, or scroll-pinned.
- `VISUAL_DENSITY > 7` bans generic card containers.
- `MOTION_INTENSITY > 4` means the page must actually move. A static page claiming 7 is broken.
- `MOTION_INTENSITY > 3` makes `prefers-reduced-motion` non-negotiable.
- `MOTION_INTENSITY > 5` unlocks perpetual micro-interactions. **See the carve-out below.**

### The one carve-out

At motion 6 taste-skill permits pulse, shimmer, float, typewriter, and infinite loops.
**That unlock stays off.** Adam's no-pulse, no-glow rule is a standing aesthetic call, not
a craft standard. Everything else at motion 6 is in play: entry sequences, scroll reveals,
hover physics, spring easing, magnetic micro-physics.

Practically: before shipping, grep the CSS for `infinite` and for tinted `box-shadow`, and
neutralize what you find. That grep is already in Adam's rules and it is cheap.

### What it is genuinely good at

Named bans with real values, not vibes. Banned default background hexes for
premium-consumer briefs (`#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db`, `#faf7f1`,
`#e8dfcb`) and accents (`#b08947`, `#b6553a`, `#9a2436`). Fraunces and Instrument Serif
banned by name as display serifs. Section 9 runs 110 lines of specific layout tells:
`01 / 02 / 03` section numbers, `Scroll to explore` cues, locale and weather strips, fake
version footers, photo-credit captions as decoration, "Quietly trusted by", split headers,
zigzag past two consecutive rows, three equal feature cards, eyebrows on every section.

Its eyebrow rule is mechanical and worth obeying: **max 1 eyebrow per 3 sections**, hero
counts as one.

### What to ignore

Section 3 (stack) assumes React or Next.js with Server Components, Tailwind v4, and Motion.
Most demo work here is a static single file or a small multi-page static build. Skip that
layer entirely. Its icon rule survives the skip: Phosphor, one family, one strokeWidth.

Its 55-item pre-flight is self-administered. Treat it as a genuine checklist, but know that
Impeccable is the thing that will actually catch you.

---

## 3. Impeccable: verification

A plugin, not a prompt. 39 markdown files plus a JavaScript detector, 2.9MB.

### Structure

- **Router.** `SKILL.md` is small and loads one of 23 command playbooks on demand, rather
  than one huge always-on prompt. `critique.md` is 788 lines, `live.md` 730.
- **Craft floor** (`reference/craft-floor.md`, 40 lines). Loaded right before editing UI.
  Measurable checks: body and placeholder text 4.5:1, large text 3:1, body measure 65-75ch,
  display max 6rem, tracking floor -0.04em, shadows carry an offset and a soft blur.
  Plus the refuse list: same-size icon-heading-text cards as page structure, the hero-metric
  template, an eyebrow over every section, gradient text, colored side borders above 1px,
  monospace as a costume for "technical."
- **Detector.** Real JavaScript, roughly 60 rules. A sample: `ai-color-palette`, `nested-cards`,
  `gradient-text`, `pulsing-dot`, `dark-glow`, `radial-halo`, `side-tab`, `em-dash-overuse`,
  `cream-palette`, `oversized-h1`, `tiny-text`, `low-contrast`, `bounce-easing`, `marquee`,
  `wide-tracking`, `tight-leading`, `hero-eyebrow-chip`, `theater-slop-phrase`,
  `marketing-buzzword`, `broken-image`, `text-occlusion`, `flat-type-hierarchy`.
- **Hooks.** `PostToolUse` on Edit/Write/MultiEdit (5s) and `Stop` (30s). Already wired
  globally via the user-scoped plugin. It fires whether or not anyone remembered to ask.
- **Subagents.** `asset-producer`, `finish-reviewer`, `documenter`, `manual-edit-applier`.
- **Memory.** `PRODUCT.md` for durable product context, `DESIGN.md` for the design system,
  derived from the shipped artifact rather than from intentions.

### Commands that matter for demo builds

| Command | Use it for |
|---|---|
| `/impeccable critique` | UX review with heuristic scoring. Run before deploy. |
| `/impeccable audit` | Technical pass: a11y, perf, responsive. Run before deploy. |
| `/impeccable polish` | Final quality pass when the build is done but feels unfinished. |
| `/impeccable typeset` | Type hierarchy is flat or the scale steps are unclear. |
| `/impeccable layout` | Spacing, rhythm, and visual hierarchy are off. |
| `/impeccable bolder` / `quieter` | The build came out timid, or too loud. |
| `/impeccable live` | Pick elements in the browser and generate variants in place. |
| `/impeccable document` | Write `DESIGN.md` from an existing build. |

### Handling findings

**Fix them, or classify them as false positives with a stated reason.** Never add an inline
`impeccable-disable` comment to skip fixing something. Suppress only after Adam confirms a
finding is intentional, and prefer the narrowest config ignore over a file-wide one.

The detector is mechanical, which cuts both ways. It cannot tell decoration from function.
Worked example from the 2026-07-25 Halloran build: it correctly flagged `side-tab` on a 3px
accent stripe decorating a success callout, which was a real tell and got removed. The same
3px pattern on the vertical tablist next to it is a selected-state indicator doing real work,
and to the detector those look identical. Somebody has to make that call.

Its own hook output states the ceiling honestly: "No deterministic design-quality issues
found. That does not mean the design is good."

---

## Conflict table

**Read the profile column.** Since 2026-07-30 Adam's aesthetic rules are the DEFAULT
(profile `local-service`), not the universe — see `design-profiles.md`. The craft floor
(16px body, 4.5:1, 44px taps, reduced-motion, schema, sixteen social tags, headers) never
bends on any profile. Everything in this table is an aesthetic default unless marked.

| Topic | Adam's rule | Skill says | Resolution | Bendable? |
|---|---|---|---|---|
| Serif display | no rule | taste-skill: very discouraged as default, Fraunces + Instrument Serif banned by name | Follow taste-skill on `local-service` | **Yes** — `creative-portfolio` permits it, and a Didone at 190px is the genre. Named bans still hold. |
| Display type size | capped ~92px in practice | craft floor: display max 6rem (96px) | Hold on `local-service` | **Yes** — `creative-portfolio` goes to `clamp(64px,12vw,190px)`. Measured refs run 128-201px. |
| Hero scrim | 40-60% over a bright photo | no rule | Hold on `local-service` | **Yes** — down to 8-16% on `creative-portfolio`, but ONLY with an art-directed frame, and measure it. |
| Conversion furniture | sticky bar, stat band, reviews high | no rule | Required on `local-service` | **Yes** — `creative-portfolio` strips most of it. Selling hard reads as insecurity there. |
| Ambient video | not covered by the no-infinite-animation rule | no rule | A silent looping film loop is CONTENT, not decoration | The `infinite` ban targets decorative CSS pulse/glow only. |
| Body size / contrast / taps | 16px, 4.5:1, 44px | craft floor agrees | Enforce | **NO. Craft floor.** The reference portfolios ship 7px text and 1.63:1 headlines; those are defects to beat, not a style. |

| Topic | Adam's rule | Skill says | Resolution |
|---|---|---|---|
| Icons | was lucide | taste-skill discourages lucide, wants Phosphor | **Phosphor.** CLAUDE.md updated 2026-07-25. |
| Perpetual motion | no pulse, no glow, ever | taste-skill unlocks it at motion > 5 | **Adam wins.** Unlock stays off, rest of motion 6 allowed. |
| Tinted shadows | banned outright | craft floor bans zero-offset colored halos; taste-skill allows "subtle tinted shadows" | **Adam wins.** Neutral `rgba(0,0,0,…)` only. Exception: an accent focus ring is an a11y indicator, not decoration. |
| Em-dashes | banned everywhere | both ban them | Agree. Detector rule `em-dash-overuse` backs it up. |
| Custom cursor | banned | taste-skill 9.A bans it | Agree. |
| Stack | static single-file demos | taste-skill mandates React, Next, Tailwind v4 | **Adam wins.** Skip taste-skill section 3 on static builds. |
| Carousels | seamless-infinite, native scroll, cloned sets | neither has a rule | Adam's rule stands. See `components.md`. |
| Serif display | no rule | taste-skill: very discouraged as default, Fraunces and Instrument Serif banned by name | Follow taste-skill. |

---

## The honest read

Neither skill generates ideas. On the Halloran build the subject, thesis, signature device,
and palette all came from the brief and Adam's rules. What the skills did was block four
specific shortcuts and catch two real defects (an empty-src `<img>`, the accent side-stripe).

That is worth having. It is guardrails, not direction. `frontend-design` and the brief still
do the actual designing.

## Reference build: BadgerLayer (torn down 2026-07-30)

A fully documented, well-executed **editorial-technical** system worth studying when a brief calls
for restraint rather than imagery. Full spec (tokens, type scale, section rhythm, buttons,
responsive, rebuild CSS): `~/.claude/explanations/20260730_badgerlayer/DESIGN.md`.

**The system in one line:** warm paper, near-black ink, ONE red accent, a serif used for everything
including body copy, a mono used for every label, **radius 0 everywhere, zero animations**.

Transferable moves:
- **Red italic emphasis inside a black serif headline** — same family, same size, just italic +
  accent. Used on nearly every heading. This is exactly the emphasis rule our doctrine already
  mandates (italic of the SAME font, never a second family injected mid-headline).
- **`// EYEBROW` in accent mono, uppercase, +0.2em tracking** above every section. Cheap, consistent,
  signals "technical" without saying it.
- **Tracking contrast as the core device**: display gets NEGATIVE tracking (−0.02 to −0.04em) and
  tight leading (0.95-1.05); mono labels get POSITIVE tracking (+0.1 to +0.2em). That contrast is
  what makes the page feel designed.
- **Section rhythm**: three background levels (paper → paper-warm → ink) plus a full-accent closing
  CTA band. Uniform 96px padding-block, broken deliberately exactly twice (72px for a low-priority
  band, 120px for the CTA). Variation without inventing new spacing values.
- **Depth from background bands + 1px hairlines only.** One neutral shadow in the entire site.
- **Featured-card device**: accent tab badge notched on the top-right corner + the card inverted to
  ink while neighbours stay on paper. Cards share single hairline seams in a grid, not gaps.

⚠️ **Two of their choices are on our own ban list**: `#f5f1ea` (the AI-default premium-consumer
background) and **Fraunces** (a named banned display serif). Their execution dodges the cliché the
ban targets — the ban is aimed at beige + brass/clay/ochre, and they pair cream with a hard red and
a mono, which reads editorial rather than artisanal. **Take the structure, swap the two faces**, and
raise body copy: theirs runs 13-16px serif with 10-11px labels, which fails our readability floor.

## Counter-example: Liquid Agency (liquidagency.eu, torn down 2026-07-30)

**The cleanest available example of a competent, commercially successful site breaking our hard
rules.** Worth knowing precisely so we recognise the drift, not so we copy it.
Full spec: `~/.claude/explanations/20260730_liquidagency/DESIGN.md`.

System: mint-white ground (`rgb(248,251,250)`), one emerald accent `rgb(39,176,125)`, **Inter Tight**
set huge and italic, **JetBrains Mono** for labels, shadcn/ui HSL tokens, `--radius: .75rem` up to
full pills.

**What it breaks, verified live:**
- CTAs carry `box-shadow: rgba(39,176,125,0.6) 0 10px 30px -10px` on `border-radius:9999px` —
  an **accent-tinted glow**, which our rules ban by name.
- Custom **`orb-float` 18s infinite** and **`orb-spin` 60s infinite** decorative gradient orbs,
  plus Tailwind `ping 1s infinite` observed live.
- Centred hero occupying the whole first viewport.

It does handle `prefers-reduced-motion`. **It does not look bad — it looks like current SaaS.** That
is the point: the ban is a deliberate taste call, not a craft standard, and this is what the other
side of it looks like when executed well.

**Take from it instead:** inline example-business.com booking above the fold; numbered section eyebrows
(`[ 01 ] — Lavori selezionati`); mono eyebrow preceded by a small coloured status dot; and the
IT/EN pill toggle pattern (our version: EN/ES).
