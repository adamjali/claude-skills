# Example: Stateful Multi-Actor

Use when ≥2 actors touch the state (routine, session, user, etc.) and attribution matters. E.g. a shared bot/human workflow (3 actors: routine + session + user).

Builds on Example 03 (checkpointed) + adds:
- Multi-file state (different memory files for different concerns)
- Attribution suffix on every memory line: `— [actor <ET timestamp>]`
- Actor-prefixed commits: `[routine]`, `[session]`, etc.
- Multiple compaction patterns across the various state files (one might be Pattern 1, another Pattern 5, another Pattern 8)

```markdown
<objective>...</objective>

<context>
@~/external-repo/sync-history.md      # if multi-device
@./memory/recent_log.md
@./memory/precedents.md
@./memory/feedback_inbox.md
@./memory/run_status.md
</context>

<execution_context>
- 🟢 Auto-execute safe items
- 🟡 ASK on uncertain (AskUserQuestion 3-option gate)
- 🔴 NEVER touch (starred, protected, etc.)
- Attribution: every memory line ends `— [<actor> <ET>]`
- Commits: prefix with `[<actor>]`; include Co-Authored-By trailer for AI commits
</execution_context>

<process>
... phases as 03 ...
</process>

<saved_rules_format>
## Multi-Actor Attribution

| Actor | Git identity | Commit prefix | Memory suffix |
|---|---|---|---|
| **<Actor1>** | <name> <email> | `[actor1]` | `— [actor1 <ET>]` |
| **<Actor2>** (Claude session) | local git user | `[session]` | `— [session <ET>]` |
| **User direct** | user GitHub identity | (free-form) | `— [user <ET>]` |

When acting on user feedback: `— [actor1, from user's feedback <ET>]`
</saved_rules_format>

<recovery_protocol>... as 03 ...</recovery_protocol>
<error_handling>... as 03 ...</error_handling>
<success_criteria>
- [ ] Every memory line has attribution suffix
- [ ] Commits have correct actor prefix
- [ ] Co-Authored-By trailer on AI commits
... rest as 03 ...
</success_criteria>
```

**Compaction patterns combined**:
- `recent_log.md` → Pattern 4 (two-tier into summary.md)
- `precedents.md` → Pattern 5 (1-per-unique-entity)
- `processed_ids.md` → Pattern 6 (TTL hard-delete)
- `pending_rules.md` → Pattern 7 (TTL with grace period)
- `pending_actions.md` → Pattern 8 (NEVER auto-prune)
- `feedback_inbox.md` → Pattern 14 (single-use, clear after read)

**Pattern**: a `SKILL.md` + a worker `PROMPT.md` + several attributed memory files.
