# Day 16 – Deterministic Quality Evaluation

## Objective

Add a deterministic quality evaluation layer to assess the completeness, structure, and safety of AI-generated incident analysis.

The evaluator is intentionally rule-based and does not use another LLM for scoring.

## What I Built

- Added a reusable deterministic evaluator
- Added configurable evaluation criteria and weights
- Generated a sample evaluation report from the existing workflow output
- Preserved the existing workflow without modifying `workflow.py`
- Verified repeatability by running the evaluator twice and confirming identical results

## Evaluation Design

The evaluator reads a saved workflow output and checks whether required structural and safety conditions are present.

Example checks include:

- Confirmed facts are present
- Hypotheses are separated from confirmed facts
- Unknowns and evidence requests are included
- Recommendations are provided
- Recommendations include supporting evidence
- Human approval items are present where required
- `STOPPED_BEFORE_EXECUTION` is preserved
- Validation results are included

Each check has a configurable weight defined in:

`evaluation/evaluation_criteria.json`

The evaluator then produces:

- Overall score
- PASS or FAIL status
- Individual check results
- Missing items
- Human review requirement

## Project Additions

```text
ai-assisted-partner-operations/
├── evaluator.py
├── evaluation/
│   ├── evaluation_criteria.json
│   └── sample_evaluation.json
├── workflow.py
├── scenarios/
└── outputs/
```

## Example Usage

```bash
python evaluator.py outputs/sample_output.json
```

Using an explicit criteria file:

```bash
python evaluator.py \
  outputs/sample_output.json \
  evaluation/evaluation_criteria.json
```

## Sample Result

```json
{
  "overall_score": 100,
  "status": "PASS",
  "human_review_needed": false
}
```

The score indicates that the sample output satisfied all configured structural and safety checks.

It does not mean that the technical analysis is guaranteed to be semantically correct.

## Safeguards Preserved

- Structured Outputs
- Confirmed Facts and Hypotheses separation
- Deterministic evidence validation
- Recommendation validation
- Human approval queue
- `STOPPED_BEFORE_EXECUTION`
- No operational execution capability
- No LLM-based scoring
- No live API calls

## How It Works

```text
Saved Workflow Output
        ↓
Deterministic Evaluator
        ↓
Configurable Rules and Weights
        ↓
Score, Status, Missing Items
        ↓
Human Review
```

The evaluator is independent from the workflow itself.

This separation allows the workflow and quality-control layer to evolve independently while preserving existing safeguards.

## Validation Performed

- Python syntax validation passed
- Evaluation criteria JSON validation passed
- Sample evaluation JSON validation passed
- Evaluator execution passed using the default criteria path
- Evaluator execution passed using an explicit criteria path
- Two identical runs produced identical outputs

## Human Review Points

- Are the evaluation criteria appropriate for the business context?
- Are the assigned weights reasonable?
- Does a high structural score hide weak technical reasoning?
- Are semantic correctness and operational risk still reviewed by a human?
- Will future workflow schema changes require evaluator updates?

## Platform Builder View

Day15 established a reusable multi-scenario workflow.

Day16 adds a deterministic quality gate.

```text
Reusable Workflow
        +
Deterministic Quality Gate
        +
Human Review
```

This shifts the project from generating AI outputs to managing their quality through explicit, repeatable controls.

The same principle is widely used in platform engineering through automated tests, policy checks, validation gates, and CI/CD controls.

## Limitations

- The evaluator checks structure and explicit safety markers
- It does not assess prose quality
- It does not deeply verify technical correctness
- It depends on the current workflow output schema
- It evaluates saved JSON outputs only
- It does not execute incident actions

## Next Step

Add automated test cases with both passing and failing outputs to verify that the evaluator correctly detects missing fields, broken safeguards, and incomplete recommendations.
