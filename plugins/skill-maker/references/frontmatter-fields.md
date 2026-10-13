# Skill Frontmatter — Full Field Reference (2026)

Complete spec of YAML frontmatter fields available on `~/.claude/skills/<name>/SKILL.md`. Sourced from Anthropic 2026 docs + research synthesis.

> ⚠️ **VERSION COMPATIBILITY (verified 2026-04-27)**: your running CLI version supports ONLY `name:` and `description:` reliably. Fields like `when_to_use:`, `paths:`, `argument-hint:`, `allowed-tools:` are documented in 2026 spec but **silently break skill loading** if the CLI doesn't support them yet — the skill won't appear in the available-skills list, and `/<name>` returns "Unknown command". For now, `/skill-maker` should generate skills with **frontmatter limited to `name:` + `description:`**. Move all "when to use" content into the `description:` field as one long string. Once the CLI catches up to spec, this restriction can be relaxed.

| Field | Required? | Type | Purpose | Notes |
|---|---|---|---|---|
| `name` | YES | string (kebab-case) | Skill identifier; must match dirname | Auto-discovery uses this |
| `description` | YES | string (multi-line OK with `>`) | When to trigger + what it does | **HARD CAP: 1,536 chars** combined with `when_to_use`. Pushy phrasing recommended. |
| `when_to_use` | optional | string | Adds to trigger budget; cleaner separation from `description` prose | Splits "what" from "when" |
| `argument-hint` | optional | string | Hint shown to user when they call `/<name> ` | ONLY use if body references `$ARGUMENTS` |
| `arguments` | optional | structured | Newer fielded version of arguments | See Anthropic docs for schema |
| `allowed-tools` | optional | array | Restrict which tools the skill can use | ONLY when restricting; default allows all |
| `disable-model-invocation` | optional | bool | If `true`, skill is manual-only (no auto-discovery from description) | Use for dangerous skills that should be `/explicit` only |
| `user-invocable` | optional | bool | If `false`, only the model can invoke (not user via `/`) | Rare |
| `paths` | optional | array of globs | Auto-load only when CWD or open file matches glob | New 2026; underused. Use for path-scoped skills |
| `model` | optional | string (`sonnet`/`haiku`/`opus`) | Force specific model for this skill | Most skills inherit; only set if specific need |
| `effort` | optional | string | Resource hint | See docs for values |
| `context` | optional | object | E.g., `{fork: true}` to fork session | Rare |
| `agent` | optional | string | Force routing to specific agent | Rare |
| `hooks` | optional | object | Skill-level hook config | Rare |
| `shell` | optional | string | Override shell for `! \`\`` injection | Rare |

## The `description` field — the most important

It does double duty:
1. **Trigger phrase database**: every word in the description is matched against user prompts for auto-invoke
2. **Documentation**: shown in `/help`, on hover, etc.

**Best practice for high-recall**:
```yaml
description: >
  <One sentence of what the skill does>. Use when the user asks to "verb-phrase X",
  "verb-phrase Y", or "verb-phrase Z" — or any phrasing that implies <related concepts>.
  <Specific scope statement so it doesn't over-trigger>.
```

**Example (good — pushy + scoped)**:
```yaml
description: >
  Manage marketing emails for PERM Tracker. Use when the user asks to "send an email",
  "draft an email", "check contacts", "sync contacts", "email blast", "broadcast",
  "newsletter", "marketing email", "how many users", "email history", "what emails have
  we sent", "review request", "Senja", "Resend audience", "unsubscribe", or anything
  related to PERM Tracker marketing/product-update emails.
```

**Example (bad — vague + under-trigger)**:
```yaml
description: Email management.
```

## Splitting description from when_to_use

When the description gets long, split into:
- `description`: focused on triggers (verbs + topics)
- `when_to_use`: focused on context (when this is the right tool)

```yaml
description: >
  Create new Claude Code skills matching the house style. Use when the user asks to
  "make a skill", "create a skill", "build a skill", "scaffold", or any phrasing
  that implies turning a workflow into a reusable skill.
when_to_use: >
  User wants to create OR redesign OR audit a Claude Code skill in their personal
  library. Especially when the skill has any state, recovery, or multi-actor
  context — those need careful pattern selection.
```

Both fields combined ≤ 1,536 chars.

## `paths:` — when to use

Auto-load only when CWD or an open file matches one of the globs. Reduces noise — skill doesn't activate when irrelevant.

```yaml
paths:
  - "~/my-project/**"        # activates only when in this repo
  - "~/.claude/skills/**"     # skill-maker activates when working on skills
  - "~/my-project/sub/**"     # activates when in this dir
```

**Don't use** for general-purpose skills (frontend-design, jina-image-search). Their value is universal.
**Do use** for project-specific or dir-scoped skills.

## `disable-model-invocation: true`

Use sparingly. Examples:
- Skill is dangerous if accidentally triggered (e.g., production-deploy)
- Skill is `/audit-only` — user should explicitly invoke
- Skill is for advanced workflows the LLM shouldn't decide to use

When set, skill body doesn't load into context until user types `/<name>`. Saves tokens but loses auto-discovery.

## `model:` field

```yaml
model: sonnet     # default for most skills
model: haiku      # fast/cheap, simple tasks
model: opus       # only if the skill specifically needs it
```

Most skills should inherit the session model — leave `model:` unset. Only set it if the skill explicitly needs a smaller/cheaper model (rare).

## `argument-hint:` field

ONLY when the skill's body uses `$ARGUMENTS`. Format: a short hint shown after the slash command.

```yaml
argument-hint: "<skill-path>"        # for /audit-skill
argument-hint: "[upstream-remote]"   # for /sync (optional argument indicated by brackets)
```

Don't set if the skill is a no-argument skill.

## `allowed-tools:` field

Restrict tool access. Default = all allowed. Use to:
1. Prevent destructive tools in low-risk skills (read-only)
2. Comply with security boundaries
3. Reduce LLM's "tool choice fatigue"

```yaml
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]  # explicit allow-list
allowed-tools: [Bash(git:*), Bash(ls:*)]              # restrict bash to specific commands
allowed-tools: [Skill(perm-email)]                    # one-line router that delegates
```

The last form is a one-line command file (e.g. `~/.claude/commands/create-hook.md`) that just delegates to a real skill via the Skill() tool.

## What NOT to put in frontmatter

- Long prose → put in `<objective>` block in body
- Multi-paragraph context → put in `<context>` block in body
- Examples → put in `references/examples/`
- Behavior config → use the body's `<execution_context>`

Frontmatter is for METADATA only. Behavior goes in the body.
