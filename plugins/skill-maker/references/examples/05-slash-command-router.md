# Example: Slash-Command Router (one-line delegate)

Use when you want a `/<short-name>` shortcut that delegates to a skill. Like `~/.claude/commands/debug.md` → invokes `debug-like-expert` skill.

```yaml
---
allowed-tools: [Skill(debug-like-expert)]
description: Apply expert debugging methodology to investigate a specific issue
argument-hint: <issue description>
---

Invoke the `debug-like-expert` skill with: $ARGUMENTS
```

That's the entire file. ~5 lines.

**Pattern**: pure delegate. The slash command is just a UX shortcut; the actual logic lives in the skill.

**Examples in `~/.claude/commands/`**:
- `create-hook.md` → invokes `create-hooks` skill
- `create-subagent.md` → invokes `create-subagents` skill
- `create-meta-prompt.md` → invokes `create-meta-prompts` skill
- `debug.md` → invokes `debug-like-expert` skill

**When to use**:
- Skill name is awkward to type (`create-hooks` is plural; user might type `create-hook`)
- Want a `/short` form for an auto-discoverable skill
- Skill is auto-discoverable but user wants explicit invocation

**Don't use** for: skills the user always types fully or skills where the slash form == the skill name.
