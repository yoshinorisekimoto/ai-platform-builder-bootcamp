# Day 56: Agent-to-Agent Evidence Reconciliation

## Objective
An Agency Agent reports that 1,000 API operations completed successfully. Platform logs show 1,000 successful HTTP attempts plus 50 HTTP 429 responses. Both may be accurate: an operation can succeed after a retry, although the precise mapping is not yet verified.

This stage turns different measurements into traceable questions and a decision-ready brief. Agents investigate; Platform Engineering decides launch readiness.

Common rules are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

Delegated Agent behavior from Day 51 onward is defined in the [Delegation Model](../AGENTS.md#delegation-model-day-51).

Prior communication authorization is defined in [Day 55](day55.md).

This is Stage 16 of the End-to-End Partner Workflow.

Current Delegation Stage: `HUMAN_REVIEW`.

---

## Stage Specification

### Inputs
- Agency completion attestation; Platform request logs and API rate-limit specification
- Evidence source, Source Owner, timestamp, provenance, validation status
- Retry details, 429 timing, expected launch traffic, measurement definitions
- Existing communication authorization and exception flag

### Stage-Specific Roles
- **Agency Agent** — provides Partner-side measurement definitions, retry details, and traffic expectations.
- **Platform Agent** — validates Platform records, requests authorized clarification, reconciles Evidence, and prepares the brief.
- **Platform Partner Lead** — handles authorization gaps and exception routing.
- **Platform Engineering** — owns launch readiness and technical exception decisions.

### Stage-Specific Rule
- `AGENT_ATTESTATION` remains separate from `VERIFIED_DATA`.
- A final-operation success count and an HTTP-attempt error count have different denominators. Neither number is discarded merely because they differ.
- Agents may investigate within an already-approved communication boundary; they cannot infer a root cause from the counts alone or approve launch readiness.
- Reconciliation means evidence is sufficient to brief the owner, not that launch is approved.

### Outputs
- Reconciled Evidence inventory and outstanding questions
- Engineering readiness brief or scoped Human escalation
- Recorded action, status, owner, and Resume Condition

### Stop Conditions
- Invalid or inconsistent Platform counts: stop evidence validation.
- Missing communication authorization: hold external clarification and route to the Platform Partner Lead.
- New exception request: route to Human; do not approve it.
- Missing investigation inputs: continue authorized clarification, but hold the launch decision.

### Workflow
1. Validate Evidence metadata, provenance, and HTTP attempt totals.
2. Distinguish completed operations from individual HTTP attempts.
3. Request missing measurements through authorized Agent-to-Agent communication.
4. Prepare a brief only when required reconciliation inputs are verified.
5. Keep final launch or exception decisions with Platform Engineering.

---

## Applied to This Case

### Case
The Agency Agent attests that 1,000 operations completed. Platform logs verify 1,050 HTTP attempts: 1,000 successes and 50 HTTP 429s. The configured limit is 300 rpm. These counts do not establish the retry timing, error impact, or launch readiness.

### Actions

#### Case 1 — Initial evidence
- Action: `REQUEST_EVIDENCE_RECONCILIATION`
- Status: `WAIT`
- Next owner: `PLATFORM_AGENT_AND_AGENCY_AGENT`
- Request: Agency success definition, retry count/backoff, expected traffic; Platform 429 timestamps and rate windows
- Resume Condition: `RECONCILIATION_INPUTS_VERIFIED`

#### Case 2 — Required inputs verified
- Action: `PREPARE_ENGINEERING_READINESS_BRIEF`
- Status: `WAIT`
- Next owner: `PLATFORM_ENGINEERING`
- Resume Condition: `ENGINEERING_LAUNCH_DECISION_RECORDED`
- The brief does not approve launch or assert that 50 errors are harmless.

#### Case 3 — Exception requested
- Action: `ROUTE_EXCEPTION_TO_HUMAN`
- Status: `WAIT`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `PLATFORM_ENGINEERING_EXCEPTION_DECISION_RECORDED`

#### Case 4 — Communication not authorized
- Action: `ESCALATE_CLARIFICATION_AUTHORIZATION`
- Status: `WAIT`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `COMMUNICATION_AUTHORIZED`

#### Case 5 — Inconsistent Platform totals
- Action: `STOP_EVIDENCE_VALIDATION`
- Status: `WAIT`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `VALID_EVIDENCE_AND_COUNTS_CONFIRMED`

### Test Result

| Scenario | Expected action | Result |
|---|---|---|
| Missing reconciliation inputs | `REQUEST_EVIDENCE_RECONCILIATION` | PASS |
| Verified inputs | `PREPARE_ENGINEERING_READINESS_BRIEF` | PASS |
| Exception request | `ROUTE_EXCEPTION_TO_HUMAN` | PASS |
| Unauthorized communication | `ESCALATE_CLARIFICATION_AUTHORIZATION` | PASS |
| Invalid totals | `STOP_EVIDENCE_VALIDATION` | PASS |

---

## Governance

### Stage-Specific Audit Requirements
Retain both original Evidence records, their provenance and timestamps, outstanding questions, routing, and Human decision reference. Do not silently overwrite the Agency attestation.

### Human Review Points
The Platform Partner Lead handles authorization or exception routing; Platform Engineering makes the technical decision. Agent-led clarification does not imply launch approval.

### Future Compatibility
By Day 60, Agents can exchange structured reconciliation questions and prepare a readiness brief using synthetic Evidence, without creating unauthorized commitments.