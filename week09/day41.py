"""Day 41: Partner request intake."""


INTAKE_FIELDS = (
    "partner_id",
    "requested_limit",
    "business_reason",
    "target_date",
    "production_endpoint",
)

REVIEW_EVIDENCE = (
    "current_traffic",
    "expected_peak_traffic",
    "recent_429_logs",
    "engineering_capacity_approval",
)


def is_missing(value):
    return value is None or value == ""


def evaluate_intake(case):
    missing_intake = [
        field for field in INTAKE_FIELDS
        if is_missing(case.get(field))
    ]

    missing_evidence = [
        field for field in REVIEW_EVIDENCE
        if is_missing(case.get(field))
    ]

    result = {
        "action": None,
        "intake_status": None,
        "evidence_status": None,
        "missing_intake": missing_intake,
        "missing_evidence": missing_evidence,
        "routing": "PLATFORM_PARTNER_LEAD",
        "decision_owner": "ENGINEERING",
        "external_communication": "NOT_AUTHORIZED",
        "audit_trail": "REQUIRED",
    }

    if missing_intake:
        result["action"] = "STOP_INTAKE"
        result["intake_status"] = "INCOMPLETE"
        result["evidence_status"] = "NOT_EVALUATED"
        result["missing_evidence"] = []
        result["decision_owner"] = "NOT_ASSIGNED"
        return result

    result["action"] = "RECORD_AND_ROUTE_REQUEST"
    result["intake_status"] = "COMPLETE"

    if missing_evidence:
        result["evidence_status"] = "COLLECTION_REQUIRED"
    else:
        result["evidence_status"] = "READY_FOR_VALIDATION"

    return result


cases = {
    "Complete intake with missing review evidence": {
        "partner_id": "partner-001",
        "requested_limit": 500,
        "business_reason": "Planned production launch",
        "target_date": "2026-09-25",
        "production_endpoint": "/applications",
        "current_traffic": None,
        "expected_peak_traffic": None,
        "recent_429_logs": None,
        "engineering_capacity_approval": None,
    },
    "Incomplete intake": {
        "partner_id": "partner-002",
        "requested_limit": 500,
        "business_reason": "",
        "target_date": "2026-09-25",
        "production_endpoint": "/applications",
        "current_traffic": None,
        "expected_peak_traffic": None,
        "recent_429_logs": None,
        "engineering_capacity_approval": None,
    },
    "Complete intake with all review evidence": {
        "partner_id": "partner-003",
        "requested_limit": 500,
        "business_reason": "Expected traffic growth",
        "target_date": "2026-10-01",
        "production_endpoint": "/applications",
        "current_traffic": 90,
        "expected_peak_traffic": 450,
        "recent_429_logs": "log-reference-003",
        "engineering_capacity_approval": "APPROVED",
    },
}


for name, case in cases.items():
    result = evaluate_intake(case)
    print(name)
    print("Action:", result["action"])
    print("Intake status:", result["intake_status"])
    print("Evidence status:", result["evidence_status"])
    print("Missing intake:", result["missing_intake"])
    print("Missing evidence:", result["missing_evidence"])
    print("Routing:", result["routing"])
    print("Decision owner:", result["decision_owner"])
    print("External communication:", result["external_communication"])
    print("Audit trail:", result["audit_trail"])
    print()