"""Day 47: Internal decision handoff and communication control."""


REQUIRED_ENGINEERING_CONDITIONS = (
    "approved_limit_rpm",
    "approval_scope",
    "rollback_condition",
    "operations_verification_required",
)

REQUIRED_CONTEXT = (
    "partner_id",
    "endpoint",
    "engineering_decision_id",
    "timestamp",
)


def is_missing(value):
    return value is None or value == ""


def prepare_internal_notice(case):
    missing_conditions = [
        field for field in REQUIRED_ENGINEERING_CONDITIONS
        if is_missing(case.get(field))
    ]

    missing_context = [
        field for field in REQUIRED_CONTEXT
        if is_missing(case.get(field))
    ]

    result = {
        "action": None,
        "notice_status": "PENDING",
        "engineering_conditions": {},
        "recipients": case.get("recipients", []),
        "routing": "INTERNAL_TEAMS",
        "next_owner": "PRODUCT_OPERATIONS",
        "decision_owner": "ENGINEERING",
        "communication_owner": "PLATFORM_PARTNER_LEAD",
        "internal_send_authorized": False,
        "external_communication": "NOT_AUTHORIZED",
        "resume_condition": None,
        "audit_trail": "REQUIRED",
        "missing_conditions": missing_conditions,
        "missing_context": missing_context,
    }

    if missing_conditions or missing_context:
        result["action"] = "STOP_INCOMPLETE_INTERNAL_NOTICE"
        result["notice_status"] = "BLOCKED"
        result["resume_condition"] = (
            "ALL_ENGINEERING_CONDITIONS_AND_CONTEXT_VERIFIED"
        )
        return result

    result["engineering_conditions"] = {
        field: case[field]
        for field in REQUIRED_ENGINEERING_CONDITIONS
    }

    result["action"] = "PREPARE_INTERNAL_NOTICE"
    result["notice_status"] = "READY_FOR_LEAD_REVIEW"
    result["resume_condition"] = "PLATFORM_PARTNER_LEAD_APPROVAL"

    return result


def approve_internal_notice(result, lead_approved):
    if result["notice_status"] != "READY_FOR_LEAD_REVIEW":
        return result

    if not lead_approved:
        result["action"] = "WAIT_FOR_LEAD_APPROVAL"
        return result

    result["internal_send_authorized"] = True
    result["notice_status"] = "APPROVED_FOR_INTERNAL_SEND"
    result["action"] = "SEND_INTERNAL_NOTICE"
    result["resume_condition"] = "INTERNAL_NOTICE_SENT_AND_RECORDED"

    return result


def evaluate_execution(
    result,
    engineering_approval_for_rollback,
    partner_traffic_normal_confirmed,
    limit_restored_verified,
):
    if result["notice_status"] != "APPROVED_FOR_INTERNAL_SEND":
        return result

    if not engineering_approval_for_rollback:
        result["action"] = "STOP_UNAPPROVED_ROLLBACK_CHANGE"
        result["resume_condition"] = (
            "ENGINEERING_APPROVES_ROLLBACK_METHOD"
        )
        return result

    if not partner_traffic_normal_confirmed:
        result["action"] = "WAIT_FOR_PARTNER_TRAFFIC_CONFIRMATION"
        result["resume_condition"] = (
            "PARTNER_CONFIRMS_TRAFFIC_RETURNED_TO_NORMAL"
        )
        return result

    if not limit_restored_verified:
        result["action"] = "WAIT_FOR_OPERATIONS_VERIFICATION"
        result["resume_condition"] = (
            "PRODUCT_OPERATIONS_VERIFIES_LIMIT_RESTORED"
        )
        return result

    result["action"] = "COMPLETE_INTERNAL_HANDOFF"
    result["notice_status"] = "COMPLETED"
    result["resume_condition"] = "NOT_REQUIRED"

    return result


cases = {
    "Approved internal handoff": {
        "approved_limit_rpm": 500,
        "approval_scope": "LAUNCH_WINDOW_ONLY",
        "rollback_condition": (
            "ROLLBACK_AFTER_PARTNER_CONFIRMS_TRAFFIC_NORMAL"
        ),
        "operations_verification_required": True,
        "partner_id": "partner-001",
        "endpoint": "/production/applications",
        "engineering_decision_id": "eng-decision-047",
        "timestamp": "2026-10-05T14:30:00+09:00",
        "recipients": [
            "PRODUCT_OPERATIONS",
            "SUPPORT",
        ],
    },
}


for name, case in cases.items():
    result = prepare_internal_notice(case)

    result = approve_internal_notice(
        result,
        lead_approved=True,
    )

    result = evaluate_execution(
        result,
        engineering_approval_for_rollback=True,
        partner_traffic_normal_confirmed=True,
        limit_restored_verified=True,
    )

    print(name)
    print("Action:", result["action"])
    print("Notice status:", result["notice_status"])
    print(
        "Engineering conditions:",
        result["engineering_conditions"],
    )
    print("Recipients:", result["recipients"])
    print("Routing:", result["routing"])
    print("Next owner:", result["next_owner"])
    print("Decision owner:", result["decision_owner"])
    print(
        "Communication owner:",
        result["communication_owner"],
    )
    print(
        "Internal send authorized:",
        result["internal_send_authorized"],
    )
    print(
        "External communication:",
        result["external_communication"],
    )
    print("Resume condition:", result["resume_condition"])
    print("Audit trail:", result["audit_trail"])
    print()