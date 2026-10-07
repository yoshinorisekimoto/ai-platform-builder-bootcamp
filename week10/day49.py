"""Day 49: Workflow closure and incident-risk control."""


REQUIRED_CLOSURE_ITEMS = (
    "engineering_decision_complete",
    "internal_handoff_complete",
    "partner_communication_complete",
    "temporary_limit_removed",
    "operations_rollback_verified",
    "partner_traffic_normal_confirmed",
    "audit_trail_complete",
)


def evaluate_closure(case):
    incomplete_items = [
        field for field in REQUIRED_CLOSURE_ITEMS
        if not case.get(field)
    ]

    result = {
        "action": None,
        "closure_status": "PENDING",
        "incomplete_items": incomplete_items,
        "decision_owner": "ENGINEERING",
        "operational_owner": "PRODUCT_OPERATIONS",
        "communication_owner": "PLATFORM_PARTNER_LEAD",
        "routing": None,
        "next_owner": None,
        "resume_condition": None,
        "audit_trail": "REQUIRED",
        "criticality": None,
        "reason": None,
        "impact": None,
        "approved_window_breached": False,
    }

    if incomplete_items:
        result["action"] = "STOP_INCOMPLETE_CLOSURE"
        result["closure_status"] = "BLOCKED"
        result["routing"] = "PLATFORM_PARTNER_LEAD"
        result["next_owner"] = "PLATFORM_PARTNER_LEAD"
        result["resume_condition"] = "ALL_CLOSURE_ITEMS_VERIFIED"
        return result

    result["action"] = "READY_FOR_CLOSURE_REVIEW"
    result["closure_status"] = "READY_FOR_REVIEW"
    result["routing"] = "ENGINEERING"
    result["next_owner"] = "ENGINEERING"
    result["resume_condition"] = "NO_UNRESOLVED_RISK"

    return result


def evaluate_timestamp_gap(
    result,
    approved_end_time,
    actual_rollback_time,
    rollback_was_automatic,
    rollback_delay_reason=None,
    operational_impact=False,
):
    if result["closure_status"] != "READY_FOR_REVIEW":
        return result

    if approved_end_time == actual_rollback_time:
        result["action"] = "CLOSE_CASE"
        result["closure_status"] = "CLOSED"
        result["criticality"] = "LOW"
        result["reason"] = "NO_TIMESTAMP_DISCREPANCY"
        result["impact"] = "NONE"
        result["resume_condition"] = "NOT_REQUIRED"
        return result

    result["approved_window_breached"] = True
    result["action"] = "INVESTIGATE_ROLLBACK_DELAY"
    result["closure_status"] = "OPEN"
    result["routing"] = "ENGINEERING"
    result["next_owner"] = "ENGINEERING"
    result["reason"] = rollback_delay_reason or "UNKNOWN"
    result["impact"] = (
        "OPERATIONAL_IMPACT_CONFIRMED"
        if operational_impact
        else "NO_CONFIRMED_PARTNER_IMPACT"
    )

    if rollback_was_automatic:
        result["criticality"] = "HIGH"
        result["resume_condition"] = (
            "ROOT_CAUSE_AND_OPERATIONAL_RISK_RESOLVED"
        )
    else:
        result["criticality"] = "MEDIUM"
        result["resume_condition"] = (
            "EXECUTION_DELAY_EXPLAINED_AND_RISK_RESOLVED"
        )

    return result


def apply_engineering_findings(
    result,
    root_cause,
    temporary_mitigation,
    permanent_fix_planned,
    unresolved_operational_risk,
):
    if result["action"] != "INVESTIGATE_ROLLBACK_DELAY":
        return result

    result["reason"] = root_cause
    result["temporary_mitigation"] = temporary_mitigation
    result["permanent_fix_planned"] = permanent_fix_planned

    if unresolved_operational_risk:
        result["action"] = "KEEP_CASE_OPEN"
        result["closure_status"] = "OPEN"
        result["resume_condition"] = (
            "UNRESOLVED_OPERATIONAL_RISK_ADDRESSED"
        )
        return result

    if result["criticality"] == "HIGH" and permanent_fix_planned:
        result["action"] = "MITIGATED_WITH_FOLLOW_UP"
        result["closure_status"] = "FOLLOW_UP_REQUIRED"
        result["resume_condition"] = (
            "PERMANENT_FIX_IMPLEMENTED_AND_VERIFIED"
        )
        return result

    result["action"] = "CLOSE_CASE"
    result["closure_status"] = "CLOSED"
    result["resume_condition"] = "NOT_REQUIRED"

    return result


cases = {
    "Automatic rollback delayed by queue saturation": {
        "engineering_decision_complete": True,
        "internal_handoff_complete": True,
        "partner_communication_complete": True,
        "temporary_limit_removed": True,
        "operations_rollback_verified": True,
        "partner_traffic_normal_confirmed": True,
        "audit_trail_complete": True,
    },
}


for name, case in cases.items():
    result = evaluate_closure(case)

    result = evaluate_timestamp_gap(
        result,
        approved_end_time="18:00",
        actual_rollback_time="18:12",
        rollback_was_automatic=True,
        rollback_delay_reason="QUEUE_SATURATION",
        operational_impact=False,
    )

    result = apply_engineering_findings(
        result,
        root_cause="QUEUE_SATURATION",
        temporary_mitigation="TEMPORARY_MONITORING_AND_ALERTING",
        permanent_fix_planned=True,
        unresolved_operational_risk=False,
    )

    print(name)
    print("Action:", result["action"])
    print("Closure status:", result["closure_status"])
    print("Reason:", result["reason"])
    print("Impact:", result["impact"])
    print("Criticality:", result["criticality"])
    print(
        "Approved window breached:",
        result["approved_window_breached"],
    )
    print("Routing:", result["routing"])
    print("Next owner:", result["next_owner"])
    print("Decision owner:", result["decision_owner"])
    print("Operational owner:", result["operational_owner"])
    print(
        "Communication owner:",
        result["communication_owner"],
    )
    print("Resume condition:", result["resume_condition"])
    print("Audit trail:", result["audit_trail"])
    print()