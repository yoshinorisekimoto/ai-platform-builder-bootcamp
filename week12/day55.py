from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Set


# ------------------------------------------------------------
# Human-defined governance
# ------------------------------------------------------------

MIN_REVIEWED_CASES = 5

ENGINEERING_INPUT_CLARIFICATION_CLASS = (
    "ENGINEERING_INPUT_CLARIFICATION"
)

HUMAN_GATE_TOPICS = {
    "NEW_COMMITMENT",
    "EXCEPTION_APPROVAL",
    "RISK_ACCEPTANCE",
    "CONTRACT_CHANGE",
}


class WorkflowStatus(Enum):
    CONTINUE = "CONTINUE"
    WAIT = "WAIT"


class DelegationStage(Enum):
    HUMAN_REVIEW = "HUMAN_REVIEW"
    PARTIAL_DELEGATION = "PARTIAL_DELEGATION"


class InformationType(Enum):
    VERIFIED_DATA = "VERIFIED_DATA"
    AGENT_ATTESTATION = "AGENT_ATTESTATION"
    AI_INFERENCE = "AI_INFERENCE"


@dataclass
class RequestBranch:
    branch_name: str
    approved: bool
    independent: bool
    requested_rate: int
    start_time: str
    end_time: str


@dataclass
class MaterialInput:
    input_name: str
    value: str
    source: str
    source_owner: str
    timestamp: str
    provenance: InformationType
    validation_status: str


@dataclass
class ClarificationRequest:
    requested_rate: Optional[int]
    endpoints: List[str]
    start_time: Optional[str]
    end_time: Optional[str]
    material_inputs: List[MaterialInput]


@dataclass
class DelegationHistory:
    reviewed_cases: int
    missing_field_errors: int
    unauthorized_commitments: int
    audit_record_errors: int


# ------------------------------------------------------------
# Q1
# Composite request
# ------------------------------------------------------------

def process_composite_request(
    branch_a: RequestBranch,
    branch_b: RequestBranch,
) -> dict:
    """
    Independent approved work may continue while an unresolved
    branch waits for clarification.

    ENGINEERING_INPUT_CLARIFICATION is a new communication
    class and starts in HUMAN_REVIEW.
    """

    if branch_a.approved:
        branch_a_status = WorkflowStatus.CONTINUE.value
    else:
        branch_a_status = WorkflowStatus.WAIT.value

    if branch_b.approved:
        branch_b_status = WorkflowStatus.CONTINUE.value
    else:
        branch_b_status = WorkflowStatus.WAIT.value

    return {
        "action": "CONTINUE_APPROVED_BRANCH",
        "branch_a_status": branch_a_status,
        "branch_b_status": branch_b_status,
        "branches_independent":
            branch_a.independent and branch_b.independent,
        "communication_class":
            ENGINEERING_INPUT_CLARIFICATION_CLASS,
        "clarification_target": "AGENCY_AGENT",
        "pre_send_review": "PLATFORM_PARTNER_LEAD",
        "resume_condition":
            "PLATFORM_ENGINEERING_DECISION_RECORDED",
    }


# ------------------------------------------------------------
# Q2
# Agent-to-Agent clarification and provenance
# ------------------------------------------------------------

def validate_clarification_request(
    request: ClarificationRequest,
) -> dict:
    """
    Each material input keeps its own source, Source Owner,
    timestamp, provenance, and validation status.

    AGENT_ATTESTATION is recorded as Evidence but is not
    converted into VERIFIED_DATA.
    """

    missing_fields = []

    if request.requested_rate is None:
        missing_fields.append("requested_rate")

    if not request.endpoints:
        missing_fields.append("endpoints")

    if not request.start_time:
        missing_fields.append("start_time")

    if not request.end_time:
        missing_fields.append("end_time")

    if not request.material_inputs:
        missing_fields.append("material_inputs")

    for index, item in enumerate(request.material_inputs):
        prefix = "material_inputs[{}]".format(index)

        if not item.input_name:
            missing_fields.append(
                "{}.input_name".format(prefix)
            )

        if not item.value:
            missing_fields.append(
                "{}.value".format(prefix)
            )

        if not item.source:
            missing_fields.append(
                "{}.source".format(prefix)
            )

        if not item.source_owner:
            missing_fields.append(
                "{}.source_owner".format(prefix)
            )

        if not item.timestamp:
            missing_fields.append(
                "{}.timestamp".format(prefix)
            )

        if not item.validation_status:
            missing_fields.append(
                "{}.validation_status".format(prefix)
            )

    if missing_fields:
        return {
            "action": "REQUEST_MISSING_INFORMATION",
            "workflow_status": WorkflowStatus.WAIT.value,
            "missing_fields": missing_fields,
            "communication_class":
                ENGINEERING_INPUT_CLARIFICATION_CLASS,
            "send_to": "AGENCY_AGENT",
            "record_communication": True,
            "resume_condition":
                "REQUIRED_INFORMATION_COMPLETE",
        }

    evidence_records = []

    for item in request.material_inputs:
        evidence_records.append({
            "input": item.input_name,
            "value": item.value,
            "source": item.source,
            "source_owner": item.source_owner,
            "timestamp": item.timestamp,
            "provenance": item.provenance.value,
            "validation_status":
                item.validation_status,
        })

    return {
        "action": "PREPARE_ENGINEERING_DECISION_INPUT",
        "workflow_status": WorkflowStatus.CONTINUE.value,
        "requested_rate": request.requested_rate,
        "endpoints": request.endpoints,
        "time_window":
            "{} - {}".format(
                request.start_time,
                request.end_time,
            ),
        "evidence_records": evidence_records,
        "record_communication": True,
        "next_owner": "PLATFORM_ENGINEERING",
        "decision_owner": "PLATFORM_ENGINEERING",
    }


# ------------------------------------------------------------
# Q3
# Request class-level delegation approval
# ------------------------------------------------------------

def evaluate_delegation_readiness(
    history: DelegationHistory,
) -> dict:
    """
    The Platform Agent may determine that Human-defined
    delegation criteria are met.

    It may request delegation approval but cannot approve its
    own move to PARTIAL_DELEGATION.
    """

    criteria_met = (
        history.reviewed_cases >= MIN_REVIEWED_CASES
        and history.missing_field_errors == 0
        and history.unauthorized_commitments == 0
        and history.audit_record_errors == 0
    )

    if not criteria_met:
        return {
            "action": "KEEP_HUMAN_REVIEW",
            "communication_class":
                ENGINEERING_INPUT_CLARIFICATION_CLASS,
            "current_stage":
                DelegationStage.HUMAN_REVIEW.value,
            "reason":
                "DELEGATION_CRITERIA_NOT_MET",
        }

    return {
        "action": "REQUEST_DELEGATION_APPROVAL",
        "communication_class":
            ENGINEERING_INPUT_CLARIFICATION_CLASS,
        "reviewed_cases": history.reviewed_cases,
        "requested_stage":
            DelegationStage.PARTIAL_DELEGATION.value,
        "next_owner": "PLATFORM_PARTNER_LEAD",
        "decision_owner": "PLATFORM_PARTNER_LEAD",
    }


# ------------------------------------------------------------
# Q4 / Q5
# Route communication after Human-approved delegation
# ------------------------------------------------------------

def route_engineering_input_clarification(
    topics: Set[str],
    delegation_stage: DelegationStage,
    validation_passed: bool = True,
) -> dict:
    """
    After Human-approved delegation, communication inside the
    Delegation Boundary may proceed without per-message review.

    Human Gate topics return only the affected request to Human
    Review.

    A validation failure returns the communication class to
    HUMAN_REVIEW.
    """

    if not validation_passed:
        return {
            "action": "RETURN_CLASS_TO_HUMAN_REVIEW",
            "workflow_status": WorkflowStatus.WAIT.value,
            "communication_class":
                ENGINEERING_INPUT_CLARIFICATION_CLASS,
            "delegation_stage":
                DelegationStage.HUMAN_REVIEW.value,
            "pre_send_review":
                "PLATFORM_PARTNER_LEAD",
            "next_owner":
                "PLATFORM_PARTNER_LEAD",
            "resume_condition":
                "DELEGATION_REAPPROVED",
        }

    detected_human_gate_topics = (
        topics.intersection(HUMAN_GATE_TOPICS)
    )

    if detected_human_gate_topics:
        resume_condition = "HUMAN_GATE_DECISION_RECORDED"

        if "NEW_COMMITMENT" in detected_human_gate_topics:
            resume_condition = (
                "HUMAN_COMMITMENT_DECISION_RECORDED"
            )

        return {
            "action": "RETURN_TO_HUMAN_REVIEW",
            "workflow_status": WorkflowStatus.WAIT.value,
            "communication_class":
                ENGINEERING_INPUT_CLARIFICATION_CLASS,
            "detected_human_gate_topics":
                sorted(detected_human_gate_topics),
            "class_delegation_stage":
                delegation_stage.value,
            "pre_send_review":
                "PLATFORM_PARTNER_LEAD",
            "next_owner":
                "PLATFORM_PARTNER_LEAD",
            "resume_condition":
                resume_condition,
        }

    if (
        delegation_stage
        == DelegationStage.PARTIAL_DELEGATION
    ):
        return {
            "action":
                "SEND_ENGINEERING_INPUT_CLARIFICATION",
            "workflow_status":
                WorkflowStatus.CONTINUE.value,
            "communication_class":
                ENGINEERING_INPUT_CLARIFICATION_CLASS,
            "pre_send_review": "NONE",
            "send_to": "AGENCY_AGENT",
            "record_communication": True,
        }

    return {
        "action": "REQUIRE_PRE_SEND_HUMAN_REVIEW",
        "workflow_status": WorkflowStatus.WAIT.value,
        "communication_class":
            ENGINEERING_INPUT_CLARIFICATION_CLASS,
        "pre_send_review":
            "PLATFORM_PARTNER_LEAD",
        "next_owner":
            "PLATFORM_PARTNER_LEAD",
    }


# ------------------------------------------------------------
# Demo
# ------------------------------------------------------------

def main():
    print("=== Case 1: Composite Request ===")

    branch_a = RequestBranch(
        branch_name="LAUNCH_WINDOW",
        approved=True,
        independent=True,
        requested_rate=500,
        start_time="10:00 JST",
        end_time="12:00 JST",
    )

    branch_b = RequestBranch(
        branch_name="Q4_EXTENSION",
        approved=False,
        independent=True,
        requested_rate=500,
        start_time="2026-10-21",
        end_time="2026-12-31",
    )

    case_1 = process_composite_request(
        branch_a,
        branch_b,
    )

    for key, value in case_1.items():
        print("{}: {}".format(key, value))

    print(
        "\n=== Case 2: Agent-to-Agent Clarification ==="
    )

    material_inputs = [
        MaterialInput(
            input_name="OBSERVED_PEAK_TRAFFIC",
            value="420-470 rpm",
            source="PLATFORM_TRAFFIC_LOGS",
            source_owner="PLATFORM_OBSERVABILITY_OWNER",
            timestamp="2026-10-21T13:30:00+09:00",
            provenance=InformationType.VERIFIED_DATA,
            validation_status="VALIDATED",
        ),
        MaterialInput(
            input_name="REQUIRED_RATE_THROUGH_Q4",
            value="500 rpm",
            source="AGENCY_AGENT",
            source_owner="PARTNER_ENGINEERING",
            timestamp="2026-10-21T13:35:00+09:00",
            provenance=InformationType.AGENT_ATTESTATION,
            validation_status="RECORDED",
        ),
    ]

    clarification = ClarificationRequest(
        requested_rate=500,
        endpoints=["/applications"],
        start_time="2026-10-21",
        end_time="2026-12-31",
        material_inputs=material_inputs,
    )

    case_2 = validate_clarification_request(
        clarification
    )

    for key, value in case_2.items():
        print("{}: {}".format(key, value))

    print(
        "\n=== Case 3: Request Delegation Approval ==="
    )

    history = DelegationHistory(
        reviewed_cases=5,
        missing_field_errors=0,
        unauthorized_commitments=0,
        audit_record_errors=0,
    )

    case_3 = evaluate_delegation_readiness(
        history
    )

    for key, value in case_3.items():
        print("{}: {}".format(key, value))

    print(
        "\n=== Case 4: Clarification After Delegation ==="
    )

    case_4 = route_engineering_input_clarification(
        topics={
            "TRAFFIC_FORECAST",
            "ENDPOINT",
            "TIME_WINDOW",
            "SOURCE",
        },
        delegation_stage=
            DelegationStage.PARTIAL_DELEGATION,
    )

    for key, value in case_4.items():
        print("{}: {}".format(key, value))

    print(
        "\n=== Case 5: Human Gate Topic Detected ==="
    )

    case_5 = route_engineering_input_clarification(
        topics={
            "TRAFFIC_FORECAST",
            "NEW_COMMITMENT",
        },
        delegation_stage=
            DelegationStage.PARTIAL_DELEGATION,
    )

    for key, value in case_5.items():
        print("{}: {}".format(key, value))


if __name__ == "__main__":
    main()