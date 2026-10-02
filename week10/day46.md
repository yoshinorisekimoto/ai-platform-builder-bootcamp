# Day 46: Decision Preparation and Engineering Review Control

## Objective

Define how the Platform AI prepares a Decision Brief for Engineering once all required Evidence has been collected, clarified, and verified, without making the final technical decision itself.

Common rules, vocabulary, roles, and AI–Human boundaries are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

This is Stage 6 of the End-to-End Partner Workflow (Days 41–50).

---

## Stage Specification

### Inputs

- validated, minimized, and permission-cleared Evidence Package (Day 44)
- resolved clarifications (Day 45)
- verified business context (reason, target date)

### Stage-Specific Role

**Engineering:** reviews the Decision Brief and makes the final technical decision, including approval scope and conditions.

### Decision Brief Structure

The Platform AI must keep three categories separate:

- **Verified Facts** — e.g. current traffic, expected peak, requested limit, peak duration, confirmed 429 logs, verified calculation basis
- **Business Context** — e.g. business reason, launch date, expected Partner impact
- **AI Analysis** — clearly labeled as analysis, never presented as a decision (e.g. "Traffic increase appears temporary")

### Outputs

- `ROUTED_FOR_ENGINEERING_REVIEW`
- `DECISION_RECORDED`

A recorded decision must include:

- approval scope and conditions
- completion requirements
- Resume Condition, if the case remains open

### Stop Conditions

The Platform AI must stop when:

- AI analysis would be presented as, or mistaken for, a decision
- Engineering's decision has not yet been recorded
- a completion condition (e.g. normal traffic confirmed, temporary limit removed) has not been met
- external communication would occur before the Platform Partner Lead has the confirmed decision

### Workflow

1. Receive the verified Evidence Package and business context.
2. Separate the content into Verified Facts, Business Context, and AI Analysis.
3. Route the Decision Brief internally to Engineering.
4. Record Engineering's decision, scope, and conditions.
5. Notify the Platform Partner Lead to communicate externally.
6. Track completion requirements.
7. Close the case only once all completion requirements are met.

---

## Applied to This Case

### Case

A Partner requests a production API rate-limit increase ahead of a major customer launch tomorrow.

- Current traffic: 320 rpm
- Expected peak: 450 rpm
- Requested limit: 500 rpm
- Peak duration: 8 minutes
- Recent 429 errors confirmed; calculation basis verified
- Business reason and target date verified

### Actions

**Decision Brief prepared**

- Action: `PREPARE_DECISION_BRIEF`
- Status: `ROUTED_FOR_ENGINEERING_REVIEW`
- Categories: `VERIFIED_FACTS`, `BUSINESS_CONTEXT`, `AI_ANALYSIS`
- Next owner: `ENGINEERING`

**AI analysis offered as reference only**

- Action: `LABEL_ANALYSIS_AS_REFERENCE`
- Status: `PENDING_ENGINEERING_DECISION`
- Analysis: "500 rpm may provide enough headroom" (reference only, not approval)
- Next owner: `ENGINEERING`

**Engineering decision recorded**

- Action: `RECORD_ENGINEERING_DECISION`
- Status: `DECISION_RECORDED`
- Approval: `500_RPM_APPROVED_FOR_LAUNCH_WINDOW_ONLY`
- Conditions: temporary limit removed after launch; Partner confirms return to normal traffic
- Next owner: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `NORMAL_TRAFFIC_CONFIRMED_AND_TEMPORARY_LIMIT_REMOVED`

### Test Result

| Test case | Expected result | Result |
|---|---|---|
| Decision Brief prepared | Route structured brief to Engineering | Passed |
| AI analysis offered | Analysis labeled as reference, not approval | Passed |
| Engineering decision recorded | Record approval, conditions, and completion requirement | Passed |

---

## Governance

Common governance requirements are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

### Stage-Specific Audit Requirements

Record:

- Verified Facts, Business Context, and AI Analysis as separate fields
- Engineering decision, approval scope, and conditions
- temporary-limit removal requirement
- Partner confirmation
- final completion status

### Human Review Points

A Human must confirm:

- AI analysis is not recorded as fact or decision
- Engineering's decision is recorded before the case proceeds
- external communication is owned by the Platform Partner Lead
- the case does not close before all completion conditions are met

### Future Compatibility

The Decision Brief format separates fact, context, and analysis so that a future Partner AI Agent could supply structured input without gaining decision authority. Agent-to-Agent decision-making is not implemented in Day 46.