# Profile: `creative-portfolio`

Photographers, designers, artists, studios, directors. The work IS the product and the
site is a gallery, not a shopfront.

Read `design-profiles.md` first for the craft-floor / aesthetic-default split. Evidence
below is measured, from the 2026-07-30 teardown of `marco-basini2.vercel.app` and
`valerio-di-domenica.liquidagency.eu` (full data: `~/money/latent/research/PORTFOLIO-TEARDOWN.md`).

---

## Who it serves

Someone deciding whether this person is **good**, and whether they want to be around
them for eight hours. They are not comparing three tabs on a phone at 11pm with a
leaking roof. They arrived from Instagram or a recommendation, they will scroll a long
way, and they are judging taste before they judge price.

That inverts almost everything the default profile optimises for.

---

## Bends

| Default | Becomes | Why |
|---|---|---|
| Display type capped ~92px | **`clamp(64px, 12vw, 190px)`** | Marco runs `14vw` = **201.6px**; Valerio `8.89vw` = **128px**. This is the single most transferable move and the biggest reason a portfolio reads as designed. |
| Serif display very discouraged | **Permitted, and often correct.** Not Fraunces, not Instrument Serif, not Cormorant Garamond (the reference already uses it). | taste-skill's own exception list names editorial and publication work. A Didone at 190px is the genre. Use one with a real `opsz` axis. |
| Hero scrim 40-60% | **8-16%, but ONLY if the frame is art-directed** | Marco's overlay is `rgba(0,0,0,.12)` and his h1 still measures **12.18:1 median**, because the photograph is baked black-and-white in the file (mean saturation 0.000). The image does the contrast work. **Un-art-directed stock still needs the heavy scrim** — this bend is conditional, and measuring it is not optional. |
| Tracking limits | **`-0.05 to -0.07em` on display, `+0.30 to +0.36em` on small caps labels** | The contrast between the two is what makes the page feel typeset rather than styled. |
| Leading floor | **0.84-0.96 on display type only** | Body copy leading is unchanged. |
| Conversion furniture required | **Strip most of it.** No sticky call bar, no stat band, no trust badges, no guarantee copy. | Marco's entire nav is four words and there is one contact point at the end. Selling hard reads as insecurity in this genre. |
| Alternating band tone | **Long runs of one tone are fine** | A gallery is not a marketing page. Sequence and pacing replace alternation. |
| Every band needs a visual | **Still true, but a band may be a single photograph at full bleed with no copy at all** | Silence is a compositional device here. |
| One accent colour | **Achromatic is often better** | The photographs supply all the colour. A system with no colour of its own is a real design position, not an absence. |
| Icon family everywhere | **Icons largely disappear** | Marco and Valerio use essentially none. An arrow and a close glyph is the whole set. |
| Restrained motion | **Motion becomes a differentiator** — see below | |

---

## Motion: the opportunity, not the constraint

**Both reference sites have literally zero motion.** Measured across 631 KB of bundles:
no GSAP, no Lenis, no Locomotive, no Motion, no `@keyframes`, no `requestAnimationFrame`,
no `mix-blend-mode`, no `clip-path`, no custom cursor, no scroll hijacking, no carousels.
`document.hidden` was `false`, so that is real and not the automation-tab artefact.

Their impact comes entirely from type scale and art direction.

**So motion is where this profile beats them, provided it stays in service of the work:**

- Ambient looping video behind a hero, muted, `playsinline`, desaturated in CSS to match
  the stills. This is NOT the banned "infinite animation" rule, which targets decorative
  CSS pulse and glow. A silent film loop is content.
- Hover-to-play micro clips on work cards.
- Scroll-driven re-crop of a still (scale and position, composited transforms only).
- Staggered reveals on a grid, once, on entry.
- Page transitions, if they are fast and never delay content.

**Still banned, unchanged:** decorative pulse, glow, shimmer, breathing gradients,
accent-tinted shadows, custom cursors.

---

## Holds — defaults this profile does NOT bend

Naming these keeps the boundary visible:

- **No glow, no pulse, no tinted shadows, no custom cursor.** Adam's standing call.
- **No em-dashes.**
- **Multipage with real IA.** Marco is a single 12,784px page with anchor nav; it is worse
  for SEO and worse on a phone. Valerio's multi-page structure is the better model.
- **Full schema, full social card, full security headers.** See below.
- **Copy in the markup.**
- **Neutral shadows only.**

---

## Craft floor: untouched, and this genre will tempt you

The reference sites fail the floor repeatedly. **These are defects to beat, not a house
style to copy:**

| What they do | Measured | The floor |
|---|---|---|
| Body type | Marco `--body-size: 12px`, **7px** on mobile; Valerio 9-10px labels | **16px** |
| Headline contrast | Valerio h1 worst **1.63:1**, eyebrow **1.75:1** | **4.5:1** body, 3:1 large |
| Tap targets | 19 sub-44px on Marco, 11 on Valerio at 500px | **44px** |
| Structured data | `grep -c 'application/ld+json'` returns **0** on both | Narrowest fitting type |
| Social card | Both ship 7 tags, `twitter:card=summary`, **no `og:image`** | The full sixteen |
| Reduced motion | Neither has a block | Required |
| Desktop nav | Marco's hamburger has **no `onClick`** and is the only desktop nav | Must work |

That last table is most of the answer to "but way better."

**For a photographer specifically, the missing `og:image` is the single highest-leverage
defect on either site.** Their entire product is pictures, their distribution is people
sharing links, and every share renders as a text-only card.

---

## Devices worth stealing

- **Mixed case inside one headline.** Marco alternates uppercase-roman and lowercase-italic
  spans in a single sentence: *"STORIE che meritano di RESTARE"*. Cheap, distinctive, safe.
  Needs a display face with a real italic.
- **A deliberately plain grotesque eyebrow against the Didone.** The plainness is the point.
- **A house colour grade.** Two valid approaches, and they are opposites: Marco bakes
  monochrome into the files; Valerio applies `filter: grayscale(.2) contrast(1.08)
  saturate(.72)` in CSS and grades the hero harder than the grid, which pushes the hero
  back and makes the work read as more colourful. Baking is faster; CSS is tunable.
- **The demo's `rel=canonical` pointing at the prospect's real production domain.** Valerio's
  canonical is `valeriodidomenica.it`, a different domain running WordPress. This stops a
  pitch build competing with or duplicating the incumbent's site in the index. **Directly
  applicable to Adam's operation** and we were not doing it.

---

## Do not copy

Single-page-with-anchors IA · 12px body and 7px mobile text · sub-2:1 headline contrast ·
hover-only dropdowns with no keyboard path · dead nav controls · preloading a 28.7 KB font
that is never rendered (Marco preloads Josefin Sans; `--font-sans` is `""`) · shipping zero
structured data · shipping no social card · a 2.87s FCP on a site with no animation.

---

# Learned building LATENT (2026-07-30/31)

## Picking a hero: optimise for AIR, not for drama

The obvious metric is wrong. "Most colourful plus most contrast" sounds right and
reliably selects a **tight, dark, high-ISO night frame full of bokeh**: gorgeous
alone, hostile to a headline, and it was rejected on sight twice.

What the reference sites in this genre actually use is a wide, calm establishing
frame with somewhere quiet for the type. Score for that instead
(`scripts/pick-hero.py`):

| signal | why |
|---|---|
| `calm` | share of the LOWER-LEFT quadrant with low local stddev, weighted highest: that is where the headline goes |
| `air` | same measure over the whole frame |
| `wide` | native ratio; a portrait in a 2.2:1 band is 60% thrown away |
| `light` | mean luminance; airy beats moody for an opening frame |
| `zone fit` | penalise the type region at BOTH ends: blown out needs a heavy scrim, black is dead where it shows |

On the build this came from, the winner scored 0.868 against 0.732 for second
place, with a local-variance of 8.8 where the rejected frames ran 47.

**If the site is monochrome, re-score.** The criteria change completely: tonal
RANGE becomes the constraint. A sunset wins on colour and measures 0.44 range,
which is flat and muddy in grey. Re-running the same field on grayscale criteria
picked a different frame entirely, and it was obviously right on sight.

## Solve the scrim, do not choose it

A scrim is a tax on the photograph. The habit is to pick a comfortable 45% and
stop thinking, which is why so many photo heroes look muddy. Composite the real
frame under candidate values, sample the pixels the type actually covers, take
the **lightest** value that clears 4.5:1 on small text and 3:1 on display
(`scripts/hero-scrim.py`). One frame solved at 14% where the build was shipping
40-60%.

**Scrim and pool composite multiplicatively:** `a_total = 1 - (1-a_scrim)(1-a_pool)`.
For a frame that is bright exactly where the headline sits, a flat scrim had to
run 46% to pass. A 14% global plus a 40% feathered pool reaches the same local
contrast and leaves 86% of the image nearly untouched.

**Solve the nav and the corner metadata separately.** The headline solver does not
cover them and they fail differently: on one bright frame the nav links measured
1.86:1 at 16% and still only 3.48:1 at 40%. Fix with a short heavy band over the
nav strip only (52%, ~110px tall, costs the photograph nothing). Corner exif that
cannot be solved should MOVE into the pooled column, not get its own scrim.

## Monochrome-first is the answer to mixed-source photography

Photographs from mixed sources have mixed white balance, mixed grade and mixed
era. No CSS filter makes them agree, so a colour wall reads as a collection of
other people's pictures. Three passes at a colour "system" were all rejected
before the real fix, which was to stop having one:

> **The site is a contact sheet. Everything is a proof, printed grey. Colour is
> the verdict that a frame got circled and printed.**

Around 10-15% colour. It is information, not decoration: each page's opening
frame plus the circled selects. Enforce with `scripts/colour-system.py`.

**One photograph, ONE treatment, site-wide.** A contextual rule (colour in panels,
grey in the sheet) is a real rule and still reads as random, because the same
photograph appears both ways on one screen. That is what the client keeps
reporting as "the colour is inconsistent".

**An audit that reads only CSS classes is blind.** The first version reported
"every photograph carries exactly one treatment" while every inner page opened on
a hard-baked `-mono-2000.webp` FILE. A treatment is the class AND the file.

**Only the page's OPENING frame is a keeper.** Marking every `.hero-media` also
catches the closing CTA panel at the foot of the page, which is not an opening
frame and should be grey like everything else.

## Cool grading is a channel scale, not a hue rotate

`hue-rotate()` rotates every hue and wrecks skin tones. A real white-balance shift
scales the channels the way a lower colour temperature does: R x0.915, G x0.995,
B x1.085, plus a small blue lift in the shadows. Do it at build time so it costs
nothing at runtime and cannot fight a grayscale filter chain. Verify by the R/B
mean ratio before and after.

## The line must not run behind the words

A scroll-drawn line weaving behind content reads as depth until it crosses a
paragraph, at which point it is just noise: a 3.4px near-black stroke under body
copy measurably competes with the text. Measured on one build, the weave crossed
**9 of 27 text blocks** and 7.4% of its length sat directly behind copy.

Routing it into the gutters fixes it and throws away the thing worth having.
Instead, mask it out over every text block, built once from measured rects:

- a full-page white rect (shows the line), plus a black rect per text block
- ~22px padding and `rx:14`
- one `feGaussianBlur` on the mask group, so the line fades rather than snapping
- the white rect oversized past the viewBox, or the blur eats the document edges

It reads as the line passing behind the words. Because it is a mask built at
layout time and not a filter on the animated stroke, it costs nothing per frame.

## Cormorant Garamond needs 600, and its small sizes need bumping

Tested at 500 in the first specimen, called "elegant but weedy", and rejected. At
**600** that objection disappears and it is warmer and more distinctive at display
size than the alternatives.

Its one real weakness is a small x-height, so every use under ~30px reads thin
unless it is bumped. On one build that meant the brand mark 25px -> 28px and the
pull-quote 21px -> 24px, both at 600. Skipping that step is exactly how a Garamond
ends up looking washed out, and it is why the face gets unfairly rejected.
