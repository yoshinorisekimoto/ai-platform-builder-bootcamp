"""Day 42: Evidence collection and validation."""


FRESHNESS_LIMIT_HOURS = 24

AUDIT_FIELDS = (
    "value",
    "source",
    "source_owner",
    "partner_id",
    "endpoint",
    "environment",
    "timestamp",
    "validation_failure",
)


def evaluate_evidence(case):
    result = {
        "action": None,
        "validation_status": None,
        "issue": "NONE",
        "routing": "PLATFORM_PARTNER_LEAD",
        "next_owner": None,
        "collection_route": None,
        "resume_condition": None,
        "decision_owner": "ENGINEERING",
        "external_communication": "NOT_AUTHORIZED",
        "communication_owner": "PLATFORM_PARTNER_LEAD",
        "audit_fields": AUDIT_FIELDS,
        "audit_trail": "REQUIRED",
    }

    if case["evidence_conflict"]:
        result["action"] = "STOP_AND_RESOLVE_CONFLICT"
        result["validation_status"] = "BLOCKED"
        result["issue"] = "CONFLICTING_EVIDENCE"
        result["next_owner"] = case["conflict_owner"]
        result["collection_route"] = "INTERNAL"
        result["resume_condition"] = (
            "DATA_OWNER_RESOLVES_OR_EXPLAINS_CONFLICT"
        )
        return result

    if not case["peak_basis_complete"]:
        result["action"] = "STOP_AND_REQUEST_EVIDENCE"
        result["validation_status"] = "BLOCKED"
        result["issue"] = "MISSING_PEAK_CALCULATION_BASIS"
        result["next_owner"] = "PARTNER"
        result["collection_route"] = (
            "PARTNER_VIA_PLATFORM_PARTNER_LEAD"
        )
        result["resume_condition"] = (
            "PARTNER_PROVIDES_PEAK_CALCULATION_BASIS"
        )
        return result

    if case["traffic_age_hours"] > FRESHNESS_LIMIT_HOURS:
        result["action"] = "STOP_AND_REFRESH_EVIDENCE"
        result["validation_status"] = "BLOCKED"
        result["issue"] = "STALE_TRAFFIC_EVIDENCE"
        result["next_owner"] = case["traffic_source_owner"]
        result["collection_route"] = case["traffic_collection_route"]
        result["resume_condition"] = (
            "TRAFFIC_EVIDENCE_IS_WITHIN_24_HOURS"
        )
        return result

    result["action"] = "COMPLETE_EVIDENCE_VALIDATION"
    result["validation_status"] = "READY_FOR_DECISION"
    result["next_owner"] = "ENGINEERING"
    result["collection_route"] = "INTERNAL"
    result["resume_condition"] = "NOT_REQUIRED"
    return result


cases = {
    "Missing peak calculation basis": {
        "evidence_conflict": False,
        "conflict_owner": None,
        "peak_basis_complete": False,
        "traffic_age_hours": 2,
        "traffic_source_owner": "MONITORING_TEAM",
        "traffic_collection_route": "INTERNAL",
    },
    "Conflicting official traffic evidence": {
        "evidence_conflict": True,
        "conflict_owner": "MONITORING_DATA_OWNER",
        "peak_basis_complete": True,
        "traffic_age_hours": 2,
        "traffic_source_owner": "MONITORING_TEAM",
        "traffic_collection_route": "INTERNAL",
    },
    "Stale Partner-provided traffic evidence": {
        "evidence_conflict": False,
        "conflict_owner": None,
        "peak_basis_complete": True,
        "traffic_age_hours": 72,
        "traffic_source_owner": "PARTNER",
        "traffic_collection_route": (
            "PARTNER_VIA_PLATFORM_PARTNER_LEAD"
        ),
    },
    "All evidence valid": {
        "evidence_conflict": False,
        "conflict_owner": None,
        "peak_basis_complete": True,
        "traffic_age_hours": 2,
        "traffic_source_owner": "MONITORING_TEAM",
        "traffic_collection_route": "INTERNAL",
    },
}


for name, case in cases.items():
    result = evaluate_evidence(case)
    print(name)
    print("Action:", result["action"])
    print("Validation status:", result["validation_status"])
    print("Issue:", result["issue"])
    print("Routing:", result["routing"])
    print("Next owner:", result["next_owner"])
    print("Collection route:", result["collection_route"])
    print("Resume condition:", result["resume_condition"])
    print("Decision owner:", result["decision_owner"])
    print(
        "External communication:",
        result["external_communication"],
    )
    print("Communication owner:", result["communication_owner"])
    print("Audit fields:", result["audit_fields"])
    print("Audit trail:", result["audit_trail"])
    print()