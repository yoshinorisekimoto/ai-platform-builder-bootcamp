# Writing Guide: End-to-End Partner Workflow (Days 41-50)

This guide defines the writing format for the Day 41-50 sub-series, "End-to-End
Partner Workflow." It exists so that drafting (via ChatGPT) and review (via
Claude) stay consistent even across separate sessions that don't share
conversation history.

## Article Template (fixed from Day 44 onward)

```markdown
# Day [N]: [Stage Name]

## Objective

[The purpose of this stage, in 1-2 sentences.]
Common rules, vocabulary, roles, and AI–Human boundaries are defined in
the [Shared Framework](https://github.com/yoshinorisekimoto/ai-platform-builder-bootcamp/blob/main/AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).
This is Stage [X] of the End-to-End Partner Workflow (Days 41–50).

## Stage Specification

### Inputs

### Stage-Specific Role(s)

*(Whenever a new role appears, define it in one line.)*

### [Name of the rule unique to this stage]

### Outputs

### Stop Conditions

### Workflow

## Applied to This Case

### Case

### Actions

For each pattern:

- Action: `UPPERCASE_SNAKE_CASE` (start with a base-form imperative verb)
- Status: ...
- Next owner: ...
- Resume Condition: ... (if the action stops)

### Test Result (table: Test case / Expected result / Result)

## Governance

### Stage-Specific Audit Requirements

### Human Review Points

### Future Compatibility
```

## Rules (important)

- Do not repeat shared rules (the 8 Platform AI prohibitions, the
  Notify/Escalate/Resume Condition definitions, the standard AI and Human
  Boundary language). Always link to the Shared Framework in AGENTS.md
  instead.
- Do not add non-English explanatory sections (e.g. a "plain-language"
  or "for a younger reader" summary). This practice was discontinued as of
  Day 36; the series is written entirely in English from that point on.
- Day 41-43 remain in their original, heavier format and are not retrofitted.
  This lighter template applies from Day 44 onward only.

## Why This Exists

Day 41 was 177 lines; by Day 43, repeated boilerplate had pushed a single
entry to 343 lines, risking abandonment by external readers (e.g. hiring
managers skimming the repository). Starting Day 44, shared content moved to
AGENTS.md so each entry documents only what's new at that stage, keeping
articles in the 150-200 line range.

## Production Process

Each Day entry is drafted by ChatGPT from a working session, then reviewed by
Claude for structural consistency, logical gaps, and alignment with this
guide before being committed.