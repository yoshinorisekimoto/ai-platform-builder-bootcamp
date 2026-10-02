"""Day 46: Decision preparation and Engineering review control."""


REQUIRED_TECHNICAL_EVIDENCE = (
    "current_traffic_rpm",
    "expected_peak_rpm",
    "requested_limit_rpm",
    "peak_duration_minutes",
    "recent_429_logs",
    "calculation_basis",
)

REQUIRED_BUSINESS_CONTEXT = (
    "business_reason",
    "target_date",
)

REQUIRED_CONTEXT = (
    "partner_id",
    "endpoint",
    "timestamp",
)


def is_missing(value):
    return value is None or value == ""


def prepare_decision_brief(case):
    missing_technical = [
        field for field in REQUIRED_TECHNICAL_EVIDENCE
        if is_missing(case.get(field))
    ]

    missing_business = [
        field for field in REQUIRED_BUSINESS_CONTEXT
        if is_missing(case.get(field))
    ]

    missing_context = [
        field for field in REQUIRED_CONTEXT
        if is_missing(case.get(field))
    ]

    result = {
        "action": None,
        "decision_status": "PENDING",
        "technical_evidence": {},
        "business_context": {},
        "ai_analysis": case.get("ai_analysis"),
        "missing_technical_evidence": missing_technical,
        "missing_business_context": missing_business,
        "missing_context": missing_context,
        "routing": "ENGINEERING",
        "next_owner": "ENGINEERING",
        "decision_owner": "ENGINEERING",
        "communication_owner": "PLATFORM_PARTNER_LEAD",
        "external_communication": "NOT_AUTHORIZED",
        "resume_condition": None,
        "audit_trail": "REQUIRED",
    }

    if missing_technical or missing_business or missing_context:
        result["action"] = "STOP_INCOMPLETE_DECISION_BRIEF"
        result["decision_status"] = "BLOCKED"
        result["routing"] = "PLATFORM_PARTNER_LEAD"
        result["next_owner"] = "PLATFORM_PARTNER_LEAD"
        result["resume_condition"] = "ALL_REQUIRED_DATA_VERIFIED"
        return result

    result["technical_evidence"] = {
        field: case[field]
        for field in REQUIRED_TECHNICAL_EVIDENCE
    }

    result["business_context"] = {
        field: case[field]
        for field in REQUIRED_BUSINESS_CONTEXT
    }

    result["action"] = "PREPARE_AND_ROUTE_DECISION_BRIEF"
    result["decision_status"] = "READY_FOR_ENGINEERING"
    result["resume_condition"] = "ENGINEERING_DECISION_RECORDED"

    return result


def apply_engineering_decision(result, engineering_decision):
    if result["decision_status"] != "READY_FOR_ENGINEERING":
        return result

    if is_missing(engineering_decision):
        result["action"] = "WAIT_FOR_ENGINEERING_DECISION"
        return result

    result["engineering_decision"] = engineering_decision
    result["decision_status"] = "ENGINEERING_DECIDED"
    result["action"] = "RECORD_ENGINEERING_DECISION"
    result["routing"] = "PLATFORM_PARTNER_LEAD"
    result["next_owner"] = "PLATFORM_PARTNER_LEAD"
    result["resume_condition"] = (
        "ENGINEERING_DECISION_RECORDED_AND_VERIFIED"
    )

    return result


def evaluate_completion(
    result,
    partner_confirmation,
    limit_removed,
):
    if result["decision_status"] != "ENGINEERING_DECIDED":
        return result

    if not partner_confirmation or not limit_removed:
        result["action"] = "KEEP_CASE_OPEN"
        result["resume_condition"] = (
            "NORMAL_TRAFFIC_CONFIRMED_"
            "AND_TEMPORARY_LIMIT_REMOVED"
        )
        return result

    result["action"] = "CLOSE_CASE"
    result["decision_status"] = "COMPLETED"
    result["resume_condition"] = "NOT_REQUIRED"

    return result


cases = {
    "Complete Decision Brief": {
        "current_traffic_rpm": 320,
        "expected_peak_rpm": 450,
        "requested_limit_rpm": 500,
        "peak_duration_minutes": 8,
        "recent_429_logs": True,
        "calculation_basis": "VERIFIED",
        "business_reason": "MAJOR_CUSTOMER_LAUNCH",
        "target_date": "2026-10-03",
        "partner_id": "partner-001",
        "endpoint": "/production/applications",
        "timestamp": "2026-10-02T15:00:00+09:00",
        "ai_analysis": (
            "Traffic increase appears temporary. "
            "Final technical decision remains with Engineering."
        ),
    },
}


for name, case in cases.items():
    result = prepare_decision_brief(case)

    result = apply_engineering_decision(
        result,
        {
            "approved_limit_rpm": 500,
            "approval_scope": "LAUNCH_WINDOW_ONLY",
            "temporary_limit_removal_required": True,
        },
    )

    result = evaluate_completion(
        result,
        partner_confirmation=True,
        limit_removed=True,
    )

    print(name)
    print("Action:", result["action"])
    print("Decision status:", result["decision_status"])
    print("Technical evidence:", result["technical_evidence"])
    print("Business context:", result["business_context"])
    print("AI analysis:", result["ai_analysis"])
    print("Routing:", result["routing"])
    print("Next owner:", result["next_owner"])
    print("Decision owner:", result["decision_owner"])
    print(
        "Communication owner:",
        result["communication_owner"],
    )
    print(
        "External communication:",
        result["external_communication"],
    )
    print("Resume condition:", result["resume_condition"])
    print("Audit trail:", result["audit_trail"])
    print()