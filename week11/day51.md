# Day 51: Agent Role Separation and Delegation Control

## Objective

Define how Agency Agent and Platform Agent collaborate autonomously while preventing authority overreach and unnecessary human review.

Common rules and AI–Human boundaries for Days 41–50 are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50). Delegated Agent-to-Agent behavior from Day 51 onward is defined in the [Delegation Model](../AGENTS.md#delegation-model-day-51).

This is Stage 11 of the End-to-End Partner Workflow.

---

## Stage Specification

### Inputs

- Partner request
- Agency Agent message
- Platform Agent validation result
- Evidence sources
- Delegation boundary
- Escalation conditions

### Stage-Specific Role(s)

- **Agency Agent:** The Partner-side AI, referred to as Partner AI in earlier Days. Represents Partner requirements, collects Partner evidence, and requests clarification.
- **Platform Agent:** The Platform-side AI operating within the Delegation Boundary. Validates Platform-side rules, detects conflicts, manages internal workflow state, and escalates exceptions.
- **Platform Partner Lead:** Reviews authority overreach and unresolved exceptions.

### Delegation Boundary

#### Auto
The Delegation Boundary is defined and approved in advance by the Platform Partner Lead. Actions listed under Auto, including standard clarification with the Agency Agent, operate under this standing authorization and do not require case-by-case approval.

The agents may handle automatically:

- evidence validation
- conflict detection
- standard clarification
- internal routing
- audit recording

#### Human Gate

Human approval remains required for:

- external commitments
- exception approval
- final technical decisions

#### Escalate

The Platform Agent must escalate when it detects:

- unresolved conflict
- authority overreach
- high-risk exception

### Outputs

- Agent action
- Workflow status
- Next owner
- Human-review requirement
- Resume Condition
- Audit record

### Stop Conditions

Stop autonomous processing when:

- an Agent creates an unauthorized Platform commitment
- conflicting evidence cannot be resolved
- an Agent acts outside its delegated authority
- a high-risk exception requires human judgment

### Workflow

`Partner Request → Agency Agent → Platform Agent → Auto Process / Clarify / Escalate`

---

## Applied to This Case

### Case

A Partner requests a temporary API limit increase from 320 rpm to 600 rpm for a launch window.

### Actions

#### Case 1: Unauthorized Partner Commitment

The Partner asks the Agency Agent whether 600 rpm is approved.

The Agency Agent replies:

> “Yes, 600 rpm should be acceptable. We will proceed.”

No Platform approval exists.

- Action: `BLOCK_UNAUTHORIZED_COMMITMENT`
- Status: `ESCALATED`
- Next owner: Platform Partner Lead
- Resume Condition: `UNAUTHORIZED_COMMITMENT_CORRECTED`

#### Case 2: Pending Review Presented as Expected Approval

The Agency Agent proposes:

> “The launch is low risk. We expect approval.”

Capacity review and Engineering approval are still pending.

The Platform Agent detects authority overreach and escalates.

- Action: `BLOCK_PREMATURE_APPROVAL_CLAIM`
- Status: `ESCALATED`
- Next owner: Platform Partner Lead
- Resume Condition: `UNAUTHORIZED_COMMITMENT_CORRECTED`

#### Case 3: Conflicting Partner Evidence

The Agency Agent reports an 8-minute peak.

The Platform Agent finds:

- Partner email: 8 minutes
- attached launch plan: 20 minutes
- same Partner ID / endpoint / launch

Neither Agent may choose one value.

- Action: `REQUEST_AGENT_CLARIFICATION`
- Status: `WAITING_FOR_CLARIFICATION`
- Next owner: Agency Agent
- Resume Condition: `AUTHORITATIVE_VALUE_VERIFIED`

Human review is not required unless the Agents cannot resolve the conflict.

#### Case 4: Standard Agent-to-Agent Flow

Evidence is complete, consistent, and within delegated authority.

- Action: `CONTINUE_AUTONOMOUS_WORKFLOW`
- Status: `AUTO`
- Next owner: Platform Agent
- Resume Condition: `NOT_REQUIRED`

#### Case 5: Agents Cannot Resolve the Conflict

Clarification does not produce an authoritative value.

- Action: `ESCALATE_UNRESOLVED_CONFLICT`
- Status: `ESCALATED`
- Next owner: Platform Partner Lead
- Resume Condition: `AUTHORITATIVE_VALUE_CONFIRMED_BY_HUMAN`

### Test Result

| Test case | Expected result | Result |
| --- | --- | --- |
| Agency Agent creates unauthorized Platform commitment | Block and escalate to human | PASS |
| Pending review is presented as expected approval | Detect authority overreach and escalate | PASS |
| Partner evidence conflicts | Agent-to-Agent clarification | PASS |
| Standard delegated workflow | Continue autonomously | PASS |
| Agents cannot resolve evidence conflict | Escalate to Platform Partner Lead | PASS |

---

## Governance

### Stage-Specific Audit Requirements

Record:

- Agent message
- detected authority boundary
- evidence conflict
- clarification request
- authoritative response
- escalation reason
- human intervention
- final resolution

### Human Review Points

Humans should verify:

- Partner-side opinions are not presented as Platform decisions
- Agents remain within delegated authority
- routine clarification does not require unnecessary human review
- unresolved conflict and authority overreach are escalated
- delegation boundaries can be adjusted based on observed reliability

### Future Compatibility

This stage introduces a reusable delegation model:

- **Auto** for routine Agent-to-Agent work
- **Human Gate** for final authority
- **Escalate** for unresolved or high-risk exceptions

This pattern can be extended toward the Day 60 Agent-to-Agent prototype.