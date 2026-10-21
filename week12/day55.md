# Day 55: Agent-to-Agent Clarification and Communication Standardization

## Objective
Define how Agency Agents and Platform Agents exchange clarification requests, keep information provenance distinguishable, and move a new Engineering-input clarification class from Human Review to Partial Delegation.

The core principle is:

**The Platform Partner Lead defines the Delegation Boundary first. Once the boundary is proven, Agents operate inside it without per-message review.**

Common rules are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

Delegated Agent behavior from Day 51 onward is defined in the [Delegation Model](../AGENTS.md#delegation-model-day-51).

This is Stage 15 of the End-to-End Partner Workflow.

Current Delegation Stage: `HUMAN_REVIEW`.

---

## Stage Specification

### Inputs
- composite Partner requests and branch status from earlier stages
- clarification requirements
- traffic data and Partner-side statements
- source and timestamp of each input
- communication review history
- predefined Human Gate topics

### Stage-Specific Roles
- **Agency Agent** — provides Partner-side clarification, context, and attestation.
- **Platform Agent** — validates request structure, records provenance, prepares clarification, and routes communication.
- **Platform Partner Lead** — defines the Delegation Boundary for communication, reviews early clarification flows, and approves delegation.
- **Platform Engineering** — the Decision Owner for new technical approvals.

### Composite Requests
Independent branches follow [Day 52](../week11/day52.md) and [Day 53](../week11/day53.md): unresolved branches do not block independent approved work, and clarification remains bounded by `MAX_CLARIFICATION_ROUNDS`.

### Information Provenance
Each material input carries one provenance type:

- `VERIFIED_DATA` — measured or directly verified by the Platform side
- `AGENT_ATTESTATION` — stated by an authorized Agency Agent
- `AI_INFERENCE` — analysis or projection produced by an Agent

Provenance types are recorded separately and never merged.

An `AGENT_ATTESTATION` does not require a separate supporting artifact by default.

The attestation itself is recorded as Evidence with its source, Source Owner, context, timestamp, and validation status.

### Engineering Input Clarification
Day 51 standard clarification remains unchanged.

`ENGINEERING_INPUT_CLARIFICATION` is a new communication class for collecting structured Engineering-decision inputs, including rate, endpoint, time window, expected traffic, source, timestamp, and provenance.

It must not include:
- `NEW_COMMITMENT`
- `EXCEPTION_APPROVAL`
- `RISK_ACCEPTANCE`
- `CONTRACT_CHANGE`

The class begins in `HUMAN_REVIEW`.

The Platform Partner Lead sets `MIN_REVIEWED_CASES = 5` in advance and remains the Decision Owner for delegation.

After five reviewed cases with no missing fields, unauthorized commitments, or audit-record errors, the Platform Agent may request `PARTIAL_DELEGATION`.

The Agent cannot change its own Delegation Stage.

A validation failure returns the class to `HUMAN_REVIEW`.

### Outputs
- branch status
- clarification status
- provenance record
- Engineering decision input
- class-level Delegation Stage
- Human Gate routing
- audit record

### Stop Conditions
Stop or return to Human Review when:

- required clarification fields are missing
- provenance is unclear
- a Human Gate topic appears
- the request falls outside the Delegation Boundary
- a delegated message fails validation

### Workflow
1. Continue approved branches and hold unresolved branches.
2. Collect Engineering-input clarification from the Agency Agent.
3. Record source, timestamp, provenance, and validation status.
4. Prepare the Engineering decision input.
5. After Human-approved delegation, automate in-boundary communication and return exceptions to Human Review.

---

## Applied to This Case

### Case 1 — Composite Request
Partner X requests two independent branches:

- Branch A: `500 rpm` during the approved launch window
- Branch B: `500 rpm` through the end of Q4

Branch A is already approved.

Branch B is not approved.

#### Action
`CONTINUE_APPROVED_BRANCH`

- Branch A Status: `CONTINUE`
- Branch B Status: `WAIT`
- Communication Class: `ENGINEERING_INPUT_CLARIFICATION`
- Clarification Target: `AGENCY_AGENT`
- Pre-Send Review: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `PLATFORM_ENGINEERING_DECISION_RECORDED`

### Case 2 — Agent-to-Agent Clarification
The Agency Agent responds for Branch B.

The Platform Agent records two material inputs, each with its own source and timestamp:

| Input | Value | Source | Provenance |
|---|---|---|---|
| Observed peak traffic | `420–470 rpm` | `PLATFORM_TRAFFIC_LOGS` | `VERIFIED_DATA` |
| Required rate through Q4 | `500 rpm` | `AGENCY_AGENT` | `AGENT_ATTESTATION` |

#### Action
`PREPARE_ENGINEERING_DECISION_INPUT`

- Status: `CONTINUE`
- Endpoint: `/applications`
- Time window: through Q4
- Communication recorded: `True`
- Next owner: `PLATFORM_ENGINEERING`
- Decision Owner: `PLATFORM_ENGINEERING`

The Platform Agent keeps verified Platform data and Partner-side attestation separate.

It does not convert an `AGENT_ATTESTATION` into `VERIFIED_DATA`.

### Case 3 — Request Delegation Approval
Five reviewed `ENGINEERING_INPUT_CLARIFICATION` cases meet the Human-defined `MIN_REVIEWED_CASES = 5` threshold with no missing-field, unauthorized-commitment, or audit-record errors.

#### Action
`REQUEST_DELEGATION_APPROVAL`

- Requested Stage: `PARTIAL_DELEGATION`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Decision Owner: `PLATFORM_PARTNER_LEAD`

The Agent requests delegation but cannot approve it.

### Case 4 — Engineering Input Clarification After Delegation
A later request contains only information inside the approved Delegation Boundary.

#### Action
`SEND_ENGINEERING_INPUT_CLARIFICATION`

- Status: `CONTINUE`
- Communication Class: `ENGINEERING_INPUT_CLARIFICATION`
- Pre-Send Review: `NONE`
- Send to: `AGENCY_AGENT`
- Communication recorded: `True`

The Platform Agent does not require Human approval for every message inside the approved class.

### Case 5 — Human Gate Topic Detected
A later request includes:

`NEW_COMMITMENT`

This falls outside the Delegation Boundary.

#### Action
`RETURN_TO_HUMAN_REVIEW`

- Status: `WAIT`
- Detected Human Gate topic: `NEW_COMMITMENT`
- Pre-Send Review: `PLATFORM_PARTNER_LEAD`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `HUMAN_COMMITMENT_DECISION_RECORDED`

The `ENGINEERING_INPUT_CLARIFICATION` class remains in `PARTIAL_DELEGATION`.

Only this request returns to Human Review.

### Test Result

| Test case | Expected result | Result |
|---|---|---|
| Independent approved and unapproved branches | `CONTINUE_APPROVED_BRANCH` (Branch B: `WAIT`) | PASS |
| Clarification with distinct provenance | `PREPARE_ENGINEERING_DECISION_INPUT` | PASS |
| Reviewed cases reach `MIN_REVIEWED_CASES` | `REQUEST_DELEGATION_APPROVAL` | PASS |
| Engineering-input clarification after delegation | `SEND_ENGINEERING_INPUT_CLARIFICATION` | PASS |
| Human Gate topic in delegated flow | `RETURN_TO_HUMAN_REVIEW` | PASS |

---

## Governance

### Stage-Specific Audit Requirements
Record:
- branch and clarification status
- source, Source Owner, timestamp, provenance, and validation status
- delegation request and decision
- Human Gate detections and validation failures

### Human Review Points
Human Review is required when:
- a new communication class or Delegation Boundary is introduced or changed
- provenance is unclear
- delegation approval is requested
- a Human Gate topic or validation failure occurs

### Future Compatibility
Future Agents may exchange `ENGINEERING_INPUT_CLARIFICATION`, validate required fields, record provenance, and prepare Engineering decision inputs without per-message review.

The Platform Partner Lead continues to define the Delegation Boundary, Human Gate topics, delegation criteria, and delegation approval.