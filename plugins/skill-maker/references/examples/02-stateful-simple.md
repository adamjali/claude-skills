# Example: Stateful Simple

Use when there's a single history file, rolling-N. Like `/perm-email`.

```yaml
---
name: my-stateful-skill
description: >
  Pushy trigger phrases.
---
```

```markdown
<objective>
What this skill does + WHY.
</objective>

<context>
@./history.md
</context>

<execution_context>
- Auto-fix safe items
- ASK before destructive (send/post/publish/delete)
</execution_context>

<process>
<phase name="0_initialize">...</phase>
<phase name="1_action">...</phase>
<phase name="N_finalize">
- Update history.md with new entry
- Apply rolling-window: keep last 5, archive older to one-line at bottom
</phase>
</process>

<error_handling>...</error_handling>
<success_criteria>...</success_criteria>

## History

See `~/.claude/skills/<name>/history.md` for past runs.

Format per entry:
\`\`\`
## [Date] — [Subject]
- Key 1: ...
- Key 2: ...
\`\`\`

Keep last 5. Older → one-line archive at bottom.
```

**Compaction**: Pattern 3 (simple rolling-window).

**Gold standard**: `~/.claude/skills/perm-email/SKILL.md` (215 lines) + its `history.md`.
