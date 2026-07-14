# Day 11 - Automating AI Role Handoffs

## Objective
After manually executing a multi-role AI workflow, I wanted to remove the need to copy outputs between separate AI conversations.
The goal was to implement a minimal sequential workflow that automatically passes context and outputs between specialized AI roles.

## Experiment
I created a Python workflow using the OpenAI API.
The workflow automatically executed the following roles:
1. Senior Partner Engineer
2. API Architect
3. Platform Partnerships Manager

The original HTTP 401 production scenario was preserved throughout the workflow, and each role received the outputs required from previous steps.
After the initial test produced unsupported assumptions, I added stricter prompt instructions and a separate Validator role.

The Validator reviewed:
- The original scenario
- Technical triage report
- Architecture review
- Partner response plan

It then produced a corrected final response plan.

## Evaluation
The automated workflow executed successfully.
- API calls completed successfully.
- Outputs were automatically passed between roles.
- Role-specific prompts remained separate.
- The workflow reached the final response plan without manual copy and paste.
- A Validator role was successfully added to the workflow.

However, the final validated output still introduced unsupported claims, including specific deployment timing, token behavior, and authentication hypotheses presented with excessive certainty.
The Validator also incorrectly stated that the final plan met all requirements.

## Insight
Automated AI workflows can execute successfully while still producing unsupported claims.
Adding an AI Validator does not guarantee factual accuracy because the Validator itself can fail to identify or may reinforce hallucinated information.
Human review and stronger evidence controls remain necessary, especially when AI outputs are passed sequentially between specialized roles.

## Next

Explore how to introduce explicit evidence tracking and validation rules so that AI roles can distinguish supported facts from hypotheses before generating a final output.
