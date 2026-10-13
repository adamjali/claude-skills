---
name: github-audit
description: Audit GitHub repo health, auto-fix safe issues, run quality gates, deploy, and record decisions across runs. Use when asked to audit a repo, check repo/CI/dependency health, run pre-deploy quality checks, or ship after an audit.
argument-hint: "[audit-only | fix | deploy]"
disable-model-invocation: true
allowed-tools: >
  Read Edit Write Glob Grep WebSearch WebFetch Task AskUserQuestion
  TaskCreate TaskUpdate TaskList
  Bash(gh:*)
  Bash(git status:*) Bash(git add:*) Bash(git commit:*) Bash(git diff:*)
  Bash(git log:*) Bash(git branch:*) Bash(git remote:*) Bash(git fetch:*)
  Bash(git stash:*) Bash(git checkout:*) Bash(git pull:*)
  Bash(npm:*) Bash(pnpm:*) Bash(yarn:*) Bash(npx:*) Bash(node:*)
---

# GitHub Audit

Comprehensive GitHub repo audit → auto-fix → quality gate → (confirmed) deploy → record.
Tracks decisions in `.planning/github-audit-history.md` for cross-run consistency.

> `allowed-tools` above PRE-APPROVES safe/common tools (it does NOT restrict — every
> tool stays callable). `git push`, `gh pr merge`, and any deploy command are
> deliberately NOT pre-approved, and Phase 4 is gated by an explicit confirmation.

## Run mode (from `$ARGUMENTS`)

`$0` selects scope (default = full):
- **`audit-only`** → Phases 0, 1, 5 only. Report findings; make NO changes, NO deploy.
- **`fix`** → Phases 0–3 + 5. Fix + quality gate; STOP before deploy.
- **`deploy`** or empty → all phases (Phase 4 still requires the confirmation gate).

## Execution rules
- Auto-fix only safe/small items that match a Saved Policy; otherwise STOP and discuss via `AskUserQuestion`.
- Quality gate: zero tolerance — fix ALL errors/warnings/failures (a known flaky test must pass in isolation to count as green).
- Deploy: sequential gates; each step must succeed before the next; **never** without the Phase 4 confirmation.
- Prefer a platform MCP/API over scraping CLI output when one is available (e.g. a hosting or backend MCP for deployment/env status).

---

## Phase 0 — Initialize
1. Read `.planning/github-audit-history.md` (Saved Policies + last audits). If it has an `IN_PROGRESS` block, ask the user to **resume** or **start fresh**.
2. `git remote -v`, `git branch --show-current`. Derive `owner/repo`.
3. Detect the project's toolchain (package manager + scripts) from `package.json`, lockfiles, `Makefile`, or the CI config — don't assume one. Note the run mode. Record an `IN_PROGRESS` entry (timestamp + phase) in the history file.

## Phase 1 — Audit (read-only; run checks in parallel)
- **Security:** `gh api repos/{o}/{r}/dependabot/alerts` (open, by severity + package), `.../code-scanning/alerts`, `.../secret-scanning/alerts`.
- **CI/CD:** `gh api .../actions/workflows` + recent `gh run list`; read each workflow YAML for stale matrices, missing perms, unpinned actions, broken auth secrets.
- **Branch protection:** `gh api .../branches/{default}/protection` — required checks, strict, enforce_admins, force-push/deletions, reviews.
- **PRs:** `gh pr list --state open` — categorize Dependabot (dev/patch = low, prod/major = high) vs human/bot.
- **Community:** `gh api .../community/profile` + presence of SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, templates, README, LICENSE.
- **Traffic/activity:** views/clones (flag anomalies), stars/forks, open issues.
- **Config hygiene:** `dependabot.yml` ignore rules vs actual deps; linter ignore files; stale CI references.

Compute **health score** (rubric below) and a severity-tagged findings list (auto-fix / discuss / info).

### Health rubric (start at 100, floor 0)
- secret-scanning alert: −20 each · critical dep alert: −15 · high: −8 · moderate: −3 · low: −1
- failing required CI on default branch: −15 · no branch protection: −10 · no required checks: −5 · missing SECURITY.md: −5
- community profile <100%: −(100−profile)/5 · open Dependabot PR >30d old: −2 each
Record `health_before`; recompute `health_after` post-fix.

## Phase 2 — Fix  *(skip if mode = audit-only)*
- **Auto-fix** items matching a Saved Policy (community files, stale workflow config, stale ignore rules). Log each.
- **Dependabot (Saved Policy seed):** prefer a **bulk dependency update** via the project's package manager (`npm update` / `pnpm update` / `yarn upgrade` — caret-safe) plus overrides for stubborn transitive CVEs, then run the audit (`npm audit` / `pnpm audit` / `yarn npm audit`) until clean; **close the grouped Dependabot PRs as superseded** rather than rebase-merging each. Confirm new policies with the user and save them.
- **Discuss** (via `AskUserQuestion`) anything medium/breaking: production major bumps, permission/branch-protection changes, anything that could break the build. Offer to save each decision as a policy.

## Phase 3 — Quality gate  *(skip if mode = audit-only)*
Run the project's quality scripts (detect them from `package.json` scripts / `Makefile` / CI), then fix and loop until clean. Typical order:
1. typecheck  2. test  3. build  *(e.g. `npm run typecheck && npm test && npm run build`, adapting to the detected commands)*
- A failing test that's a known parallel-flake: re-run it in isolation; an isolated pass counts as green.
- Never suppress warnings — fix them. Stuck after 3 attempts → stop and ask.

## Phase 4 — Deploy  *(only if mode = deploy/empty; otherwise STOP and report)*
**CONFIRMATION GATE (mandatory):** before any push/deploy, present an `AskUserQuestion` summarizing exactly: files to commit, the commit message, whether it pushes to the default branch, and whether a deploy will run. Proceed only on explicit approval (honor any "always deploy"/"never auto-deploy" Saved Policy).

Then, sequentially (stop on any failure):
1. **Commit** — stage only audit-changed files: `git add <files>` → `git commit`. Skip if nothing changed.
2. **Push** — `git push origin <branch>`; verify with `git status`.
3. **Backend/migration deploy — CONDITIONAL:** only if the change touches backend/infra that needs a separate deploy step (a backend service, DB migrations, etc.). Otherwise skip (frontend-only changes usually don't need it). Run the project's documented deploy command.
4. **Verify the hosting deploy** — if the repo auto-deploys on push (e.g. a connected hosting provider), confirm the deployment reached a ready/healthy state via the platform's MCP, CLI, or dashboard. Report the final URL + status.

## Phase 5 — Record & prune
Append an `Audit N` entry and prune to the **last 3 full audits** (preserve Saved Policies; compress older to one-line summaries). Full template + rules: see [reference/history-format.md](reference/history-format.md).

Then report: health before→after, what was fixed, deploy status, deferred items.

---

## Error handling
| Situation | Action |
|---|---|
| GitHub API fails | `gh auth status`; retry once; then report |
| Quality gate loops >3× | Stop; show what's failing; ask |
| Deploy step fails | Stop immediately; do NOT proceed; report |
| Resumed run (IN_PROGRESS) | Re-read checkpoint sub-steps; **guard against double commit/push/deploy** (verify the commit isn't already pushed) before re-running Phase 4 |
| History file missing/corrupted | Back up; create fresh structure; warn |
| No remote | Help add one or skip remote-dependent checks |
