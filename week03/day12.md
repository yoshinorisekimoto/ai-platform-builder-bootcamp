# Day 12 - Constraining AI with Evidence Controls

## Objective
After the automated workflow produced unsupported claims, I wanted to test how AI outputs could be constrained before they were passed through the workflow.
The goal was to reduce hallucination by controlling evidence and output structure.

## Experiment

I first redesigned the Validator as an evidence-control role.

The Validator was instructed to:
- Introduce no new facts or hypotheses.
- Preserve unknowns as unknowns.
- Reject unsupported confirmed claims.
- Escalate unsupported outputs to human review.

This approach failed. The Validator still returned `VALIDATION PASSED` for unsupported claims.
I then replaced free-text handoffs with structured outputs.

Each AI role was required to return:
- `confirmed_facts`
- `hypotheses`
- `unknowns`
- `recommendations`
- `evidence_sources`

The first JSON implementation failed because the AI did not always return valid JSON.
I then implemented strict Structured Outputs and replaced AI-based validation with deterministic Python evidence validation.

## Evaluation
The final workflow successfully:
- Enforced a shared output schema across AI roles.
- Preserved confirmed facts separately from hypotheses.
- Prevented hypotheses from being promoted to confirmed facts.
- Validated confirmed facts against previous evidence.
- Returned `VALIDATION PASSED` only after deterministic evidence checks.

However, recommendation quality and approval requirements are not yet fully controlled.

## Insight
Prompt instructions alone were not sufficient to control AI behavior.
The major improvement came from changing the workflow architecture:

> Free text → Structured Outputs → Deterministic Validation

Instead of asking the Validator to be more intelligent, I reduced its freedom and introduced explicit evidence rules.

## Next

Add recommendation controls and human approval gates.

Each recommendation should include supporting evidence, risk, and whether human approval is required before execution.
