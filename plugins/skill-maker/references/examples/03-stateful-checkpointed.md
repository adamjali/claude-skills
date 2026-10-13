# Example: Stateful Checkpointed

Use when full IN_PROGRESS recovery + saved rules across runs. Like `/sync` and `/github-audit`.

```yaml
---
name: my-checkpointed-skill
description: >
  Pushy trigger phrases.
argument-hint: "[optional-arg]"
---
```

```markdown
<objective>...</objective>

<context>
@./<state>-history.md (if exists - for resuming and decision suggestions)
</context>

<execution_context>
- Auto-fix safe/small items without asking
- STOP and discuss medium/breaking items with user
- History: keep last 5 + saved rules section + IN_PROGRESS marker
</execution_context>

<process>

<phase name="0_initialize">
## Phase 0: Initialize
- Read state file
- Check IN_PROGRESS marker → offer Resume / Fresh / Review
- Initialize current entry as IN_PROGRESS with checkpoint: INITIALIZED
</phase>

<phase name="1_first_action">
## Phase 1: First Action
... actions ...
- Update checkpoint: FIRST_DONE
</phase>

<phase name="2_second_action">
## Phase 2: Second Action
... actions ...
- Update checkpoint: SECOND_DONE
</phase>

<phase name="N_finalize">
## Phase N: Finalize + Commit
- Update state with COMPLETED entry
- Apply rolling-window: keep last 5 full + saved rules + IN_PROGRESS removed
- Append new precedents to Saved Rules section
</phase>

</process>

<saved_rules_format>
## Saved Rules

Stored in `<state>-history.md` "Saved Rules" section. Surfaced on every future run as:
"Previous rule found: '<rule>'. Apply this? (Yes / No / Delete rule)"

Format per rule:
\`\`\`
- {topic}: {rule} — set {YYYY-MM-DD ET}
\`\`\`
</saved_rules_format>

<recovery_protocol>
If state shows IN_PROGRESS:
1. Identify last completed checkpoint
2. Map checkpoint → next phase (e.g., FIRST_DONE → resume Phase 2)
3. Offer the user: Resume / Fresh / Review
4. On resume, append to existing entry; do NOT create new
</recovery_protocol>

<error_handling>...</error_handling>
<success_criteria>...</success_criteria>
```

**Compaction**: Pattern 1 (rolling-window with Saved Rules) or Pattern 2 (last N + N-line archive).

**Gold standards**:
- `~/.claude/commands/sync.md` (545L — gold standard for checkpoint resumption)
- `~/.claude/commands/github-audit.md` (249L — gold standard for phases + history pruning)
