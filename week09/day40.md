# Day 40 - Formalizing Agent Operating Rules

## Objective

Convert the Human-AI boundaries tested in Days 30–39 into reusable operating rules.

---

## Rules Formalized

### Roles

- **Platform AI:** Performs authorized work using approved evidence
- **Platform Partner Lead:** Owns Partner communication, internal routing, case coordination, and commitments
- **Domain Owner:** Owns decisions within Product, Engineering, Data, Legal, Security, or another defined domain

### Evidence and Execution

- Classification requires sufficient approved evidence.
- Execution requires complete, consistent, and authorized evidence.
- Missing execution evidence requires stopping, recording, and escalation.
- Conflicting evidence must be preserved and escalated without interpretation.

### Escalation

For a non-standard Partner case:

1. Platform AI stops standard work.
2. Platform AI escalates to the Platform Partner Lead.
3. The Platform Partner Lead routes issues to the relevant Domain Owners.
4. Domain Owners make decisions within their authority.
5. The Platform Partner Lead integrates the decisions and communicates with the Partner.

### Communication

Platform AI must not independently:

- Make commitments
- Approve exceptions
- Resolve evidence conflicts
- Accept material risk
- Send unapproved external communication

### Workflow Action Naming

Workflow actions use uppercase snake case and begin with a base-form imperative verb.

Examples:

- `EXECUTE_STANDARD_WORK`
- `STOP_EXECUTION`
- `STOP_CLASSIFICATION`
- `ESCALATE_TO_PLATFORM_PARTNER_LEAD`

---

## Test Cases

The same rules were tested against four workflow states:

1. Approved standard work
2. Missing execution evidence
3. Conflicting evidence
4. Non-standard Partner case

External communication was not authorized in any test case.

## Test Result

### Approved Standard Work

```text
Action: EXECUTE_STANDARD_WORK
Escalation: NOT_REQUIRED
External communication: NOT_AUTHORIZED
Audit trail: REQUIRED
```

---

### Missing Execution Evidence

```text
Action: STOP_EXECUTION
Escalation: ESCALATE_TO_PLATFORM_PARTNER_LEAD
External communication: NOT_AUTHORIZED
Audit trail: REQUIRED
```
### Conflicting Evidence

```text
Action: STOP_EXECUTION
Escalation: ESCALATE_TO_PLATFORM_PARTNER_LEAD
External communication: NOT_AUTHORIZED
Audit trail: REQUIRED
```

### Non-Standard Partner Case

```text
Action: STOP_STANDARD_WORK
Escalation: ESCALATE_TO_PLATFORM_PARTNER_LEAD
External communication: NOT_AUTHORIZED
Audit trail: REQUIRED
```

The rules correctly allowed only approved standard work to execute. All other cases stopped and escalated to the Platform Partner Lead.

---

## AGENTS.md Update

The operating rules now define:

- Role and authority boundaries
- Classification and execution controls
- Missing and conflicting evidence handling
- Escalation and communication flow
- Human approval requirements
- Workflow action naming
- Autonomy and audit requirements

## AI and Human Boundary

Platform AI controls workflow execution within approved boundaries.

Humans retain authority over judgment, commitments, exceptions, risk acceptance, relationships, and final authorization.

## Points Requiring Human Review

Humans must confirm:

- The standard-work scope remains current
- Evidence requirements are clearly defined
- Domain Owners remain accountable for their decisions
- External communication has explicit authorization
- Audit records remain complete as autonomy expands

## Key Learning

Agent governance becomes reusable only when principles are converted into explicit roles, evidence requirements, routing rules, approval gates, and audit records.