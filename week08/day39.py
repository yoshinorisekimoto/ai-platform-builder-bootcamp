"""Day 39: Integrated boundary test."""


def evaluate_case(case):
    if case["unapproved_data_fields"]:
        return {
            "route": "ESCALATE_TO_PLATFORM_PARTNER_LEAD",
            "launch": "HOLD_LAUNCH",
            "next_action": "REQUEST_ENGINEERING_AND_DATA_OWNER_REVIEW",
            "external_response": "NOT_AUTHORIZED",
        }

    redesign_approved = (
        case["engineering_approval"]
        and case["data_owner_approval"]
    )

    if redesign_approved:
        return {
            "route": "RETURN_TO_PLATFORM_PARTNER_LEAD",
            "launch": "DO_NOT_CONFIRM_ORIGINAL_DATE",
            "next_action": "PREPARE_REVISED_PLAN_FOR_PARTNER_CONFIRMATION",
            "external_response": "HUMAN_REQUIRED",
        }

    return {
        "route": "ESCALATE_TO_PLATFORM_PARTNER_LEAD",
        "launch": "HOLD_LAUNCH",
        "next_action": "REQUEST_MISSING_APPROVALS",
        "external_response": "NOT_AUTHORIZED",
    }


current_design = {
    "unapproved_data_fields": ["raw_email", "raw_ip_address"],
    "engineering_approval": False,
    "data_owner_approval": False,
}

approved_redesign = {
    "unapproved_data_fields": [],
    "engineering_approval": True,
    "data_owner_approval": True,
}


for stage, case in [
    ("Current design", current_design),
    ("Approved redesign", approved_redesign),
]:
    result = evaluate_case(case)
    print(stage)
    print("Route:", result["route"])
    print("Launch:", result["launch"])
    print("Next action:", result["next_action"])
    print("External response:", result["external_response"])
    print()