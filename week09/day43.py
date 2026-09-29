"""Day 43: Minimum-information control."""


REQUIRED_FIELDS = (
    "partner_id",
    "production_endpoint",
    "current_traffic",
    "expected_peak_traffic",
    "peak_calculation_basis",
    "recent_429_count",
    "recent_429_time_window",
)

PROHIBITED_STANDARD_FIELDS = (
    "end_user_ip",
    "user_id",
    "full_request_payload",
    "raw_logs",
)

AUDIT_FIELDS = (
    "original_fields",
    "missing_fields",
    "excluded_fields",
    "retrieved_fields",
    "minimum_information_rule",
    "action",
    "notification",
    "escalation",
)


def evaluate_package(case):
    original_package = case["package"].copy()
    working_package = original_package.copy()

    result = {
        "action": None,
        "package_status": None,
        "missing_fields": [],
        "missing_exception_conditions": [],
        "excluded_fields": [],
        "retrieved_fields": [],
        "original_data": "PROTECTED",
        "routing": None,
        "notification": "NOT_REQUIRED",
        "escalation": "NOT_REQUIRED",
        "next_owner": None,
        "resume_condition": "NOT_REQUIRED",
        "external_communication": "NOT_AUTHORIZED",
        "audit_fields": AUDIT_FIELDS,
        "audit_trail": "REQUIRED",
    }

    prohibited_fields = [
        field
        for field in PROHIBITED_STANDARD_FIELDS
        if field in working_package
    ]

    if case["exception_requested"]:
        missing_conditions = []

        if not case["technical_purpose_documented"]:
            missing_conditions.append("technical_purpose")

        if not case["required_scope_documented"]:
            missing_conditions.append("required_scope")

        if not case["access_controls_documented"]:
            missing_conditions.append("access_controls")

        if not case["retention_period_documented"]:
            missing_conditions.append("retention_period")

        if not case["privacy_approval"]:
            missing_conditions.append("privacy_approval")

        if missing_conditions:
            result["missing_exception_conditions"] = (
                missing_conditions
            )
            result["action"] = "STOP_EXCEPTION_REQUEST"
            result["action"] = "STOP_EXCEPTION_REQUEST"
            result["package_status"] = "BLOCKED"
            result["excluded_fields"] = prohibited_fields
            result["routing"] = "PLATFORM_PARTNER_LEAD"
            result["escalation"] = (
                "ESCALATE_TO_PLATFORM_PARTNER_LEAD"
            )
            result["next_owner"] = "DATA_PRIVACY_OWNER"
            result["resume_condition"] = (
                "ALL_EXCEPTION_CONDITIONS_APPROVED"
            )
            return result

    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if not working_package.get(field)
    ]

    result["missing_fields"] = missing_fields

    if missing_fields:
        available_updates = case["approved_internal_updates"]

        retrievable_fields = [
            field
            for field in missing_fields
            if available_updates.get(field)
        ]

        if len(retrievable_fields) != len(missing_fields):
            result["action"] = "STOP_INCOMPLETE_PACKAGE"
            result["package_status"] = "BLOCKED"
            result["missing_fields"] = missing_fields
            result["routing"] = "PLATFORM_PARTNER_LEAD"
            result["escalation"] = (
                "ESCALATE_TO_PLATFORM_PARTNER_LEAD"
            )
            result["next_owner"] = "SOURCE_OWNER"
            result["resume_condition"] = (
                "ALL_REQUIRED_FIELDS_VALIDATED"
            )
            return result

        for field in retrievable_fields:
            working_package[field] = available_updates[field]

        result["retrieved_fields"] = retrievable_fields

    excluded_fields = [
        field
        for field in working_package
        if field not in REQUIRED_FIELDS
    ]

    minimized_package = {
        field: working_package[field]
        for field in REQUIRED_FIELDS
    }

    result["excluded_fields"] = excluded_fields
    result["routing"] = "ENGINEERING"
    result["notification"] = (
        "NOTIFY_PLATFORM_PARTNER_LEAD"
    )
    result["next_owner"] = "ENGINEERING"

    if result["retrieved_fields"]:
        result["action"] = (
            "RETRIEVE_VALIDATE_AND_ROUTE_PACKAGE"
        )
    elif excluded_fields:
        result["action"] = "MINIMIZE_AND_ROUTE_PACKAGE"
    else:
        result["action"] = "ROUTE_MINIMUM_PACKAGE"

    result["package_status"] = "READY_FOR_ENGINEERING"
    result["minimized_package"] = minimized_package
    return result


base_package = {
    "partner_id": "partner-001",
    "production_endpoint": "/applications",
    "current_traffic": 90,
    "expected_peak_traffic": 450,
    "peak_calculation_basis": "launch_forecast_v1",
    "recent_429_count": 18,
    "recent_429_time_window": "last_24_hours",
}


cases = {
    "Standard minimization": {
        "package": {
            **base_package,
            "end_user_ip": "192.0.2.1",
            "user_id": "user-001",
            "full_request_payload": "sensitive-payload",
            "raw_logs": "raw-log-data",
        },
        "exception_requested": False,
        "technical_purpose_documented": False,
        "required_scope_documented": False,
        "access_controls_documented": False,
        "retention_period_documented": False,
        "privacy_approval": False,
        "approved_internal_updates": {},
    },
    "Unapproved exception request": {
        "package": {
            **base_package,
            "raw_logs": "raw-log-data",
        },
        "exception_requested": True,
        "technical_purpose_documented": False,
        "required_scope_documented": False,
        "access_controls_documented": False,
        "retention_period_documented": False,
        "privacy_approval": False,
        "approved_internal_updates": {},
    },
    "Missing internal time window": {
        "package": {
            key: value
            for key, value in base_package.items()
            if key != "recent_429_time_window"
        },
        "exception_requested": False,
        "technical_purpose_documented": False,
        "required_scope_documented": False,
        "access_controls_documented": False,
        "retention_period_documented": False,
        "privacy_approval": False,
        "approved_internal_updates": {
            "recent_429_time_window": "last_24_hours",
        },
    },
    "Minimum package ready": {
        "package": base_package.copy(),
        "exception_requested": False,
        "technical_purpose_documented": False,
        "required_scope_documented": False,
        "access_controls_documented": False,
        "retention_period_documented": False,
        "privacy_approval": False,
        "approved_internal_updates": {},
    },
}


for name, case in cases.items():
    result = evaluate_package(case)
    print(name)
    print("Action:", result["action"])
    print("Package status:", result["package_status"])
    print("Missing fields:", result["missing_fields"])
    print(
        "Missing exception conditions:",
        result["missing_exception_conditions"],
    )
    print("Excluded fields:", result["excluded_fields"])
    print("Retrieved fields:", result["retrieved_fields"])
    print("Original data:", result["original_data"])
    print("Routing:", result["routing"])
    print("Notification:", result["notification"])
    print("Escalation:", result["escalation"])
    print("Next owner:", result["next_owner"])
    print("Resume condition:", result["resume_condition"])
    print(
        "External communication:",
        result["external_communication"],
    )
    print("Audit trail:", result["audit_trail"])
    print()