# Day 14: Reusable AI-Assisted Partner Operations Package

## What Changed

Packaged the latest Day10-13 sequential role workflow into a reusable project:

```text
projects/ai-assisted-partner-operations/
```

The workflow now separates the HTTP 401 incident scenario from the Python code and accepts a scenario file at runtime:

```bash
python workflow.py scenario.json
```

## Files Added

- `projects/ai-assisted-partner-operations/workflow.py`
- `projects/ai-assisted-partner-operations/scenario.json`
- `projects/ai-assisted-partner-operations/requirements.txt`
- `projects/ai-assisted-partner-operations/outputs/sample_output.json`

## Safeguards Preserved

- Structured role outputs through a strict JSON schema
- deterministic evidence validation
- exact-match confirmed fact validation
- hypothesis promotion checks
- recommendation evidence validation
- provisional marking for hypothesis-only recommendations
- human approval queue for high-risk or irreversible actions
- no action execution capability

## Scenario Separation

The incident description and initial evidence now live in `scenario.json`.

The scenario file contains:

- `description`
- `confirmed_facts`
- `hypotheses`
- `unknowns`
- `evidence_sources`

## Limitations

The workflow still requires `OPENAI_API_KEY` for live role generation.

The sample output is sanitized and illustrative. It is not produced by a live incident system and does not execute or approve any operational action.
