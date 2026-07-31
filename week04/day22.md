# Day 22 — Partner Launch vs Platform Risk

## Objective

Practice making a business decision under incomplete technical evidence while using AI as decision support.

## Scenario

A partner wants to launch a new Analytics API integration in two weeks.

* Potential deal value: $3M
* Load testing shows about 15% timeout risk at expected peak traffic
* Engineering estimates that two additional weeks could reduce the risk to around 3%
* Engineering capacity is limited

The key question is whether to launch as planned or delay.

## AI-Assisted Analysis

Before making the decision, several missing facts needed to be clarified:

* Who will use the API?
* Does the risk affect end users or only the partner's internal users?
* Does Engineering have another lower-risk option?
* Does the partner understand and accept the known risk?

The final evidence showed:

* The API is used only by the partner's internal users
* The partner understands the 15% timeout risk
* The partner still prefers to launch on schedule

## Recommendation

Launch as planned.

The impact is limited to the partner's internal users, and the partner has explicitly accepted the known technical risk.

The risk should be clearly communicated within the partner organization before launch.

## Trade-off

The decision balances:

**$3M commercial opportunity**

vs.

**Known timeout and user-experience risk**

Because the impact is limited and understood, delaying the launch is not necessary.

## Human Review / Ownership

AI can organize the evidence and identify missing information.

The human decision owner must determine:

* whether the risk is acceptable
* who is affected
* whether the partner has genuinely accepted the risk
* whether Engineering resources should be reprioritized

Engineering capacity should not normally be reallocated for a single $3M request unless broader strategic value justifies an exception.

## Key Learning

A senior decision is not always about choosing quickly.

Sometimes the correct first action is to identify what information is still missing.

**Audience → Risk Scope → Alternatives → Risk Acceptance → Decision**

Good judgment depends on asking the right questions before committing to a recommendation.

## Plain-English Summary

Before deciding whether to launch, first understand who could be affected and how serious the problem is.

AI can help organize the facts, but people must decide whether the risk is acceptable and take responsibility for the final decision.
