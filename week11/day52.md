# Day 52: Clarification Retry and State Consistency Control

## Objective

Define how Agency Agent and Platform Agent handle repeated clarification, normalize Partner-side state, and stop only the workflow branch affected by unresolved evidence conflicts.

Common rules and AI–Human boundaries for Days 41–50 are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

Delegated Agent-to-Agent behavior from Day 51 onward is defined in the [Delegation Model](../AGENTS.md#delegation-model-day-51).

This is Stage 12 of the End-to-End Partner Workflow.

---

## Stage Specification

### Inputs

- Partner Human response
- Agency Agent clarification result
- Platform Agent validation result
- Partner-side current / authoritative state
- clarification round count
- conflicting authoritative values
- workflow branch dependencies

### Stage-Specific Role(s)

- **Partner Human:** Provides the authoritative business answer when Agent clarification cannot resolve ambiguity.
- **Agency Agent:** Normalizes Partner Human responses and corrects Partner-side state.
- **Platform Agent:** Validates structured Partner data, detects unresolved conflicts, controls branch-level workflow status, and escalates when retry limits are reached.
- **Platform Partner Lead:** Handles unresolved clarification after autonomous Agent-to-Agent retries are exhausted.

### Retry and Escalation Rule

Standard clarification may be handled autonomously between the Agency Agent and Platform Agent.

The current retry limit is:

`MAX_CLARIFICATION_ROUNDS = 2`

After the retry limit is reached without an authoritative value, autonomous clarification must stop and the case must escalate to the Platform Partner Lead.

The limit is set by the Platform Partner Lead. The Agents may not change it.

### Partner State Rule

A Partner Human answer should be normalized into structured state before the Platform workflow resumes.

The Agency Agent should maintain:

- authoritative value
- current value
- previous conflicting values
- conflict resolution status
- Partner ID / endpoint
- timestamp

Old conflicting values must no longer remain marked as current.

### Branch-Level Blocking Rule

If conflicting evidence affects only one downstream decision branch, only that branch should be blocked.

Unrelated workflow steps may continue.

This narrows the earlier rule of stopping on conflicting evidence: only the branch that depends on the conflicting value is blocked.

Branch dependencies are defined in advance by the Platform Partner Lead. The Platform Agent applies them and does not decide them case by case.

### Outputs

- clarification status
- authoritative value
- Partner-side state
- retry count
- escalation status
- blocked workflow branch
- Resume Condition

### Stop Conditions

Stop autonomous clarification and escalate when:

- the retry limit is reached without a verified authoritative value

Block the affected workflow branch, while clarification continues within the retry limit, when:

- no authoritative value has been returned yet
- Partner-side state is inconsistent
- multiple different authoritative values exist
- a required decision branch cannot safely continue

### Workflow

`Detect Conflict → Clarify → Normalize → Verify → Resume or Escalate`

---

## Applied to This Case

### Case

A Partner requests a temporary API limit increase from 320 rpm to 600 rpm.

Expected peak traffic is 520 rpm.

The duration of the peak is inconsistent:

- Partner email: 8 minutes
- launch plan: 20 minutes

The same Partner ID, endpoint, and launch are involved.

### Actions

#### Case 1: Clarification Retry Limit Reached

After two clarification rounds, the Partner Human replies:

> “Please use whichever value is safer.”

No authoritative duration is provided.

- Action: `ESCALATE_UNRESOLVED_CONFLICT`
- Status: `ESCALATED`
- Next owner: Platform Partner Lead
- Resume Condition: `AUTHORITATIVE_VALUE_CONFIRMED_BY_HUMAN`

The Agents stop autonomous clarification until a human-confirmed value is available.

#### Case 2: previous conflicting value: 8 minutes (superseded)

The Partner Human confirms:

> “20 minutes is correct. The earlier 8-minute email was outdated.”

The Agency Agent normalizes the response:

- authoritative value: 20 minutes
- current value: 20 minutes
- previous conflicting values: 8 / 20 minutes
- conflict resolved: Yes

The Platform Agent verifies the structured state.

- Action: `VERIFY_AND_RESUME`
- Status: `READY_TO_RESUME`
- Next owner: Platform Agent
- Resume Condition: `AUTHORITATIVE_VALUE_VERIFIED`

#### Case 3: Old Partner State Remains Current

The Partner Human confirms 20 minutes, but the Partner-side system still shows:

- 8 minutes → `current = true`
- 20 minutes → `authoritative = true`

The Platform Agent does not resume.

- Action: `CORRECT_PARTNER_STATE`
- Status: `BLOCKED`
- Next owner: Agency Agent
- Resume Condition: `OLD_VALUE_NOT_CURRENT_AND_NEW_VALUE_VERIFIED`

The Agency Agent corrects the Partner-side state before the workflow continues.

#### Case 4: Partner State Becomes Consistent

The Partner-side system is corrected:

- 8 minutes → `current = false`
- 20 minutes → `current = true`
- 20 minutes → `authoritative = true`

- Action: `VERIFY_PARTNER_STATE`
- Status: `READY_TO_RESUME`
- Next owner: Platform Agent
- Resume Condition: `PARTNER_STATE_CONSISTENT`

#### Case 5: Two Different Authoritative Values Exist

The Partner-side system contains:

- 20 minutes → `authoritative = true`
- 30 minutes → `authoritative = true`

Both belong to the same Partner ID / endpoint / launch.

The Platform Agent cannot safely choose one value.

Only the capacity-review branch depends on this duration.

- Action: `BLOCK_CAPACITY_REVIEW_BRANCH`
- Status: `WAITING_FOR_CLARIFICATION`
- Blocked branch: `CAPACITY_REVIEW`
- Next owner: Agency Agent
- Resume Condition: `SINGLE_AUTHORITATIVE_VALUE_VERIFIED`

Other unrelated workflow steps may continue.

Clarification counts toward `MAX_CLARIFICATION_ROUNDS`. If no single value is verified within the limit, Case 1 applies.

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

Record:

- clarification round count
- conflicting values
- Partner Human answer
- normalized authoritative value
- Partner-side state changes
- branch-level blocking
- escalation reason
- Resume Condition
- final conflict resolution

### Human Review Points

Humans should verify:

- autonomous clarification does not continue indefinitely
- Partner Human answers are normalized before reuse
- old conflicting state is removed
- multiple authoritative values do not silently enter downstream decisions
- only affected workflow branches are blocked
- unresolved ambiguity escalates after the retry limit

### Future Compatibility

This stage introduces a reusable Agent-to-Agent clarification pattern:

`Clarify → Normalize → Verify → Branch Resume or Human Escalation`

The same model can later support multiple Agents exchanging structured requirements and evidence before escalating only unresolved exceptions to humans.