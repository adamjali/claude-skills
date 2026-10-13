# History file format — `.planning/github-audit-history.md`

Repo-local file (run the skill from the repo root). It persists Saved Policies and the
last 3 full audits so runs stay consistent. Loaded in Phase 0, written in Phase 5.

## Structure

```markdown
# GitHub Audit History

## Saved Policies
<!-- Persistent rules applied automatically on future audits. -->
<!-- Format: - **[pattern/item]**: [action] — [reason] -->

## Current Audit
<!-- Only present during an IN_PROGRESS run; remove on completion. -->
- **started:** [ISO timestamp]
- **status:** IN_PROGRESS
- **checkpoint:** [phase + completed sub-steps, e.g. "phase 2 — PRs #41/#42 closed, #43 pending"]

## Audit N — [YYYY-MM-DD]
- **health_before:** [score / summary]
- **health_after:** [score / summary]
- **items_fixed:** [n]
- **items_discussed:** [n]
- **prs_merged:** [n] (and any closed-as-superseded)
- **quality_issues_fixed:** [n]
- **deployed:** yes/no (commit, backend deploy?, hosting status)
- **duration:** [time]

### Changes Made
- [item]: [what was done]

### Decisions
- [item]: [decision] — [reason]

## Archived Summaries
- [date]: health [X]→[Y]%, fixed [n], merged/closed [n] PRs
```

## Rules
- **Always preserve** the `Saved Policies` section verbatim (append new ones; never drop).
- Keep the **last 3 full `Audit N` entries**. Compress older ones to a one-line `Archived Summaries` bullet, then delete the full entry.
- Target the whole file **< 200 lines**.
- `checkpoint` must capture **sub-step granularity** so a resumed run never re-merges a PR or re-deploys.
- On completion, delete the `Current Audit` (IN_PROGRESS) block.

## Saved-policy seeds (carry forward; confirm before applying)
- **Dependabot grouped PRs:** bulk dependency update via the project's package manager + overrides for transitive CVEs → audit clean → close grouped PRs as superseded.
- **`update --latest`:** never blind — it bumps majors. Prefer a caret-safe `update` + manual major review.
- **Backend deploy:** only when the relevant backend/infra path changed (frontend-only audits skip it).
- **Deploy gating:** Phase 4 always requires explicit confirmation; honor any "always/never deploy" policy the user sets.
