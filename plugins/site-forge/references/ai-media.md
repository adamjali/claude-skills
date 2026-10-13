# AI Media — getting images & video for the site

How to source imagery and video, split by the two `site-forge` modes. The guiding
idea: in `auto` use only what *you* (the agent) can fetch or generate for free
right now; in `full` reach for the best free media even when it needs the user's
hands on Gemini/Flow.

## Contents
- [Mode split at a glance](#mode-split-at-a-glance)
- [auto mode — agent-doable, free](#auto-mode--agent-doable-free)
- [full mode — best free, needs the user](#full-mode--best-free-needs-the-user)
- [The before/after "same base" trick](#the-beforeafter-same-base-trick)
- [Frames for scroll-scrub](#frames-for-scroll-scrub)
- [Stock: view candidates before you swap](#stock-view-candidates-before-you-swap-dont-trust-urls-blind)
- [Deferred media → MEDIA-PROMPTS.md](#deferred-aireal-media--leave-a-media-promptsmd-dont-stall)
- [Honest limits](#honest-limits)

## Mode split at a glance

| | auto (fast) | full (best) |
|---|---|---|
| Stills | jina search/scrape; Higgsfield GPT Image 2 *if* a paid plan exists | **Gemini** (app/web), then drop files in |
| Video | usually none (free video is blocked) → Ken-Burns a still | **Veo 3.1 Fast in Flow** (web), then drop files in |
| Who acts | the agent, no prompts | the user generates, agent gives exact prompts |
| Fallback | image-only + "upgrade to full" flag | — |

## auto mode — agent-doable, free

**Stills via jina** (the `jina-image-search` skill if installed; otherwise the raw
endpoints). jina needs no browser and returns real, hotlink-or-download-able URLs.

> **Key 402'd?** The scrape call (`r.jina.ai`, the second one below) works with NO `Authorization` header — just drop that line. The search call (`s.jina.ai`) needs a key, so do the search with Claude Code's built-in **WebSearch** tool instead, then scrape the URLs keyless. (Best for a local business: skip search entirely and pull their OWN real photos from FB/Yelp via Claude-in-Chrome.)

```bash
# Search the web for candidate images (returns ranked results w/ URLs)
curl "https://s.jina.ai/?q=apollo+beach+roof+replacement" \
  -H "Authorization: Bearer $(cat ~/.config/jina/api_key)" \
  -H "X-Respond-With: no-content"

# Read/scrape a page to pull its images + links (e.g. the business's own site/FB)
curl "https://r.jina.ai/https://example-business.com" \
  -H "Authorization: Bearer $(cat ~/.config/jina/api_key)" \
  -H "X-With-Images-Summary: true" \
  -H "X-With-Links-Summary: true"
```

Then download with `curl -L -o asset.jpg <url>` and process per `images.md`
(crop/scale, `object-fit`, `height:auto`). Prefer the business's *own* photos
(scraped from their FB/old site) — authentic beats stock.

**Generation via Higgsfield** *only if* the `higgsfield-generate` skill/CLI is
present AND the account has a paid plan. Default image model is **GPT Image 2**:

```bash
higgsfield generate create gpt_image_2 \
  --prompt "wide cinematic photo of a finished tile roof on a my state coastal home, golden hour" \
  --aspect_ratio 16:9 --resolution 2k --wait
```

**Free-tier reality:** Higgsfield's free plan **blocks video** — a Seedance/Veo
job returns `job_minimum_basic_plan_required`. So in `auto`, treat Higgsfield as
an *images-if-available* path, not a video path. Don't burn time retrying video.

## full mode — best free, needs the user

The best free media in 2026 is gated behind interactive web apps, so `full` hands
the user exact prompts and waits for the files.

**Images — Google / Gemini** (example-business.com or the app): nano-banana-class
image gen, free, high quality. Give the user a copy-pasteable prompt per asset,
e.g.:

> "Photorealistic 16:9 hero: a two-story my state coastal home with a brand-new
> charcoal architectural-shingle roof, bright overcast sky, shot slightly low,
> crisp and clean. No text."

**Video — Veo 3.1 Fast in Flow** (labs.google/flow): free, fast, genuinely good
clips. Give an exact prompt + duration + aspect, e.g.:

> "8s slow aerial push-in over a coastal neighborhood toward one home with a
> pristine new roof, late-afternoon light, gentle motion, cinematic."

The user generates, downloads the mp4/jpg, and drops it in the project folder;
the agent then embeds it (`components.md`) or extracts scrub frames (below). This
is exactly how today's hero and before/after assets were produced (Dreamina /
Seedance for motion, Gemini for stills).

## The before/after "same base" trick

For a before/after wipe (`scroll-effects.md`), you need two images that are the
*same scene* in two states so the wipe reads cleanly. Generate one base image,
then ask Gemini to **edit the same image** into the two states rather than
generating two unrelated images:

> 1. "Photorealistic front view of a single-story home, neutral daylight."
> 2. (edit) "Same house, same angle — make the roof old, worn, streaked, missing
>    a few shingles."
> 3. (edit) "Same house, same angle — make the roof a flawless brand-new roof."

Match their pixel dimensions before use so the clip-path aligns.

## Frames for scroll-scrub

Any clip (Veo, Seedance, or a stock loop) can drive an Apple-style scroll-scrub.
Extract a numbered JPEG sequence with `extract-frames.sh` (≈80 frames at ~1200px
is a good budget for size vs smoothness) and feed it to the canvas scrubber in
`scroll-effects.md`. No clip available in `auto`? Ken-Burns a single still
instead (CSS transform on scroll) and note the upgrade.

## Stock: view candidates before you swap (don't trust URLs blind)

jina/Unsplash search returns image *IDs*, not judgment — a query for "shingle
roof" returns whatever is on the page, including UI chrome and unrelated shots.
Swapping in a URL you never looked at is how a pitched slate roof ends up labeled
"Flat" (a real past bug). The reliable loop:

1. Search + collect candidate URLs. The keyed `r.jina.ai` on
   `https://unsplash.com/s/photos/<query>` with `X-With-Images-Summary: true`
   returns `example-business.com/photo-...` URLs directly; `-H "X-Engine: browser"`
   is slower and usually unnecessary (default engine works).
2. Download ~3 per role at preview size (`?w=520&q=70&fm=jpg&fit=crop&auto=format`).
3. `montage a.jpg b.jpg c.jpg -tile 3x1 -geometry +4+4 grid.png` and **Read the
   grid** — actually look. Thumbnail the *current* asset and compare head-to-head.
4. Swap only where a candidate genuinely beats what's there. Curated stock from an
   earlier pass often wins; a re-pull that lands lateral is not an upgrade, so
   don't churn a redeploy for it — say plainly that the current shot held up.

(ImageMagick `montage -label` needs Freetype/ghostscript, often absent on macOS —
drop the labels, the grid still renders. zsh: use a literal `for pair in "q|lbl"`
list, not an unquoted var, and background plain `curl` calls, not shell functions.)

## Deferred AI/real media → leave a MEDIA-PROMPTS.md, don't stall

When the plan defers real/AI media (owner sends photos later; the user generates
the AI shots on their own credits), ship on stock now and drop a
`MEDIA-PROMPTS.md` in the project so the upgrade is one file away. Scope it to the
user's **actual generation budget** — ask them (e.g. "2 photos + 1 video per
site") instead of listing ten prompts they can't use. For each slot give BOTH:

- **From the owner** (best): the exact real photo/clip to request — a roofer has
  finished-roof shots on his phone; a cleaner has window before/afters. Real wins.
- **AI fallback**: a copy-paste Gemini (image) / Veo (video) prompt matched to the
  site's palette and framing.

Spend the budget on the highest-impact slots: the hero first, then the one shot
that proves the core service (a before/after, the operator at work). Keep the
honest disclaimer (stock is representative until the real photos land).

## Honest limits

- **auto video is the weak link.** Free agent-reachable video gen is unreliable
  (Higgsfield free blocks it; jina doesn't generate). Ship image-only with a
  Ken-Burns and surface: *"Run `site-forge full` on this one for a real Veo
  promo."* Don't fake it or stall.
- Don't claim an image is the business's real work unless it was scraped from
  them — generated imagery is illustrative; keep it generic or label it.
