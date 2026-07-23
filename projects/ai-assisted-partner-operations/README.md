# AI-Assisted Partner Operations

This project demonstrates how a single AI-assisted workflow can process multiple API incident scenarios by separating workflow logic from scenario definitions.
A reusable Python prototype demonstrating a safe, structured AI-assisted workflow for API and partner incident analysis.

This project explores how Large Language Models (LLMs) can support technical investigation while maintaining deterministic validation, human approval, and execution safeguards.

---

## Features

- Structured Outputs for predictable AI responses
- Separation of Confirmed Facts and Hypotheses
- Deterministic evidence validation
- Recommendation validation against confirmed evidence
- Human approval queue
- STOPPED_BEFORE_EXECUTION safeguard
- No live action execution
- Reusable scenario-based architecture
- Deterministic quality evaluation
  
---

## Supported Scenarios

The same workflow can process multiple incident types by changing only the scenario input.

Currently supported scenarios include:

- HTTP 401 Unauthorized
- API Timeout
- Webhook Delivery Failure
- HTTP 429 Rate Limit

Additional scenarios can be added by creating a new JSON file under the `scenarios/` directory.

---

## Project Structure

```
ai-assisted-partner-operations/
├── workflow.py
├── evaluator.py
├── requirements.txt
├── scenarios/
├── evaluation/
│   ├── evaluation_criteria.json
│   └── sample_evaluation.json
└── outputs/
```

---

## Example Usage

```bash
python workflow.py scenarios/http401.json

python workflow.py scenarios/api_timeout.json

python workflow.py scenarios/webhook_failure.json

python workflow.py scenarios/rate_limit.json

python evaluator.py outputs/sample_output.json
```

---

## How It Works

The workflow logic is intentionally kept independent from incident data.

Each incident is defined as a standalone JSON scenario, allowing the same workflow to process different situations without modifying the application logic.

This approach improves maintainability, reusability, and scalability while preserving deterministic validation and human review.
The generated workflow output can also be evaluated by a deterministic rule-based evaluator to verify structural completeness and safety before human review.

---

## Safety Design

The workflow intentionally does **not** execute operational actions.

Instead, it:

- analyzes structured incident data
- validates supporting evidence
- verifies recommendations
- prepares approval items for human review

All execution remains outside the scope of this prototype.

---

## Future Improvements

Possible future enhancements include:

- reusable validator modules
- configurable workflow policies
- additional incident categories
- automated evaluation framework
- multi-model support

---

## Learning Goal

This repository is part of my AI Platform Builder Bootcamp.

The focus is not only learning Python and LLM APIs, but also applying platform thinking to build reusable, safe, and human-centered AI workflows inspired by real-world partner operations.

## Design Principle

Separate workflow logic from business scenarios.

Keep AI outputs structured and verifiable.

Require human approval before operational actions.

Favor reusable platform components over one-off automations.
