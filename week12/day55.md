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
Independent branches are handled as defined in [Day 52](../week11/day52.md) and [Day 53](../week11/day53.md).

An unapproved branch does not block an approved independent branch.

Clarification rounds remain limited by `MAX_CLARIFICATION_ROUNDS`.

### Information Provenance
Each material input carries one provenance type:

- `VERIFIED_DATA` — measured or directly verified by the Platform side
- `AGENT_ATTESTATION` — stated by an authorized Agency Agent
- `AI_INFERENCE` — analysis or projection produced by an Agent

Provenance types are recorded separately and never merged.

An `AGENT_ATTESTATION` does not require a separate supporting artifact by default.

The attestation itself is recorded as Evidence with its source, Source Owner, context, timestamp, and validation status.

### Engineering Input Clarification
Standard clarification under the Day 51 standing authorization is unchanged; this is a new class.

The `ENGINEERING_INPUT_CLARIFICATION` class collects structured information required for a Platform Engineering decision.

It may contain:
- requested rate
- endpoint
- time window
- expected traffic
- source
- timestamp
- provenance of each material input

It must not contain any Human Gate topic:

- `NEW_COMMITMENT`
- `EXCEPTION_APPROVAL`
- `RISK_ACCEPTANCE`
- `CONTRACT_CHANGE`

### Delegation Rule
A Delegation Stage can be set for a communication class, not for one fixed message.

The workflow itself remains in `HUMAN_REVIEW`.

A new `ENGINEERING_INPUT_CLARIFICATION` class begins in `HUMAN_REVIEW`.

The Platform Partner Lead sets the minimum validation requirement in advance:

`MIN_REVIEWED_CASES = 5`

When reviewed cases reach `MIN_REVIEWED_CASES` with:

- no missing required fields
- no unauthorized commitments
- no audit-record errors

the Platform Agent may request delegation approval.

The Platform Agent does not change the class Delegation Stage.

The Platform Partner Lead is the Decision Owner for moving the class to `PARTIAL_DELEGATION`.

After approval, messages inside the approved Delegation Boundary no longer require per-message Human Review.

If a delegated message fails validation, the class returns to `HUMAN_REVIEW`.

Only the Platform Partner Lead may approve delegation again.

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
1. Continue approved branches and hold unapproved branches for clarification.
2. Collect required Engineering-input clarification from the Agency Agent.
3. Record source, timestamp, and provenance for each material input.
4. Prepare structured decision input for Platform Engineering.
5. Route the new communication class through Human Review until delegation criteria are met.
6. Request delegation approval from the Platform Partner Lead.
7. After approval, send Engineering-input clarification directly inside the Delegation Boundary.
8. Return Human Gate topics and failed validations to Human Review.

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
Five reviewed cases in the `ENGINEERING_INPUT_CLARIFICATION` class show:

- `0` missing-field errors
- `0` unauthorized commitments
- `0` audit-record errors

The human-defined minimum is:

`MIN_REVIEWED_CASES = 5`

#### Action
`REQUEST_DELEGATION_APPROVAL`

- Communication Class: `ENGINEERING_INPUT_CLARIFICATION`
- Reviewed Cases: `5`
- Requested Stage: `PARTIAL_DELEGATION`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Decision Owner: `PLATFORM_PARTNER_LEAD`

The Platform Agent does not change the class Delegation Stage itself.

After Human approval, the class moves to `PARTIAL_DELEGATION`.

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

- request branch and branch status
- clarification request and required fields
- source, Source Owner, timestamp, provenance type, and validation status of each material input
- Human review history
- delegation request and decision
- Human Gate detections
- validation failures and class returns to `HUMAN_REVIEW`

### Human Review Points
Human Review is required when:

- a new communication class is introduced
- the Delegation Boundary changes
- provenance is unclear
- delegation approval is requested
- a Human Gate topic appears
- a delegated message fails validation

### Future Compatibility
Future Agents may exchange `ENGINEERING_INPUT_CLARIFICATION`, validate required fields, record provenance, and prepare Engineering decision inputs without per-message review.

The Platform Partner Lead continues to:

- define communication classes
- define the Delegation Boundary
- define Human Gate topics
- set delegation criteria, including `MIN_REVIEWED_CASES`
- approve or withdraw delegation