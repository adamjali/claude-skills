---
name: site-prospector
description: >-
  Find local businesses worth pitching a free demo website to, present them with
  honest reasoning, let the user pick, then for each: verify the facts, build a
  site via site-forge, deploy it, and draft tailored multi-channel outreach —
  logging everything to a bounded ledger. Use whenever the user wants to find
  prospects, leads, or candidates for web-design / demo-site outreach, scout
  local businesses with no or weak websites, run client-finding for the website
  business, or "find someone to pitch" — even without saying "site-prospector".
  Runs autonomously and orchestrates site-forge for the build.
argument-hint: "<trade + area, e.g. 'roofers in Example Town ST'> [how many]"
---

# Site Prospector

<objective>
The front of the local-website business: find businesses that would benefit from
a free demo site, surface them with honest reasoning, and — for the ones the
user picks — verify the facts, build and deploy a site, and produce ready-to-send
outreach. It **orchestrates `site-forge`** for the build (Claude invokes it; they
hand off via a shared brief file) and keeps a **bounded ledger** so the pipeline
never loses state and never grows forever. Truth discipline is core: claims get
verified or labeled, and demo sites carry a not-affiliated disclaimer.
</objective>

<context>
@ledger/index.md
@references/adam-operation-context.md
</context>

<execution_context>
Autonomous by default — a hands-off finder→builder. Required stops: (1) the user
picks which candidates to pursue (Phase 2), and (2) anything that sends or
publishes externally.
- 🟢 Auto: search, evaluate, fact-verify, write the brief, invoke site-forge (in
  `auto`), deploy the demo, draft outreach, update the ledger.
- 🟡 Ask: which candidates to build (always); **every deploy, immediately before it**
  (default is local preview; deploy only for a paying client or a scheduled demo);
  repointing form leads; custom domains.
- 🔴 Never: send/publish outreach without explicit go (drafts only); publish a
  flagged-unverified claim without the demo disclaimer; pay for anything.
Quality note: each demo is built as well as is *autonomously* reachable, then a
per-site "upgrade to full" flag is surfaced so a winner can be re-run with
`site-forge full` for Gemini/Veo media.
</execution_context>

<process>

<phase name="1_scout">
## Phase 1 — Scout candidates
**Read `references/scouting-doctrine.md` first, and read section 2d (THE CONVERTING-LEAD PROFILE) before anything else in it: that section is derived from 5 interested vs 19 declined across 79 real calls and it OUTRANKS every other heuristic in the file when they conflict. In one line: an ESTABLISHED trade (often 10+ yrs) hustling for leads on Nextdoor / local FB groups / GreenPal, with ZERO or ONE review, NO Google Business Profile, and either no site or a dead domain they still own. Not 'no online presence' but maximum effort, zero owned assets. You cannot find these people on Google because their absence from Google IS the gap, so hunt Nextdoor and community groups, not the map pack.** It is also the canonical scope + rubric (supersedes the older `candidate-search.md`). Scope: state-wide except the two largest metros; RURAL small towns weighted UP; the full spread of local verticals (not just home services — see the catalog: marine, rural land/structure/mechanical/ag, guides/makers, auto, pets, food, professional, events, etc.). Priority order **(reordered 2026-07-28 on live call evidence — the old list led with NEW, which was wrong)**: (1) **owner is already marketing themselves** and posting personally in the last 30 days (proved demand — this is the strongest predictor of a reply), (2) **established 2+ years with few reviews and no Google Business Profile** (a concrete free-to-fix gap they usually already know about), (3) no website or a broken/parked/ugly/outdated one, (4) bonus older/non-tech owner and/or rural. **NEW/recently-opened is no longer a top signal** — the the state corporate registry daily feed is the most-scraped list in the state, so weeks-old LLCs answer with AI screeners; keep that lane for text/Messenger or the cross-reference play, not cold calls.
Find businesses via jina/web/maps + the **verified state-data pipelines** in the doctrine (the state corporate registry daily filings + fictitious-name/DBA feed off the public SFTP; the state licensing board weekly licensee downloads; the state wildlife/marine licence registry charter licenses). Strongest signal: a real, reputable business with **no working website or a parked/for-sale domain** — and clear G1 by the permutation + fetch-and-read method (doctrine 2d), never from search results and never from an HTTP status. Score each candidate with the doctrine's 0-100 rubric (gates → factors A-G → modifiers → bands 75+/60-74/45-59). Require a findable owner channel (an FB page with recent posts) as a HARD GATE, not a scoring factor — the 2026-07-28 Tier 1 sweep produced 0 engagement from 10 calls largely on unreachable/unverifiable owners. Gather per candidate: name, owner, contact channels, current web presence (or lack), score+band, and one specific honest hook.
</phase>

<phase name="2_present_and_pick">
## Phase 2 — Present + pick
Present candidates with **honest reasoning** (hook, reputation reality, fit,
ease) using the rubric in `references/scouting-doctrine.md`. Let the user pick one
or more (AskUserQuestion). No cheerleading — surface the weak ones as weak.
</phase>

<phase name="3_verify">
## Phase 3 — Verify facts (truth discipline)
Before building, verify each pick — license, ratings, affiliations, years,
entity identity — per `references/fact-verification.md` (the state corporate registry, the state licensing board, BBB,
manufacturer locators, Yelp/BuildZoom; watch the same-name entity trap). Mark
each claim **verified** or **aspirational**; aspirational claims may go on a
*demo* with the disclaimer, never presented as fact.
</phase>

<phase name="4_build">
## Phase 4 — Build (orchestrate site-forge)
Per picked business, write/update its ledger entry `ledger/active/<slug>.md`
(details, verified facts, hook, voice, assets — the entry doubles as the build
brief, so there's one file, not two). Then **invoke the `site-forge` skill in
`auto` mode**, pointing it at that file. site-forge owns the build — do not
duplicate its recipes here. If `site-forge` isn't installed, say so and offer to
install/locate it.
</phase>

<phase name="5_deploy">
## Phase 5 — Deploy (GATED) + disclaimer
**Do not deploy by default.** Builds stay local until the user asks, in the moment, for
a live URL. Once approved, site-forge deploys; confirm the live URL and that the demo carries the
not-affiliated disclaimer. Record the URL.
</phase>

<phase name="6_outreach">
## Phase 6 — Tailored outreach (drafts only)
Generate a copy-pastable outreach page with `scripts/outreach-page.sh` —
sequenced FB DM → email → text, cross-referenced, with timing + one follow-up —
per `references/outreach.md`. **Draft only; never send.** Pricing/positioning in
`references/monetization.md`.

**Commercial / B2B is out of scope for the default scout.** This skill targets B2C: a homeowner searches and calls. If the user asks about commercial work (HOA and property management, GCs, facility managers, municipal bids), none of the B2C stack applies and it is a list problem rather than a search problem. Read `references/commercial-b2b.md` before answering.

**Paid ads / conversion tracking is also out of scope for the default offer, and there is an objective reason to decline it.** If the user asks about Facebook/Google ads, CAPI, pixels, closed-won attribution, cost-per-lead, or a prospect probes them on it, read `references/paid-ads-and-attribution.md` first. Short version: the current stack is organic (GBP + local SEO + reviews), the honest answer to "are you feeding closed-won back via CAPI" is **"neither, I don't run paid acquisition"**, and ad platforms need roughly **50 conversions/week** to optimize at all — which a trade doing 30 jobs a month will never reach. Never bluff competence on paid acquisition; it collapses in two follow-up questions.
</phase>

<phase name="7_ledger">
## Phase 7 — Ledger update
Append/update the entry per `references/docs-ledger.md`: status, URL, verified
facts, outreach drafted, decisions, $. Apply the rolling-window bound (recent
entries full; older compacted to one-liners in `ledger/archive.md`).
</phase>

</process>

<saved_rules_format>
Accumulate learnings in `ledger/lessons.md` (durable). Format:
`- {topic}: {rule} — set {YYYY-MM-DD ET}`
e.g. "channel: FB DM first for solo trades", "verify: same-name LLC trap is
common", "skip: businesses with a current modern site". Surface relevant rules
at the start of a run.
</saved_rules_format>

## Bounded ledger (never grows forever)
- `ledger/index.md` (@-loaded): one line per business — slug · status · URL ·
  last-touched. Pruned to the most recent ~30; older roll to `archive.md`.
- `ledger/active/<slug>.md` — full entry while in-flight.
- `ledger/archive.md` — one-liners for closed/cold businesses.
- `ledger/lessons.md` — saved rules.
Format + rollover rule: `references/docs-ledger.md`.

<recovery_protocol>
Interrupted mid-scout → resume from candidates in `ledger/active/`. Mid-build →
check whether the site-forge run produced a deploy; resume from Phase 5.
Mid-outreach → the drafts page is idempotent; regenerate. Never re-send (drafts
only, nothing to double-send).
</recovery_protocol>

<error_handling>
- `site-forge` not installed → surface; offer to install/locate. Never inline its
  build logic.
- Fact sources blocked/empty → fall back to a researcher agent; an unverifiable
  claim stays aspirational, never asserted.
- Same-name entity ambiguity → stop and confirm identity before building.
- Ledger index > ~30 entries → roll oldest to `archive.md` (one-liners).
</error_handling>

<success_criteria>
- [ ] Candidates presented with honest, evidence-based reasoning.
- [ ] User explicitly picked which to pursue.
- [ ] Facts verified or labeled aspirational; demo carries the disclaimer.
- [ ] Site built via site-forge (not re-implemented here) and deployed.
- [ ] Outreach drafted (never sent), sequenced + cross-referenced.
- [ ] Ledger updated; index bounded; lessons captured.
</success_criteria>
