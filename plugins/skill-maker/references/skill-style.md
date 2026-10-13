# Canonical Skill Style — The Definitive Guide

> **Related references**: `compaction-patterns.md`, `frontmatter-fields.md`, `intake-questions.md`, `examples/`

This is the house style guide. Every skill this generator produces should match it. `/skill-maker` enforces it; the bundled `scripts/validate-skill.sh` checks it.

---

## 1. Frontmatter (terse, structured)

```yaml
---
name: skill-name              # kebab-case, must match dirname
description: >                # multi-line pushy trigger-phrase block (>= 200 chars, <= 1,536 chars combined with when_to_use)
  What this skill does in 1 sentence. Use when the user asks to "X", "Y", or "Z" — or any phrasing
  that implies <related concepts>. <Specific scope statement.>
when_to_use: >                # OPTIONAL — splits trigger-budget from prose; cleaner separation
  Condition under which this skill is the right tool. E.g., "user wants to create a Claude Code skill"
argument-hint: "[optional]"   # ONLY if $ARGUMENTS used in body
allowed-tools: [Tool1, Tool2] # ONLY if restricting (rare)
paths:                         # OPTIONAL — auto-load only when CWD or open file matches glob
  - "~/.claude/skills/**"
  - "~/path/specific/to/this/skill/**"
model: sonnet                  # OPTIONAL — most skills inherit from session, set only if specific need
disable-model-invocation: true # ONLY if manual-only (no auto-discovery from description)
---
```

**Rules**:
- `name` MUST match the directory name (kebab-case)
- `description` MUST start with what the skill does (1 sentence) THEN list trigger phrases ("Use when…")
- Trigger-phrase list MUST include both happy-path phrases AND adjacent ones (combats Claude's tendency to undertrigger skills)
- Don't use `model:` unless you specifically need a smaller/cheaper model — most skills inherit fine
- Don't use `disable-model-invocation: true` unless the skill is dangerous and should be `/explicit` only

**Description writing tips** (from Anthropic's own skill-creator):
> "Currently Claude has a tendency to 'undertrigger' skills. To combat this, please make the skill descriptions a little bit 'pushy'. Instead of 'How to build a simple fast dashboard', write 'How to build a simple fast dashboard. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a "dashboard."'"

## 2. Body — XML-tagged sections

> **NOTE**: XML tags are a community-evolved convention, NOT Anthropic-blessed. Anthropic's own skills use plain markdown. Both work. XML gives explicit structural cues; if you ever want to switch to plain markdown later, no syntactic change is needed (skills just read the body).

### Required tags (every skill)

| Tag | Purpose |
|---|---|
| `<objective>` | 2-5 sentences. WHAT this skill does + WHY it matters. Front-load load-bearing constraints in plain language. |
| `<process>` | The phases/steps. Wraps `<phase name="N_named">` or `<step name="N_named">` blocks. |
| `<success_criteria>` | Checklist (`- [ ]`) of measurable outcomes that must hold true at end of run. |

### Conditional tags (use when applicable)

| Tag | When |
|---|---|
| `<context>` | Use to inject state file via `@./state.md` syntax. Required for stateful skills. |
| `<execution_context>` | Use to define autonomy matrix (auto-do vs ask vs never). Required for skills that take destructive action. |
| `<error_handling>` | Use for skills that touch external systems (APIs, git, network). Maps specific failures → recovery. |
| `<recovery_protocol>` | Use for stateful checkpointed skills. Maps `IN_PROGRESS` checkpoint → next phase. |
| `<saved_rules_format>` | Use for skills that accumulate rules across runs. Defines format + when to surface. |
| `<verification>` | Use for skills that need validation steps before final commit. |
| `<testing>` | Use for skills with explicit test cases. |
| `<output>` | Use for skills with structured output requirements. |
| `<intake_gate>` | Nested pattern. Use for skills that need adaptive Q&A before execution. Wraps `<no_context_handler>` + `<context_analysis>` + `<initial_questions>` + `<decision_gate>`. |

### Numbered phases / steps

```xml
<process>

<phase name="0_initialize">
## Phase 0 — Initialize
... (or just list bullets, both fine)
</phase>

<phase name="1_action">
## Phase 1 — Specific Action
...
</phase>

<phase name="N_finalize">
## Phase N — Finalize + Commit
...
</phase>

</process>
```

**Naming convention**: `<phase name="0_initialize">` — number prefix + underscored snake_case. The `## Phase N` markdown heading inside is OPTIONAL (most skills include it for human-readability; it's slight redundancy with the XML attribute but improves grep-ability).

**For pure linear flows without phases, use `<step>` instead:** `<step name="1_validate_environment">` etc.

**For one-shot skills with no recovery needs, just use plain markdown bullets** — no XML required.

## 3. Dynamic context injection

```xml
<context>
@./state.md                              # current dir, for skill-relative state
@./references/compaction-patterns.md     # bundled reference
!`ls -1 ~/.claude/skills/`               # shell command output
@~/some-repo/history.md                  # absolute path for cross-repo state
</context>
```

`@file` injects file contents. `! \`command\`` injects shell stdout. Both load BEFORE the skill body executes — use this for state files, recent activity logs, configuration the LLM needs as context.

## 4. State files (the load-bearing pattern)

For any skill that accumulates information across runs:

- **Plain markdown file** in skill dir, repo, or `.planning/` (see `compaction-patterns.md` for which file lives where)
- **Saved Rules section** at top — durable, never auto-pruned, surfaced as "Previous rule found: X. Apply? Y/N/Delete"
- **Active section** — current run with `IN_PROGRESS` marker + checkpoint state
- **Last N full entries** — rolling window of recent runs (typically 3-5)
- **Compacted older entries** — one-line summaries (or distilled into separate file)
- **Archive at bottom** — older than retention window, dropped or compressed

See `compaction-patterns.md` for the 14 distinct flavors.

## 5. Gates and confirmations (autonomy matrix)

Every skill that takes action MUST define what's auto-do vs ask vs never:

```xml
<execution_context>
- Auto-fix safe items without asking (e.g., __pycache__ deletion, empty dirs)
- STOP and ask on medium-risk (e.g., file deletes outside skill dir)
- NEVER touch (e.g., starred items, protected data, global CLAUDE.md without explicit ask)
- Quality bar: zero 🔴 findings before completion
</execution_context>
```

Pattern: 🟢 (auto) / 🟡 (ask) / 🔴 (never).

For asks: use `AskUserQuestion` with 3-4 labeled options. Max 4 questions per call. Batch related questions.

Common 3-option gate:
```yaml
options:
  - label: "Approve"   description: "Execute as proposed"
  - label: "Modify"    description: "Tell me how instead"
  - label: "Skip"      description: "Defer to next run"
```

## 6. Self-preview before destructive action

For ANY skill that sends/posts/publishes/deletes:

- **First action MUST be preview-to-self** (e.g., send a test/preview before the real send)
- **Show before/after diff** for any file modification
- **Literal user confirmation required**: "yes send it" / "yes commit it" / "yes apply it"
- **Never proceed on inferred consent** — explicit phrase only

## 7. Progressive disclosure

- SKILL.md under ~500 lines (a convention; no hard cap)
- Long docs → `references/<topic>.md`
- Shell scripts → `scripts/<name>.sh`
- Templates → `templates/<name>.md`
- Examples → `references/examples/<flavor>.md`

`<context>` block uses `@references/X.md` to inject specific references. Don't load all references; pull on demand.

## 8. Voice and style

- **Imperative** ("Run X", "Read Y", "Apply Z") — not declarative
- **Reserve ALL-CAPS MUST/NEVER** for genuinely load-bearing invariants only (test-before-send, never-touch-starred, etc.)
- **Explain the WHY** — agent should understand intent, not just follow commands
- **No emoji** in skill body — except 🟢🟡🔴 for autonomy matrix and ⭐ for starred-protected
- **Use tables** for routing / config / autonomy matrices

## 9. Attribution conventions

For multi-actor skills (≥2 actors touching state — e.g., a scheduled routine + an interactive session + the user):

- Every memory-file line ends `— [actor <timestamp>]`
- Commits prefixed `[actor]` (e.g., `[routine]`, `[session]`, `[user]`)
- Co-authored trailers when humans + AI both contributed:
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

For single-actor skills (most): no attribution suffix needed.

## 10. Reference examples

The bundled `references/examples/` illustrate each pattern — read the matching one when in doubt:

- **State + checkpoints + saved rules**: `examples/03-stateful-checkpointed.md`
- **Phases + history pruning (one rolling file)**: `examples/02-stateful-simple.md`
- **One-shot, no state**: `examples/01-stateless.md`
- **Multi-actor attribution**: `examples/04-stateful-multi-actor.md`
- **Slash-command router (one-line delegate)**: `examples/05-slash-command-router.md`
- **Zero-context information display**: `examples/06-information-display.md`
- **Multi-phase / per-feature dirs**: `examples/07-multi-phase-feature.md`

Read these when in doubt about a specific pattern.

## 11. Token budget awareness

- SKILL.md auto-re-attaches after `/compact` at **~5K tokens per skill** / **25K combined budget** filled most-recent-first
- Convention: under ~500 lines (no hard cap, but tight)
- If you're approaching 500 lines, offload depth to `references/` and use `@` injection for the relevant parts only

## 12. Migration notes

- **Slash commands and skills are unified** as of 2026 (Anthropic's docs: "Custom commands have been merged into skills"). Existing `~/.claude/commands/*.md` still work; new things go to `~/.claude/skills/<name>/SKILL.md`.
- For commands that need state + references + scripts → migrate to skill form. Pure-prompt commands can stay as `.md` files.
- Plugin namespace form: `plugin-name:skill-name` (e.g., `vercel:nextjs`).
