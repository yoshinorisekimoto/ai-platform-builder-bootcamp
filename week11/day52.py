"""Day 52: Clarification retry, state normalization, and escalation control."""


MAX_CLARIFICATION_ROUNDS = 2


def evaluate_clarification(case):
    result = {
        "action": None,
        "status": None,
        "next_owner": None,
        "human_review_required": False,
        "resume_condition": None,
        "audit_trail": "REQUIRED",
    }

    rounds = case.get("clarification_rounds", 0)
    authoritative_value = case.get("authoritative_value")
    conflict_resolved = case.get("conflict_resolved", False)

    if authoritative_value and conflict_resolved:
        result["action"] = "VERIFY_AND_RESUME"
        result["status"] = "READY_TO_RESUME"
        result["next_owner"] = "PLATFORM_AGENT"
        result["resume_condition"] = "AUTHORITATIVE_VALUE_VERIFIED"
        return result

    if rounds >= MAX_CLARIFICATION_ROUNDS:
        result["action"] = "ESCALATE_UNRESOLVED_CONFLICT"
        result["status"] = "ESCALATED"
        result["next_owner"] = "PLATFORM_PARTNER_LEAD"
        result["human_review_required"] = True
        result["resume_condition"] = (
            "AUTHORITATIVE_VALUE_CONFIRMED_BY_HUMAN"
        )
        return result

    result["action"] = "REQUEST_AGENT_CLARIFICATION"
    result["status"] = "WAITING_FOR_CLARIFICATION"
    result["next_owner"] = "AGENCY_AGENT"
    result["resume_condition"] = "AUTHORITATIVE_VALUE_RETURNED"

    return result


def evaluate_partner_state(case):
    result = {
        "action": None,
        "status": None,
        "next_owner": None,
        "resume_condition": None,
    }

    old_value_current = case.get("old_value_current")
    new_value_current = case.get("new_value_current")
    new_value_authoritative = case.get("new_value_authoritative")

    if old_value_current:
        result["action"] = "CORRECT_PARTNER_STATE"
        result["status"] = "BLOCKED"
        result["next_owner"] = "AGENCY_AGENT"
        result["resume_condition"] = (
            "OLD_VALUE_NOT_CURRENT_AND_NEW_VALUE_VERIFIED"
        )
        return result

    if new_value_current and new_value_authoritative:
        result["action"] = "VERIFY_PARTNER_STATE"
        result["status"] = "READY_TO_RESUME"
        result["next_owner"] = "PLATFORM_AGENT"
        result["resume_condition"] = "PARTNER_STATE_CONSISTENT"
        return result

    result["action"] = "STOP_INCONSISTENT_PARTNER_STATE"
    result["status"] = "BLOCKED"
    result["next_owner"] = "AGENCY_AGENT"
    result["resume_condition"] = "PARTNER_STATE_CORRECTED"

    return result


def evaluate_authoritative_records(case):
    records = case.get("authoritative_records", [])

    unique_values = set(records)

    result = {
        "action": None,
        "status": None,
        "blocked_branch": None,
        "next_owner": None,
        "resume_condition": None,
    }

    if len(unique_values) > 1:
        result["action"] = "BLOCK_CAPACITY_REVIEW_BRANCH"
        result["status"] = "WAITING_FOR_CLARIFICATION"
        result["blocked_branch"] = "CAPACITY_REVIEW"
        result["next_owner"] = "AGENCY_AGENT"
        result["resume_condition"] = (
            "SINGLE_AUTHORITATIVE_VALUE_VERIFIED"
        )
        return result

    result["action"] = "CONTINUE_INTERNAL_ROUTING"
    result["status"] = "READY"
    result["blocked_branch"] = "NONE"
    result["next_owner"] = "PLATFORM_AGENT"
    result["resume_condition"] = "NOT_REQUIRED"

    return result


cases = {
    "Unresolved after retry limit": {
        "clarification_rounds": 2,
        "authoritative_value": None,
        "conflict_resolved": False,
    },
    "Partner state corrected": {
        "old_value_current": False,
        "new_value_current": True,
        "new_value_authoritative": True,
    },
    "Two authoritative values": {
        "authoritative_records": [20, 30],
    },
}


clarification_result = evaluate_clarification(
    cases["Unresolved after retry limit"]
)

partner_state_result = evaluate_partner_state(
    cases["Partner state corrected"]
)

authoritative_result = evaluate_authoritative_records(
    cases["Two authoritative values"]
)


print("Clarification Retry")
print("Action:", clarification_result["action"])
print("Status:", clarification_result["status"])
print("Next owner:", clarification_result["next_owner"])
print(
    "Human review required:",
    clarification_result["human_review_required"],
)
print(
    "Resume condition:",
    clarification_result["resume_condition"],
)
print()

print("Partner State")
print("Action:", partner_state_result["action"])
print("Status:", partner_state_result["status"])
print("Next owner:", partner_state_result["next_owner"])
print(
    "Resume condition:",
    partner_state_result["resume_condition"],
)
print()

print("Authoritative Records")
print("Action:", authoritative_result["action"])
print("Status:", authoritative_result["status"])
print(
    "Blocked branch:",
    authoritative_result["blocked_branch"],
)
print("Next owner:", authoritative_result["next_owner"])
print(
    "Resume condition:",
    authoritative_result["resume_condition"],
)
print()