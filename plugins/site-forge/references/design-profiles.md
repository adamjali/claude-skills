# Design profiles

*Created 2026-07-30, after Adam looked at the LATENT photography build next to two
Italian photographer sites and said the rules were holding it back: "it works for
the services stuff but if its a diff animal then it should be way diff."*

**Read this at Phase 2, before `frontend-design`, and name the profile out loud.**

---

## The problem this solves

Every rule in `~/.claude/CLAUDE.md` was learned building **local trades and services
demo sites**: roofers, junk haulers, lawn care, a barbershop, a small-engine shop.
Twenty-six of them. The rules are good and they were expensive to learn.

They are also, silently, a **genre**. A wedding photographer is not a roofer, and a
rule that reads as craft on a roofer's site reads as timidity on a photographer's.
Applying one set of aesthetic instincts to both produces a competent trades site
wearing a portfolio's photographs, which is what the first LATENT build was.

So the rules split in two, and only one half is negotiable.

---

## The split

### Craft floor — NEVER bendable, on any profile

These are engineering facts, not taste. No brief, no reference site, and no client
preference overrides them. If a profile appears to require breaking one, the profile
is wrong.

| Floor | Value |
|---|---|
| Body text size | **16px minimum** on anything a phone touches. Below it iOS Safari zooms on focus and never zooms back. |
| Body text contrast | **4.5:1**. Large text (24px+, or 18.66px+ bold) may sit at 3:1. |
| Tap targets | **44x44px** for standalone controls. Inline links inside a sentence are exempt (WCAG 2.5.8). |
| Motion | `prefers-reduced-motion` honoured, always. |
| Keyboard | Every interactive element reachable and operable. Visible focus. No hover-only paths. |
| Structured data | JSON-LD, narrowest fitting schema.org type, never bare `LocalBusiness`. |
| Social card | The full sixteen og/twitter tags, every page, absolute URLs, self-referential `og:url`. |
| Security | The seven headers. CSP generated per site. |
| Publishing | Ship an explicit `dist/`. Never the project root. |
| Truth | No invented facts presented as real. Unverified claims disclosed. |
| Crawlability | Copy lives in the markup. JS may filter or reveal it, never be its only source. |
| Correctness | One declaration per selector. No dead CSS. Verified at a real mobile viewport. |

**These are what "way better" actually means.** The two reference sites torn down on
2026-07-30 fail nine of them, and beating them there costs nothing.

### Aesthetic defaults — bendable per profile, with a stated reason

Everything else. These are Adam's taste calls, correct for the default profile and
open to challenge elsewhere:

no glow / no pulse / no infinite animation · icon family and stroke weight · type
scale ceiling · tracking and leading limits · scrim opacity · section composition
(no text-only bands, alternating tone, dividers between bands) · carousel behaviour ·
nav shape and depth · conversion furniture (sticky bars, stat bands, review blocks) ·
em-dashes · colour restraint · photo mask rotation · band padding rhythm.

**A profile bends a default by naming it and saying why.** Silent divergence is drift,
not design.

---

## How to use this

1. At Phase 2, classify the brief and **say which profile you are on**, in one line:
   *"Profile: creative-portfolio. Bending display-size ceiling, serif ban, scrim floor
   and conversion furniture. Craft floor unchanged."*
2. Load `profile-<name>.md` and apply its bends on top of the defaults.
3. If the brief needs a bend the profile does not list, either add it to the profile
   (if it generalises) or note it as a one-off in the build.
4. If no profile fits, use the default and say so. Do not invent a profile silently.

---

## The profiles

| Profile | For | File |
|---|---|---|
| **`local-service`** | Trades, home services, local businesses with a phone number and a service area. **The default.** | this file, below |
| **`creative-portfolio`** | Photographers, designers, artists, studios. Work is the product; the site is a gallery. | `profile-creative-portfolio.md` |
| **`personal-agency`** | Adam's own brand and agency site. | `profile-personal-agency.md` |

More get added as they earn it. A profile is worth creating when a *second* build in
the same genre hits the same fights with the defaults.

---

## Profile: `local-service` (the default)

This is what every rule in CLAUDE.md already assumes. Written down so it is a choice
rather than the universe.

**Who it serves.** Someone with a problem right now: a leaking roof, a dead mower, a
garage full of junk. They arrived from Google or a neighbour's recommendation, they
are on a phone, and they are comparing three tabs.

**What that demands.**
- **The hero states what you do, where, and how to reach you.** A mood is a wasted screen.
- **Conversion furniture is load-bearing**: sticky call bar, click-to-call in the header,
  reviews high on the page, a form that works, service-area proof.
- **Readability over texture.** 16px floor is a floor, not a target. Bolder and darker
  when in doubt.
- **Restrained motion.** Scroll reveals and hover states, nothing that delays content.
- **Depth signals scope**: dropdowns, hubs and children make a one-person operation
  read as established.
- **Every band carries a visual.** Text-only sections are why builds felt empty.
- **Local SEO is the point**: `LocalBusiness` subtype, service-area pages, real reviews
  linked to source.

**Aesthetic defaults, all in force.** No glow, no pulse, no infinite animation. Phosphor
icons, one family, one stroke weight. Display type capped around 92px. Neutral shadows
only. Alternating band tone. Dividers between sections. No em-dashes.

**Where this profile is genuinely right and portfolios are wrong:** a trades customer
does not want atmosphere. They want the phone number. Every ounce of restraint the
portfolio profile spends on mood, this one spends on clarity.

---

## Adding a profile

Create `profile-<name>.md` with exactly these sections:

1. **Who it serves** and what they arrived to do.
2. **Bends** — a table: which default, what it becomes, and *why the genre requires it*.
3. **Holds** — the defaults this profile explicitly does NOT bend, so the boundary is
   visible rather than assumed.
4. **Craft floor** — restate that it is untouched, and call out any floor the genre will
   tempt you to break (portfolios tempt you to break the type-size and contrast floors).
5. **Reference evidence** — measured, from real sites, with values. Not vibes.

Then add a row to the table above.


---

## Learned 2026-07-31: what the craft floor did NOT cover

Three defects got through a build that passed every floor item, because the floor
is about the artefact and these are about the **method**:

1. **A dead feature passes every check.** Complete markup, complete CSS, no
   handler. Add "click it and assert a state change" to the floor, not just
   "it renders".
2. **A checker that reads one representation is blind to the other.** A colour
   audit reading CSS classes reported perfect consistency while every inner page
   opened on a hard-baked `-mono` FILE. When something can be expressed two ways,
   check both.
3. **A per-item check cannot see a set.** Crop checking each image against its own
   frame passed clean on a visibly ragged row of three cards. Rows and grids need
   their own consistency assertion.

**Craft floor addition, non-bendable on any profile:** every interactive control
is exercised in a real browser before a build is called done.
