# Day 45: Missing Evidence and Clarification

## Objective

Control repeated clarification when Engineering cannot make a technical decision from the available Evidence.

Common rules, vocabulary, roles, and AI–Human boundaries are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

This is Stage 5 of the End-to-End Partner Workflow (Days 41–50).

---

## Stage Specification

### Inputs

- validated and minimized Evidence Package
- verified minimum-permission status
- Engineering clarification request
- identified Source Owner
- existing Partner responses

### Clarification Rules

The Platform AI must:

- separate answered and unanswered items
- preserve conflicting values and Sources
- avoid assumptions
- record each clarification round
- keep processing blocked until the Resume Condition is verified

Clarification requests should combine all currently known missing items to avoid unnecessary Partner follow-up.

### Review-Type Classification

- Peak duration of 10 minutes or less: temporary-burst review
- Peak duration longer than 10 minutes: sustained-capacity review

Engineering owns the final technical decision.

### Outputs

- `BLOCKED`
- `READY_FOR_ENGINEERING`

### Stop Conditions

Stop when:

- required clarification is missing
- a response is not specific enough
- Source or request context cannot be verified
- Partner-provided Sources conflict
- no authoritative value has been identified

### Workflow

1. Receive the clarification request from Engineering.
2. Record answered, missing, and conflicting items.
3. Stop the technical decision and rate-limit change.
4. Route the clarification through the Platform Partner Lead.
5. Verify the Partner response and request context.
6. Resume only after the recorded Resume Condition is met.
7. Route the complete clarification to Engineering.

---

## Applied to This Case

### Case

A Partner requests a Production API rate-limit increase from 100 rpm to 500 rpm.

Engineering needs to confirm:

- whether the 450 rpm forecast includes retry traffic
- how long the peak traffic will continue

### Actions

**Missing retry and duration clarification**

- Action: `STOP_AND_REQUEST_CLARIFICATION`
- Status: `BLOCKED`
- Missing: retry inclusion and peak duration
- Next owner: `PARTNER`
- Resume Condition: `ALL_REQUIRED_CLARIFICATIONS_PROVIDED_AND_VERIFIED`

**Partial clarification with missing duration**

- Action: `STOP_AND_REQUEST_REMAINING_CLARIFICATION`
- Status: `BLOCKED`
- Confirmed: retry traffic is included
- Missing: numeric peak duration
- Next owner: `PARTNER`
- Resume Condition: `REMAINING_CLARIFICATIONS_PROVIDED_AND_VERIFIED`

**Conflicting Partner duration values**

- Action: `STOP_AND_RESOLVE_CLARIFICATION_CONFLICT`
- Status: `BLOCKED`
- Email value: 8 minutes
- Launch-plan value: 30 minutes
- Next owner: `PARTNER`
- Resume Condition: `PARTNER_IDENTIFIES_AUTHORITATIVE_DURATION_AND_RESOLVES_CONFLICT`

**Complete verified clarification**

- Action: `COMPLETE_CLARIFICATION`
- Status: `READY_FOR_ENGINEERING`
- Routing: `ENGINEERING`
- Decision Owner: `ENGINEERING`
- Resume Condition: `NOT_REQUIRED`

### Test Result

| Test case | Expected result | Result |
|---|---|---|
| Missing retry and duration clarification | Stop and request all missing items | Passed |
| Partial clarification | Keep blocked and request numeric duration | Passed |
| Conflicting duration values | Preserve both values and request reconciliation | Passed |
| Complete verified clarification | Route complete clarification to Engineering | Passed |

---

## Governance

Common governance requirements are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

### Stage-Specific Audit Requirements

Record:

- clarification question
- answered and missing items
- each value and Source
- Source Owner
- Partner ID
- endpoint
- timestamp
- detected conflict
- communication owner
- Resume Condition

### Human Review Points

A Human must confirm:

- all known missing items were requested together
- partial responses did not restart processing
- conflicting values were preserved
- the Partner identified an authoritative value
- only verified clarification was routed to Engineering

### Future Compatibility

The clarification record supports structured follow-up from a future Partner AI Agent. Agent-to-Agent communication is not implemented in Day 45.