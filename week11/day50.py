"""Day 50: End-to-end Partner workflow orchestration."""


REQUIRED_PARTNER_DATA = (
    "partner_id",
    "endpoint",
    "current_traffic_rpm",
    "expected_peak_rpm",
    "requested_limit_rpm",
    "retry_traffic_included",
    "peak_duration_minutes",
    "requested_end_time",
)

REQUIRED_CLOSURE_DATA = (
    "partner_traffic_normal_confirmed",
    "rollback_verified",
    "engineering_decision_recorded",
    "partner_communication_recorded",
    "no_missing_evidence",
    "no_conflicting_evidence",
    "no_unresolved_operational_risk",
)


def is_missing(value):
    return value is None or value == ""


def evaluate_partner_request(case):
    missing_data = [
        field for field in REQUIRED_PARTNER_DATA
        if is_missing(case.get(field))
    ]

    result = {
        "action": None,
        "workflow_status": None,
        "missing_data": missing_data,
        "routing": None,
        "next_owner": None,
        "decision_owner": "ENGINEERING",
        "communication_owner": "PLATFORM_PARTNER_LEAD",
        "external_send_authorized": False,
        "audit_trail": "REQUIRED",
        "resume_condition": None,
    }

    if missing_data:
        result["action"] = "STOP_AND_REQUEST_MISSING_INFORMATION"
        result["workflow_status"] = "BLOCKED_MISSING_INFORMATION"
        result["routing"] = "PLATFORM_PARTNER_LEAD"
        result["next_owner"] = "PARTNER"
        result["resume_condition"] = (
            "ALL_REQUIRED_PARTNER_DATA_VERIFIED"
        )
        return result

    result["action"] = "ROUTE_TO_ENGINEERING"
    result["workflow_status"] = "READY_FOR_ENGINEERING"
    result["routing"] = "ENGINEERING"
    result["next_owner"] = "ENGINEERING"
    result["resume_condition"] = "ENGINEERING_DECISION_RECORDED"

    return result


def apply_engineering_decision(result, decision):
    if result["workflow_status"] != "READY_FOR_ENGINEERING":
        return result

    result["engineering_decision"] = decision
    result["action"] = "PREPARE_INTERNAL_AND_EXTERNAL_HANDOFF"
    result["workflow_status"] = "APPROVED_WITH_CONDITIONS"
    result["routing"] = "PRODUCT_OPERATIONS"
    result["next_owner"] = "PRODUCT_OPERATIONS"
    result["resume_condition"] = "LEAD_APPROVES_EXTERNAL_MESSAGE"

    return result


def evaluate_closure(result, closure):
    if result["workflow_status"] != "APPROVED_WITH_CONDITIONS":
        return result

    incomplete = [
        field for field in REQUIRED_CLOSURE_DATA
        if not closure.get(field)
    ]

    if incomplete:
        result["action"] = "KEEP_WORKFLOW_OPEN"
        result["workflow_status"] = "FOLLOW_UP_REQUIRED"
        result["resume_condition"] = (
            "ALL_CLOSURE_CONDITIONS_VERIFIED"
        )
        return result

    result["action"] = "PREPARE_FINAL_CLOSURE"
    result["workflow_status"] = "READY_TO_CLOSE"
    result["routing"] = "PLATFORM_PARTNER_LEAD"
    result["next_owner"] = "PLATFORM_PARTNER_LEAD"
    result["resume_condition"] = "FINAL_HUMAN_CLOSURE_APPROVAL"

    return result


case = {
    "partner_id": "partner-001",
    "endpoint": "/production/applications",
    "current_traffic_rpm": 320,
    "expected_peak_rpm": 520,
    "requested_limit_rpm": 600,
    "retry_traffic_included": True,
    "peak_duration_minutes": 8,
    "requested_end_time": "18:00",
}


result = evaluate_partner_request(case)

result = apply_engineering_decision(
    result,
    {
        "approved_limit_rpm": 600,
        "approval_scope": "LAUNCH_WINDOW_ONLY",
        "automatic_rollback_required": True,
        "operations_verification_required": True,
        "partner_confirmation_required": True,
    },
)

result = evaluate_closure(
    result,
    {
        "partner_traffic_normal_confirmed": True,
        "rollback_verified": True,
        "engineering_decision_recorded": True,
        "partner_communication_recorded": True,
        "no_missing_evidence": True,
        "no_conflicting_evidence": True,
        "no_unresolved_operational_risk": True,
    },
)

print("Action:", result["action"])
print("Workflow status:", result["workflow_status"])
print("Routing:", result["routing"])
print("Next owner:", result["next_owner"])
print("Decision owner:", result["decision_owner"])
print("Communication owner:", result["communication_owner"])
print("External send authorized:", result["external_send_authorized"])
print("Resume condition:", result["resume_condition"])
print("Audit trail:", result["audit_trail"])