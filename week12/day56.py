"""Day 56: synthetic Agent-to-Agent evidence reconciliation.

This is a decision-preparation prototype, not an API client or launch approval engine.
"""
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Evidence:
    name: str
    value: int
    source: str
    source_owner: str
    timestamp: str
    provenance: str
    validation_status: str


@dataclass
class ReadinessCase:
    case_id: str
    agency_completed: Evidence
    platform_success: Evidence
    platform_429: Evidence
    platform_total: Evidence
    rate_limit_rpm: Evidence
    retry_count: Optional[int] = None
    retry_policy_verified: bool = False
    timing_verified: bool = False
    expected_traffic_verified: bool = False
    agency_measurement_definition_verified: bool = False
    communication_authorized: bool = True
    exception_requested: bool = False


def reconcile(case: ReadinessCase) -> dict:
    """Compare governed records without rewriting partner attestation as verified data."""
    records = [case.agency_completed, case.platform_success, case.platform_429,
               case.platform_total, case.rate_limit_rpm]
    required = ("source", "source_owner", "timestamp", "provenance", "validation_status")
    invalid = [e.name for e in records if any(not getattr(e, field) for field in required)]
    invalid += [e.name for e in records if e.value < 0]
    invalid += [e.name for e in records if e.validation_status != "VALID"]
    if case.agency_completed.provenance != "AGENT_ATTESTATION":
        invalid.append("agency_completed.provenance")
    for item in (case.platform_success, case.platform_429, case.platform_total, case.rate_limit_rpm):
        if item.provenance != "VERIFIED_DATA":
            invalid.append(item.name + ".provenance")
    if case.rate_limit_rpm.value <= 0:
        invalid.append("rate_limit_rpm.value")

    audit = [{"name": e.name, "value": e.value, "source": e.source,
              "source_owner": e.source_owner, "timestamp": e.timestamp,
              "provenance": e.provenance, "validation_status": e.validation_status}
             for e in records]
    base = {"case_id": case.case_id, "evidence_records": audit,
            "launch_decision": "NOT_MADE", "decision_owner": "PLATFORM_ENGINEERING",
            "record_communication": True}

    if invalid or case.platform_total.value != case.platform_success.value + case.platform_429.value:
        return dict(base, action="STOP_EVIDENCE_VALIDATION", status="WAIT",
                    invalid_evidence=invalid,
                    count_mismatch=(case.platform_total.value !=
                                    case.platform_success.value + case.platform_429.value),
                    next_owner="PLATFORM_PARTNER_LEAD",
                    resume_condition="VALID_EVIDENCE_AND_COUNTS_CONFIRMED")

    if case.exception_requested:
        return dict(base, action="ROUTE_EXCEPTION_TO_HUMAN", status="WAIT",
                    next_owner="PLATFORM_PARTNER_LEAD",
                    resume_condition="PLATFORM_ENGINEERING_EXCEPTION_DECISION_RECORDED")

    # One operation may generate multiple HTTP attempts; don't infer causality
    # or that the 50 errors all represent exactly one retry each.
    questions: List[dict] = []
    if not case.agency_measurement_definition_verified:
        questions.append({"owner": "AGENCY_AGENT", "field": "success_definition_and_correlation"})
    if case.retry_count is None or not case.retry_policy_verified:
        questions.append({"owner": "AGENCY_AGENT", "field": "retry_count_and_backoff_policy"})
    if not case.timing_verified:
        questions.append({"owner": "PLATFORM_AGENT", "field": "429_timestamps_and_rate_windows"})
    if not case.expected_traffic_verified:
        questions.append({"owner": "AGENCY_AGENT", "field": "expected_launch_traffic"})

    if questions:
        if not case.communication_authorized:
            return dict(base, action="ESCALATE_CLARIFICATION_AUTHORIZATION", status="WAIT",
                        outstanding_questions=questions, next_owner="PLATFORM_PARTNER_LEAD",
                        resume_condition="COMMUNICATION_AUTHORIZED")
        return dict(base, action="REQUEST_EVIDENCE_RECONCILIATION", status="WAIT",
                    outstanding_questions=questions,
                    next_owner="PLATFORM_AGENT_AND_AGENCY_AGENT",
                    resume_condition="RECONCILIATION_INPUTS_VERIFIED")

    return dict(base, action="PREPARE_ENGINEERING_READINESS_BRIEF", status="WAIT",
                observations={"agency_completed": case.agency_completed.value,
                              "platform_success": case.platform_success.value,
                              "platform_429": case.platform_429.value,
                              "platform_http_attempts": case.platform_total.value,
                              "rate_limit_rpm": case.rate_limit_rpm.value,
                              "retry_count": case.retry_count},
                note="429 impact and acceptable launch risk require Engineering judgment",
                next_owner="PLATFORM_ENGINEERING",
                resume_condition="ENGINEERING_LAUNCH_DECISION_RECORDED")


def sample_case() -> ReadinessCase:
    def ev(name, value, source, owner, provenance):
        return Evidence(name, value, source, owner, "2026-10-26T10:00:00Z",
                        provenance, "VALID")
    return ReadinessCase(
        case_id="SYNTHETIC-D56-001",
        agency_completed=ev("agency_completed", 1000, "agency_agent_attestation",
                            "AGENCY_ENGINEERING", "AGENT_ATTESTATION"),
        platform_success=ev("platform_success", 1000, "platform_request_logs",
                            "PLATFORM_ENGINEERING", "VERIFIED_DATA"),
        platform_429=ev("platform_429", 50, "platform_request_logs",
                        "PLATFORM_ENGINEERING", "VERIFIED_DATA"),
        platform_total=ev("platform_total", 1050, "platform_request_logs",
                          "PLATFORM_ENGINEERING", "VERIFIED_DATA"),
        rate_limit_rpm=ev("rate_limit_rpm", 300, "api_specification",
                          "PLATFORM_ENGINEERING", "VERIFIED_DATA"),
    )


if __name__ == "__main__":
    import json
    from dataclasses import replace
    case = sample_case()
    scenarios = [
        ("investigate", case),
        ("brief", replace(case, retry_count=50, retry_policy_verified=True,
                          timing_verified=True, expected_traffic_verified=True,
                          agency_measurement_definition_verified=True)),
        ("exception", replace(case, exception_requested=True)),
        ("unauthorized", replace(case, communication_authorized=False)),
        ("bad_counts", replace(case, platform_total=replace(case.platform_total, value=1040))),
    ]
    expected_actions = {
        "investigate": "REQUEST_EVIDENCE_RECONCILIATION",
        "brief": "PREPARE_ENGINEERING_READINESS_BRIEF",
        "exception": "ROUTE_EXCEPTION_TO_HUMAN",
        "unauthorized": "ESCALATE_CLARIFICATION_AUTHORIZATION",
        "bad_counts": "STOP_EVIDENCE_VALIDATION",
    }
    for label, current in scenarios:
        result = reconcile(current)
        assert result["action"] == expected_actions[label]
        assert result["launch_decision"] == "NOT_MADE"
        print(json.dumps({"case": label, "action": result["action"],
                          "status": result["status"], "next_owner": result["next_owner"],
                          "launch_decision": result["launch_decision"]}, indent=2))
