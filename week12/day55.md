# Day 55: Agent-to-Agent Clarification and Communication Standardization

## Objective
Define how Agency Agents and Platform Agents exchange clarification requests, keep information provenance distinguishable, and move a standard communication class from Human Review to Partial Delegation.

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
Independent branches are handled as defined in [Day 52](../week11/day52.md) and [Day 53](../week11/day53.md). An unapproved branch does not block an approved independent branch. Clarification rounds remain limited by `MAX_CLARIFICATION_ROUNDS`.

### Information Provenance
Each material input carries one provenance type:

- `VERIFIED_DATA` — measured or directly verified by the Platform side
- `AGENT_ATTESTATION` — stated by an authorized Agency Agent
- `AI_INFERENCE` — analysis or projection produced by an Agent

Provenance types are recorded separately and never merged.

An `AGENT_ATTESTATION` does not require a separate supporting artifact by default.

The attestation itself is recorded as Evidence with its source, Source Owner, context, timestamp, and validation status.

### Standard Clarification Communication
The `STANDARD_CLARIFICATION_COMMUNICATION` class may contain the requested rate, endpoint, time window, expected traffic, and the source, timestamp, and provenance of each input.

It must not contain any Human Gate topic:
- `NEW_COMMITMENT`
- `EXCEPTION_APPROVAL`
- `RISK_ACCEPTANCE`
- `CONTRACT_CHANGE`

### Delegation Rule
A Delegation Stage can be set for a single communication class, not for one fixed message. The Current Delegation Stage of the workflow does not change.

The class starts in `HUMAN_REVIEW`. The Platform Partner Lead sets `MIN_REVIEWED_CASES = 5` in advance.

When reviewed cases reach `MIN_REVIEWED_CASES` with:
- no missing required fields
- no unauthorized commitments
- no audit-record errors

the Platform Agent requests approval to move the class to `PARTIAL_DELEGATION`. The Platform Partner Lead is the Decision Owner.

If a delegated message fails validation, the class returns to `HUMAN_REVIEW`. Only the Platform Partner Lead can delegate it again.

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
2. Record provenance for each material input and prepare decision input for Platform Engineering.
3. Route clarification through Human Review until delegation is approved.
4. Request delegation approval when `MIN_REVIEWED_CASES` is met.
5. After approval, send standard clarification directly and return Human Gate topics and failed validations to Human Review.

---

## Applied to This Case

### Case 1 — Composite Request
Partner X requests two independent branches:

- Branch A: `500 rpm` during the approved launch window (approved)
- Branch B: `500 rpm` through the end of Q4 (not approved)

#### Action
`CONTINUE_APPROVED_BRANCH`

- Branch A Status: `CONTINUE`
- Branch B Status: `WAIT`
- Clarification Target: `AGENCY_AGENT`
- Pre-Send Review: `PLATFORM_PARTNER_LEAD`
- Resume Condition: Platform Engineering decides on Branch B.

### Case 2 — Agent-to-Agent Clarification
The Agency Agent responds for Branch B. The Platform Agent records three inputs, each with a timestamp:

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

### Case 3 — Request Delegation Approval
Five reviewed cases in the class show `0` missing-field errors, `0` unauthorized commitments, and `0` audit-record errors.

#### Action
`REQUEST_DELEGATION_APPROVAL`

- Communication Class: `STANDARD_CLARIFICATION_COMMUNICATION`
- Reviewed Cases: `5` (`MIN_REVIEWED_CASES = 5`)
- Requested Stage: `PARTIAL_DELEGATION`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Decision Owner: `PLATFORM_PARTNER_LEAD`

The Platform Agent does not change the stage itself. After approval, the class moves to `PARTIAL_DELEGATION`.

### Case 4 — Standard Clarification After Delegation
A later request asks only for information inside the class.

#### Action
`SEND_STANDARD_CLARIFICATION`

- Status: `CONTINUE`
- Pre-Send Review: `NONE`
- Send to: `AGENCY_AGENT`
- Communication recorded: `True`

### Case 5 — Human Gate Topic Detected
A later request includes `NEW_COMMITMENT`.

#### Action
`RETURN_TO_HUMAN_REVIEW`

- Status: `WAIT`
- Detected Human Gate topic: `NEW_COMMITMENT`
- Pre-Send Review: `PLATFORM_PARTNER_LEAD`
- Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: The Platform Partner Lead decides on the commitment and records the decision.

The class stays in `PARTIAL_DELEGATION`. Only this request returns to Human Review.

### Test Result

| Test case | Expected result | Result |
|---|---|---|
| Independent approved and unapproved branches | `CONTINUE_APPROVED_BRANCH` (Branch B: `WAIT`) | PASS |
| Clarification with three provenance types | `PREPARE_ENGINEERING_DECISION_INPUT` | PASS |
| Reviewed cases reach `MIN_REVIEWED_CASES` | `REQUEST_DELEGATION_APPROVAL` | PASS |
| Standard clarification after delegation | `SEND_STANDARD_CLARIFICATION` | PASS |
| Human Gate topic in a delegated flow | `RETURN_TO_HUMAN_REVIEW` | PASS |

---

## Governance

### Stage-Specific Audit Requirements
Record:
- request branch and branch status
- clarification request and required fields
- source, timestamp, and provenance type of each input
- Human review history
- delegation request and decision
- Human Gate detections
- validation failures and class returns to `HUMAN_REVIEW`

### Human Review Points
Human Review is required when:
- a communication class is first introduced
- the Delegation Boundary changes
- provenance is unclear
- a Human Gate topic appears
- a delegated message fails validation

### Future Compatibility
Future Agents may exchange standard clarification, validate required fields, record provenance, and prepare Engineering decision inputs without per-message review.

The Platform Partner Lead continues to:
- define communication classes and allowed fields
- define Human Gate topics
- set delegation criteria, including `MIN_REVIEWED_CASES`
- approve or withdraw delegation