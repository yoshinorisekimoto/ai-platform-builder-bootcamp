"""Day 38: Escalation-routing test."""


def evaluate_case(case):
    evidence_conflict = (
        case["http_status"] == 429
        and case["observed_requests_per_second"]
        < case["documented_limit_per_second"]
    )

    issues = []

    if evidence_conflict:
        issues.append("INVESTIGATE_429_ROOT_CAUSE")

    if case["requested_limit_per_second"] > case["documented_limit_per_second"]:
        issues.append("CLARIFY_AND_ASSESS_CAPACITY_REQUEST")

    if case["launch_confirmation_requested"]:
        issues.append("HOLD_LAUNCH_COMMITMENT")

    return {
        "route": "ESCALATE_TO_PLATFORM_PARTNER_LEAD",
        "issues": issues,
        "external_response": "NOT_AUTHORIZED",
    }


case = {
    "http_status": 429,
    "observed_requests_per_second": 60,
    "documented_limit_per_second": 100,
    "requested_limit_per_second": 150,
    "launch_confirmation_requested": True,
}

result = evaluate_case(case)

print("Route:", result["route"])
for issue in result["issues"]:
    print("Issue:", issue)
print("External response:", result["external_response"])