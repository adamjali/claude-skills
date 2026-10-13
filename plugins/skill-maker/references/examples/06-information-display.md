# Example: Information-Display Skill (zero-context output)

Use when the skill's job is to display reference content / help / config without ever editorializing. Like `/gsd-help`.

```yaml
---
name: my-info-skill
description: >
  Show <reference content>. Use when the user asks "how do I X", "what's the X reference", etc.
---
```

```markdown
# Title

## Output Rules

**CRITICAL**: Output ONLY the reference content. Do NOT add:
- Project-specific analysis
- Git status or workspace state
- Next-step suggestions
- Any commentary or prose between sections

The user wants the reference, not your interpretation.

## Reference Content

<the actual content - tables, lists, code examples, etc.>
```

**Pattern**: zero-context output rule. The skill says explicitly "don't add commentary."

**Gold standard**: `~/.claude/skills/gsd-help/SKILL.md` (496L — long because it's a comprehensive reference, but the rule at top keeps invocations tight).

**When to use**:
- Help / documentation skills
- Config display skills
- "Show me X" skills

**Don't use** for: skills that need to reason or take action.
