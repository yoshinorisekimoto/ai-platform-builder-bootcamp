"""Day 44: Minimum-permission control."""


PROHIBITED_PERMISSIONS = (
    "CHANGE_RATE_LIMIT",
    "CHANGE_PRODUCTION_SETTINGS",
    "READ_ALL_RAW_PRODUCTION_LOGS",
    "EDIT_EXISTING_AUDIT_RECORDS",
    "DELETE_EXISTING_AUDIT_RECORDS",
    "MODIFY_TECHNICAL_REVIEW",
    "SEND_EXTERNAL_COMMUNICATION",
)


def evaluate_permissions(case):
    required = case["required_permissions"]
    granted = case["granted_permissions"]

    missing = [
        permission for permission in required
        if permission not in granted
    ]
    excessive = [
        permission for permission in granted
        if permission in PROHIBITED_PERMISSIONS
    ]

    result = {
        "action": None,
        "permission_status": "BLOCKED",
        "missing_permissions": missing,
        "excessive_permissions": excessive,
        "routing": "PLATFORM_PARTNER_LEAD",
        "next_owner": "ACCESS_CONTROL_OWNER",
        "resume_condition": None,
        "external_communication": "NOT_AUTHORIZED",
        "audit_trail": "REQUIRED",
    }

    if not case["scope_valid"] or not case["duration_valid"]:
        result["action"] = "STOP_OVERBROAD_PERMISSION"
        result["resume_condition"] = (
            "EXCESSIVE_PERMISSION_REMOVED_SCOPE_AND_DURATION_CORRECTED_AND_VERIFIED"
        )
        return result

    if excessive:
        result["action"] = "STOP_EXCESSIVE_PERMISSION"
        result["resume_condition"] = (
            "EXCESSIVE_PERMISSIONS_REMOVED_AND_VERIFIED"
        )
        return result
    

    if missing:
        result["action"] = "STOP_MISSING_PERMISSION"
        result["resume_condition"] = (
            "REQUIRED_PERMISSIONS_ADDED_TESTED_AND_VERIFIED"
        )
        return result

    if not case["permission_verified"]:
        result["action"] = "STOP_UNVERIFIED_PERMISSION"
        result["resume_condition"] = (
            "ACCESS_CONTROL_OWNER_VERIFIES_PERMISSIONS"
        )
        return result

    result["action"] = "AUTHORIZE_MINIMUM_PERMISSION"
    result["permission_status"] = "READY"
    result["routing"] = case["approved_routing"]
    result["next_owner"] = case["next_owner"]
    result["resume_condition"] = "NOT_REQUIRED"
    return result


cases = {
    "Excessive rate-limit permission": {
        "required_permissions": (
            "READ_MINIMIZED_EVIDENCE_PACKAGE",
        ),
        "granted_permissions": (
            "READ_MINIMIZED_EVIDENCE_PACKAGE",
            "CHANGE_RATE_LIMIT",
        ),
        "scope_valid": True,
        "duration_valid": True,
        "permission_verified": False,
        "approved_routing": "ENGINEERING",
        "next_owner": "ENGINEERING",
    },
    "Overbroad log permission": {
        "required_permissions": (
            "READ_SANITIZED_ERROR_LOGS",
        ),
        "granted_permissions": (
            "READ_ALL_RAW_PRODUCTION_LOGS",
        ),
        "scope_valid": False,
        "duration_valid": False,
        "permission_verified": False,
        "approved_routing": "ENGINEERING",
        "next_owner": "ENGINEERING",
    },
    "Missing audit-write permission": {
        "required_permissions": (
            "READ_TECHNICAL_REVIEW",
            "APPEND_AUDIT_RECORD",
        ),
        "granted_permissions": (
            "READ_TECHNICAL_REVIEW",
        ),
        "scope_valid": True,
        "duration_valid": True,
        "permission_verified": False,
        "approved_routing": "PLATFORM_PARTNER_LEAD",
        "next_owner": "PLATFORM_PARTNER_LEAD",
    },
    "Minimum permissions verified": {
        "required_permissions": (
            "READ_TECHNICAL_REVIEW",
            "APPEND_AUDIT_RECORD",
        ),
        "granted_permissions": (
            "READ_TECHNICAL_REVIEW",
            "APPEND_AUDIT_RECORD",
        ),
        "scope_valid": True,
        "duration_valid": True,
        "permission_verified": True,
        "approved_routing": "PLATFORM_PARTNER_LEAD",
        "next_owner": "PLATFORM_PARTNER_LEAD",
    },
}


for name, case in cases.items():
    result = evaluate_permissions(case)
    print(name)
    print("Action:", result["action"])
    print("Permission status:", result["permission_status"])
    print("Missing permissions:", result["missing_permissions"])
    print("Excessive permissions:", result["excessive_permissions"])
    print("Routing:", result["routing"])
    print("Next owner:", result["next_owner"])
    print("Resume condition:", result["resume_condition"])
    print("External communication:", result["external_communication"])
    print("Audit trail:", result["audit_trail"])
    print()