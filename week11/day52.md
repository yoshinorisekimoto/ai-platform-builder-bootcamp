# Day 52: Clarification Retry and State Consistency Control

## Objective

Define how the Agency Agent and Platform Agent handle repeated clarification, normalize Partner-side state, and block only the workflow branch affected by an unresolved conflict.

Common rules and AI–Human boundaries for Days 41–50 are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50). Delegated Agent-to-Agent behavior from Day 51 onward is defined in the [Delegation Model](../AGENTS.md#delegation-model-day-51).

This is Stage 12 of the End-to-End Partner Workflow.

---

## Stage Specification

### Inputs

Partner Human response, Agency Agent clarification result, Platform Agent validation result, Partner-side current / authoritative state, clarification round count, branch dependencies.

### Stage-Specific Role(s)

- **Partner Human:** Provides the authoritative business answer when Agent clarification cannot resolve the ambiguity.
- **Agency Agent:** Normalizes Partner Human responses and corrects Partner-side state.
- **Platform Agent:** Validates Partner data, detects unresolved conflicts, controls branch-level status, and escalates when the retry limit is reached.
- **Platform Partner Lead:** Handles unresolved clarification after autonomous retries are exhausted.

### Retry and Escalation Rule

Standard clarification may run autonomously between the two Agents, up to:

`MAX_CLARIFICATION_ROUNDS = 2`

If no verified authoritative value exists after the limit, autonomous clarification stops and the case escalates to the Platform Partner Lead. The limit is set by the Platform Partner Lead; the Agents may not change it.

### Partner State Rule

Before the workflow resumes, the Agency Agent normalizes the Partner Human answer into structured state: authoritative value, current value, previous conflicting values, resolution status, Partner ID / endpoint, and timestamp. A superseded value must no longer be marked as current.

### Branch-Level Blocking Rule

If a conflict affects only one downstream decision branch, only that branch is blocked; unrelated steps may continue. This narrows the earlier rule of stopping on conflicting evidence.

Branch dependencies are defined in advance by the Platform Partner Lead. The Platform Agent applies them and does not decide them case by case.

### Outputs

Clarification status, authoritative value, Partner-side state, retry count, escalation status, blocked branch, Resume Condition.

### Stop Conditions

Stop autonomous clarification and escalate when:

- the retry limit is reached without a verified authoritative value

Block the affected branch, while clarification continues within the limit, when:

- no authoritative value has been returned yet
- Partner-side state is inconsistent
- multiple different authoritative values exist
- a required decision branch cannot safely continue

### Workflow

`Detect Conflict → Clarify → Normalize → Verify → Resume or Escalate`

---

## Applied to This Case

### Case

A Partner requests a temporary limit increase from 320 rpm to 600 rpm (expected peak: 520 rpm). The peak duration is inconsistent for the same Partner ID, endpoint, and launch: 8 minutes in the Partner email, 20 minutes in the launch plan.

### Actions

#### Case 1: Retry Limit Reached

After two rounds, the Partner Human replies: “Please use whichever value is safer.” No authoritative duration is provided.

- Action: `ESCALATE_UNRESOLVED_CONFLICT`
- Status: `ESCALATED`
- Next owner: Platform Partner Lead
- Resume Condition: `AUTHORITATIVE_VALUE_CONFIRMED_BY_HUMAN`

#### Case 2: Partner Human Provides an Authoritative Value

The Partner Human confirms: “20 minutes is correct. The earlier 8-minute email was outdated.” The Agency Agent records 20 minutes as the authoritative and current value, 8 minutes as the previous conflicting value (superseded), and the conflict as resolved.

- Action: `VERIFY_AND_RESUME`
- Status: `READY_TO_RESUME`
- Next owner: Platform Agent
- Resume Condition: `AUTHORITATIVE_VALUE_VERIFIED`

#### Case 3: Old Partner State Remains Current

The Partner Human confirms 20 minutes, but the Partner-side system still shows 8 minutes as `current = true`, while 20 minutes is only `authoritative = true`.

- Action: `CORRECT_PARTNER_STATE`
- Status: `BLOCKED`
- Next owner: Agency Agent
- Resume Condition: `OLD_VALUE_NOT_CURRENT_AND_NEW_VALUE_VERIFIED`

#### Case 4: Partner State Becomes Consistent

The Partner-side system now shows 8 minutes as `current = false`, and 20 minutes as both `current = true` and `authoritative = true`.

- Action: `VERIFY_PARTNER_STATE`
- Status: `READY_TO_RESUME`
- Next owner: Platform Agent
- Resume Condition: `PARTNER_STATE_CONSISTENT`

#### Case 5: Two Authoritative Values Exist

The Partner-side system marks both 20 and 30 minutes as `authoritative = true`. The Platform Agent cannot choose one. Only the capacity-review branch depends on this duration, so other steps continue.

- Action: `BLOCK_CAPACITY_REVIEW_BRANCH`
- Status: `WAITING_FOR_CLARIFICATION`
- Blocked branch: `CAPACITY_REVIEW`
- Next owner: Agency Agent
- Resume Condition: `SINGLE_AUTHORITATIVE_VALUE_VERIFIED`

This clarification counts toward `MAX_CLARIFICATION_ROUNDS`. If no single value is verified within the limit, Case 1 applies.

### Test Result

| Test case | Expected result | Result |
| --- | --- | --- |
| Retry limit reached without authoritative answer | Escalate to Platform Partner Lead | PASS |
| Partner Human confirms authoritative value | Normalize and verify before resume | PASS |
| Old conflicting value remains current | Correct Partner-side state | PASS |
| Partner-side state becomes consistent | Resume Platform workflow | PASS |
| Two different authoritative values exist | Block capacity-review branch only | PASS |

---

## Governance

### Stage-Specific Audit Requirements

Record: clarification round count, conflicting values, Partner Human answer, normalized authoritative value, Partner-side state changes, branch-level blocking, escalation reason, Resume Condition, final resolution.

### Human Review Points

Humans should verify: