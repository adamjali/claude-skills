---
name: {{SKILL_NAME}}
description: >
  {{ONE_LINE_PURPOSE}}. Use when the user asks to "{{TRIGGER1}}", "{{TRIGGER2}}", "{{TRIGGER3}}",
  or any phrasing that implies {{RELATED_CONCEPTS}}. {{SCOPE_STATEMENT}}.
when_to_use: >
  {{WHEN_TO_USE_CONTEXT}}
{{ARGUMENT_HINT_LINE}}{{PATHS_LINES}}{{ALLOWED_TOOLS_LINE}}
---

<objective>
{{OBJECTIVE_PARAGRAPH}}
</objective>

<context>
{{CONTEXT_REFS}}
</context>

<execution_context>
{{EXECUTION_RULES}}
</execution_context>

<process>

<phase name="0_initialize">
## Phase 0 — Initialize

{{PHASE_0_BODY}}

`TaskUpdate` Phase 0 → completed.
</phase>

<phase name="1_action">
## Phase 1 — {{PHASE_1_TITLE}}

{{PHASE_1_BODY}}

`TaskUpdate` Phase 1 → completed.
</phase>

<phase name="N_finalize">
## Phase N — Finalize

{{PHASE_N_BODY}}

`TaskUpdate` Phase N → completed.
</phase>

</process>

{{SAVED_RULES_BLOCK}}

{{RECOVERY_PROTOCOL_BLOCK}}

<error_handling>
{{ERROR_HANDLING_RULES}}
</error_handling>

<success_criteria>
{{SUCCESS_CRITERIA_CHECKLIST}}
</success_criteria>

{{DIRECT_ACTIONS_BLOCK}}

{{NEVER_DO_BLOCK}}
