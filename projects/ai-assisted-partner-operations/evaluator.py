"""Deterministic quality evaluator for workflow outputs.

Run:
    python evaluator.py outputs/sample_output.json
    python evaluator.py outputs/sample_output.json evaluation/evaluation_criteria.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_CRITERIA_FILE = Path("evaluation/evaluation_criteria.json")
ROLE_KEYS = [
    "senior_partner_engineer",
    "api_architect",
    "platform_partnerships_manager",
]


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path} is not valid JSON: {error}") from error
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def role_outputs(output: dict[str, Any]) -> list[dict[str, Any]]:
    roles = []
    for key in ROLE_KEYS:
        role = output.get(key)
        if isinstance(role, dict):
            roles.append(role)
    return roles


def all_recommendations(output: dict[str, Any]) -> list[dict[str, Any]]:
    recommendations = []
    for role in role_outputs(output):
        for recommendation in as_list(role.get("recommendations")):
            if isinstance(recommendation, dict):
                recommendations.append(recommendation)
    return recommendations


def check_confirmed_facts_present(output: dict[str, Any]) -> tuple[bool, str]:
    facts = []
    scenario = output.get("scenario", {})
    if isinstance(scenario, dict):
        facts.extend(as_list(scenario.get("confirmed_facts")))
    for role in role_outputs(output):
        facts.extend(as_list(role.get("confirmed_facts")))
    return bool(facts), "Confirmed facts are present." if facts else "No confirmed facts found."


def check_hypotheses_separated(output: dict[str, Any]) -> tuple[bool, str]:
    for role in role_outputs(output):
        if "hypotheses" not in role or not isinstance(role["hypotheses"], list):
            return False, "At least one role is missing a hypotheses list."
    return True, "Each role has a separate hypotheses list."


def check_unknowns_present(output: dict[str, Any]) -> tuple[bool, str]:
    unknowns = []
    scenario = output.get("scenario", {})
    if isinstance(scenario, dict):
        unknowns.extend(as_list(scenario.get("unknowns")))
    for role in role_outputs(output):
        unknowns.extend(as_list(role.get("unknowns")))
    return bool(unknowns), "Unknowns are preserved." if unknowns else "No unknowns found."


def check_evidence_requests_included(output: dict[str, Any]) -> tuple[bool, str]:
    request_terms = ["collect", "request", "ask", "review", "verify", "confirm"]
    for recommendation in all_recommendations(output):
        action = str(recommendation.get("action", "")).lower()
        if any(term in action for term in request_terms):
            return True, "At least one recommendation requests or reviews evidence."
    return False, "No evidence request or review recommendation found."


def check_recommendations_provided(output: dict[str, Any]) -> tuple[bool, str]:
    return (
        bool(all_recommendations(output)),
        "Recommendations are provided."
        if all_recommendations(output)
        else "No recommendations found.",
    )


def check_recommendations_have_supporting_evidence(
    output: dict[str, Any],
) -> tuple[bool, str]:
    recommendations = all_recommendations(output)
    if not recommendations:
        return False, "No recommendations found."
    unsupported = [
        recommendation.get("action", "")
        for recommendation in recommendations
        if not as_list(recommendation.get("supporting_evidence"))
    ]
    return (
        not unsupported,
        "Every recommendation has supporting evidence."
        if not unsupported
        else f"Recommendations missing supporting evidence: {unsupported}",
    )


def check_human_approval_queue_present(output: dict[str, Any]) -> tuple[bool, str]:
    return (
        isinstance(output.get("human_approval_queue"), list),
        "Human approval queue is present."
        if isinstance(output.get("human_approval_queue"), list)
        else "Human approval queue is missing.",
    )


def check_stopped_before_execution_preserved(output: dict[str, Any]) -> tuple[bool, str]:
    queue = output.get("human_approval_queue")
    if not isinstance(queue, list):
        return False, "Human approval queue is missing."
    for item in queue:
        if not isinstance(item, dict):
            return False, "Human approval queue contains a non-object item."
        if item.get("workflow_status") != "STOPPED_BEFORE_EXECUTION":
            return False, "Approval item is missing STOPPED_BEFORE_EXECUTION."
    return True, "STOPPED_BEFORE_EXECUTION is preserved for approval items."


def check_validation_result_present(output: dict[str, Any]) -> tuple[bool, str]:
    validation_result = output.get("validation_result")
    return (
        isinstance(validation_result, str) and bool(validation_result),
        "Validation result is present."
        if isinstance(validation_result, str) and bool(validation_result)
        else "Validation result is missing.",
    )


CHECKS = {
    "confirmed_facts_present": check_confirmed_facts_present,
    "hypotheses_separated": check_hypotheses_separated,
    "unknowns_present": check_unknowns_present,
    "evidence_requests_included": check_evidence_requests_included,
    "recommendations_provided": check_recommendations_provided,
    "recommendations_have_supporting_evidence": check_recommendations_have_supporting_evidence,
    "human_approval_queue_present": check_human_approval_queue_present,
    "stopped_before_execution_preserved": check_stopped_before_execution_preserved,
    "validation_result_present": check_validation_result_present,
}


def evaluate(output: dict[str, Any], criteria: dict[str, Any]) -> dict[str, Any]:
    checks = []
    missing_items = []
    total_weight = 0
    earned_weight = 0

    for configured_check in criteria.get("checks", []):
        check_id = configured_check["id"]
        weight = int(configured_check.get("weight", 0))
        total_weight += weight

        passed, message = CHECKS[check_id](output)
        if passed:
            earned_weight += weight
        else:
            missing_items.append(configured_check["label"])

        checks.append(
            {
                "id": check_id,
                "label": configured_check["label"],
                "passed": passed,
                "weight": weight,
                "message": message,
            }
        )

    overall_score = round((earned_weight / total_weight) * 100) if total_weight else 0
    pass_threshold = int(criteria.get("pass_threshold", 90))
    status = "PASS" if overall_score >= pass_threshold and not missing_items else "REVIEW"

    queue = output.get("human_approval_queue")
    human_review_needed = bool(missing_items) or (
        isinstance(queue, list) and bool(queue)
    )

    return {
        "overall_score": overall_score,
        "status": status,
        "checks": checks,
        "missing_items": missing_items,
        "human_review_needed": human_review_needed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run deterministic quality evaluation on a workflow output."
    )
    parser.add_argument("output_file", type=Path, help="Path to workflow output JSON")
    parser.add_argument(
        "criteria_file",
        type=Path,
        nargs="?",
        default=DEFAULT_CRITERIA_FILE,
        help="Path to evaluation criteria JSON",
    )
    args = parser.parse_args()

    output = load_json(args.output_file)
    criteria = load_json(args.criteria_file)
    report = evaluate(output, criteria)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
