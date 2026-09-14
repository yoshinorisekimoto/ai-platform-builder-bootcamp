"""Day 37: Standard-work eligibility test."""


def classify_request(case):
    required_evidence = {
        "approved_api_guide",
        "sanitized_logs",
        "approved_runbook",
    }

    if not required_evidence.issubset(case["available_evidence"]):
        return "ESCALATE_MISSING_APPROVED_EVIDENCE"

    if not case["matches_standard_runbook"]:
        return "ESCALATE_NON_STANDARD_REQUEST"

    if "retry_configuration" not in case["available_evidence"]:
        return "REQUEST_MISSING_EVIDENCE"

    return "DRAFT_STANDARD_RESPONSE_FOR_REVIEW"


before = {
    "available_evidence": {
        "approved_api_guide",
        "sanitized_logs",
        "approved_runbook",
    },
    "matches_standard_runbook": True,
}

after = {
    "available_evidence": {
        "approved_api_guide",
        "sanitized_logs",
        "approved_runbook",
        "retry_configuration",
    },
    "matches_standard_runbook": True,
}

print("Before:", classify_request(before))
print("After:", classify_request(after))