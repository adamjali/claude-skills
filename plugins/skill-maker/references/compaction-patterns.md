# The 14 Compaction-with-Preservation Patterns

> **The hardest part of stateful skills**: keep recent N entries full, compact older into useful summaries, but PRESERVE THE IMPORTANT THINGS THROUGHOUT — never destroy decisions, rules, action items, or precedents.
>
> Source: real-world skills + research synthesis.

## Master Principle

**"Compaction is destructive on log entries, but never destructive on action items."**

Action items / pending decisions / rules-learned / precedents get extracted into SEPARATE dedicated files BEFORE the main log gets compacted. This means compaction is always reversible at the information level — you can lose specific dates and verbose timestamps, but you never lose the "what did we decide and why" residue.

---

## Pattern 1 — Rolling-window with Saved Rules

**Use when**: stateful skill with checkpoint resumption + accumulated rules. Most common pattern.

**Mechanism**:
- `## Saved Rules` section at top — durable, surfaced on every future run
- `## Current <Action>` block with `status: IN_PROGRESS` + `checkpoint: <STATE>`
- Last N (typically 5) full entries archived
- Older: dropped entirely OR compressed to one-line per Pattern 2

**Files**: a `sync-history.md` / activity log

**Code template**:
```bash
# Trim old syncs to keep last N
N=5
awk '/^## Sync #/{c++} c<=N{print}' sync-history.md > tmp && mv tmp sync-history.md

# Surface saved rules on next run
grep -A1 '^- ' SAVED_RULES_SECTION
```

## Pattern 2 — Last N full + N-line archive

**Use when**: trends matter (was last week's audit cleaner?) but per-decision detail is gone.

**Mechanism**:
- `## Saved Policies` (durable)
- Last 3 full entries
- `## Archived Summaries` section with one-line entries: `[date]: health X→Y%, fixed N items, merged N PRs`
- Target: file under 200 lines

**Files**: `.planning/github-audit-history.md`

**Compaction is LLM-driven** (extracts key metrics into one-liner) + deterministic trim.

## Pattern 3 — Simple rolling-window (no saved rules)

**Use when**: read-only history, not a resumable workflow.

**Mechanism**:
- Last 5 full entries
- Older: one-line archive at bottom

**Files**: `~/.claude/skills/perm-email/history.md`

**Simpler than Pattern 1** — no checkpoints, no saved rules. Just rolling.

## Pattern 4 — Two-tier compact-into-other-file

**Use when**: log + summary are both useful at different scales.

**Mechanism**:
- Live log file (`recent_log.md`) — full detail of last 7 days
- When > 3000 words → LLM summarizes oldest half into `summary.md`, deletes from `recent_log.md`
- `summary.md` keeps thematic compact view of older runs
- When `summary.md` > 10000 words → LLM compacts again (themes only, drop specifics)
- Three tiers: recent (full) → mid-term (one-line per run) → long-term (themes only)

**Files**: e.g. `memory/recent_log.md` + `summary.md`

**Critical**: action items / pending rules / flagged senders get extracted to dedicated files BEFORE this compaction (`pending_rules.md`, `flagged.md`, `pending_actions.md`). Compaction is destructive on log entries, never on action items.

## Pattern 5 — Identity-based preservation (1 per unique entity)

**Use when**: long-tail decisions matter (sender precedents, firm decisions, etc.).

**Mechanism**:
- Append-only log of `<entity> | <decision> | <why> | <timestamp>` per event
- When file > 200 entries → keep last 200 + 1 entry per unique entity (so every-known-entity always has a prior)
- Pure last-N would lose decisions about entities that haven't appeared in a while → re-decide from scratch when they reappear → drift

**Files**: e.g. `memory/precedents.md`

**Pure deterministic pruning** (dedupe by entity), no LLM needed.

## Pattern 6 — TTL-based hard delete (no compaction)

**Use when**: idempotency markers / pure technical IDs with no decision content.

**Mechanism**:
- Format: `<id> <YYYY-MM-DD>` per line
- On every run: drop entries with date > N days ago (typically 30)

**Files**: e.g. `memory/processed_ids.md`

**Why hard-delete instead of compact**: no decision content to preserve. If an ID hasn't been seen in N days, safe to forget.

## Pattern 7 — TTL with grace period

**Use when**: pending decisions awaiting human approval — shouldn't pile up forever, but need a window.

**Mechanism**:
- Each entry has a status field
- Auto-drop entries with status `pending` and age > 30 days
- User can promote (approve) or demote (reject) via Gmail label or feedback file
- 30-day TTL = same as Trash (consistent with reversibility window)

**Files**: e.g. `memory/pending_rules.md`

## Pattern 8 — NEVER auto-prune

**Use when**: the file's purpose IS preservation. Auto-pruning defeats it.

**Mechanism**:
- Append-only forever
- User manually prunes when they review
- Header explicitly says "DO NOT auto-prune — entries can be deleted by hand"

**Files**: e.g. `memory/pending_actions.md`

**Why**: extracted-from-deleted-drafts content. Auto-pruning would re-introduce the original "info loss" problem. Trade file growth for guaranteed preservation.

## Pattern 9 — Atomic per-event dirs (git history is the archive)

**Use when**: multi-phase, multi-agent, or multi-artifact work where merge conflicts would be a problem.

**Mechanism**:
- Each event/feature/work-item gets its own directory: `.planning/<category>/NNN-slug/`
- Multiple named artifact files inside (EXPLORATION.md, CLARIFICATIONS.md, ARCHITECTURE.md, PLAN.md, SUMMARY.md, REVIEW.md)
- Once event is done, dir is immutable (committed to git)
- Compaction happens at INDEX level only — `STATE.md` references the dir, no full content
- Old dirs stay in git history forever

**Files**: `gsd-feature` per-feature directories, `gsd-debug` resolved subfolders

**Why this beats appending-to-one-big-file**: avoids merge conflicts when multiple events overlap, each artifact has single owner, file system IS the index.

## Pattern 10 — Move-on-status

**Use when**: items have a binary status (done / not done) and you want to query by listing.

**Mechanism**:
- Pending: `<dir>/pending/<slug>.md`
- Done: `<dir>/done/<slug>.md`
- Move file (don't delete) when status changes
- No compaction — git history preserves everything

**Files**: `~/.claude/skills/gsd-add-todo/`, `~/.claude/skills/gsd-debug/`

**Why this works**: file system IS the index. `ls pending/ | wc -l` is the count. Trades file count for query simplicity.

## Pattern 11 — Per-event dir + completed/ subfolder + SUMMARY.md

**Use when**: long outputs, but the "shape" of decisions made is the long-term value.

**Mechanism**:
- Each event: `<dir>/{NNN}-{topic}-{purpose}/`
- After execution: full output stays in parent, prompt file moves to `completed/`, SUMMARY.md created
- Re-run support: move prompt back from `completed/` to parent
- SUMMARY.md is the long-term durable artifact (one-liner, version, key findings, files created, decisions, blockers, next step)

**Files**: `~/.claude/skills/create-meta-prompts/`

## Pattern 12 — Auto-memory MEMORY.md index + linked typed files

**Use when**: cross-session memory at the project level.

**Mechanism**:
- `MEMORY.md` is one-line-per-entry index (`- [Title](file.md) — one-line hook`)
- Each linked file is its own typed memory (`type: user | feedback | project | reference`)
- First 200 lines / 25KB of MEMORY.md auto-loads every session
- Topic files load on demand
- Pruning: outdated memories deleted/updated when discovered (LLM-driven, no schedule)
- "Stale memory" warning auto-prefixed when files read (system-reminder: "This memory is N days old")

**Files**: `~/.claude/projects/<encoded-cwd>/memory/MEMORY.md` per Anthropic's auto-memory spec

## Pattern 13 — Framework-level sync-history (Pattern 1 + Secondary Sources)

**Use when**: building a framework or fork that periodically pulls from upstream.

**Mechanism**:
- Pattern 1 base (Saved Rules + last 5 syncs)
- ADDITIONAL `## Secondary Sources` section — durable comparison state for each upstream source: `last_checked`, `last_version`, `items_taken`, `items_left`
- Each sync touches Secondary Sources to update the comparison

**Files**: e.g. a repo `sync-history.md`

## Pattern 14 — Single-use file (clear after read)

**Use when**: user → agent communication channel; ephemeral by design.

**Mechanism**:
- Header explains "you edit this, agent clears it"
- On read: agent parses + executes + writes outcome to recent_log.md + clears file back to scaffold
- No history retained; the consumed action is the only artifact

**Files**: e.g. `memory/feedback_inbox.md`

---

## Picker (which to use when)

| Need | Pattern |
|---|---|
| Resumable workflow + accumulated rules | Pattern 1 |
| Trends matter but per-decision detail can compact | Pattern 2 |
| Read-only history, no resume | Pattern 3 |
| Detailed log + thematic mid-term + long-term themes | Pattern 4 |
| Long-tail entity decisions (senders, firms, etc.) | Pattern 5 |
| Pure technical IDs (idempotency, processed-markers) | Pattern 6 |
| Pending decisions awaiting approval | Pattern 7 |
| Action items / extracted-from-deleted content | Pattern 8 |
| Multi-phase / multi-agent / multi-artifact work | Pattern 9 |
| Binary status items (done / not done) | Pattern 10 |
| Long outputs with summary as long-term artifact | Pattern 11 |
| Cross-session project memory | Pattern 12 |
| Framework forks pulling from upstream | Pattern 13 |
| User→agent channel (ephemeral) | Pattern 14 |

## Cross-pattern principles

1. **ALWAYS extract action items first**. Compaction is destructive on logs but never on action items. Add a Phase 5.5 (or similar) that extracts pending decisions, flagged items, rules-learned to dedicated files BEFORE main log compaction.

2. **Importance flags via emoji** survive compaction better than text labels. Use 🔴 (critical) / ⚓ (permanent) / 📎 (reference) prefixes.

3. **Compaction logs**: append-only audit trail of what was compacted (e.g., `compaction-audit.md`) so the user can verify nothing critical was lost.

4. **State machine for IN_PROGRESS**: named checkpoints (INITIALIZED, FETCHED, ANALYZED, REVIEWING, COMPLETED) so resume is unambiguous.

5. **TTL aligned with reversibility window**: 30 days = same as Gmail Trash. Consistent mental model.

6. **Atomic per-event dirs > append-to-one-big-file** when multi-actor.

7. **File-system as index** beats separate index files when query is `ls`.

8. **Stale-memory warnings** when memory files load — system-reminder prefix that nudges LLM to verify before relying.

9. **Plain markdown beats JSON/YAML** for state — diffable in git, readable by humans, parseable by LLM.

10. **Header docs in state files** — every state file should have a header explaining its format + retention policy + when to update.
