"""Day 51: Agent role separation and delegation control."""


AUTO_ACTIONS = (
    "EVIDENCE_VALIDATION",
    "CONFLICT_DETECTION",
    "STANDARD_CLARIFICATION",
    "INTERNAL_ROUTING",
    "AUDIT_RECORDING",
)

HUMAN_GATE_ACTIONS = (
    "EXTERNAL_COMMITMENT",
    "EXCEPTION_APPROVAL",
    "FINAL_TECHNICAL_DECISION",
)

ESCALATION_TRIGGERS = (
    "UNRESOLVED_CONFLICT",
    "AUTHORITY_OVERREACH",
    "HIGH_RISK_EXCEPTION",
)


def evaluate_agent_message(case):
    result = {
        "action": None,
        "status": None,
        "next_owner": None,
        "human_review_required": False,
        "resume_condition": None,
        "audit_trail": "REQUIRED",
    }

    if case.get("unauthorized_commitment"):
        result["action"] = "BLOCK_UNAUTHORIZED_COMMITMENT"
        result["status"] = "ESCALATED"
        result["next_owner"] = "PLATFORM_PARTNER_LEAD"
        result["human_review_required"] = True
        result["resume_condition"] = (
            "UNAUTHORIZED_COMMITMENT_CORRECTED"
        )
        return result

    if case.get("source_conflict"):
        result["action"] = "REQUEST_AGENT_CLARIFICATION"
        result["status"] = "WAITING_FOR_CLARIFICATION"
        result["next_owner"] = "AGENCY_AGENT"
        result["resume_condition"] = (
            "AUTHORITATIVE_VALUE_VERIFIED"
        )
        return result

    result["action"] = "CONTINUE_AUTONOMOUS_WORKFLOW"
    result["status"] = "AUTO"
    result["next_owner"] = "PLATFORM_AGENT"
    result["resume_condition"] = "NOT_REQUIRED"

    return result


cases = {
    "Unauthorized Partner commitment": {
        "unauthorized_commitment": True,
        "source_conflict": False,
    },
    "Conflicting Partner duration": {
        "unauthorized_commitment": False,
        "source_conflict": True,
    },
    "Standard Agent-to-Agent flow": {
        "unauthorized_commitment": False,
        "source_conflict": False,
    },
}


for name, case in cases.items():
    result = evaluate_agent_message(case)

    print(name)
    print("Action:", result["action"])
    print("Status:", result["status"])
    print("Next owner:", result["next_owner"])
    print(
        "Human review required:",
        result["human_review_required"],
    )
    print("Resume condition:", result["resume_condition"])
    print("Audit trail:", result["audit_trail"])
    print()