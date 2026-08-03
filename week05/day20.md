# Day 20: Managing AI-Assisted Decisions

## Human Judgment, Trade-offs, and Executive Communication

## Objective

Use AI to organize an ambiguous platform decision while keeping the final recommendation and accountability with the human decision-maker.

---

## Scenario

A platform is deprecating an existing API.

Thirty partners are affected, but Engineering can directly support only two.

| Partner | Situation |
|---|---|
| A | High revenue, migration not started, small engineering team |
| B | Medium revenue, testing started, strong engineering team, possible API defect |
| C | Low current revenue, high future value, migration not started |

---

## How AI Supports the Decision

AI can help:

- organize facts
- compare partner risk
- identify trade-offs
- challenge assumptions
- draft a concise recommendation

AI should not make the final prioritization decision.

---

## Decision 1: Engineering Support

### Recommendation

Support Partner A and Partner C.

### Rationale

Partner A presents immediate revenue and execution risk.

Partner C presents high strategic value and migration risk.

Partner B has stronger engineering capability and has already started testing. Its reported issue should first be investigated as a possible product defect.

### Trade-off

This decision balances:

- current revenue
- migration readiness
- partner capability
- execution risk
- future strategic value

---

## Decision 2: Possible API Defect

### Recommendation

Maintain the current deprecation timeline until the defect is confirmed.

Review:

- reproducibility
- severity
- platform-wide impact
- available workaround
- expected resolution timeline

If the defect is platform-wide and blocks migration, adjust the broader timeline.

If it is partner-specific, consider a limited exception.

---

## Decision 3: Extension Request

I would not approve a six-month extension.

I would consider a time-bound three-month exception only if Partner C provides:

- a documented migration plan
- executive sponsorship
- measurable milestones
- regular progress reporting
- agreement that no further extension will be granted

---

## Human Review Points

Before accepting an AI-generated recommendation, confirm:

- the quality of the underlying data
- the assumptions used
- the real business impact
- contractual or fairness risks
- who owns the final decision

---

## Executive Communication Framework

1. Recommendation
2. Reason
3. Trade-off
4. Conditions
5. Next action

Example:

> My recommendation is to approve a time-bound three-month exception. The partner has high strategic value, but the exception requires a clear migration plan, executive sponsorship, and measurable milestones.

---

## Key Learning

AI can improve the quality and clarity of a decision, but it does not own the decision.

The human must validate the evidence, define the trade-off, make the recommendation, and own the outcome.

---

## Plain-English Summary

AI helps organize the decision.

The human checks the facts, chooses the direction, and takes responsibility.