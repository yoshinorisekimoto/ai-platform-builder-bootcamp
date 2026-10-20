# Day 54: Model Governance and Mandatory Guardrails

## Objective
Control how AI-supported prioritization models are changed, and separate normal business prioritization from mandatory regulatory requirements.

Common rules are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

Delegated Agent behavior from Day 51 onward is defined in the [Delegation Model](../AGENTS.md#delegation-model-day-51).

This is Stage 14 of the End-to-End Partner Workflow.

Current stage: `HUMAN_REVIEW`.

## Stage Specification

### Inputs
- prioritization model results
- missing or incomplete inputs
- scoring rubric
- proposed scoring-weight changes
- historical cases
- regulatory requirements
- Partner migration status
- internal and external deadlines
- Engineering capacity
- exception requests

### Stage-Specific Roles
- **Platform Agent** — applies approved rules, runs comparisons, tracks migration, and records evidence.
- **Platform Partner Lead** — owns workflow governance, Partner coordination, and escalation.
- **Engineering** — owns technical implementation and validation.
- **Compliance** — confirms mandatory regulatory requirements.
- **Migration Program Owner** — may approve use of internal migration buffer but cannot extend the regulatory deadline.

### Scoring Model Governance
A poor recommendation does not automatically mean the scoring model is wrong.

Before changing weights, separate:
- missing input
- rubric-definition problems
- scoring-weight problems

The rubric must define how inputs such as urgency, ambiguity, commitment, and evidence readiness are scored.

AI may calculate and back-test scores but may not change the scoring model or rubric.

### Mandatory Guardrail Rule
A mandatory regulatory requirement does not compete with normal business work over whether it must be completed.

Business and technical factors may still determine:
- migration order
- Partner sequencing
- Engineering scheduling
- communication timing

They cannot extend the regulatory deadline.

### Internal Safety Buffer Rule
The Platform may set an internal deadline earlier than the regulatory deadline.

The internal safety buffer:
- is not a standard Partner extension
- is not disclosed as negotiable time
- is used only through an exception process
- cannot extend the regulatory deadline

### Outputs
- model-change status
- migration-program status
- Partner migration plan
- exception status
- next owner
- Decision Owner
- audit record

### Stop Conditions
Stop or escalate when:
- model change is requested without sufficient evidence
- the rubric is undefined
- back-testing is incomplete
- mandatory migration risks missing the Platform deadline
- a Partner requests use of the internal buffer
- an exception exceeds Platform Lead authority

### Workflow
1. Separate missing-input issues from model-design issues.
2. Define the scoring rubric before changing weights.
3. Back-test proposed changes against historical cases.
4. Require Human Review before model change.
5. Create a mandatory migration program for regulatory work.
6. Track Partner-specific migration milestones.
7. Keep the internal safety buffer outside normal Partner negotiation.
8. Escalate genuine deadline risk through the exception process.

## Applied to This Case

### Case 1 — Revenue Weight Change Is Not Yet Justified
The model was used for 20 cases.

- 17 recommendations matched Human decisions.
- 3 did not.
- All 3 mismatches involved missing Sales commitment data.
- Sales requests that Revenue weight be doubled.

The current evidence does not show that Revenue weighting caused the mismatches.

#### Action
`HOLD_MODEL_CHANGE`

- Status: `WAIT`
- Next owner: `PLATFORM_PARTNER_LEAD`
- AI can change weights: `False`
- Resume Condition: `RUBRIC_DEFINED_AND_BACKTEST_COMPLETED`

AI should re-run the historical cases with corrected inputs and compare the current and proposed models.

### Case 2 — Mandatory Regulatory Migration
A new regulatory requirement becomes mandatory in Japan in 12 months.

The existing consent mechanism already exists on the Platform, but 40 Partner integrations must enable the required control.

#### Action
`CREATE_MANDATORY_MIGRATION_PROGRAM`

- Status: `CONTINUE`
- Affected integrations: `40`
- Regulatory deadline: Month `12`
- Platform deadline: Month `11`
- Internal safety buffer: `1 month`
- Normal revenue override allowed: `False`
- Next owner: `PLATFORM_PARTNER_LEAD`

The regulatory requirement determines what must be completed.

Normal business prioritization may still determine migration sequence inside the allowed window.

### Case 3 — Large Partner Requires Early Planning
A large Partner may already have Engineering work committed for future quarters.

The required technical change itself is small, but scheduling, testing, and production coordination require early alignment.

#### Action
`TRACK_MIGRATION`

- Planning mode: `EARLY_INDIVIDUAL_PLANNING`
- Status: `CONTINUE`
- Next owner: `PLATFORM_AGENT`

The migration plan records:
- migration owner
- required change
- target quarter
- test date
- production deadline

Large Partner planning is based on Engineering lead time, not automatically on business tier.

### Case 4 — Standard Partner Uses Migration Wave
A standard Partner has the same mandatory requirement but does not require long-range individual Engineering planning.

#### Action
`TRACK_MIGRATION`

- Planning mode: `QUARTERLY_MIGRATION_WAVE`
- Status: `CONTINUE`
- Next owner: `PLATFORM_AGENT`

AI tracks milestones and flags missing ownership, test dates, or production deadlines.

### Case 5 — Partner Requests the Safety Buffer Early
Partner X asks to move its Platform deadline one month later.

There is currently no confirmed reason that the Partner cannot meet the standard Platform deadline.

#### Action
`KEEP_STANDARD_PLATFORM_DEADLINE`

- Status: `CONTINUE`
- Extension approved: `False`
- Internal buffer disclosed as extension: `False`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Reason: `NO_CONFIRMED_NEED_FOR_EXCEPTION`

The standard external deadline remains unchanged.

### Case 6 — Partner Later Risks Missing the Platform Deadline
Partner X later shows a genuine risk of missing the Platform deadline.

The Platform Lead cannot grant the internal buffer automatically.

#### Action
`ESCALATE_BUFFER_EXCEPTION_REVIEW`

- Status: `ESCALATE`
- Extension approved: `False`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Decision Owner: `MIGRATION_PROGRAM_OWNER`
- Compliance review required: `True`
- Resume Condition: `EXCEPTION_DECISION_RECORDED`
- Reason: `PLATFORM_DEADLINE_AT_RISK`

The Migration Program Owner may approve use of the internal safety buffer.

The regulatory deadline itself cannot be extended.

### Test Result

| Test case | Expected result | Result |
|---|---|---|
| Model mismatch caused by missing inputs | `HOLD_MODEL_CHANGE` | PASS |
| Mandatory regulatory migration identified | `CREATE_MANDATORY_MIGRATION_PROGRAM` | PASS |
| Large Partner needs early planning | `EARLY_INDIVIDUAL_PLANNING` | PASS |
| Standard Partner can use migration wave | `QUARTERLY_MIGRATION_WAVE` | PASS |
| Early extension request without confirmed need | `KEEP_STANDARD_PLATFORM_DEADLINE` | PASS |
| Confirmed Platform deadline risk | `ESCALATE_BUFFER_EXCEPTION_REVIEW` | PASS |

## Governance

### Stage-Specific Audit Requirements
Record:
- model version
- scoring rubric
- corrected input data
- back-test results
- proposed weight changes
- Human model-change decision
- Partner migration milestones
- exception request
- exception Decision Owner
- final exception outcome

### Human Review Points
Human Review is required when:
- scoring rules or weights may change
- the rubric does not cover the case
- migration risks missing the Platform deadline
- the internal safety buffer may be used

### Future Compatibility
Future Agents may:
- back-test approved scoring models
- identify missing model inputs
- maintain migration trackers
- detect milestone risk
- prepare exception records

Agents may not:
- redefine the rubric
- change model weights
- waive mandatory regulatory requirements
- grant use of the internal safety buffer

The target remains controlled delegation: routine execution may increase over time, while governance changes and exceptions remain under Human authority.