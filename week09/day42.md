# Day 42: Evidence Collection and Validation

## Objective

Validate the evidence collected for a Partner request before it is sent to the technical Decision Owner.

This is Stage 2 of the multi-day End-to-End Partner Workflow (Days 41–50).

From this stage onward, **Evidence** is capitalized to mark it as a governed object with its own source, owner, and validation status — not a casual reference to supporting information.

---

## Stage Specification

### Inputs

Day 42 receives the following output from Day 41:

- intake status: `COMPLETE`
- Partner ID
- requested limit
- business reason
- target date
- production endpoint
- collected review evidence
- identified missing evidence

### Roles

**Platform AI**

- checks whether the Evidence source is approved
- checks Partner ID, endpoint, environment, and timestamp
- checks Evidence freshness
- detects missing calculation basis
- detects conflicting Evidence
- records validation results
- stops and escalates blocked validation

**Platform Partner Lead**

- confirms the correct Source Owner
- routes missing or conflicting Evidence to the correct owner
- coordinates internal and Partner follow-up
- owns external communication

**Monitoring Data Owner**

- Source Owner for internal Monitoring Evidence
- Collection Route: `INTERNAL`
- explains or resolves conflicting internal Monitoring Data
- provides updated internal traffic Evidence

**Partner**

- Source Owner for Partner-provided Evidence
- Collection Route: `PARTNER_VIA_PLATFORM_PARTNER_LEAD`
- provides Partner-owned Evidence and calculation basis

**Engineering**

- receives validated Evidence after Day 42
- makes the final technical decision in a downstream stage

### Authority

The Platform AI may collect, validate, classify, record, stop, and escalate Evidence.

It may not:

- select one value when approved Sources conflict
- create a missing calculation basis
- change the Evidence freshness requirement
- make a technical capacity decision
- approve or execute a rate-limit change
- communicate externally without Human authorization

### Validation Criteria

Evidence must:

- come from an approved Source
- identify its Source Owner
- match the correct Partner ID
- match the correct endpoint
- match the correct environment
- include a timestamp
- meet the 24-hour freshness requirement for traffic data
- include a calculation basis for expected peak traffic
- have no unexplained conflict with other approved Evidence

### Outputs

Day 42 produces one of the following:

- `READY_FOR_DECISION`
- `BLOCKED`

A blocked result must include:

- detected issue
- Source Owner
- Collection Route
- next owner
- Resume Condition

### Stop Conditions

The Platform AI must stop validation when:

- the calculation basis is missing
- approved Evidence conflicts
- traffic Evidence is more than 24 hours old
- the Source or Source Owner cannot be verified
- Partner ID, endpoint, environment, or timestamp is missing
- the Evidence does not match the request

### Workflow

1. Receive the complete intake from Day 41.
2. Identify each Evidence item and Source Owner.
3. Validate Source, Partner ID, endpoint, environment, and timestamp.
4. Check freshness and calculation basis.
5. Detect missing, stale, or conflicting Evidence.
6. Record the value, Source, Source Owner, context, and validation result.
7. Stop validation if any Stop Condition is detected.
8. Route the issue through the Platform Partner Lead.
9. Resume only after the recorded Resume Condition is met.
10. Route validated Evidence to Engineering for the final technical decision.

---

## Applied to This Case

### Case

A Partner requests an increase in the Production API rate limit from 100 rpm to 500 rpm.

The review uses:

- current traffic
- expected peak traffic
- recent 429 logs

### Actions

**Missing peak calculation basis**

- Action: `STOP_AND_REQUEST_EVIDENCE`
- Validation status: `BLOCKED`
- Issue: `MISSING_PEAK_CALCULATION_BASIS`
- Routing: `PLATFORM_PARTNER_LEAD`
- Next owner: `PARTNER`
- Collection Route: `PARTNER_VIA_PLATFORM_PARTNER_LEAD`
- Resume Condition: `PARTNER_PROVIDES_PEAK_CALCULATION_BASIS`

**Conflicting official traffic Evidence**

- Action: `STOP_AND_RESOLVE_CONFLICT`
- Validation status: `BLOCKED`
- Issue: `CONFLICTING_EVIDENCE`
- Routing: `PLATFORM_PARTNER_LEAD`
- Next owner: `MONITORING_DATA_OWNER`
- Collection Route: `INTERNAL`
- Resume Condition: `DATA_OWNER_RESOLVES_OR_EXPLAINS_CONFLICT`

**Stale Partner-provided traffic Evidence**

- Action: `STOP_AND_REFRESH_EVIDENCE`
- Validation status: `BLOCKED`
- Issue: `STALE_TRAFFIC_EVIDENCE`
- Routing: `PLATFORM_PARTNER_LEAD`
- Next owner: `PARTNER`
- Collection Route: `PARTNER_VIA_PLATFORM_PARTNER_LEAD`
- Resume Condition: `TRAFFIC_EVIDENCE_IS_WITHIN_24_HOURS`

**All Evidence valid**

- Action: `COMPLETE_EVIDENCE_VALIDATION`
- Validation status: `READY_FOR_DECISION`
- Issue: `NONE`
- Routing: `PLATFORM_PARTNER_LEAD`
- Next owner: `ENGINEERING`
- Collection Route: `INTERNAL`
- Resume Condition: `NOT_REQUIRED`

### Test Result

| Test case | Expected result | Result |
|---|---|---|
| Missing peak calculation basis | Stop and request Partner Evidence | Passed |
| Conflicting official traffic Evidence | Stop and route to Monitoring Data Owner | Passed |
| Stale Partner-provided traffic Evidence | Stop and request fresh Partner Evidence | Passed |
| All Evidence valid | Complete validation and route to Engineering | Passed |

---

## Governance

### Audit Requirements

The audit trail must record:

- Evidence value
- Source
- Source Owner
- Partner ID
- endpoint
- environment
- timestamp
- validation result
- validation failure
- routing destination
- Collection Route
- Resume Condition
- external communication status

### Human Review Points

A Human must confirm:

- whether the correct Source Owner was identified
- whether the correct Collection Route was selected
- whether conflicting Evidence was resolved by its Data Owner
- whether the Resume Condition was actually met
- whether only validated Evidence is routed to Engineering
- whether external communication is authorized

### AI and Human Boundary

The Platform AI may detect, record, stop, route, and resume validation based on defined rules.

The Platform AI may not resolve Evidence conflicts, invent missing Evidence, change validation requirements, or make the final technical decision.

The Platform Partner Lead owns routing, coordination, and external communication.

The relevant Data Owner resolves Source-specific Evidence issues.

Engineering owns the final technical decision.

### Future Compatibility

The Evidence structure includes Source Owner, Collection Route, validation status, and Resume Condition so that a future Partner AI Agent can exchange Evidence in a controlled format.

Agent-to-Agent communication is not implemented in Day 42. The current workflow remains Platform-AI-only and Human-controlled.