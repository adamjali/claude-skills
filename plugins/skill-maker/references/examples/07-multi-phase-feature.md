# Example: Multi-Phase Feature (per-feature dirs + multi-agent)

Use when each "instance" of work is large enough to warrant its own directory + multiple artifacts + multiple agents. Like `/gsd-feature`.

```yaml
---
name: my-feature-skill
description: >
  Pushy trigger phrases for "feature work" / "build feature" / etc.
argument-hint: "[feature-name]"
---
```

```markdown
<objective>
Multi-phase feature development with dedicated artifacts per phase, multi-agent execution.
</objective>

<context>
@./.planning/STATE.md       # index of all features
</context>

<execution_context>
- Each feature gets its own dir: .planning/features/NNN-slug/
- Multiple named artifacts inside: NNN-EXPLORATION.md, NNN-CLARIFICATIONS.md, NNN-ARCHITECTURE.md, NNN-PLAN.md, NNN-SUMMARY.md, NNN-REVIEW.md
- Each artifact has a dedicated agent (explorer, architect, planner, executor, reviewer)
- Once feature is done, dir is immutable (committed to git)
- STATE.md only has a one-line row referencing the dir
- Compaction happens at STATE.md level only — feature dirs preserved forever via git
</execution_context>

<process>

<phase name="0_initialize">
- Number this feature (NNN)
- Create dir: .planning/features/NNN-slug/
- Initialize NNN-EXPLORATION.md
</phase>

<phase name="1_explore">
Spawn `code-explorer` subagent → writes NNN-EXPLORATION.md
</phase>

<phase name="2_clarify">
- Read EXPLORATION.md
- Identify ambiguities
- AskUserQuestion → write NNN-CLARIFICATIONS.md
</phase>

<phase name="3_architect">
Spawn `code-architect` subagent → writes NNN-ARCHITECTURE.md
</phase>

<phase name="4_plan">
Spawn `planner` subagent → writes NNN-PLAN.md (atomic tasks)
</phase>

<phase name="5_execute">
Spawn `executor` subagent → atomic commits per task
</phase>

<phase name="6_review">
Spawn `code-reviewer` subagent → writes NNN-REVIEW.md
</phase>

<phase name="7_finalize">
- Update STATE.md with feature row: status=COMPLETED + dir reference
- Commit feature dir
</phase>

</process>

<error_handling>
- If subagent fails → write partial artifact, mark IN_PROGRESS, allow Resume
- If conflict during merge → STATE.md conflict at row-level only (not full content)
</error_handling>

<success_criteria>
- [ ] All 6 artifacts present in .planning/features/NNN-slug/
- [ ] STATE.md has row for this feature
- [ ] Atomic commits during execute phase (one per task in PLAN.md)
- [ ] git history preserves the dir
</success_criteria>
```

**Compaction**: Pattern 9 (atomic per-event dirs + git history is the archive).

**Gold standard**: `~/.claude/skills/gsd-feature/SKILL.md` (821L) + `.planning/features/` directory structure.

**When to use**: complex work where merge conflicts and multi-agent ownership matter. Overkill for simple stuff.
