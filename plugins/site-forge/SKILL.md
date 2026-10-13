---
name: site-forge
description: >-
  Build a distinctive, production-grade website (single-page or multi-page) — and an optional
  Remotion promo video — for any business, product, or person, then deploy it
  free. Use whenever the user wants to build, design, mock up, prototype, or
  pitch a website, landing page, demo/spec site, or portfolio — for a local
  business, a product launch, cold-outreach demos, or themselves — even if they
  never say "site-forge". Adapts a unique aesthetic and structure to each brief
  (never a template). Two modes: auto (fast, autonomous, free agent-made media)
  and full (interactive, best quality, Gemini + Veo media).
argument-hint: "[auto|full] <what to build, for whom, any assets/links>"
---

# Site Forge

<objective>
Turn a one-line brief into a finished, deployed, award-quality website. The
output is a self-contained site with no build step on a CDN stack — a single
`index.html` for a one-pager, or a multi-page set that shares one byte-identical
shell (head, nav, footer, scripts) — optionally paired with a Remotion promo video. The rule that makes this worth
running: **every site is designed fresh for its brief** — a plumber's one-pager
and a SaaS launch must look nothing alike (different palette, fonts, layout,
sections, motion). The references here are a **capability library you draw
from**, never a checklist you fill in. Start from a clean, fast, responsive
floor and add only what the brief earns; the references are a starting point,
not a ceiling — exceed them when the brief calls for it.
</objective>

<execution_context>
Phase 0 resolves the mode:

- **auto (fast):** Do as much as possible yourself. After the one plan/approval
  gate (Phase 3), run to completion without asking. Use only media you can make
  yourself for free (jina; MCP/Higgsfield if present). If a step blocks, needs
  interaction, or fails — skip it, keep going, list it under "Skipped / upgrade
  later" at the end. Bias to shipping.
- **full (best quality):** Interactive. Ask whenever a choice meaningfully
  changes the result, and use the best *free* media even when it needs the user
  (Google/Gemini for images, Veo 3.1 Fast in Flow for video — hand them exact
  prompts, they generate, drop the files). A blocked step → ask them to step in.

Both modes:
- 🟢 Auto: explore the environment, design, write code, extract frames, run
  ffmpeg, local-preview, and deploy *after* approval.
- 🟡 TWO mandatory gates in both modes: (1) the Phase 3 plan before building, and
  (2) **the deploy itself — ask immediately before every deploy, every time.**
  Approval for one deploy is never approval for the next. Default is local preview.
- 🔴 Never: invent fake credentials/keys; publish claims the user flagged as
  unverified without a disclaimer; enter the user's secrets into forms.
</execution_context>

<process>

<phase name="0_mode_and_brief">
## Phase 0 — Mode + brief
First token of the invocation (`auto`/`full`) sets the mode; the rest is the
brief. If no mode is given, ask once. Capture: who it's for, the goal, any
assets/links/voice. Thin brief → in `full` ask 1–2 sharpening questions; in
`auto` infer sensibly and record assumptions in the plan.
</phase>

<phase name="1_explore">
## Phase 1 — Explore (this is what makes it portable)
Detect what's actually on this machine before planning, quickly and in parallel:
- **Skills:** `frontend-design`, `design-taste-frontend`, `impeccable`,
  `jina-image-search`, `remotion`, `higgsfield-generate`, `here-now`
  (`ls ~/.claude/skills` + plugin list).
- **MCP:** context7, higgsfield, any image/video servers.
- **CLI/runtime:** `node`, `npx`, `python3`, `ffmpeg`, `edge-tts`, `netlify`,
  and the **OS + version** (`sw_vers` — version matters; macOS < 15 needs the
  Remotion workaround in `references/remotion-video.md`).
Record what's present. Prefer live skills/tools when found; fall back to this
skill's baked-in references when not. Install nothing yet — install *just before*
the step that needs it (Phase 5/6), Netlify only at deploy.
</phase>

<phase name="2_design">
## Phase 2 — Design direction (the design stack, in order)
**All three run, every build. See `references/design-stack.md` for the full
detail, command list, and conflict table — read it now if you have not.**

0. **Pick the PROFILE before anything else.** Read `references/design-profiles.md`
   and state it in one line: *"Profile: creative-portfolio. Bending display-size
   ceiling, serif ban, scrim floor, conversion furniture. Craft floor unchanged."*
   The default is `local-service`; `creative-portfolio` covers photographers,
   designers and artists; `personal-agency` is Adam's own. The profile decides which
   of Adam's aesthetic rules are in force — the **craft floor never bends**, so
   16px body, 4.5:1 contrast, 44px taps, reduced-motion, schema, the sixteen social
   tags and the security headers apply no matter what the brief or a reference site
   does. Getting this wrong produces a trades site wearing a portfolio's photographs.

1. **Read `references/page-composition.md` first** (it is the difference between a
page that feels designed and one that feels empty), then **invoke `frontend-design`
before any markup** (installed → use it; else read
   `references/frontend-design.md` — the **full skill, bundled verbatim**, so you get
   its complete guidance even offline).
2. **Invoke `design-taste-frontend`.** State its one-line design read
   ("Reading this as: <page kind> for <audience>, with a <vibe> language…") and set
   the three dials. Use taste-skill's own defaults and presets. **The one carve-out:
   its perpetual-motion unlock at MOTION_INTENSITY > 5 stays off** — no pulse,
   shimmer, float, typewriter, or infinite loops. Skip its React/Tailwind stack
   section on static builds.
3. **Impeccable** is already running: its hook fires on every write. Its commands
   are the Phase 7 gate.

Then use `references/aesthetics.md` as the theme/type/layout-derivation helper.
This is the anti-slop gate and the biggest quality lever. Commit to
a bold, brief-specific direction:
- One clear aesthetic, executed precisely; a distinctive font pairing (never
  Inter/Roboto/Arial); a cohesive palette as CSS variables.
- The *structure* — which sections, what hierarchy, the one memorable moment —
  derived from the brief. **Do not reuse the last site's shape.**
- Which capabilities fit, and which to leave out (see the Reference map). A
  simple brief may use none of the heavy effects; a flagship may use several.
Write a 3–5 line design brief to carry into the plan.
</phase>

<phase name="3_plan_and_approve">
## Phase 3 — Plan + approve (the one gate, both modes)
Present a tight plan: design direction, sections, capabilities you'll use, what
you'll **install/run**, what **spends credits** (AI media), and (in `full`) what
**needs the user**. In `auto`, also list likely skips. Approval here is the only
mandatory stop in `auto`.
</phase>

<phase name="4_media">
## Phase 4 — Media (per mode)
See `references/ai-media.md` and `references/images.md`.
- `auto`: jina for images (and try for embeddable/scrub video); MCP/Higgsfield
  if present and free; extract scroll-scrub frames from any clip with ffmpeg.
  No good video available → ship image-only (Ken-Burns) and flag the upgrade.
- `full`: best free media — Gemini images, Veo 3.1 Fast in Flow video (hand the
  user exact prompts) — plus everything `auto` can do.
Always: right dimensions, `object-fit`, lazy-load, the `img{height:auto}` rule,
and the before/after same-base edit trick when the brief wants it.
</phase>

<phase name="5_build">
## Phase 5 — Build the site
Write the site as self-contained HTML — one `index.html`, or a multi-page set
(see below) — with CDN libs via SRI'd `<script>` tags (nothing to install). Compose from the capability references chosen in Phase 2,
reading each only when you use it (see the Reference map). Stagger heavy effects
(one per viewport), lazy-init below the fold, keep the console clean, and match
implementation complexity to the aesthetic — restraint for minimal briefs,
elaboration for maximal ones. Two starting points: `assets/templates/index-skeleton.html` for a one-pager, and
**`assets/templates/terrain/`** for a multipage home-services build (19 pages,
photo headers, wave dividers, rotating masks, 120 forced skin variations via
`skin.py --slug <client>`). Treat both as *starting points to reshape*, not
templates to fill blindly — but do NOT undo terrain's composition rules.

**Impeccable's hook fires on every write.** Resolve its findings as they appear,
not in a pile at the end — each one either gets fixed or explicitly classified as a
false positive with a stated reason. Never inline-suppress a rule to skip fixing it;
suppression needs Adam's confirmation. After ~6 edits it goes quiet to avoid noise,
which is why the Phase 7 audit is a separate hard gate.

**Single-page vs multi-page.** A one-pager ships as a single `index.html`. A brief
with distinct audiences or real depth (a business site with patient / physician /
pricing / about sections, a marketing site with a Science page) earns a **multi-page**
set instead — separate `*.html` pages sharing one chrome. With no build step the
shared blocks are hand-copied, so **drift is a real bug**: keep the `<head>` (incl.
the no-FOUC theme snippet), nav, footer, and `<script>` tags byte-identical across
every page, and verify by hashing them before deploy — a page that quietly diverges
(different fonts, a missing toggle, a dead link) is the classic failure. Give each
page its own self-referential `canonical`/`og:url` + `<title>`/description, emit a
`sitemap.xml` + `robots.txt`, and `noindex` any private/app mockup pages. If the page
count or shared-block size makes hand-copying fragile, a tiny include step (Node
concat, or Eleventy/Astro) is a fair trade — but only when the brief earns it;
default to no-build.
</phase>

<phase name="6_video">
## Phase 6 — Promo video (optional)
**When the brief asks for a promo video — a "full shebang", "with video",
"VO/karaoke captions/music" — BUILD it here. Do NOT defer it to a MEDIA-PROMPTS
prompt.** The Remotion promo is my-tools work (edge-tts + ffmpeg + Remotion, all
free and local) and runs on whatever images the site already has — stock
placeholders are perfectly fine for it. Deferring-with-a-prompt is ONLY for
credit/paid AI media (Gemini stills, Veo clips). Confusing the two is a real
miss: on a "full shebang" build the promo must be rendered and embedded (a
click-to-play film section) before the site is called done.
If the brief wants a video, build it with Remotion — full pipeline (VO →
karaoke captions → audio mix → **sequence render → ffmpeg stitch**, incl. the
macOS < 15 workaround) in `references/remotion-video.md`, using
`scripts/build-captions.py`, `scripts/mix-audio.sh`, `scripts/render-video.sh`.
Install Remotion/edge-tts/ffmpeg just before this step. In `auto`, a render
failure → skip + flag; in `full`, ask the user to help.
</phase>

<phase name="7_qa_and_deploy">
## Phase 7 — QA, then STOP. Deploy is gated.
Run `references/quality-checklist.md` (CSS collisions, JS TDZ, `img` stretch,
form detection, lazy-load timing, mobile pass, console-clean, reduced-motion).

**Then three mechanical gates, all of which have caught real shipped defects:**
```bash
python3 <skill>/scripts/audit-seo.py        # SEO, local SEO, security. exit 1 on HIGH
python3 <skill>/scripts/check-crops.py      # object-fit:cover discarding the subject
python3 <skill>/scripts/colour-system.py    # one treatment per photograph, site-wide
```
**And click every interactive element in a real browser**, asserting a state
change. An FAQ, a filter bar and a map panel have all shipped with complete
markup, complete CSS and no handler at all: nothing looks broken in the source.
Use `document.elementFromPoint` at the control's own centre, not `.click()`,
which skips hit-testing and passes on a control that is completely buried.

**If anything feels janky, TRACE it, do not sample it.** `performance_start_trace`
then scroll then `performance_analyze_insight("ForcedReflow")` names the offending
function by file and line. Frame-rate sampling has plus or minus ten points of
variance and will send you after the wrong thing. See `scroll-performance.md`.

**Design-stack gate — hard, before deploy, no exceptions:**
1. `/impeccable critique` (UX review) then `/impeccable audit` (a11y, perf, responsive).
2. Every finding fixed, or classified a false positive with a stated reason. Never
   inline-suppress. Suppression needs Adam's confirmation.
3. Run taste-skill's own pre-flight checklist (its Section 14).
4. Grep the CSS for `infinite` animations and tinted `box-shadow`, and neutralize
   both. This catches the one taste-skill setting we deliberately override.

**Default is LOCAL.** Preview with `python3 -m http.server 8080` in the build dir and
iterate there. **Do not deploy unless the user asks in that moment** — a live URL is
only warranted for a paying client or a scheduled demo, and every deploy costs Netlify
credits (38 deploys to one site exhausted a monthly allowance and forced a paid
upgrade). Batch every outstanding fix into ONE deploy per review round.

**Mobile QA is deferred to the first real deploy** — it cannot be done locally and the
automation browser cannot emulate a true mobile viewport. Plan for a dedicated mobile
pass at demo time rather than pretending it was verified earlier.

**NEVER deploy the project root.** `.netlifyignore` is NOT honoured by `netlify deploy --dir`,
and deploying a root once published a client's HOME ADDRESS and a tracker PASSWORD across the
fleet. Build an explicit publish directory and verify the live surface, every time:

```bash
python3 scripts/make-dist.py .        # publishes only web files, withholds .py/.md/package.json
netlify deploy --prod --dir dist
scripts/verify-published.sh <host> [owner-street-name]   # must print "clean"; non-zero exit = leak
```

When the user does approve, deploy with `scripts/deploy-netlify.sh`
(`references/deploy.md`) — Netlify is the only thing installed at the end;
enable Forms (`ignore_html_forms`) + the notification hook if there's a form.
**Then set up Cloudflare Web Analytics by default** (the user usually wants it):
ask for a beacon token for the deployed hostname, inject the snippet before
`</body>` with NO SRI (Cloudflare rotates it — the documented exception), and
redeploy. In `auto`, surface it as a "needs the user" item with the exact
hostname. Details in `references/deploy.md`.
Report the live URL, what was used, and (in `auto`) the Skipped / upgrade-later
list.
</phase>

</process>

## Reference map (read on demand — do NOT preload all of these)
| Need | File |
|---|---|
| **Design profiles**: the craft-floor / aesthetic-default split, and which genre bends what. **Read at Phase 2 before designing.** | references/design-profiles.md |
| Profile: photographers, designers, artists, studios | references/profile-creative-portfolio.md |
| Profile: Adam's own brand and agency site (stub) | references/profile-personal-agency.md |
| **Adam's operation context**: live demo fleet + URLs, required head steps (favicon files, OG card, site-name signals), media policy, truth discipline | `~/.claude/skills/site-prospector/references/adam-operation-context.md` |
| GSAP+Lenis wiring, reduced-motion, CDN/SRI | references/stack-and-wiring.md |
| **Why a page feels full or empty: no text-only bands, layering, masks, dividers** | **references/page-composition.md** |
| Scroll scrub (frames), before/after, progress bar + back-to-top ring, reveals, perf rules | references/scroll-effects.md |
| **Why a scroll effect janks**: TRACE don't sample, layout thrashing, lazy-loading forces decode, when promotion hurts, dropping GSAP | references/scroll-performance.md |
| **Scroll-drawn SVG line**: page-height path, stacking, per-band gradient, tangent-continuous loops, monotonic anchor | references/svg-line-work.md |
| **SEO + local SEO + security audit** (run scripts/audit-seo.py) | references/seo-security-audit.md |
| Canvas pseudo-3D (no bundler, default) + Three.js (capability-gated) | references/interactive-3d.md |
| Carousel, video player, counters, Netlify Forms | references/components.md |
| **The design stack**: frontend-design + taste-skill + Impeccable, dials, commands, conflict table | references/design-stack.md |
| frontend-design — full skill, verbatim (offline fallback) | references/frontend-design.md |
| Theme system, fonts, deriving a unique look | references/aesthetics.md |
| Swipe file: real sites worth stealing from, what to copy vs leave (read at Phase 2 when the brief is a local trade) | references/reference-sites.md |
| AI image/video gen (auto vs full), free-vs-paid | references/ai-media.md |
| Image handling, height:auto fix, ffmpeg crop/scale | references/images.md |
| Remotion VO→captions→mix→render→stitch, macOS fix | references/remotion-video.md |
| Bug checklist before shipping | references/quality-checklist.md |
| Netlify deploy, Forms API, rename | references/deploy.md |
| **Social card verifier** (run after EVERY deploy) | `scripts/verify-og.py <host>` |

This is a toolkit, not a sequence. Use what the brief earns; ignore the rest.

<error_handling>
- Missing skill/tool → `auto` falls back to the baked-in reference and notes it;
  `full` offers to install or asks.
- Install fails / needs interaction → `auto` skips + surfaces; `full` asks.
- macOS < 15 Remotion render abort → sequence-render + ffmpeg-stitch path
  (`references/remotion-video.md`), never the direct mp4 mux.
- AI media unavailable / out of credits → `auto` ships image-only + flags
  upgrade; `full` routes to Gemini/Flow.
- Netlify form not detected → set `ignore_html_forms:false` via API + redeploy
  (`references/deploy.md`).
</error_handling>

<success_criteria>
- [ ] Design is unique to the brief — not a reuse of a prior site's look.
- [ ] frontend-design applied (invoked, or its principles via aesthetics.md).
- [ ] taste-skill applied: design read declared, dials set, its pre-flight run.
- [ ] `/impeccable critique` + `/impeccable audit` run; every finding fixed or classified.
- [ ] No `infinite` animations, no tinted `box-shadow` (grep-verified).
- [ ] Icons from Phosphor (or HugeIcons/Radix/Tabler), one family, one strokeWidth.
- [ ] Self-contained site (one index.html, or a multi-page set sharing byte-identical chrome); console-clean; mobile passes.
- [ ] Only brief-earned capabilities included (no gratuitous effects).
- [ ] Plan approved before build (both modes).
- [ ] Deployed from an explicit `dist/`, NOT the project root.
- [ ] `verify-published.sh` run against the live host and printed "clean".
- [ ] Deployed; live URL reported; `auto` lists any skips/upgrades.
</success_criteria>

**CMS / "can I edit it myself?"** — read `references/cms-options.md` before answering. Short version: **default is NO CMS; content changes are included in the monthly, and that is a feature, not a gap** (a trade changes their site ~twice a year and will forget the login). If one is genuinely warranted, the only category that fits hand-written static HTML is a **git-based CMS** (Sveltia or Decap), never WordPress — we sell against WordPress explicitly. A CMS is a paid tier feature, never a default.

**Twilio / missed-call text-back / A2P 10DLC** — read `references/twilio-a2p-10dlc.md` before quoting or building it. Three things that decide everything: (1) **the reseller rule** — brand registrations carry the CLIENT's email and address, not ours; using ours caps the business at 10 clients, silently; (2) **campaign vetting takes WEEKS, not days** — start the day they sign; (3) **a live website + a business email on a real domain are REQUIRED FIELDS**, and our gmail-using prospects have neither, which makes the website a prerequisite for texting rather than a nice-to-have. That is the strongest sales argument in the ladder.
