# AI-Assisted Partner Operations

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

---

## Supported Scenarios

The same workflow can process multiple incident types by changing only the scenario input.

Current examples include:

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
├── requirements.txt
├── scenarios/
│   ├── http401.json
│   ├── api_timeout.json
│   ├── webhook_failure.json
│   ├── rate_limit.json
├── outputs/
│   └── sample_output.json
```

---

## Example Usage

```bash
python workflow.py scenarios/http401.json

python workflow.py scenarios/api_timeout.json

python workflow.py scenarios/webhook_failure.json

python workflow.py scenarios/rate_limit.json
```

---

## How It Works

The workflow logic is intentionally kept independent from incident data.

Each incident is defined as a standalone JSON scenario, allowing the same workflow to process different situations without modifying the application logic.

This approach improves maintainability, reusability, and scalability while preserving deterministic validation and human review.

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

- reusable validation policy modules
- configurable workflow pipelines
- scenario categorization
- richer structured outputs
- evaluation and testing framework
- integration with additional LLM providers

---

## Learning Goal

This repository is part of my AI Platform Builder Bootcamp.

The focus is not only learning Python and LLM APIs, but also applying platform thinking to build reusable, safe, and human-centered AI workflows inspired by real-world partner operations.
