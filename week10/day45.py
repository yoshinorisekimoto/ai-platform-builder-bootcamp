"""Day 45: Missing Evidence and clarification control."""


REQUIRED_CLARIFICATIONS = (
    "retry_traffic_included",
    "peak_duration_minutes",
)

REQUIRED_CONTEXT = (
    "source",
    "partner_id",
    "endpoint",
    "timestamp",
)


def is_missing(value):
    return value is None or value == ""


def evaluate_clarification(case):
    missing_clarifications = [
        field for field in REQUIRED_CLARIFICATIONS
        if is_missing(case.get(field))
    ]

    missing_context = [
        field for field in REQUIRED_CONTEXT
        if is_missing(case.get(field))
    ]

    duration_values = case.get("duration_values", [])
    conflicting_durations = (
        len(set(duration_values)) > 1
    )

    result = {
        "action": None,
        "clarification_status": "BLOCKED",
        "missing_clarifications": missing_clarifications,
        "missing_context": missing_context,
        "conflicting_duration_values": duration_values
        if conflicting_durations else [],
        "routing": "PLATFORM_PARTNER_LEAD",
        "next_owner": "PARTNER",
        "communication_owner": "PLATFORM_PARTNER_LEAD",
        "resume_condition": None,
        "decision_owner": "ENGINEERING",
        "external_communication": "NOT_AUTHORIZED",
        "audit_trail": "REQUIRED",
    }

    if conflicting_durations:
        result["action"] = "STOP_AND_RESOLVE_CLARIFICATION_CONFLICT"
        result["resume_condition"] = (
            "PARTNER_IDENTIFIES_AUTHORITATIVE_DURATION_"
            "AND_RESOLVES_CONFLICT"
        )
        return result

    if missing_context:
        result["action"] = "STOP_UNVERIFIED_CLARIFICATION"
        result["resume_condition"] = (
            "SOURCE_AND_REQUEST_CONTEXT_VERIFIED"
        )
        return result

    if len(missing_clarifications) == len(REQUIRED_CLARIFICATIONS):
        result["action"] = "STOP_AND_REQUEST_CLARIFICATION"
        result["resume_condition"] = (
            "ALL_REQUIRED_CLARIFICATIONS_PROVIDED_AND_VERIFIED"
        )
        return result

    if missing_clarifications:
        result["action"] = "STOP_AND_REQUEST_REMAINING_CLARIFICATION"
        result["resume_condition"] = (
            "REMAINING_CLARIFICATIONS_PROVIDED_AND_VERIFIED"
        )
        return result

    result["action"] = "COMPLETE_CLARIFICATION"
    result["clarification_status"] = "READY_FOR_ENGINEERING"
    result["routing"] = "ENGINEERING"
    result["next_owner"] = "ENGINEERING"
    result["resume_condition"] = "NOT_REQUIRED"
    return result


cases = {
    "Missing retry and duration clarification": {
        "retry_traffic_included": None,
        "peak_duration_minutes": None,
        "duration_values": [],
        "source": "PARTNER",
        "partner_id": "partner-001",
        "endpoint": "/production/applications",
        "timestamp": "2026-10-01T09:00:00+09:00",
    },
    "Partial clarification with missing duration": {
        "retry_traffic_included": True,
        "peak_duration_minutes": None,
        "duration_values": [],
        "source": "PARTNER",
        "partner_id": "partner-001",
        "endpoint": "/production/applications",
        "timestamp": "2026-10-01T10:00:00+09:00",
    },
    "Conflicting Partner duration values": {
        "retry_traffic_included": True,
        "peak_duration_minutes": None,
        "duration_values": [8, 30],
        "source": "PARTNER",
        "partner_id": "partner-001",
        "endpoint": "/production/applications",
        "timestamp": "2026-10-01T10:30:00+09:00",
    },
    "Complete verified clarification": {
        "retry_traffic_included": True,
        "peak_duration_minutes": 30,
        "duration_values": [30],
        "source": "PARTNER",
        "partner_id": "partner-001",
        "endpoint": "/production/applications",
        "timestamp": "2026-10-01T11:00:00+09:00",
    },
}


for name, case in cases.items():
    result = evaluate_clarification(case)
    print(name)
    print("Action:", result["action"])
    print("Clarification status:", result["clarification_status"])
    print(
        "Missing clarifications:",
        result["missing_clarifications"],
    )
    print("Missing context:", result["missing_context"])
    print(
        "Conflicting duration values:",
        result["conflicting_duration_values"],
    )
    print("Routing:", result["routing"])
    print("Next owner:", result["next_owner"])
    print(
        "Communication owner:",
        result["communication_owner"],
    )
    print("Resume condition:", result["resume_condition"])
    print("Decision owner:", result["decision_owner"])
    print(
        "External communication:",
        result["external_communication"],
    )
    print("Audit trail:", result["audit_trail"])
    print()