---
name: cold-outreach
description: >
  Research a prospect, evaluate fit, draft a personalized cold email, preview it to
  yourself, send it via Resend, and track it in a bounded ledger. Use when the user asks to
  "research a company/prospect", "check out this lead", "draft a cold email", "send cold
  outreach", "outreach to this business", "deep dive on this prospect", "add to my prospect
  list", or "follow up". Config-driven: you set your sender identity, product, and ideal
  customer in references/config.md — the skill stays generic across industries.
---

# Cold Outreach

<objective>
Run personalized 1:1 cold-email outreach for whatever you're selling. Covers the full
workflow: deep prospect research (parallel agents — web search + page scraping + public
profiles), a 1-10 fit rating, a personalized draft, a **mandatory preview to your own inbox
before any real send**, sending via the Resend API, and tracking in a bounded ledger. You
define who you are and what you sell in `references/config.md`; the skill reads it each run.
NEVER send without a preview confirmation.
</objective>

<context>
@references/config.md
@ledger/prospects.md
</context>

<execution_context>
- 🟢 Auto: research, evaluation, draft generation, preview-to-self send
- 🟡 ASK on: which recipient to target if there are multiple candidates, custom personalization, follow-up timing
- 🔴 NEVER: send to a generic inbox without a specific Attn line; send to the real recipient without a preview + explicit "yes send it"; modify the ledger without an explicit request
- Mandatory self-preview: ALWAYS send the draft to your own address (from config) with a "(test)" subject prefix BEFORE the real send
- History: append-only `ledger/prospects.md` (one row per prospect; status tracked via cell updates)
</execution_context>

## Setup (one time)

Fill in `references/config.md` with your sender identity, product one-liner, target profile,
and subject line. Set two environment variables:

```bash
export RESEND_API_KEY="your-key"   # free key at https://resend.com
export JINA_API_KEY="your-key"     # optional; free key at https://jina.ai (Reader also works keyless)
```

## Core Workflow

1. **Research** — deep-dive a prospect using parallel agents (page scraping + web search).
2. **Evaluate** — rate the prospect 1-10 on fit signal, size, and contact accessibility.
3. **Draft** — personalize the template with a prospect-specific hook.
4. **Preview** — send the draft to your own inbox (from config) for a visual review.
5. **Send** — after explicit confirmation, send to the target via Resend.
6. **Log** — update `ledger/prospects.md` with send date, recipient, and follow-up notes.

## Research Protocol

Launch 2-3 parallel research agents:

**Agent 1 — Site scrape**: scrape the prospect's website for team members, roles, emails,
bios, and the pages most relevant to what you sell. Use the `jina-image-search` skill or
raw jina endpoints — Reader (`r.jina.ai`) works keyless; Search (`s.jina.ai`) needs
`JINA_API_KEY` (or use the built-in `WebSearch` tool instead).

**Agent 2 — External research**: search each decision-maker by name on public profiles
(LinkedIn, industry directories, review sites). Find reviews, ratings, awards, talks,
publications, and the company's external reputation.

**Agent 3 (optional) — Depth on the buying signal**: scrape the pages that indicate whether
they have the problem you solve, and identify the specific gap your product fills.

## Fit Evaluation

Rate prospects 1-10:

| Factor | Weight | What to look for |
|--------|--------|------------------|
| Buying signal | High | Evidence they have the exact problem you solve |
| Size | Medium | The size band where your offer lands best (define it in config) |
| Contact accessibility | High | A direct decision-maker email >> a generic inbox >> a contact form only |
| Readiness | Medium | No incumbent solution = easier; an entrenched competitor = harder |
| Reputation | Low | Public ratings as a tiebreaker |

**8-10**: strong target. **5-7**: moderate. **1-4**: low priority.

## Who to Send To

1. The person who owns the problem you solve day-to-day.
2. A direct, named email over a generic inbox (`firstname@company.com` > `info@company.com`).
3. Skip `admin@`/`noreply@`. For a generic inbox at a larger org, add a bold **Attn: [team]** line using their actual internal team name.

## Email Template

Read `references/email-template.html` and `references/email-template.txt`. Fill the
placeholders from `references/config.md` and the prospect research.

### Personalization rules
- Replace `[prospect specific thing]` with something concrete from their site (a 30-second skim).
- Reference their actual content, work, or details — show you looked.
- **Do NOT personalize the subject line.** For B2B cold email, a generic, low-key subject
  generally out-performs a personalized one; keep it short and non-salesy (set it in config).

### Template style rules
- Inline styles only (email clients strip `<style>` tags); plain-text version always included.
- System font stack, ~15px, line-height 1.6, near-black text; one clear link, not a loud button.
- Keep it short and text-first for deliverability — avoid heavy images on a first send.

## Sending Protocol

Send via the Resend API — see `scripts/send-email.sh` (reads `RESEND_API_KEY`; takes the
from-address, subject, recipient, and bodies so nothing is hardcoded).

- **From / subject**: from `references/config.md`.
- Always send both HTML and plain-text versions.
- Always confirm the recipient with the user before the real send.
- For previews, send to your own address (config) with a "(test)" subject prefix.

## Tracking

After each send, update `ledger/prospects.md`: add/refresh the prospect's row (name, contact,
size, signal), mark **SENT [date]** with recipient + role, and note the next follow-up.

## Follow-Up Sequence

3-4 days after the initial send, up to two follow-ups, each hitting a different angle
(a different pain point, a proof point, or a short nudge). Stop after two; never spam.

<saved_rules_format>
Accumulate learnings in `references/lessons.md` (durable). Format:
`- {topic}: {rule} — set {YYYY-MM-DD}`
e.g. "channel: direct email beats generic inbox", "subject: never personalized", "timing:
Tuesday morning best open rate", "skip: prospects with an entrenched incumbent".
Surface relevant rules at the start of a run.
</saved_rules_format>

<recovery_protocol>
- Interrupted mid-research → check which agents completed; resume only the missing ones.
- Interrupted mid-draft → reload the prospect research; regenerate the draft.
- Interrupted mid-send → check Resend for the last send id; verify it actually sent before retrying (avoid duplicate sends).
</recovery_protocol>

<error_handling>
- Scrape returns blocked/empty → fall back to web search; never block on one source.
- Resend rate limit → sleep and retry once.
- No direct email → require explicit user go before sending to a generic inbox.
- Bounce / hard fail → mark the row `BOUNCED [date]`; do not retry without confirmation.
</error_handling>

<success_criteria>
- [ ] Prospect research completed (multi-agent output)
- [ ] Fit rating assigned (1-10) with rationale
- [ ] Draft personalized with a prospect-specific hook
- [ ] Preview sent to your own inbox with a "(test)" prefix
- [ ] User confirmed before the real send
- [ ] Ledger row appended/updated with SENT [date]
- [ ] Follow-up notes added
</success_criteria>
