
# Day 59: Standard Work, Exception Tickets, and Human Authorization

## Objective
A synthetic Commerce SaaS partner requests a three-day API integration review instead of the standard two weeks. The partner marks the request `CRITICAL`, but the Platform has not approved an exception. Other standard integration tasks can proceed independently.

This stage separates routine Agent execution from Human exception handling and uses past decisions as reference Evidence—not transferable approvals.

Common rules: [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50) and [Delegation Model](../AGENTS.md#delegation-model-day-51). Prior Agent communication rules: [Day 55](day55.md).

This is Stage 19 of the End-to-End Partner Workflow.

Current Delegation Stage: `HUMAN_REVIEW`.

---

## Stage Specification

### Inputs
- Standard-work authorization; requested review period and exception flag
- Partner-submitted Exception Ticket, business rationale, impact, and declared priority
- Prior comparable decisions, repeated-pattern indicator, case-specific Human approval
- Evidence provenance, owner, timestamp, and validation status

### Stage-Specific Roles
- **Agency Agent** — exchanges authorized standard requirements with the Platform Agent.
- **Partner Human** — submits the exception rationale and self-assessed priority.
- **Platform Agent** — continues authorized work, records tickets, and prepares Human decision inputs.
- **Platform Partner Lead** — assesses business value and priority, coordinates the exception, and owns Partner communication.
- **Platform Engineering** — decides technical feasibility and any review-period exception.

### Stage-Specific Rule
- Standard API and authentication work continues independently of an exception request.
- Agents explain standard terms and direct exceptions to a Partner Human-submitted Ticket; they do not negotiate or approve expedited review.
- `NORMAL`, `URGENT`, and `CRITICAL` are Partner-declared labels, not Platform-approved priority.
- A prior approval is reference Evidence, never authorization for a different Partner.
- Repeated cases may support a Human-reviewed standardization proposal, not automatic policy or delegation changes.

### Outputs
- Per-branch status, action, next owner, and Resume Condition
- Exception Ticket or Human decision brief, with supporting Evidence
- Recorded approval and Partner notification when available

### Stop Conditions
- No standard-work authorization: hold that work and request authorization.
- No Human-submitted Ticket: hold the exception branch and explain the submission route.
- Missing business context: route the Ticket to the Platform Partner Lead for assessment.
- No case-specific approval: do not promise an expedited review.

### Workflow
1. Separate the standard-work branch from the exception branch.
2. Continue authorized standard work; provide the Exception Ticket route when required.
3. Record declared priority and available business Evidence without assigning Platform priority.
4. Route the exception to the Platform Partner Lead and Engineering for their respective decisions.
5. Use historical cases only to inform a Human-reviewed decision or standardization proposal.
6. After recorded case approval, prepare notice for the Platform Partner Lead.

---

## Applied to This Case

### Case
Partner A requests a three-day review rather than two weeks, citing a major customer launch. The self-declared priority is `CRITICAL`; business impact and feasibility require Human assessment. A similar prior approval for another Partner does not authorize this case. All scenarios use synthetic inputs.

### Actions

#### Case 1 — Standard request only
- Action: `CONTINUE_AUTHORIZED_STANDARD_WORK`
- Status: `CONTINUE`; Next owner: `PLATFORM_AGENT`
- Resume Condition: `STANDARD_WORK_RECORDED`

#### Case 2 — Exception Ticket needed
- Action: `DIRECT_PARTNER_TO_EXCEPTION_TICKET`
- Status: `WAIT`; Next owner: `PARTNER_HUMAN`
- Resume Condition: `EXCEPTION_TICKET_SUBMITTED`

#### Case 3 — Ticket lacks business impact
- Action: `ROUTE_TICKET_FOR_HUMAN_ASSESSMENT`
- Status: `WAIT`; Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `BUSINESS_IMPACT_ASSESSED_BY_HUMAN`

#### Case 4 — Ticket ready for Human review
- Action: `PREPARE_HUMAN_EXCEPTION_DECISION`
- Status: `WAIT`; Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `PLATFORM_ENGINEERING_AND_PARTNER_LEAD_DECISIONS_RECORDED`

#### Case 5 — Similar prior approval
- Action: `PREPARE_HUMAN_EXCEPTION_DECISION`
- Status: `WAIT`; Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `PLATFORM_ENGINEERING_AND_PARTNER_LEAD_DECISIONS_RECORDED`
- Prior approval is reference Evidence only.

#### Case 6 — Repeated exception pattern
- Action: `PROPOSE_STANDARDIZATION_FOR_HUMAN_REVIEW`
- Status: `PROVISIONAL`; Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `HUMAN_POLICY_AND_CASE_DECISIONS_RECORDED`

#### Case 7 — Case-specific Human approval recorded
- Action: `PREPARE_APPROVED_EXCEPTION_NOTICE`
- Status: `CONTINUE`; Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `PARTNER_NOTICE_RECORDED`

#### Case 8 — Standard work not authorized
- Action: `ROUTE_STANDARD_WORK_AUTHORIZATION`
- Status: `WAIT`; Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `STANDARD_WORK_AUTHORIZED`

### Test Result

| Scenario | Expected action | Result |
|---|---|---|
| Standard only | `CONTINUE_AUTHORIZED_STANDARD_WORK` | PASS |
| Ticket needed | `DIRECT_PARTNER_TO_EXCEPTION_TICKET` | PASS |
| Impact missing | `ROUTE_TICKET_FOR_HUMAN_ASSESSMENT` | PASS |
| Ticket ready | `PREPARE_HUMAN_EXCEPTION_DECISION` | PASS |
| Prior approval | `PREPARE_HUMAN_EXCEPTION_DECISION` | PASS |
| Repeated pattern | `PROPOSE_STANDARDIZATION_FOR_HUMAN_REVIEW` | PASS |
| Case approved | `PREPARE_APPROVED_EXCEPTION_NOTICE` | PASS |
| Standard unauthorized | `ROUTE_STANDARD_WORK_AUTHORIZATION` | PASS |

All tested outputs use `WAIT`, `PROVISIONAL`, or `CONTINUE`; `commitment_made_by_agent = false`. Exception branches remain `WAIT` until case-specific approval, while independently authorized standard work continues.

---

## Governance

### Stage-Specific Audit Requirements
Retain Ticket origin, Partner-declared priority, business Evidence, authorization, prior-case references, Human decisions, and notice status without converting past approvals into standing authority.

### Human Review Points
The Platform Partner Lead determines business priority and coordinates decisions; Platform Engineering owns technical exceptions. Only an explicitly approved policy can expand the Agent's Delegation Boundary.

### Future Compatibility
Day 60 can connect synthetic Agency and Platform Agents for standard requirement exchange, while routing exceptional requests to the Human Ticket and decision path.
