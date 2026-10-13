# Example: Stateless Skill

Use when the skill is one-shot, no history, no recovery. Like `/jina-image-search`.

```yaml
---
name: my-stateless-skill
description: >
  One-line of what it does. Use when the user asks to "X", "Y", or "Z".
  Specific scope statement.
---
```

```markdown
# Skill Title

## Overview
What this skill does in 2-3 sentences.

## Workflow

### Step 1: <action>
Imperative description.

### Step 2: <action>
Imperative description.

## Reference

| Key | Value |
|---|---|
| API endpoint | URL |
| Auth | Bearer token |
```

**Use the gold standard**: `~/.claude/skills/jina-image-search/SKILL.md` (115 lines).

**Don't include**: `<process>`, `<recovery_protocol>`, `<saved_rules_format>`. The skill has no state to manage.

**Do include**: clear sections, tables for config, example commands inline.
