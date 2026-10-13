---
name: explain
description: >
  Comprehensive deep-dive explanation of GitHub repos, live websites/products, competitors,
  data products, algorithms/calculators, concepts, or any topic. Spawns parallel research +
  exploration agents, drives a real browser for live products, reverse-engineers calculators to
  runnable validated code, and saves a full doc set. Use when the user asks to "explain", "deep
  dive", "break down", "understand", "teardown", "reverse-engineer", "analyze a competitor",
  "how does X work / how do they do it", "compare us vs them", "what's the full landscape", "find
  all the others in this space", or to figure out a website/app/API/pricing/estimator/data
  pipeline — even if they don't say "explain".
when_to_use: >
  The user wants to deeply understand a repo, concept, OR (the heavy mode) tear down a live web
  product / competitor / data product / algorithm, map a competitive landscape, or reverse-engineer
  a calculator. Repos & concepts use the cheap path; live products escalate to browser + Workflow.
argument-hint: "[github-url | website | competitor | concept | landscape]"
---

<essential_principles>
## How This Skill Works

Two modes, auto-routed by subject (see routing table):
- **Mode A — Repo / concept / docs** (the cheap path): research → clone (if repo) → explore → synthesize → output. Loose parallel agents are fine.
- **Mode B — Live web product / competitor / data product / algorithm / landscape** (the full shebang): scout → confirm → Workflow-orchestrated deep recon → real-browser capture → reverse-engineer-to-validated-code → synthesize. Read `@references/competitor-teardown.md` and follow it.

### Subject-type routing
| Subject | Signal | Mode | Spine |
|---|---|---|---|
| GitHub repo | `github.com` | A | clone + Explore agents |
| Concept / tech | no URL | A | researcher agents |
| Docs / static site | URL, informational | A | researcher + WebFetch |
| **Live product / app / SaaS / competitor** | URL is a product; "competitor/teardown/vs us/how do they" | **B** | browser + Workflow + per-subject schema |
| **Calculator / estimator / predictor / pricing / ranking** | a formula/algorithm to crack | **B** | live-probe grid → runnable reference impl → validate |
| **Whole landscape** | "find all the others / everyone in this space" | **B** | namespace discovery → teardown the YES set |

**Tiebreaker**: if a URL is BOTH a product and has docs, default to **B** — the scout pass is cheap and downgrades to A if there's nothing to tear down.

### Execution Rules
1. **Right tool for scale**: Mode A = parallel Task/Agent calls. Mode B = the **Workflow tool** (pipelines, structured-output schemas, resume) once there are 3+ subjects or multi-phase work.
2. **Ground, then confirm**: Mode B does a cheap scout pass + a confirm gate (scope + recon boundary + browser) before the expensive dive — unless the user already said "full shebang / go deep / everything."
3. **Reverse-engineer to runnable, validated code** for any calculator/algorithm; benchmark vs the authoritative ground truth, not the competitor's own claim.
4. **Visual-heavy**: every major concept gets a diagram or table.
5. **Dual output**: display the exec read + file index in conversation; save the full doc set to `~/.claude/explanations/<date>_<slug>/`.
6. **Resilient**: heavy Mode-B research runs as a background Workflow; persist artifacts incrementally; resume (`resumeFromRunId`) on a cutoff.
7. **Clean up**: offer to delete cloned repos / saved files when done.
</essential_principles>

<scope_boundary>
## Mode B recon boundary (load-bearing — read before any live probing)
Competitive recon is legal and normal on PUBLIC surfaces. Full rules in `@references/competitor-teardown.md`. The invariants:
- ALLOWED: public pages/assets, public OpenAPI/`/docs`, public JS bundles, a MODEST polite grid (~15-40, low rate) of normal user-level requests to public endpoints to derive a formula, header fingerprinting, WHOIS/DNS.
- NEVER: defeat CAPTCHA / bot-challenges, bypass auth, bulk-harvest whole datasets (sample only), stress-test, or invoke admin/mutating/destructive endpoints (DOCUMENT them, don't call them). Observe exposures; never exploit them. Never submit the user's real data into a competitor's form. If unsure, don't — and say why.
</scope_boundary>

<intake_gate>

<no_context_handler>
IF $ARGUMENTS is empty:
→ Use AskUserQuestion:
  - header: "Explain"
  - question: "What would you like me to explain?"
  - options:
    - "GitHub repository" - Analyze a codebase from GitHub
    - "Website or documentation" - Understand a website, docs, or API
    - "Competitor / live product / landscape" - Tear down a live product, reverse-engineer a calculator, or map a whole competitive space (Mode B)
    - "Concept or technology" - Explain a concept, framework, or tool

Then proceed to context_analysis.
</no_context_handler>

<context_analysis>
Analyze $ARGUMENTS to extract:
- **Type**: GitHub repo, website, concept, or other
- **URL/Topic**: The specific thing to explain
- **Implicit goal**: Learn to use? Evaluate? Understand architecture? Contribute?

Detect type automatically:
- Contains `github.com` → GitHub repo (Mode A)
- Mode-B signals → "competitor", "teardown", "reverse-engineer", "vs us", "how do they", "find all the others", or a URL that is a product/app/calculator → Mode B
- Contains `http` (informational/docs) → Website (Mode A)
- Otherwise → Concept (Mode A)
</context_analysis>

<initial_questions>
Use AskUserQuestion for genuine gaps only (2-3 questions max):

**Goal** (if unclear):
- "What's your goal?" with options:
  - "Understand how it works" - Architecture, flow, implementation
  - "Evaluate for adoption" - Pros/cons, alternatives, fit for my use case
  - "Learn to use it" - Setup, API, getting started
  - "Learn to contribute" - Codebase structure, development workflow

**Focus** (if broad topic):
- "Any specific focus?" with options:
  - "Everything" - Full comprehensive analysis
  - "Architecture only" - High-level structure and patterns
  - "Specific feature" - One particular aspect (specify)

**Background** (if helpful):
- "Your technical level?" with options:
  - "Non-technical" - Explain from first principles with analogies
  - "Technical but new to this domain" - Skip basics, focus on specifics
  - "Expert" - Deep technical, assume knowledge
</initial_questions>

<decision_gate>
After answers, use AskUserQuestion (Mode A):
- question: "Ready to start the deep dive?"
- options:
  - "Yes, go" - Begin multi-phase analysis
  - "More questions first" - I have clarifications
  - "Let me add context" - I want to add details

**Mode B supersedes this gate with B2** (snapshot + scope + recon-boundary + go/depth/browser) — don't ask both; B2 is the single authoritative gate for teardowns.
</decision_gate>

</intake_gate>

<process>

## Mode select
Run `<intake_gate>`, then route by the subject-type table. **Mode B** (live product / competitor / data product / calculator / landscape) → load `@references/competitor-teardown.md` and follow its scout → confirm → deep → synthesize flow (skeleton below). **Mode A** (repo / concept / docs) → Phases 1-7 below.

## Mode B — Live product / competitor / data-product teardown
Full playbook in `references/competitor-teardown.md`. Skeleton:
- **B0 Ground**: check memory + `~/.claude/explanations/` for prior analysis; extend, don't redo.
- **B1 Scout**: one light passive-recon agent per target (WebFetch + headers + WebSearch) → grounded snapshot + what needs a browser.
- **B2 Confirm gate**: present snapshot + scope + the recon boundary (`<scope_boundary>`); `AskUserQuestion` for go/depth/browser — skip only if the user already said "go deep / full shebang".
- **B3 Deep recon (Workflow)**: one structured agent per subject, all sharing the per-subject schema (in the reference). `pipeline()` by default; split big outputs to disk.
- **B4 Browser (Claude-in-Chrome)**: capture on-load network, render SPAs, **live-probe estimators across an input grid**, security headers, paywall/auth copy — within the boundary (no CAPTCHA/auth bypass, no mutating endpoints, never submit the user's data). Persist captures as you go.
- **B5 Reverse-engineer**: every calculator → runnable TypeScript reference impl → validate vs the live grid → benchmark vs authoritative ground truth.
- **B6 Namespace** (if "any others?"): DNS+curl+search candidate domains, classify, find operator clusters, flag defensive-buy domains, teardown only the genuinely-distinct YES set.
- **B7 Synthesize**: fan-out synthesis agents → `DETAILED-<slug>.md` ×N + `ESTIMATORS.md` + `COMPARISON.md` (incl. a data-integrity + operator-cluster section) + `REPLICATION-BLUEPRINT.md` + `ARCHITECTURE.md` + `NAMESPACE.md` + `SOURCES-*.md` + `SUMMARY.md` (exec read + file index). Then Phase 7 output/cleanup.

---
## Mode A — Repo / concept / docs

## Phase 1: Parallel Web Research (5 research agents)

Spawn ALL in one message:
```
Task(subagent_type="general-purpose", prompt="Research [TOPIC]: What is it? Who made it? When? Why?")
Task(subagent_type="general-purpose", prompt="Research [TOPIC]: Technical stack, architecture, key technologies")
Task(subagent_type="general-purpose", prompt="Research [TOPIC]: Articles, reviews, community discussions, opinions")
Task(subagent_type="general-purpose", prompt="Research [TOPIC]: Alternatives, comparisons, when to use vs not")
Task(subagent_type="general-purpose", prompt="Research [TOPIC]: Documentation, tutorials, getting started guides")
```

## Phase 2: Clone Repository (if GitHub)

```bash
REPO_DIR=~/.claude/explanations/$(date +%Y%m%d_%H%M%S)_$(basename [URL] .git)
git clone [URL] $REPO_DIR
cd $REPO_DIR
```

## Phase 3: Parallel Codebase Exploration (6 explore agents)

Spawn ALL in one message with thoroughness="very thorough":
```
Task(subagent_type="Explore", prompt="Architecture: Overall structure, modules, how they relate")
Task(subagent_type="Explore", prompt="Entry points: Main files, CLI, API endpoints, how it starts")
Task(subagent_type="Explore", prompt="Core logic: Key algorithms, patterns, abstractions")
Task(subagent_type="Explore", prompt="Configuration: Settings, environment, extensibility points")
Task(subagent_type="Explore", prompt="Dependencies: Key packages, integrations, external services")
Task(subagent_type="Explore", prompt="Tests and quality: Test patterns, coverage, CI/CD")
```

## Phase 4: Parallel Claude Code Context (2-3 general-purpose agents)

If relevant to Claude/AI/agents:
```
Task(subagent_type="general-purpose", prompt="Explain relevant Claude Code concepts for understanding this")
Task(subagent_type="general-purpose", prompt="Compare to Claude tools/SDK if applicable")
```

## Phase 5: Mid-Point Check (if complex)

Use AskUserQuestion if findings reveal complexity:
- "I found [X]. Want me to focus on anything specific?"
- Options based on discoveries

## Phase 6: Synthesis

Combine all findings into comprehensive explanation with:

1. **Opening analogy** (non-technical comparison)
2. **What it is** (1-2 sentences)
3. **Architecture diagram** (ASCII)
4. **How it works** (step-by-step with diagrams)
5. **Key components table** (name, purpose, how it works)
6. **What's special** (differentiators)
7. **Capabilities list** (what it can do)
8. **Comparison table** (vs alternatives)
9. **Technical deep-dive** (implementation details)
10. **Gotchas and considerations**

## Phase 7: Output

### Display in conversation
Full formatted explanation with all visuals.

### Save to files
```bash
OUTPUT_DIR=~/.claude/explanations/$(date +%Y%m%d_%H%M%S)_[topic-slug]
mkdir -p $OUTPUT_DIR

# Save files:
# $OUTPUT_DIR/SUMMARY.md - Quick reference (30-second version)
# $OUTPUT_DIR/DETAILED.md - Full analysis
# $OUTPUT_DIR/ARCHITECTURE.md - All diagrams
# $OUTPUT_DIR/COMPARISON.md - Alternatives analysis
```

### Follow-up
After displaying, ask:
- "What aspect would you like to explore deeper?"
- "Any questions about what I explained?"
- Encourage follow-up

### Cleanup
Use AskUserQuestion for cleanup (combine if both apply):

**If cloned repo:**
- question: "Delete the cloned repository?"
- options:
  - "Yes, delete it" - Remove $REPO_DIR automatically
  - "No, keep it" - Show path: "Repo kept at: $REPO_DIR"

If yes: `rm -rf $REPO_DIR`
If no: Display path for manual access

**Always (explanation files):**
- question: "Delete the saved explanation files?"
- options:
  - "Yes, delete them" - Remove $OUTPUT_DIR automatically
  - "No, keep them" - Show path: "Explanations saved at: $OUTPUT_DIR"

If yes: `rm -rf $OUTPUT_DIR`
If no: Display path for manual access

**Combined question (if both repo and files):**
- question: "Analysis complete. What would you like to clean up?"
- options:
  - "Delete both repo and explanation files"
  - "Delete repo only, keep explanations"
  - "Delete explanations only, keep repo"
  - "Keep everything"

Execute deletions based on selection, display paths for anything kept.

</process>

<visual_formats>
## Standard Diagram Formats

**Architecture:**
```
┌─────────────┐     ┌─────────────┐
│  Component  │────►│  Component  │
└─────────────┘     └─────────────┘
```

**Flow:**
```
START → Step 1 → Step 2 → Decision?
                            ├─ Yes → Path A
                            └─ No  → Path B
```

**Comparison table:**
```
| Aspect      | Option A | Option B | Winner |
|-------------|----------|----------|--------|
| Speed       | Fast     | Slow     | A      |
```

**Component breakdown:**
```
┌──────────────────────────────────────┐
│           System Name                │
├──────────────────────────────────────┤
│ ┌────────┐ ┌────────┐ ┌────────┐    │
│ │Module A│ │Module B│ │Module C│    │
│ └───┬────┘ └───┬────┘ └───┬────┘    │
│     └──────────┴──────────┘         │
│              Shared Layer            │
└──────────────────────────────────────┘
```
</visual_formats>

<success_criteria>
Both modes:
- Asked clarifying questions / grounded before starting; routed to the correct mode
- Produced visual diagrams for every major concept; included recreatable technical depth
- Displayed exec read in conversation AND saved the doc set to files
- Offered follow-up + cleanup; honored the user's keep/delete choice

Mode B (live product / competitor / data product / landscape) also:
- Did a scout pass + confirm gate (or honored an explicit "go deep") and stated the recon boundary
- Stayed strictly within the boundary: no CAPTCHA/auth bypass, no bulk-harvest, no mutating/admin endpoints called, never submitted the user's data; exposures observed not exploited
- Used the Workflow tool with a shared per-subject schema once 3+ subjects/multi-phase; persisted artifacts; resilient to cutoffs (resume)
- Live-probed every calculator and shipped a runnable reference impl validated N/N against observed outputs, benchmarked vs authoritative ground truth
- For landscapes: discovered the full namespace, classified each, found operator clusters, flagged defensive-buy domains, tore down only the distinct ones
- Synthesis includes a data-integrity section + an operator-cluster/brand section + a build-it-in-our-stack blueprint
</success_criteria>
