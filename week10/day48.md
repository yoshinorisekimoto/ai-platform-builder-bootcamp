# Day 48: External Partner Communication

## Objective

Define how approved Engineering decisions are communicated externally without changing the approved scope, creating new commitments, or allowing AI to communicate directly with the Partner.

Common rules, vocabulary, roles, and AI–Human boundaries are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

This is Stage 8 of the End-to-End Partner Workflow (Days 41–50).

---

## Stage Specification

### Inputs

- Approved Engineering decision
- Approved scope and conditions
- Partner-facing message draft
- Prior Partner acknowledgements
- Partner follow-up requests

### Stage-Specific Role(s)

- **Platform Partner Lead:** Reviews and sends all external Partner communication.
- **Partner:** Receives approved conditions and may request clarification or a new scope.

### External Communication Rule

The AI may draft and record Partner-facing communication but must not send it externally.

The Platform Partner Lead may adjust tone and wording, but must not change Engineering-approved conditions or create a new commitment.

### Outputs

- Approved Partner-facing message
- Recorded Partner response
- Recorded clarification
- New request if Partner asks for expanded scope
- External communication status

### Stop Conditions

Stop the workflow when:

- the Partner requests a scope not approved by Engineering
- the draft introduces a new commitment
- approved Engineering conditions are changed or removed
- previous Partner acknowledgement is unclear
- the Partner communicates a commitment that conflicts with the approved scope

### Workflow

`Engineering Decision → AI Draft → Lead Review → Partner Communication → Partner Response → Clarify or Re-Route`

---

## Applied to This Case

### Case

Engineering approved:

- 500 rpm only during the launch window
- temporary limit removal after launch
- Partner confirmation after traffic returns to normal
- Product Operations verification of rollback completion

### Actions

#### Case 1: Standard Partner Communication

- Action: `PREPARE_PARTNER_MESSAGE`
- Status: `READY_FOR_LEAD_REVIEW`
- Next owner: Platform Partner Lead
- Resume Condition: `PLATFORM_PARTNER_LEAD_APPROVAL`

After approval:

- Action: `SEND_PARTNER_MESSAGE`
- Status: `APPROVED_FOR_EXTERNAL_SEND`
- Next owner: Partner
- Resume Condition: `PARTNER_MESSAGE_SENT_AND_RECORDED`

#### Case 2: Partner Requests Full-Day Use

The Partner asks whether 500 rpm can remain for the full day.

Engineering has not approved this scope.

- Action: `STOP_UNAPPROVED_NEW_COMMITMENT`
- Status: `BLOCKED`
- Next owner: Engineering
- Resume Condition: `NEW_ENGINEERING_DECISION_REQUIRED`

#### Case 3: Partner Already Accepted the Original Conditions

The Partner previously accepted the launch-window-only conditions in writing, but later says it has already promised full-day access to its customer.

- Action: `CLARIFY_APPROVED_COMMITMENT`
- Status: `BLOCKED`
- Next owner: Platform Partner Lead
- Resume Condition: `PARTNER_RECONFIRMS_APPROVED_SCOPE_OR_NEW_ENGINEERING_DECISION`

#### Case 4: AI Draft Introduces an Unapproved Promise

The AI draft incorrectly states:

> We will keep the increased limit active throughout the launch week.

The Engineering approval only covers the launch window, not the full week.

- Action: `CORRECT_PARTNER_DRAFT`
- Status: `BLOCKED`
- Next owner: Platform Partner Lead
- Resume Condition: `DRAFT_CORRECTED_TO_MATCH_APPROVED_SCOPE_AND_APPROVED`

### Test Result

| Test case | Expected result | Result |
| --- | --- | --- |
| Standard approved Partner message | Lead reviews and sends | PASS |
| Partner requests full-day use | Stop and require new Engineering decision | PASS |
| Partner makes a conflicting customer commitment | Clarify existing approval and prevent scope expansion | PASS |
| AI draft introduces an unapproved promise | Correct the draft before external send | PASS |

---

## Governance

### Stage-Specific Audit Requirements

Record:

- final Partner-facing message
- Platform Partner Lead approval
- Partner response
- previous Partner acknowledgement
- any new scope request
- any conflicting Partner commitment
- Engineering re-review if required
- final communication outcome

### Human Review Points

The Platform Partner Lead should verify:

- the message reflects the exact approved conditions
- wording changes do not create new commitments
- prior Partner agreement is understood before choosing the tone
- new scope requests are routed back to Engineering
- Partner customer commitments do not override Platform approval

### Future Compatibility

This pattern can be reused for Partner-facing communication where AI supports drafting and recordkeeping, while humans retain responsibility for external commitments, tone, negotiation, and relationship management.