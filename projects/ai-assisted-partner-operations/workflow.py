"""Reusable AI-assisted partner operations workflow.

Run:
    export OPENAI_API_KEY="..."
    python workflow.py scenarios/http401.json
    python workflow.py scenarios/api_timeout.json
    python workflow.py scenarios/webhook_failure.json
    python workflow.py scenarios/rate_limit.json

Optional:
    export OPENAI_MODEL="gpt-4.1-mini"
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


RECOMMENDATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "action": {"type": "string"},
        "supporting_evidence": {
            "type": "array",
            "items": {"type": "string"},
        },
        "expected_benefit": {"type": "string"},
        "risk": {"type": "string", "enum": ["low", "medium", "high"]},
        "reversibility": {
            "type": "string",
            "enum": ["reversible", "partially_reversible", "irreversible"],
        },
        "human_approval_required": {"type": "boolean"},
        "approval_owner": {"type": "string"},
        "provisional": {"type": "boolean"},
    },
    "required": [
        "action",
        "supporting_evidence",
        "expected_benefit",
        "risk",
        "reversibility",
        "human_approval_required",
        "approval_owner",
        "provisional",
    ],
}


ROLE_OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "confirmed_facts": {
            "type": "array",
            "items": {"type": "string"},
        },
        "hypotheses": {
            "type": "array",
            "items": {"type": "string"},
        },
        "unknowns": {
            "type": "array",
            "items": {"type": "string"},
        },
        "recommendations": {
            "type": "array",
            "items": RECOMMENDATION_SCHEMA,
        },
        "evidence_sources": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "confirmed_facts",
        "hypotheses",
        "unknowns",
        "recommendations",
        "evidence_sources",
    ],
}


ROLE_TEXT_FORMAT = {
    "format": {
        "type": "json_schema",
        "name": "role_evidence_output",
        "schema": ROLE_OUTPUT_SCHEMA,
        "strict": True,
    }
}


EVIDENCE_INSTRUCTIONS = """
Rules for confirmed_facts:
- Use only exact strings already present in confirmed_facts from the original
  scenario evidence or previous role outputs.
- Do not promote hypotheses to confirmed facts.
- Put likely causes, inferred risks, and possible next steps in hypotheses or
  recommendations, not confirmed_facts.

Rules for recommendations:
- Each recommendation must include action, supporting_evidence,
  expected_benefit, risk, reversibility, human_approval_required,
  approval_owner, and provisional.
- supporting_evidence must contain exact strings from confirmed_facts or
  hypotheses in the original scenario evidence or previous role outputs.
- Recommendations supported only by hypotheses must set provisional to true.
- High-risk or irreversible recommendations must set human_approval_required
  to true and name an approval_owner.
""".strip()


SENIOR_PARTNER_ENGINEER_PROMPT = """
You are a Senior Partner Engineer.

Produce a concise technical triage report for the incident scenario.
Include:
- likely failure modes
- immediate checks
- containment options
- data needed from partners
- risks and assumptions

Guardrails:
- Do not invent facts.
- Clearly separate confirmed facts, hypotheses, and recommendations.
- Do not recommend rollback, credential rotation, or configuration changes unless supported by previous outputs.
- Preserve unknowns as unknowns.
"""
SENIOR_PARTNER_ENGINEER_PROMPT = (
    SENIOR_PARTNER_ENGINEER_PROMPT.strip() + "\n\n" + EVIDENCE_INSTRUCTIONS
)


API_ARCHITECT_PROMPT = """
You are an API Architect.

Review the original incident scenario and the Senior Partner Engineer's
technical triage report. Produce an architecture review.
Include:
- probable architectural cause
- API auth/token design concerns
- short-term remediation
- durable design improvements
- observability gaps

Guardrails:
- Do not invent facts.
- Clearly separate confirmed facts, hypotheses, and recommendations.
- Do not recommend rollback, credential rotation, or configuration changes unless supported by previous outputs.
- Preserve unknowns as unknowns.
"""
API_ARCHITECT_PROMPT = API_ARCHITECT_PROMPT.strip() + "\n\n" + EVIDENCE_INSTRUCTIONS


PLATFORM_PARTNERSHIPS_MANAGER_PROMPT = """
You are a Platform Partnerships Manager.

Review the original incident scenario, the technical triage report, and the
architecture review. Produce a partner response plan.
Include:
- partner-facing message
- escalation path
- update cadence
- information to request from affected partners
- commitments to avoid making prematurely

Guardrails:
- Do not invent facts.
- Clearly separate confirmed facts, hypotheses, and recommendations.
- Do not recommend rollback, credential rotation, or configuration changes unless supported by previous outputs.
- Preserve unknowns as unknowns.
"""
PLATFORM_PARTNERSHIPS_MANAGER_PROMPT = (
    PLATFORM_PARTNERSHIPS_MANAGER_PROMPT.strip() + "\n\n" + EVIDENCE_INSTRUCTIONS
)


@dataclass(frozen=True)
class RoleStep:
    name: str
    prompt: str


RoleOutput = dict[str, Any]
Scenario = dict[str, Any]


def load_scenario(path: Path) -> Scenario:
    try:
        scenario = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Scenario file is not valid JSON: {error}") from error

    required_keys = {
        "description",
        "confirmed_facts",
        "hypotheses",
        "unknowns",
        "evidence_sources",
    }
    missing_keys = required_keys - scenario.keys()
    if missing_keys:
        raise ValueError(f"Scenario file is missing keys: {sorted(missing_keys)}")

    if not isinstance(scenario["description"], str):
        raise ValueError("Scenario field 'description' must be a string")

    for key in ["confirmed_facts", "hypotheses", "unknowns", "evidence_sources"]:
        if not isinstance(scenario[key], list) or not all(
            isinstance(item, str) for item in scenario[key]
        ):
            raise ValueError(f"Scenario field {key!r} must be a list of strings")

    return scenario


def scenario_evidence(scenario: Scenario) -> RoleOutput:
    return {
        "confirmed_facts": scenario["confirmed_facts"],
        "hypotheses": scenario["hypotheses"],
        "unknowns": scenario["unknowns"],
        "recommendations": [],
        "evidence_sources": scenario["evidence_sources"],
    }


def call_role(client: OpenAI, step: RoleStep, role_input: str) -> str:
    """Call one role and return schema-constrained JSON text."""
    response = client.responses.create(
        model=MODEL,
        instructions=step.prompt,
        input=role_input,
        text=ROLE_TEXT_FORMAT,
    )
    return response.output_text


def human_approval_checkpoint(stage_name: str, output: str) -> None:
    """Placeholder for a future human approval gate.

    Later, this could send the output to Slack, create a ticket, pause until
    an approver clicks "Approve", or block the next role from running.
    """
    print(f"\n--- Human approval checkpoint: {stage_name} ---")
    print("Checkpoint recorded; this prototype does not execute actions.")


def build_engineer_input(scenario: Scenario) -> str:
    return f"""
Original scenario:
{scenario["description"]}

Original scenario evidence:
{json.dumps(scenario_evidence(scenario), indent=2)}
""".strip()


def build_architect_input(scenario: Scenario, triage_report: str) -> str:
    return f"""
Original scenario:
{scenario["description"]}

Senior Partner Engineer triage report:
{triage_report}
""".strip()


def build_manager_input(
    scenario: Scenario,
    triage_report: str,
    architecture_review: str,
) -> str:
    return f"""
Original scenario:
{scenario["description"]}

Senior Partner Engineer triage report:
{triage_report}

API Architect architecture review:
{architecture_review}
""".strip()


def parse_role_json(role_name: str, output: str) -> RoleOutput:
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as error:
        print(f"\nRaw output from {role_name}:\n{output}")
        raise ValueError(f"{role_name} did not return valid JSON: {error}") from error

    if not isinstance(parsed, dict):
        print(f"\nRaw output from {role_name}:\n{output}")
        raise ValueError(f"{role_name} JSON must be an object")

    required_keys = {
        "confirmed_facts",
        "hypotheses",
        "unknowns",
        "recommendations",
        "evidence_sources",
    }
    missing_keys = required_keys - parsed.keys()
    if missing_keys:
        print(f"\nRaw output from {role_name}:\n{output}")
        raise ValueError(f"{role_name} JSON is missing keys: {sorted(missing_keys)}")

    extra_keys = parsed.keys() - required_keys
    if extra_keys:
        print(f"\nRaw output from {role_name}:\n{output}")
        raise ValueError(f"{role_name} JSON has unexpected keys: {sorted(extra_keys)}")

    for key in ["confirmed_facts", "hypotheses", "unknowns", "evidence_sources"]:
        if not isinstance(parsed[key], list) or not all(
            isinstance(item, str) for item in parsed[key]
        ):
            print(f"\nRaw output from {role_name}:\n{output}")
            raise ValueError(f"{role_name} JSON field {key!r} must be a list of strings")

    if not isinstance(parsed["recommendations"], list):
        print(f"\nRaw output from {role_name}:\n{output}")
        raise ValueError(f"{role_name} JSON field 'recommendations' must be a list")

    recommendation_keys = {
        "action",
        "supporting_evidence",
        "expected_benefit",
        "risk",
        "reversibility",
        "human_approval_required",
        "approval_owner",
        "provisional",
    }
    for index, recommendation in enumerate(parsed["recommendations"]):
        if not isinstance(recommendation, dict):
            print(f"\nRaw output from {role_name}:\n{output}")
            raise ValueError(f"{role_name} recommendation {index} must be an object")

        missing_recommendation_keys = recommendation_keys - recommendation.keys()
        extra_recommendation_keys = recommendation.keys() - recommendation_keys
        if missing_recommendation_keys or extra_recommendation_keys:
            print(f"\nRaw output from {role_name}:\n{output}")
            raise ValueError(
                f"{role_name} recommendation {index} has invalid keys: "
                f"missing={sorted(missing_recommendation_keys)}, "
                f"extra={sorted(extra_recommendation_keys)}"
            )

        string_fields = [
            "action",
            "expected_benefit",
            "risk",
            "reversibility",
            "approval_owner",
        ]
        for field in string_fields:
            if not isinstance(recommendation[field], str):
                print(f"\nRaw output from {role_name}:\n{output}")
                raise ValueError(
                    f"{role_name} recommendation {index} field {field!r} must be a string"
                )

        if recommendation["risk"] not in {"low", "medium", "high"}:
            print(f"\nRaw output from {role_name}:\n{output}")
            raise ValueError(f"{role_name} recommendation {index} has invalid risk")

        if recommendation["reversibility"] not in {
            "reversible",
            "partially_reversible",
            "irreversible",
        }:
            print(f"\nRaw output from {role_name}:\n{output}")
            raise ValueError(
                f"{role_name} recommendation {index} has invalid reversibility"
            )

        if not isinstance(recommendation["supporting_evidence"], list) or not all(
            isinstance(item, str) for item in recommendation["supporting_evidence"]
        ):
            print(f"\nRaw output from {role_name}:\n{output}")
            raise ValueError(
                f"{role_name} recommendation {index} supporting_evidence must be a list of strings"
            )

        if not isinstance(recommendation["human_approval_required"], bool):
            print(f"\nRaw output from {role_name}:\n{output}")
            raise ValueError(
                f"{role_name} recommendation {index} human_approval_required must be a boolean"
            )

        if not isinstance(recommendation["provisional"], bool):
            print(f"\nRaw output from {role_name}:\n{output}")
            raise ValueError(
                f"{role_name} recommendation {index} provisional must be a boolean"
            )

    return parsed


def validate_evidence(
    scenario: Scenario,
    triage_report: RoleOutput,
    architecture_review: RoleOutput,
    partner_response_plan: RoleOutput,
) -> tuple[str, list[dict[str, Any]]]:
    unsupported_claims = []
    approval_queue = []

    def check_confirmed_facts(
        role_name: str,
        output: RoleOutput,
        allowed_confirmed_facts: set[str],
        prior_hypotheses: set[str],
    ) -> None:
        for fact in output["confirmed_facts"]:
            if fact in prior_hypotheses:
                unsupported_claims.append(
                    {
                        "role": role_name,
                        "unsupported_claim": fact,
                        "source_checked": "prior hypotheses",
                        "reason": "Hypotheses must never be promoted to confirmed facts.",
                    }
                )
            elif fact not in allowed_confirmed_facts:
                unsupported_claims.append(
                    {
                        "role": role_name,
                        "unsupported_claim": fact,
                        "source_checked": "original scenario and previous confirmed_facts",
                        "reason": "Confirmed fact does not exactly match known evidence.",
                    }
                )

    def check_recommendations(
        role_name: str,
        output: RoleOutput,
        allowed_confirmed_facts: set[str],
        allowed_hypotheses: set[str],
    ) -> None:
        known_evidence = allowed_confirmed_facts | allowed_hypotheses
        for recommendation in output["recommendations"]:
            action = recommendation["action"]
            supporting_evidence = recommendation["supporting_evidence"]
            evidence_set = set(supporting_evidence)

            if not supporting_evidence:
                unsupported_claims.append(
                    {
                        "role": role_name,
                        "unsupported_claim": action,
                        "source_checked": "recommendation supporting_evidence",
                        "reason": "Recommendations without supporting evidence are rejected.",
                    }
                )

            unsupported_evidence = evidence_set - known_evidence
            if unsupported_evidence:
                unsupported_claims.append(
                    {
                        "role": role_name,
                        "unsupported_claim": action,
                        "source_checked": "confirmed_facts and hypotheses",
                        "reason": "Recommendation cites unsupported evidence.",
                        "unsupported_evidence": sorted(unsupported_evidence),
                    }
                )

            based_only_on_hypotheses = (
                bool(evidence_set) and evidence_set <= allowed_hypotheses
            )
            if based_only_on_hypotheses and not recommendation["provisional"]:
                unsupported_claims.append(
                    {
                        "role": role_name,
                        "unsupported_claim": action,
                        "source_checked": "recommendation supporting_evidence",
                        "reason": "Recommendations based only on hypotheses must be marked provisional.",
                    }
                )

            requires_approval = (
                recommendation["risk"] == "high"
                or recommendation["reversibility"] == "irreversible"
            )
            if requires_approval and not recommendation["human_approval_required"]:
                unsupported_claims.append(
                    {
                        "role": role_name,
                        "unsupported_claim": action,
                        "source_checked": "risk and reversibility",
                        "reason": "High-risk or irreversible actions must require human approval.",
                    }
                )

            if recommendation["human_approval_required"]:
                approval_queue.append(
                    {
                        "role": role_name,
                        "action": action,
                        "approval_owner": recommendation["approval_owner"],
                        "risk": recommendation["risk"],
                        "reversibility": recommendation["reversibility"],
                        "workflow_status": "STOPPED_BEFORE_EXECUTION",
                    }
                )

    scenario_facts = set(scenario["confirmed_facts"])
    scenario_hypotheses = set(scenario["hypotheses"])
    check_confirmed_facts(
        "Senior Partner Engineer",
        triage_report,
        scenario_facts,
        scenario_hypotheses,
    )
    check_recommendations(
        "Senior Partner Engineer",
        triage_report,
        scenario_facts | set(triage_report["confirmed_facts"]),
        scenario_hypotheses | set(triage_report["hypotheses"]),
    )

    architect_allowed_facts = scenario_facts | set(triage_report["confirmed_facts"])
    architect_allowed_hypotheses = scenario_hypotheses | set(
        triage_report["hypotheses"]
    )
    check_confirmed_facts(
        "API Architect",
        architecture_review,
        architect_allowed_facts,
        architect_allowed_hypotheses,
    )
    check_recommendations(
        "API Architect",
        architecture_review,
        architect_allowed_facts | set(architecture_review["confirmed_facts"]),
        architect_allowed_hypotheses | set(architecture_review["hypotheses"]),
    )

    manager_allowed_facts = architect_allowed_facts | set(
        architecture_review["confirmed_facts"]
    )
    prior_hypotheses = (
        set(scenario["hypotheses"])
        | set(triage_report["hypotheses"])
        | set(architecture_review["hypotheses"])
    )
    check_confirmed_facts(
        "Platform Partnerships Manager",
        partner_response_plan,
        manager_allowed_facts,
        prior_hypotheses,
    )
    check_recommendations(
        "Platform Partnerships Manager",
        partner_response_plan,
        manager_allowed_facts | set(partner_response_plan["confirmed_facts"]),
        prior_hypotheses | set(partner_response_plan["hypotheses"]),
    )

    if not unsupported_claims:
        return "VALIDATION PASSED", approval_queue

    return (
        json.dumps(
            {
                "status": "VALIDATION FAILED",
                "unsupported_claims": unsupported_claims,
            },
            indent=2,
        ),
        approval_queue,
    )


def run_workflow(scenario: Scenario) -> dict[str, Any]:
    client = OpenAI()

    engineer = RoleStep(
        name="Senior Partner Engineer",
        prompt=SENIOR_PARTNER_ENGINEER_PROMPT,
    )
    architect = RoleStep(
        name="API Architect",
        prompt=API_ARCHITECT_PROMPT,
    )
    manager = RoleStep(
        name="Platform Partnerships Manager",
        prompt=PLATFORM_PARTNERSHIPS_MANAGER_PROMPT,
    )

    triage_report = call_role(client, engineer, build_engineer_input(scenario))
    human_approval_checkpoint(engineer.name, triage_report)
    triage_json = parse_role_json(engineer.name, triage_report)

    architecture_review = call_role(
        client,
        architect,
        build_architect_input(scenario, triage_report),
    )
    human_approval_checkpoint(architect.name, architecture_review)
    architecture_json = parse_role_json(architect.name, architecture_review)

    partner_response_plan = call_role(
        client,
        manager,
        build_manager_input(scenario, triage_report, architecture_review),
    )
    human_approval_checkpoint(manager.name, partner_response_plan)
    partner_response_json = parse_role_json(manager.name, partner_response_plan)

    validation_result, human_approval_queue = validate_evidence(
        scenario,
        triage_json,
        architecture_json,
        partner_response_json,
    )
    human_approval_checkpoint("Evidence-Control Validator", validation_result)

    return {
        "scenario": scenario,
        "senior_partner_engineer": triage_json,
        "api_architect": architecture_json,
        "platform_partnerships_manager": partner_response_json,
        "validation_result": validation_result,
        "human_approval_queue": human_approval_queue,
    }


def print_section(title: str, body: Any) -> None:
    print(f"\n\n## {title}\n")
    if isinstance(body, str):
        print(body)
    else:
        print(json.dumps(body, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the AI-assisted partner operations workflow."
    )
    parser.add_argument("scenario_file", type=Path, help="Path to scenario JSON")
    args = parser.parse_args()

    scenario = load_scenario(args.scenario_file)
    outputs = run_workflow(scenario)

    print_section("Original Scenario", outputs["scenario"])
    print_section(
        "Senior Partner Engineer Triage Report",
        outputs["senior_partner_engineer"],
    )
    print_section("API Architect Architecture Review", outputs["api_architect"])
    print_section(
        "Platform Partnerships Manager Partner Response Plan",
        outputs["platform_partnerships_manager"],
    )
    print_section("Evidence-Control Validation Result", outputs["validation_result"])
    print_section("Human Approval Queue", outputs["human_approval_queue"])


if __name__ == "__main__":
    main()
