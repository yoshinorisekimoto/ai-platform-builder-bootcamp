"""Day 40: Agent operating-rules test."""


def evaluate_case(case):
    result = {
        "action": None,
        "escalation": "NOT_REQUIRED",
        "external_communication": "NOT_AUTHORIZED",
        "audit_trail": "REQUIRED",
    }

    if case["evidence_conflict"]:
        result["action"] = "STOP_EXECUTION"
        result["escalation"] = "ESCALATE_TO_PLATFORM_PARTNER_LEAD"
        return result

    if not case["classification_evidence_complete"]:
        result["action"] = "STOP_CLASSIFICATION"
        result["escalation"] = "ESCALATE_TO_PLATFORM_PARTNER_LEAD"
        return result

    if not case["standard_work"]:
        result["action"] = "STOP_STANDARD_WORK"
        result["escalation"] = "ESCALATE_TO_PLATFORM_PARTNER_LEAD"
        return result

    if not case["execution_evidence_complete"]:
        result["action"] = "STOP_EXECUTION"
        result["escalation"] = "ESCALATE_TO_PLATFORM_PARTNER_LEAD"
        return result

    result["action"] = "EXECUTE_STANDARD_WORK"
    return result


cases = {
    "Approved standard work": {
        "classification_evidence_complete": True,
        "execution_evidence_complete": True,
        "evidence_conflict": False,
        "standard_work": True,
    },
    "Missing execution evidence": {
        "classification_evidence_complete": True,
        "execution_evidence_complete": False,
        "evidence_conflict": False,
        "standard_work": True,
    },
    "Conflicting evidence": {
        "classification_evidence_complete": True,
        "execution_evidence_complete": True,
        "evidence_conflict": True,
        "standard_work": True,
    },
    "Non-standard Partner case": {
        "classification_evidence_complete": True,
        "execution_evidence_complete": True,
        "evidence_conflict": False,
        "standard_work": False,
    },
}


for name, case in cases.items():
    result = evaluate_case(case)
    print(name)
    print("Action:", result["action"])
    print("Escalation:", result["escalation"])
    print("External communication:", result["external_communication"])
    print("Audit trail:", result["audit_trail"])
    print()