# Competitor / Live-Web-Product / Data-Product Teardown Playbook

> Loaded by `/explain` when the subject is a LIVE web product, a competitor, a data product, an
> algorithm/calculator, or a whole competitive landscape. This is the "full shebang" mode:
> Workflow-orchestrated, browser-grounded, reverse-engineered-to-runnable-code, evidence-based.
> Battle-tested on large multi-competitor teardowns. Scale every knob to the ask.

## When this mode fires
- A live URL that is a PRODUCT/app/SaaS/tool (not just docs) — esp. framed as "competitor", "rival", "vs us", "teardown", "how do they do X".
- A calculator / estimator / predictor / pricing engine / ranking algorithm to reverse-engineer.
- "Find all the others / the whole landscape / everyone in this space."
- A data product (who has the data, where from, how fresh, how to replicate).

## Non-negotiable scope boundary (read first, every run)
Competitive recon is legal and normal — on PUBLIC surfaces only.
- **ALLOWED**: fetch public pages/assets; read public OpenAPI/Swagger/`/docs`; read & parse public JS bundles; a MODEST, POLITE grid (~15-40 total, low rate, no tight loops) of normal user-level requests to public estimator/search/data endpoints to derive a formula; fingerprint via response headers; WHOIS/DNS; app-store/press research.
- **FORBIDDEN** (refuse, and tell the user why): defeating CAPTCHA / Cloudflare / bot-challenges; bypassing auth; bulk-harvesting/exfiltrating whole datasets (sample only to learn schema); stress/load testing; invoking admin/mutating/destructive endpoints (`reset`, `clear-cache`, `block-ip`, `scraper/run`) — DOCUMENT their existence as a finding, never call them; anything illegal.
- Observe exposures; never exploit them. Report them as findings ("observed passively, not invoked").
- If a site is bot-defended and won't render, document what IS reachable (curl DOM, bundle, search) and flag the gap — do not bypass.

## The flow (scout → confirm → deep → synthesize)

### 0. Ground in prior work
Check memory + `~/.claude/explanations/` for any prior analysis of this subject. Don't re-derive what's known; extend it and correct it.

### 1. Scout pass (cheap, fast) — before committing to the deep dive
One light passive-recon agent per target (WebFetch + WebSearch + headers). Goal: confirm what each thing actually IS, its stack/status, and what will need a real browser. Surface surprises. This grounds the plan in reality instead of assumptions.

### 2. Confirm gate
Present the grounded snapshot + the proposed deep-dive scope + the scope boundary. Use `AskUserQuestion` to confirm: go/trim/redirect, recon depth (passive vs deeper user-level probing — get explicit authorization for anything beyond passive), and browser use (real Chrome vs headless). **Do not start the expensive phase until confirmed** — unless the user already said "full shebang / go deep / everything."

### 3. Deep recon — Workflow-orchestrated, one structured agent per subject
Use the **Workflow tool** (not loose Task calls) for anything past ~3 subjects or multi-phase work: `pipeline()` by default, `parallel()` only when you need all results together, structured-output `schema` per agent so outputs are consistent and mineable, and **resume** (`resumeFromRunId`) if a run dies or hits a limit. Give every subject the SAME schema (below) so they slot into one comparison.

Per-subject teardown schema (adapt fields to the domain):
`url · name · summary · techStack (frontend+build, backend, hosting, CDN, analytics, fonts, libs, mobile, ad/monetization stack — with header evidence) · pages[] · apiCatalog[] (EXHAUSTIVE: method, url, params, responseShape, auth, notes — from OpenAPI/bundle/observed) · estimator{name, inputs, exactFormula (every constant named), referenceImplementation (RUNNABLE TypeScript), observedExamples (live input→output grid), validation (how closely the impl matches; residuals), accuracyVsReality} · dataModel{sources, schemaFields, sizeAndCoverage, freshness, pipeline, staticVsLive} · security{authModel, reachableUnauth, protected, exposures (passive obs only), headersAndWaf} · seo{keywordTargets, contentInventory, aiCrawlerPosture, structuredData, trafficSignals} · monetization · replication{dataStep, backendStep, frontendStep, formulaStep, effort, hardParts, inYourStack} · noteworthy[] · browserGaps[]`

### 4. Browser recon (Claude-in-Chrome) — for what headless can't reach
Load the core tools in ONE `ToolSearch` call (`tabs_context_mcp,navigate,computer,read_page,read_network_requests,get_page_text,javascript_tool,find,form_input`). Then per target:
- `tabs_context_mcp` once; new tab per session (don't reuse).
- Capture the **on-load network sequence** (reload after the first `read_network_requests` call so tracking is active) → the exact `/api/*` calls each page fires + params.
- For SPAs (empty `<div id=root>` to curl): render, read the DOM, find globals (`window.__NEXT_DATA__`, `__TSR_ROUTER__`, baked `window.DASHBOARD_DATA`, etc.).
- **Live-probe the estimator**: drive the form (`form_input` + click) OR same-origin `fetch()` via `javascript_tool` (CORS-locked APIs are reachable from their own origin) across a small input grid → capture input→output pairs to pin the formula.
- Grab security headers (`curl -sD-` across all targets for an apples-to-apples table), paywall/auth/OAuth flow copy (read, don't submit your data), reCAPTCHA presence (don't solve), ad/analytics beacons.
- Persist captures to an artifacts file AS YOU GO (a browser session can't be re-run cheaply).
- Stay on the boundary: never solve a challenge, never submit the user's real data, never call a mutating endpoint.

### 5. Reverse-engineer to validated code (the crown jewel for any calculator)
For every formula/algorithm: derive the exact math with every constant → write a **runnable reference implementation** → **validate** it against the live input→output grid → state residuals/unknowns → benchmark against ground truth (the authoritative upstream, not the competitor's own claim). "Cracked & validated N/N" is the bar.

### 6. Namespace / landscape discovery (when asked "any others?")
DNS-resolve + curl (browser-UA) a candidate-domain list; run 8-12 web searches; App/Play store. Classify each: live/parked/dead/no-dns/off-topic-namesake, type, operator/cluster, and **worthFullTeardown** (a genuinely distinct live product) vs NO (SEO-junk/parked/duplicate). Find operator clusters (shared analytics IDs, AdSense pub, infra, co-registration). Flag unregistered defensive-buy domains. Then teardown only the YES set.

### 7. Ground-truth verification
For data products, verify against the AUTHORITATIVE upstream (gov site, primary API, source-of-truth doc) — browser-verify the defended ones (note clean vs gated vs bot-defended). Half of "data-driven" tools are stale or fabricate; checking source-of-truth is what separates a real teardown from repeating their marketing.

### 8. Synthesis
Fan out synthesis agents (each reads only its slice — see "big outputs" below): per-subject `DETAILED-<slug>.md`, plus cross-cutting `ESTIMATORS.md` (every calculator → code + validation), `COMPARISON.md` (master matrix + accuracy + security + data-integrity + threats/opportunities), `ARCHITECTURE.md` (ASCII per subject), `REPLICATION-BLUEPRINT.md` (build-it-in-OUR-stack), `NAMESPACE.md`, `SOURCES-*.md`, and `SUMMARY.md` (exec read + full file index). Always include a **data-integrity** section (who fabricates/extrapolates/ships stale) and an **operator-cluster + brand** section — these are the highest-value, least-obvious findings.

## Handling big outputs (context hygiene)
A Workflow result over ~25K tokens won't fully page into context. Split it to disk first (`node` one-liner: parse the result JSON, write one file per subject), then have synthesis agents read only the file they need. Read the full raw output yourself only when you specifically need the detail — it fits in a 1M window, it's just wasteful to carry every turn.

## Resilience
- Launch heavy research as a **background Workflow** so a session-limit cutoff can't lose it; resume with `resumeFromRunId` (cached agents return instantly, only the failed/edited step re-runs).
- Persist incrementally (browser captures, split files) so partial progress survives.
- If an agent dies on a stream/network error, re-run just that one (filter `.filter(Boolean)`), don't restart the batch.

## Output doc set (scale to the ask)
`SUMMARY.md` · `COMPARISON.md` · `ESTIMATORS.md` · `REPLICATION-BLUEPRINT.md` · `ARCHITECTURE.md` · `NAMESPACE.md` · `SOURCES-*.md` · `DETAILED-<slug>.md` (one per subject) · `artifacts/` (raw structured recon JSON, browser captures, source-verification). Display the exec summary + file index in the conversation; save everything to `~/.claude/explanations/<date>_<slug>/`.
