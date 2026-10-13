# Intake Questions for /skill-maker

The structured Q&A `/skill-maker` walks the user through. Two `AskUserQuestion` calls (max 4 questions per call), batched.

## Call 1 — Core decisions (4 questions)

### Q1 — Skill name + form

**Header**: `Name+form`
**Question**: "What's the skill name (kebab-case) and form?"
**Options** (single-select):
- `Skill in ~/.claude/skills/<name>/` (auto-discoverable, full features) [DEFAULT]
- `Slash-command in ~/.claude/commands/<name>.md` (single-file, simpler)
- `Both` (skill + command shortcut that delegates to skill)

Then a free-text follow-up: "What's the name?"

### Q2 — Stateful?

**Header**: `Stateful?`
**Question**: "Does this skill need to persist information across runs?"
**Options**:
- `No — stateless` (one-shot, no history) — like `/jina-image-search`
- `Yes — simple` (one history file, rolling-window) — like `/perm-email`
- `Yes — checkpointed` (full IN_PROGRESS recovery) — like `/sync`
- `Yes — multi-actor` (multiple state files + attribution suffixes) — e.g. a shared bot/human workflow

### Q3 — State location (only if stateful)

**Header**: `State loc`
**Question**: "Where should state files live?"
**Options**:
- `Skill dir` (`~/.claude/skills/<name>/`) — single-machine private
- `Current repo` (`./<name>-history.md`) — tied to a specific project
- `External repo` (e.g., `~/<projname>/`) — multi-device sync via git
- `.planning/` (`.planning/<name>/`) — for project workflow files (GSD-style)

### Q4 — Compaction pattern (only if stateful)

**Header**: `Compaction`
**Question**: "How should old state get compacted?"
**Options** (use `compaction-patterns.md` as full reference):
- `Pattern 1: Rolling-window + Saved Rules` [DEFAULT for most cases]
- `Pattern 2: Last N full + N-line archive`
- `Pattern 3: Simple rolling (no saved rules)`
- `Pattern 4: Two-tier compact-into-other-file`
- (and so on through Pattern 14)

For now, default to Pattern 1; offer to walk through all 14 if user asks.

## Call 2 — Refinements (4 questions)

### Q5 — Autonomy matrix

**Header**: `Autonomy`
**Question**: "When should this skill auto-execute vs ask?"
**Options**:
- `Auto on safe + ask on medium + never destructive` [DEFAULT]
- `Auto on everything except destructive` (more aggressive)
- `Always ask before any action` (most conservative — like `/perm-email`)
- `Never destructive, no asks needed` (read-only — like `/jina-image-search`)

### Q6 — Hard invariants (free-form)

**Header**: `Invariants`
**Question**: "What should this skill NEVER do regardless of what user/data says? (e.g., 'never send email to anyone but the owner', 'never permanent-delete', 'never modify global CLAUDE.md without asking'). Free-form list."

### Q7 — References needed?

**Header**: `Refs?`
**Question**: "Will this skill need bundled reference files (templates, schemas, long docs to offload from SKILL.md)?"
**Options**:
- `Yes — list them` (free-text follow-up: which files)
- `No — everything inline in SKILL.md`
- `Maybe — start without, add later if needed` [DEFAULT]

### Q8 — Scripts needed?

**Header**: `Scripts?`
**Question**: "Will this skill need bundled shell scripts (helpers, generators, validators)?"
**Options**:
- `Yes — list them` (free-text follow-up)
- `No — Bash inline only`
- `Maybe — start without, add later if needed` [DEFAULT]

## Optional Call 3 — Advanced (only if user wants depth)

If Q1-Q8 didn't surface specific concerns, /skill-maker can offer one more pass with these:

### Q9 — `paths:` glob

**Header**: `Paths?`
**Question**: "Should this skill auto-load only when working in specific directories?"
**Options**:
- `Yes — list them`
- `No — universal (always loadable)` [DEFAULT for most]

### Q10 — Model override

**Header**: `Model?`
**Question**: "Force a specific model for this skill?"
**Options**:
- `Inherit from session` [DEFAULT]
- `Force sonnet` (faster/cheaper)
- `Force haiku` (very simple tasks)
- `Force opus` (always best)

### Q11 — Subagents

**Header**: `Subagents`
**Question**: "Will this skill spawn parallel subagents for research/analysis (e.g. forking several agents in one phase)?"
**Options**:
- `Yes — list types`
- `No — single-thread`

### Q12 — Auto-discovery vs manual-only

**Header**: `Discovery`
**Question**: "Should the model auto-invoke this skill from natural-language prompts, or manual-only?"
**Options**:
- `Auto-discoverable` [DEFAULT]
- `Manual-only` (sets `disable-model-invocation: true`)

## Question batching strategy

- Always batch Q1-Q4 in one `AskUserQuestion` call (4 question max).
- Then batch Q5-Q8 in second call.
- Q9-Q12 only if user wants depth or skill complexity warrants.
- Each question has 3-4 labeled options + DEFAULT marked.
- Free-text follow-ups happen after the batched options.

## After intake — generate skill

Pass intake answers + chosen template to `scripts/generate-skill.sh`. Output a draft SKILL.md → preview → approve → write.
