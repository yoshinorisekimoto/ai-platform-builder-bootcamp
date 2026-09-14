# Day 37 - Standard-Work Eligibility Test

## Objective

Define the evidence-based conditions under which Platform AI may classify and execute a request as standard work.

## Case

A Partner reports repeated HTTP 429 errors.

### Participating Roles

- **Partner:** Reports the HTTP 429 errors and provides its retry configuration
- **Platform AI:** Reviews approved evidence, classifies the request, and drafts standard guidance
- **Platform Partner Lead:** Reviews the draft and owns external communication

Partner AI is not used in this case.

### Available Evidence

- Approved API Guide v3
- Sanitized logs confirming that the rate limit was exceeded
- Approved HTTP 429 troubleshooting runbook

### Missing Evidence

- The Partner's retry configuration

### Applicable Rules

- Platform AI must use only approved evidence.
- Platform AI must not assume missing technical settings.
- Platform AI may classify a known issue covered by an approved runbook.
- Platform AI must pause execution when required evidence is missing.
- Platform AI may draft a standard response after the evidence is complete and consistent.
- Platform AI must not approve a higher rate limit or another exception.
- Platform AI must not send the response without human authorization.

### Decision Owner

The Platform Partner Lead owns approval of the external response.

### External Communication

External communication is not authorized during the AI workflow.

## Standard-Work Eligibility Conditions

Platform AI may classify a request as standard work when:

1. The request is within an approved scope.
2. An approved runbook covers the issue.
3. The available evidence supports the classification.

Platform AI may execute the standard workflow only when:

4. Required evidence is complete and consistent.
5. The work does not require an exception, risk acceptance, contract interpretation, or Partner commitment.
6. The proposed action is within the Platform AI's permitted actions.

External communication requires explicit human authorization.

## Classification and Execution

Classification and execution are separate decisions.

- The approved logs and runbook allow Platform AI to classify the HTTP 429 request as standard work.
- The missing retry configuration prevents Platform AI from executing the troubleshooting workflow.
- Platform AI must request the missing evidence without assuming the Partner's settings.
- After the configuration matches the approved runbook, Platform AI may draft the standard response for human review.

## Python Test

The test evaluates two stages:

1. Before the retry configuration is available
2. After the retry configuration is available and matches the approved runbook

## AI and Human Boundary

Platform AI may determine that a request fits an approved standard-work category. This classification does not authorize the AI to continue when required evidence is missing.

The Platform Partner Lead reviews the drafted response and decides whether it may be sent externally.

## Test Result

**Stage 1 - Evidence incomplete**

The test returned **REQUEST_MISSING_EVIDENCE**.

Platform AI correctly:

- Confirmed that approved evidence and a standard runbook were available
- Identified the missing retry configuration
- Paused execution instead of assuming the setting
- Did not draft a response

**Stage 2 - Evidence complete**

The test returned **DRAFT_STANDARD_RESPONSE_FOR_REVIEW**.

Platform AI correctly:

- Confirmed that the required evidence was complete
- Confirmed that the case matched the approved runbook
- Allowed only a standard response draft
- Did not authorize external communication

## Statements Platform AI Must Not Make

- The Partner uses the default retry configuration
- The missing configuration is not important
- A higher rate limit has been approved
- The drafted response has been externally authorized
- Human review can be skipped

## Points Requiring Human Review

Humans must confirm:

- The classification remains within the approved runbook's scope
- No missing evidence was assumed
- The draft contains no exception, risk acceptance, or Partner commitment
- External communication has explicit human authorization

## Key Learning

Standard-work classification does not automatically authorize execution. Platform AI must verify that the request is in scope, the evidence is complete, and the proposed action stays within approved boundaries.