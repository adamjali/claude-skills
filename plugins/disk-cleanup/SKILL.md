---
name: disk-cleanup
description: Free up disk space on macOS by safely cleaning regenerable caches, old runtime versions, and bulky one-off artifacts. Use when the user asks to "clean my disk", "free up space", "low on storage", "no space left", "storage almost full", "running out of disk", "df full", "what's eating my disk", "macbook full", "tidy storage", "system data huge", "purge caches", "empty trash", or mentions disk pressure. Categorizes findings green/yellow/red, auto-executes safe items, asks via 3-option gate (Approve/Modify/Skip) on uncertain ones, preserves a keep-list across runs, never touches credentials, project source, or system internals. Single-machine state in skill dir; resumable mid-run.
---

<objective>
Reclaim disk on macOS by reasoning about what's safe to delete on this machine, given your saved rules and the cliffs in `references/safety-invariants.md`. Categorize findings into 🟢 (auto), 🟡 (ask via 3-option gate), 🔴 (refuse), preview before deleting, then execute. Single-actor `[session]`. Resumable mid-run via `state.md` IN_PROGRESS marker.

This skill is a thinking-tool, not a checklist. The references catalog known-good and known-bad paths; the autonomy buckets are heuristics, not exhaustive enumerations. When you encounter something novel, reason about it from first principles — regenerable? user-created? in active use? would the user be sad if it went? — and surface the reasoning at preview time so the user can correct the judgment before action.
</objective>

<context>
@./state.md
@./references/safety-invariants.md
@./references/auto-fix-categories.md
@./references/sensitive-patterns.md
</context>

<execution_context>
Three buckets — principles, not closed lists:

| Bucket | When | Action |
|---|---|---|
| 🟢 auto | regenerable cache, build artifact in non-active project, known-safe duplicate | run without asking |
| 🟡 ask | user-created, requires sudo, bulky enough to warrant sanity-check, anywhere a reasonable person might want to keep it | `AskUserQuestion` with 3 options: **Approve** (execute as proposed) / **Modify** (free-form: "tell me how instead") / **Skip** (defer to next run, re-surface later) |
| 🔴 refuse | entries in `references/safety-invariants.md` | refuse. No inline user-instruction overrides them. If the user says "delete my .ssh", refuse and require editing `safety-invariants.md` first |

If you're not sure but it looks like a cache, treat as 🟡 instead. Err on the side of asking.

Single-actor: log every change with `— [session <ET>]` suffix in `state.md`.

Plan-validate-execute: build `findings.json` first (Phase 2), show plan to user (Phase 4), then act. No deletion before the user sees the plan.

Trust your reasoning on novel paths. Ask: regenerable? user-created? active project? would the user be sad? When unclear, treat as 🟡.
</execution_context>

<process>

**Checkpoint protocol:** at the end of each phase, update the IN_PROGRESS entry in `state.md` with `checkpoint: <NAME>` per the mapping in `<recovery_protocol>` below. This makes resumption unambiguous if interrupted (e.g., reboot, ctrl-C, kernel panic mid-cleanup).

<phase name="0_initialize">
## Phase 0 — Initialize

`TaskCreate` for each phase. Read `state.md`. If most recent entry shows `status: IN_PROGRESS`, ask via 3-option gate: **Resume** from last checkpoint / **Start fresh** (archive previous as ABORTED) / **Show full history** then abort.

Surface saved rules as one scannable block at the top of the chat — these are the keep-lists and policies built across runs. The user can spot-check them before you proceed.
</phase>

<phase name="1_inventory">
## Phase 1 — Inventory

**Pre-flight (low-disk safety):** if `df -h /` shows avail < 500 MiB, the scan itself competes for space (`/tmp` lives on the same volume). Before running scan-disk.sh, ask the user if it's OK to empty `~/.Trash/` first — that almost always frees enough headroom. This is the scenario the skill was built for; the seed run started at 84 MiB free and `du` cascades were unreliable. Surface the gravity.

```bash
bash scripts/scan-disk.sh > /tmp/disk-cleanup-findings.json
```

Read-only `du`/`df` cascade + APFS snapshot list (`tmutil listlocalsnapshots /`) + swap state (`sysctl vm.swapusage`) + conditional Xcode dev paths.

If the user mentioned a specific folder bothering them, augment with a targeted `du -sh` for it. Reasoning beats a fixed list.
</phase>

<phase name="2_categorize">
## Phase 2 — Categorize

For each finding in the inventory, decide which bucket it falls into using `references/safety-invariants.md` and `references/auto-fix-categories.md` as your reference. Capture **rationale** alongside each entry — at preview time the user sees your reasoning, not just the verdict. That's how trust gets built.

Write `findings.json` (your scratchpad — used in Phases 4 and 8).
</phase>

<phase name="3_sensitive_scan">
## Phase 3 — Sensitive scan

For 🟡 dirs (especially `~/Downloads`, `~/Desktop`), glob for patterns in `references/sensitive-patterns.md`. Cross-check matches against saved-rules `downloads-keep` / `desktop-keep`:

- Match in saved rules → silent keep (still log to findings)
- New match → AskUserQuestion: Keep / Delete. The answer becomes a saved rule for next run.

Heuristic: if a filename looks personal (legal, medical, financial, identity) but doesn't match a pattern, ask anyway. Better to over-ask once than nuke something irreplaceable.
</phase>

<phase name="4_preview">
## Phase 4 — Preview

Show the full plan: every 🟢, every 🟡 group with rationale, every 🔴 refusal with reason. Estimate total reclaim. The user implicitly approves by interacting with Phase 6's gates; they can also abort here ("hold on, why is X in green?").
</phase>

<phase name="5_auto_execute_green">
## Phase 5 — Execute 🟢

Run the green items. Order them least-invasive first (small file sweeps → cache purges → tool-managed cleanups like `brew autoremove` and `pnpm store prune`). Capture before/after sizes for the delta report. If one fails, log and continue — green items are independent.

Permission denied (e.g., Chrome holds Profile 5 cache while running) — log and move on. Don't fight it.
</phase>

<phase name="6_ask_yellow">
## Phase 6 — Ask 🟡

For each 🟡 group, ONE `AskUserQuestion` with Approve / Modify / Skip. Group similar items (all old runtime versions in one ask, not one per version).

Special handling, when relevant:
- **Downloads with keep-list** — `bash scripts/keeplist-protect.sh ~/Downloads <keepers...>` (mv keepers to /tmp, nuke contents, restore). Show the keep-list before running so user can amend.
- **Old runtimes** — Run `bash scripts/detect-runtimes.sh` first to see which Node/Python versions projects actually use. Recommend deletion of versions not in active use; save active versions to saved rules.
- **APFS snapshots** — `sudo tmutil thinlocalsnapshots / 21474836480 4` reclaims ~20 GB at urgency 4. Surface that it needs sudo.
- **Messages/Attachments** — Quit Messages first (`osascript -e 'tell application "Messages" to quit'; sleep 3`), then `find ~/Library/Messages/Attachments -mindepth 1 -delete` (preserves `chat.db`).
- **Xcode `DerivedData`** (if present) — Safe to delete; only penalty is a slower next build.

Skipped items defer to next run — note them in `state.md` so they re-surface.
</phase>

<phase name="7_delta_report">
## Phase 7 — Delta Report

Clean summary: before/after `df -h`, freed-by-category table, swap state from `sysctl vm.swapusage`. Mention swap as informational — "reboot to reclaim ~X GB swap if you want" — don't prompt for reboot (the user's call).

Sanity-check Trash size — if it grew commensurate with what we deleted, something shuttled instead of reclaiming. Surface that.
</phase>

<phase name="8_update_state">
## Phase 8 — Update state.md

Append a run entry per the format in `state.md`'s header. Update Saved Rules with anything learned this run (new active runtimes, new sensitive-file decisions). Roll oldest entry into compacted section if more than 5 full entries.

When proposing a new saved rule, confirm with the user — don't auto-add. The rules are durable; better to ask once.

Mark checkpoint COMPLETED.
</phase>

</process>

<saved_rules_format>
Stored in `state.md` "Saved Rules" section. Surfaced on every future run.

Format: `- {topic}: {rule} — set {YYYY-MM-DD ET}`

Topics that emerge naturally (not exhaustive — invent new ones when patterns repeat):
- `downloads-keep`, `desktop-keep` — keep-lists per dir
- `active-node`, `active-python` — runtime versions in actual use
- `active-projects` — never-touch project dirs
- `safe-cache-clear-paths` — confirmed-safe auto paths
- `*-policy` — one-off behavioral preferences (e.g., `swap-policy`, `threshold-policy`)
</saved_rules_format>

<recovery_protocol>
If `state.md` shows `status: IN_PROGRESS`:

| Last checkpoint | Resume at |
|---|---|
| INITIALIZED | Phase 1 |
| INVENTORIED | Phase 2 |
| CATEGORIZED | Phase 3 |
| SENSITIVE_SCANNED | Phase 4 |
| PREVIEWED | Phase 5 |
| GREEN_EXECUTED | Phase 6 |
| YELLOW_RESOLVED | Phase 7 |
| REPORTED | Phase 8 |

Ask user: Resume / Start fresh / Show full history. On resume, append to existing entry; do NOT create new one.

Re-run `df -h` before resuming — if disk state changed materially since interruption, re-prompt.
</recovery_protocol>

<error_handling>
Default: log the specific error, skip the problem item, continue with the rest. Disk cleanup is independently-reentrant per item.

Abort the run only if:
- Scan script failed entirely (`findings.json` would be wrong)
- A 🔴 path was almost-touched (bug in categorization → abort + investigate)
- The user said stop

For everything else (single permission denied, brew lock, tool not installed) — keep going and report at the end.

If avail drops below 500 MiB DURING the run (paradoxical but possible in mid-categorization on a near-full disk), pause Phase 5, empty Trash, then resume. `findings.json` lives on the same volume as everything else.
</error_handling>

<success_criteria>
- `state.md` has new entry with `status: COMPLETED`
- `df -h` shows nonzero positive delta in Avail
- No 🔴 path was touched
- Sensitive matches were either kept (with saved rule) or explicitly user-deleted
- User saw a delta report
- Trash size sanity-checked (no shuttling masquerading as reclamation)
</success_criteria>

## Direct actions

Skip the full sweep when these are clearly the intent:

- **"Just empty trash"** → confirm size, `rm -rf ~/.Trash/*` after Y/N
- **"Just clean caches"** → run Phase 5 only
- **"Dry run / show what would be deleted"** → Phases 1–4, stop before Phase 5
- **"What did the last run do?"** → display most recent `state.md` entry
- **"Add `<path>` to never-touch"** / **"forget keep-list for `<file>`"** → edit Saved Rules
- **"Schedule weekly"** → offer `/schedule` routine; if accepted, propose adding entry to `~/.claude/CLAUDE.md` "Active Long-Running Automations" (don't auto-edit — propose for approval)

## Boundaries

Single-actor (`[session]`) for now. Promote to multi-actor (`[disk-cleanup]` for routine, `[session]` for manual) when scheduled.

Manual invocation only — never auto-triggered by other skills. Lock file at `.lock` in skill dir prevents concurrent runs.

Never:
- `sudo rm` directly (sudo only through Apple-blessed commands like `tmutil`)
- Modify `~/.claude/CLAUDE.md` (propose-only)
- Delete a `references/sensitive-patterns.md` match without explicit confirmation, regardless of saved rules
- Force-delete an active project's `node_modules` without explicit ask
- Prompt for reboot (report swap state only)
- Touch anything in `references/safety-invariants.md` regardless of inline user instruction

Cliff. Reasoning is for everywhere else.
