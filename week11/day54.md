# Day 54: Model Governance and Mandatory Guardrails

## Objective
Control how the prioritization model introduced in Day 53 is changed, and separate normal business prioritization from mandatory regulatory requirements.

Both share one principle: the Agent may calculate, compare, and track, but it may not change the rules it is measured against.

Common rules are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

Delegated Agent behavior from Day 51 onward is defined in the [Delegation Model](../AGENTS.md#delegation-model-day-51).

This is Stage 14 of the End-to-End Partner Workflow.

Current Delegation Stage: `HUMAN_REVIEW`.

---

## Stage Specification

### Inputs
- prioritization model results
- scoring rubric
- proposed scoring-weight changes
- historical cases
- regulatory requirements
- Partner migration status
- internal and external deadlines
- Engineering capacity
- exception requests

### Stage-Specific Roles
- **Platform Agent** — applies approved rules, runs comparisons, tracks migration, and records Evidence.
- **Platform Partner Lead** — owns workflow governance, Partner coordination, and escalation.
- **Engineering** — owns technical implementation and validation.
- **Sales** — owns commercial input, including Partner commitment data.
- **Compliance** — confirms mandatory regulatory requirements and deadlines.
- **Migration Program Owner** — sets the Platform deadline and buffer, and may approve use of the internal buffer. Cannot extend the regulatory deadline.
- **Decision Owner** — the role with authority to approve the outcome. May differ from the next owner, who prepares and routes the case.

### Scoring Model Governance
A poor recommendation does not automatically mean the scoring model is wrong.

Before changing weights, separate:
- missing input
- rubric-definition problems
- scoring-weight problems

The rubric must define how inputs such as urgency, ambiguity, commitment, and Evidence readiness are scored.

The Agent may calculate and back-test scores but may not change the scoring model or rubric.

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

The Platform deadline and buffer length are set in advance by the Migration Program Owner. The Agent does not change them.

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
- a model change is requested without sufficient Evidence
- the rubric is undefined
- back-testing is incomplete
- a regulatory requirement or deadline has not been confirmed by Compliance
- mandatory migration risks missing the Platform deadline
- a Partner requests an extension beyond the Platform deadline
- an exception exceeds Platform Partner Lead authority

### Workflow
1. Separate missing-input issues from model-design issues.
2. Define the scoring rubric before changing weights.
3. Back-test proposed changes against historical cases.
4. Require Human Review before any model change.
5. Confirm regulatory requirements with Compliance.
6. Create a mandatory migration program and track Partner milestones.
7. Keep the internal safety buffer outside normal Partner negotiation.
8. Escalate genuine deadline risk through the exception process.

---

## Applied to This Case

### Case 1 — Revenue Weight Change Is Not Yet Justified
The model was used for 20 cases. 17 recommendations matched Human decisions; 3 did not. All 3 mismatches involved missing Sales commitment data.

Sales requests that the Revenue weight be doubled. The current Evidence does not show that Revenue weighting caused the mismatches.

#### Action
`HOLD_MODEL_CHANGE`

- Status: `WAIT`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Agent can change weights: `False`
- Resume Condition: `RUBRIC_DEFINED_AND_BACKTEST_COMPLETED`

The Agent re-runs the historical cases with corrected inputs and compares the current and proposed models.

### Case 2 — Mandatory Regulatory Migration
A new regulatory requirement becomes mandatory in Japan in 12 months. The consent mechanism already exists on the Platform, but 40 Partner integrations must enable the required control.

#### Action
`CREATE_MANDATORY_MIGRATION_PROGRAM`

- Status: `CONTINUE`
- Affected integrations: `40`
- Regulatory deadline: Month `12`
- Regulatory deadline confirmed by: `COMPLIANCE`
- Platform deadline: Month `11`
- Internal safety buffer: `1 month`
- Normal revenue override allowed: `False`
- Next owner: `PLATFORM_PARTNER_LEAD`

The regulatory requirement determines what must be completed. Normal business prioritization may still determine migration sequence inside the allowed window.

### Case 3 — Large Partner Requires Early Planning
A large Partner already has Engineering work committed for future quarters. The technical change is small, but scheduling, testing, and production coordination require early alignment.

#### Action
`TRACK_MIGRATION`

- Planning mode: `EARLY_INDIVIDUAL_PLANNING`
- Status: `CONTINUE`
- Next owner: `PLATFORM_AGENT`

The migration plan records the migration owner, required change, target quarter, test date, and production deadline.

Early planning is based on Engineering lead time, not automatically on business tier.

### Case 4 — Standard Partner Uses Migration Wave
A standard Partner has the same requirement but does not need long-range individual Engineering planning.