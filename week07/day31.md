# Day31: Evidence-Based Launch Communication

## Objective

Apply the Human–AI Boundary to partner communication.
Separate test results, official launch approval, and permission to send a response.

## Roles

- Partner: Runs integration tests and deploys its product.
- Platform Partner Lead: Clarifies evidence and communicates with the Partner.
- Platform Release Owner: Reviews results and grants launch approval.
- Platform AI: Organizes evidence and drafts responses; cannot approve launch.
- Partner AI: Not used in this case.

## Evidence and Decision

Testing passed, but the release owner had not yet reviewed the report.

When Platform AI drafted “We can launch on Friday,” the Partner Lead requested the approval evidence rather than accepting the claim.

After official approval is received, Platform AI may include that approval and the test results in a draft. The Partner Lead reviews the message before sending it.

## Operating Rules

- Do not infer launch approval from successful tests.
- Ask for evidence when a claim conflicts with known information.
- Relay verified human approval without creating new commitments.
- Keep external communication under human review.
- Record the evidence and routing reason.

## Prototype Validation

A deterministic Python prototype was executed in the assistant's environment using synthetic data.

- Before verified approval: Escalate to a human for evidence.
- After verified approval: Draft the approved information for human review.
- Both cases: No automatic external sending.

Result: 2/2 cases passed.

This validates manually coded rules, not an AI model's ability to interpret AGENTS.md. Model-based validation remains pending. The prototype has not yet been added to this repository.

## Delivery Learning

Clarify roles, missing facts, and decision ownership before drafting a partner response. Clarification is part of the work, not a failure to answer.

## Point of View

AI may prepare communication; humans own evidence verification and commitments.

## Plain-English Summary

AI writes the draft. People check the facts and approve the message.

## Human Review Checklist

- Is the approval genuine and applicable to this launch?
- Does the draft accurately reflect the test results and approval?
- Has the Partner Lead reviewed the message before sending?