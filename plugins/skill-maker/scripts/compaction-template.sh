#!/bin/bash
# compaction-template.sh — emits the self-prune section for a chosen compaction pattern.
#
# Usage: bash compaction-template.sh <pattern-number>
# Pattern numbers 1-14 per references/compaction-patterns.md
#
# Output goes to stdout — pipe into the SKILL.md being generated.

PATTERN=$1
[ -z "$PATTERN" ] && { echo "Usage: $0 <pattern-number 1-14>"; exit 1; }

case "$PATTERN" in
  1)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 1: Rolling-window + Saved Rules)

- ## Saved Rules section at top — durable, never auto-pruned
- ## Current <Action> block with status: IN_PROGRESS
- Last 5 full entries archived
- Older: dropped entirely (full delete after 5)

```bash
# Trim to last 5 entries
N=5
awk '/^## <Entry-Marker>/{c++} c<=N{print}' state.md > tmp && mv tmp state.md
```
EOF
    ;;
  2)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 2: Last N + N-line archive)

- ## Saved Policies section (durable, never pruned)
- ## Current <Action> block (IN_PROGRESS)
- Last 3 full entries
- ## Archived Summaries section: one-line per older entry ("date: key metric Δ")
- Target: file under 200 lines
EOF
    ;;
  3)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 3: Simple rolling-window)

- Last 5 full entries
- Older: one-line archive at bottom
EOF
    ;;
  4)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 4: Two-tier compact-into-other-file)

- Live log: recent_log.md (full detail of last 7 days)
- When > 3000 words → LLM summarizes oldest half into summary.md, deletes from recent_log.md
- summary.md > 10000 words → compact again (themes only)

CRITICAL: action items / pending rules / flagged senders extracted to dedicated files BEFORE compaction.
EOF
    ;;
  5)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 5: Identity-based preservation)

- Append-only log of <entity> | <decision> | <why> | <timestamp>
- When > 200 entries → keep last 200 + 1 entry per unique entity
- Pure deterministic pruning (dedupe by entity)
EOF
    ;;
  6)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 6: TTL-based hard delete)

- On every run: drop entries with date > 30 days ago
- No content preservation; pure idempotency markers
EOF
    ;;
  7)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 7: TTL with grace period)

- Each entry has status: pending / approved / rejected
- Auto-drop entries with status pending and age > 30 days
- 30-day TTL aligned with reversibility window
EOF
    ;;
  8)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 8: NEVER auto-prune)

- Append-only forever
- User manually prunes when reviewing
- Header explicitly: "DO NOT auto-prune — entries can be deleted by hand"
EOF
    ;;
  9)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 9: Atomic per-event dirs)

- Each event/feature gets own dir: .planning/<category>/NNN-slug/
- Multiple named artifacts per dir
- Once done, dir is immutable (committed to git)
- Compaction at INDEX level only (STATE.md row references the dir)
- Old dirs stay in git history forever
EOF
    ;;
  10)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 10: Move-on-status)

- Pending items: <dir>/pending/<slug>.md
- Done items: <dir>/done/<slug>.md
- Move file (don't delete) when status changes
- No compaction; git history preserves everything
EOF
    ;;
  11)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 11: Per-event + completed/ + SUMMARY.md)

- Each event: <dir>/{NNN}-{topic}-{purpose}/
- After execution: prompt file moves to completed/, output stays in parent, SUMMARY.md created
- Re-run support: move from completed/ back to parent
- SUMMARY.md is the long-term durable artifact
EOF
    ;;
  12)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 12: Auto-memory MEMORY.md index)

- MEMORY.md is one-line-per-entry index
- Each entry: - [Title](file.md) — one-line hook
- Each linked file is its own typed memory (type: user|feedback|project|reference)
- Lines after 200 truncated by loader
- Pruning: outdated memories deleted/updated when discovered (LLM-driven)
EOF
    ;;
  13)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 13: Framework-level + Secondary Sources)

- Pattern 1 base (Saved Rules + last 5 syncs)
- ADDITIONAL ## Secondary Sources section — comparison state per upstream:
  last_checked, last_version, items_taken, items_left
EOF
    ;;
  14)
    cat <<'EOF'
## Self-Prune (Compaction Pattern 14: Single-use clear after read)

- Header: "you edit this, agent clears it"
- On read: agent parses + executes + writes outcome to recent_log.md + clears file back to scaffold
- No history; the consumed action is the only artifact
EOF
    ;;
  *)
    echo "Unknown pattern: $PATTERN"
    echo "Valid: 1-14 per references/compaction-patterns.md"
    exit 1
    ;;
esac
