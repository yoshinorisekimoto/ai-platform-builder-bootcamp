"""Day 48: External Partner communication control."""


REQUIRED_ENGINEERING_CONDITIONS = (
    "approved_limit_rpm",
    "approval_scope",
    "rollback_required",
    "partner_confirmation_required",
)

REQUIRED_CONTEXT = (
    "partner_id",
    "engineering_decision_id",
    "timestamp",
)

REQUIRED_COMMUNICATION_RECORD = (
    "partner_message",
    "lead_reviewed",
)


def is_missing(value):
    return value is None or value == ""


def prepare_partner_message(case):
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
        "communication_status": "PENDING",
        "engineering_conditions": {},
        "partner_message": case.get("partner_message"),
        "lead_reviewed": case.get("lead_reviewed", False),
        "decision_owner": "ENGINEERING",
        "communication_owner": "PLATFORM_PARTNER_LEAD",
        "external_send_authorized": False,
        "new_commitment_allowed": False,
        "routing": "PLATFORM_PARTNER_LEAD",
        "next_owner": "PLATFORM_PARTNER_LEAD",
        "resume_condition": None,
        "audit_trail": "REQUIRED",
        "missing_conditions": missing_conditions,
        "missing_context": missing_context,
    }

    if missing_conditions or missing_context:
        result["action"] = "STOP_INCOMPLETE_PARTNER_MESSAGE"
        result["communication_status"] = "BLOCKED"
        result["resume_condition"] = (
            "ALL_ENGINEERING_CONDITIONS_AND_CONTEXT_VERIFIED"
        )
        return result

    result["engineering_conditions"] = {
        field: case[field]
        for field in REQUIRED_ENGINEERING_CONDITIONS
    }

    result["action"] = "PREPARE_PARTNER_MESSAGE"
    result["communication_status"] = "READY_FOR_LEAD_REVIEW"
    result["resume_condition"] = "PLATFORM_PARTNER_LEAD_APPROVAL"

    return result


def approve_partner_message(result):
    if result["communication_status"] != "READY_FOR_LEAD_REVIEW":
        return result

    if not result["lead_reviewed"]:
        result["action"] = "WAIT_FOR_LEAD_REVIEW"
        return result

    result["external_send_authorized"] = True
    result["communication_status"] = "APPROVED_FOR_EXTERNAL_SEND"
    result["action"] = "SEND_PARTNER_MESSAGE"
    result["resume_condition"] = "PARTNER_MESSAGE_SENT_AND_RECORDED"

    return result


def evaluate_partner_request(
    result,
    partner_requests_full_day,
    partner_previously_accepted_conditions,
    engineering_approved_full_day,
):
    if result["communication_status"] != "APPROVED_FOR_EXTERNAL_SEND":
        return result

    if partner_requests_full_day:
        if not engineering_approved_full_day:
            result["action"] = "STOP_UNAPPROVED_NEW_COMMITMENT"
            result["communication_status"] = "BLOCKED"

            if partner_previously_accepted_conditions:
                result["resume_condition"] = (
                    "NEW_ENGINEERING_DECISION_REQUIRED"
                )
            else:
                result["resume_condition"] = (
                    "PARTNER_CONDITIONS_RECONFIRMED_OR_"
                    "NEW_ENGINEERING_REVIEW_COMPLETED"
                )

            return result

    result["action"] = "COMPLETE_EXTERNAL_COMMUNICATION"
    result["communication_status"] = "COMPLETED"
    result["resume_condition"] = "NOT_REQUIRED"

    return result


cases = {
    "Approved Partner communication": {
        "approved_limit_rpm": 500,
        "approval_scope": "LAUNCH_WINDOW_ONLY",
        "rollback_required": True,
        "partner_confirmation_required": True,
        "partner_id": "partner-001",
        "engineering_decision_id": "eng-decision-048",
        "timestamp": "2026-10-06T14:00:00+09:00",
        "partner_message": (
            "500 rpm is approved only during the launch window. "
            "The temporary limit will be removed after launch. "
            "Please confirm when traffic returns to normal."
        ),
        "lead_reviewed": True,
    },
}


for name, case in cases.items():
    result = prepare_partner_message(case)

    result = approve_partner_message(result)

    result = evaluate_partner_request(
        result,
        partner_requests_full_day=False,
        partner_previously_accepted_conditions=True,
        engineering_approved_full_day=False,
    )

    print(name)
    print("Action:", result["action"])
    print(
        "Communication status:",
        result["communication_status"],
    )
    print(
        "Engineering conditions:",
        result["engineering_conditions"],
    )
    print(
        "Communication owner:",
        result["communication_owner"],
    )
    print(
        "External send authorized:",
        result["external_send_authorized"],
    )
    print(
        "New commitment allowed:",
        result["new_commitment_allowed"],
    )
    print("Routing:", result["routing"])
    print("Next owner:", result["next_owner"])
    print("Resume condition:", result["resume_condition"])
    print("Audit trail:", result["audit_trail"])
    print()