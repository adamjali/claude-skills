# Reference sites — the swipe file

Real sites worth stealing from, with an honest read on **what specifically** is good
and what to leave behind. Nothing here is endorsed wholesale. Each entry separates
**copy/structure/conversion** (usually the transferable part) from **craft/code**
(usually not, since most local-business sites are builder output).

Add an entry when a site earns it. Keep the "don't copy" half — it's the half that
stops a reference from quietly lowering the bar.

---

## Index
- [Terra Lawn Care Specialists](#terra-lawn-care-specialists--terra-lawn-carecom) — lawn/home services. Best **conversion-copy** reference in the category; builder-built, so ignore the code.

---

## Terra Lawn Care Specialists — example-business.com
*Added 2026-07-28. Southeastern PA lawn care, fertilization, tree/shrub, pest control. Est. 2003.*

**Verdict: steal the COPY and the SECTION ORDER. Do not steal the build.**
This is WordPress + Elementor 4.1.3 + WP Rocket, ~209KB of HTML on the homepage
alone with 1,368 Elementor references. It is not a craft reference. It is the best
**conversion-copy** reference in the lawn/home-services category we've found, which
matters more for the fleet than another design idea, because the fleet's design is
already stronger than this and its copy usually isn't.

### What makes it work (steal all of this)

**1. Differentiation copy that names the competitor's failure.** The "Terra Difference"
section is four claims, each written as an explicit contrast rather than a feature:
- *"Most companies operate under one generic license. At Terra, every technician is individually certified and trained, so you never get a rookie on your lawn."*
- *"We don't guess. Our staff soil scientist designs your custom program based on actual diagnostics, ensuring your lawn gets a prescription, not a sales pitch."*
- *"Solo operators cut corners to save time. Our two-man teams ensure better coverage, attention to detail, and a second set of eyes on your property."*
- *"We don't believe in locking you in. We earn your business with every visit. You stay with us because the lawn looks great, not because you signed a paper."*

Every one is a real, checkable operational fact turned into a reason to pick them.
This is the single most transferable thing on the page. Our fleet's credibility
sections tend to state facts ("licensed", "since 2003") without saying *why that
beats the other guy*. Interview the owner for four of these and the section writes
itself.

**2. Named local conditions, not generic geography.** *"We understand the unique
challenges of Pennsylvania soil — from heavy, compacted clay to nutrient
deficiencies."* Not "proudly serving PA." It names the actual dirt. The my state
equivalents are St. Augustine vs Bahia, chinch bugs, sandy soil that won't hold
nutrients, summer fungus from afternoon storms. This is also strong AEO/GEO fuel:
it's exactly the specific language an answer engine can quote.

**3. Service copy that attacks a specific failure mode.** *"Generic bags from the
hardware store won't cut it."* / *"We go where others cut corners: double-pass
aeration, twice the standard seed rate, and manually hand-seeds the tricky bare
spots that machines always miss."* Concrete, countable, falsifiable. Contrast with
the usual "quality service you can trust."

**4. One CTA, repeated after every single section.** "Book Your Free Site Visit"
appears after the intro, the services grid, the pest section, the difference
section, the bed-management section, and the process. Plus a phone number in the
sticky nav and a phone ghost button in the hero. The next step is never more than
one scroll away and it is always the *same* step. Cheap to copy, and our builds
usually put one CTA in the hero and one in the footer.

**5. Real, attributed, verifiable reviews.** Six Google reviews with the reviewer's
actual name, each linking to the live Google review page
(`example-business.com/local/reviews?placeid=...`). No fabricated star average, no
made-up count. This is our truth discipline done well by someone else, and the
linked-to-source pattern is worth adopting: it makes the reviews checkable rather
than merely claimed.

**6. Numbered process that is actually a sequence.** 01 Initial Consultation →
02 Custom Program Design → 03 Professional Application → 04 Ongoing Monitoring.
Numbers earn their place here because the order carries real information (this is
the test `frontend-design` applies to numbered markers). Set in a large green serif
against white cards.

**7. Hero credibility seal.** A circular "Est. 2003" badge with curved text around
the rim ("Serving Local Homeowners · Professional Lawn Care") sitting bottom-right
of the hero. One honest fact, presented as a stamp. Reads as heritage without
claiming anything unverifiable.

**8. Floating social-proof card overlapping a circular photo mask.** An avatar
stack + five stars + "20,600+" pinned over the corner of a round-cropped job photo.
The circle mask alone is a cheap way to make stock or amateur photos look art
directed.

**9. Utility bar above the main nav** — Service Areas / Testimonials / Blog /
Customer Login — keeps secondary destinations out of the primary nav, which stays
a clean service taxonomy (5 dropdowns, every service its own indexable page).


### Their site ARCHITECTURE, which is the part worth copying carefully

Pulled from their sitemap index on 2026-07-28:

| Sitemap | Count | Verdict |
|---|---|---|
| `page-sitemap.xml` | 54 | Service pages, nested sub-services (`/pest-control/ant-control/`). **Copy this.** |
| `service-area-sitemap.xml` | **125** | `/service-area/<county>/<city>/`. **Do not copy this.** |

**The service pages are the good part.** Every one follows the same skeleton and it is
a genuinely strong one:

> `What is it / what's included` → `Why it matters` → `How we do it` (their named
> process) → **`FAQs` with question-form H3s** → CTA

The FAQ-as-question-H3 is the AEO play. It is what Google pulls into "People also
ask" and what AI answer engines quote, and it maps 1:1 onto FAQPage schema. Sub-services
nested under a parent (`/tree-and-shrub-care/shrub-pruning/`) give real internal-link
depth without inventing pages.

**The 125 service-area pages are doorway pages and should not be cloned.** Each runs
~1,244 words but carries only four real headings, meaning it is one template with the
city name swapped. Google's spam policy names this directly under *doorway abuse*:
pages built to rank for many similar queries that are not more useful than the
destination. Plenty of local sites do it and get away with it for years; it still
carries manual-action risk, and it is not something to put on a client's domain.

**The defensible version** (what a junk-removal client got): one page per real service, one page per
county actually served, each with distinct copy and distinct FAQs, cross-linked both
ways. Ten pages instead of 125, and every one of them says something different.

### What to leave behind (do not copy)

- **Five webfont families**: Commissioner, Noto Serif SC, Inter, Montserrat, and
  Comme, each loaded at every weight 100-900 plus italics. Enormous payload for no
  design gain. Worse, the display serif is **Noto Serif SC** — a Simplified Chinese
  face being used to set Latin headings, which is a builder default, not a choice.
  Our two-or-three-family rule beats this outright.
- **The hero background does not render on first paint.** It lazy-loads, so the
  first frame is a black rectangle. That is an LCP failure on the single most
  important element of the page. Never lazy-load the hero.
- **Duplicated DOM**: the nav renders twice and the testimonials block renders twice
  in the source, an Elementor mobile/desktop-duplicate artifact.
- **Dead links**: "see all services" and "Email us" both resolve to `/#`.
- **Copy mismatch left in production**: the "Client Testimonials" heading is
  subtitled *"We focus on solving your specific pest problem first"*, a leftover
  from the pest-control section. Proof that even a well-written site ships copy
  bugs, and an argument for reading every line back before deploy.
- **Palette is unremarkable**: brand green `#0e803f` with a red `#ec2024` CTA. It
  works and it's honest, but it isn't a design idea worth borrowing.
- **Structured data is thin** for a site this size: `WebSite` + `WebPage` +
  `PostalAddress` + `OpeningHoursSpecification`, no `LocalBusiness` with services.
  Our builds already do this better.

### The one-line takeaway
Their **design** is worse than ours and their **words** are better. When a fleet
build stalls, the gap is almost never another animation — it's that nobody asked
the owner the four questions that produce a "Terra Difference" section.

---

## Studio Kiln + Kurppa Hosk (2026-07-30) — the award-winning tier, measured

Adam named these as the level he wants for his own site. Full teardown:
`~/.claude/explanations/20260730_kiln_kurppahosk/TEARDOWN.md`.

### The finding that reframes every "make it award-winning" brief

**Neither site has a single `<canvas>`. Zero WebGL, zero Three.js, zero real-time particles,
zero 3D in the browser.** Verified live on both.

| | Kiln (BAFTA case) | Kurppa Hosk (home) |
|---|---|---|
| `<canvas>` | **0** | **0** |
| `<video>` | 16, all autoplay/loop/muted | 42 |
| `<img>` | ~12 | 116 |
| Page height | 19,053px | 7,733px |

A BAFTA-grade case study is roughly **85% media, 15% text**. The site is a frame; the assets are
the show. **When a brief asks for "particles / 3D / stunning", the answer is almost always
pre-rendered media, not an engine.** Kiln's BAFTA particle identity was built in **Cavalry** (a
procedural motion app) and rendered to video. They say so in their own copy.

### Their actual stacks

**Studio Kiln = Webflow.** jQuery 3.5.1, GSAP 3.12.2 (+ScrollTrigger, Flip, CustomEase, EasePack),
**Lenis** 1.0.23, SplitType, **Ukiyo.js** (parallax), Swiper 8, Plyr, **Barba.js** (page
transitions), Intellimize. Fonts: PP Mori + Quadrant Text Mono.

**Kurppa Hosk = Next.js App Router**, GSAP bundled as a module, self-hosted fonts via `next/font`.
Their typefaces (Teka, Giga) are their own: they run a foundry. That is why the type is unplaceable.

Everything in Kiln's stack is free and well documented. **Lenis + GSAP/ScrollTrigger + SplitType +
Barba is the whole "feel", and it is a weekend of work.**

### Steal these four, they are free

1. **The four-size type scale.** Kurppa Hosk uses *exactly* `72 / 45 / 18 / 16`. Nothing between
   45 and 18. The "expensive, lots of empty space" feeling comes from the **missing middle** (the
   h3/h4/lead sizes most sites fill), not from small text.
2. **Barba page transitions + Lenis smooth scroll.** Changes the feel more than any other single
   addition.
3. **A live local clock in the header** (`21:33PM`, updating). Costs nothing, makes the page feel
   alive before a single scroll.
4. **Photography of the work in situ**, not screenshots on a gradient. Kiln's BAFTA poster shot is
   a real wall with real raking sunlight; the Games shot is a hand holding a phone under hard
   green stage light with bokeh. This does most of the work and none of it is code.

### What NOT to copy

- **16 videos with no `poster` attribute.** Empty boxes until each decodes. Always set a poster.
- **Their information architecture.** Neither site has a price, a plain service list, a phone
  number, or a visible next step. They can afford that. A site that must convert a trade owner
  cannot. Steal the visual language, not the IA.

### The lazy-load trap this exposed (bit us the same day)

Elements that are **absolutely positioned inside a sticky container and moved only by transform**
never trigger browser lazy-loading: `loading="lazy"` left **0 of 20** images unloaded and the
centrepiece section rendered empty. Load that set eagerly at `fetchpriority="low"` instead.

Related: **the automation tab reports `document.hidden: true`, so images can screenshot as blank
grey boxes while being completely fine.** Prove paint by reading pixels (`drawImage` then
`getImageData` and count distinct colours), never by screenshot.
