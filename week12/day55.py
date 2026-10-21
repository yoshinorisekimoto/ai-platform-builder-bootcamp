from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Set


# ------------------------------------------------------------
# Human-defined governance
# ------------------------------------------------------------

STANDARDIZATION_REVIEW_CASES = 5

STANDARD_CLARIFICATION_CLASS = (
    "STANDARD_CLARIFICATION_COMMUNICATION"
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
    ESCALATE = "ESCALATE"


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
class ClarificationRequest:
    requested_rate: Optional[int]
    endpoints: List[str]
    start_time: Optional[str]
    end_time: Optional[str]

    expected_traffic: Optional[str]
    traffic_source: Optional[str]
    traffic_timestamp: Optional[str]
    traffic_information_type: Optional[InformationType]

    engineering_statement: Optional[str]
    engineering_source: Optional[str]
    engineering_timestamp: Optional[str]
    engineering_information_type: Optional[InformationType]


@dataclass
class DelegationHistory:
    reviewed_cases: int
    missing_field_errors: int
    unauthorized_commitments: int
    audit_record_errors: int


# ------------------------------------------------------------
# Q1
# Split a composite Agent-to-Agent request
# ------------------------------------------------------------

def process_composite_request(
    action_a: RequestBranch,
    action_b: RequestBranch,
) -> dict:
    """
    Independent branches do not block each other.

    Approved work may continue.

    An unapproved branch is held for clarification rather than
    automatically blocking the entire request.

    During HUMAN_REVIEW, the Platform Agent prepares the
    clarification and the Platform Partner Lead reviews it
    before it is sent to the Agency Agent.
    """

    if action_a.approved:
        action_a_status = WorkflowStatus.CONTINUE.value
        action_a_action = "EXECUTE_APPROVED_LAUNCH_WINDOW"
    else:
        action_a_status = WorkflowStatus.WAIT.value
        action_a_action = "HOLD_FOR_APPROVAL"

    if action_b.approved:
        action_b_status = WorkflowStatus.CONTINUE.value
        action_b_action = "EXECUTE_APPROVED_REQUEST"
    else:
        action_b_status = WorkflowStatus.WAIT.value
        action_b_action = "HOLD_AND_CLARIFY"

    return {
        "action_a": action_a_action,
        "action_a_status": action_a_status,
        "action_b": action_b_action,
        "action_b_status": action_b_status,
        "branches_independent":
            action_a.independent and action_b.independent,
        "clarification_target": "AGENCY_AGENT",
        "clarification_pre_send_review":
            "PLATFORM_PARTNER_LEAD",
        "delegation_stage":
            DelegationStage.HUMAN_REVIEW.value,
    }


# ------------------------------------------------------------
# Q2
# Structure clarification before Engineering review
# ------------------------------------------------------------

def validate_clarification_request(
    request: ClarificationRequest,
) -> dict:
    """
    Different pieces of information may have different
    provenance.

    Verified traffic data and Partner Engineering statements
    must remain distinguishable.

    An authenticated Agency Agent may provide Partner-side
    attestation without attaching a separate proof artifact
    for every statement.

    The Platform Agent records the provenance of each material
    input before preparing the Engineering decision package.
    """

    required_values = {
        "requested_rate": request.requested_rate,
        "endpoints": request.endpoints,
        "start_time": request.start_time,
        "end_time": request.end_time,
        "expected_traffic": request.expected_traffic,
        "traffic_source": request.traffic_source,
        "traffic_timestamp": request.traffic_timestamp,
        "traffic_information_type":
            request.traffic_information_type,
        "engineering_statement":
            request.engineering_statement,
        "engineering_source":
            request.engineering_source,
        "engineering_timestamp":
            request.engineering_timestamp,
        "engineering_information_type":
            request.engineering_information_type,
    }

    missing_fields = []

    for field, value in required_values.items():
        if value is None or value == [] or value == "":
            missing_fields.append(field)

    if missing_fields:
        return {
            "action": "REQUEST_MISSING_INFORMATION",
            "workflow_status": WorkflowStatus.WAIT.value,
            "missing_fields": missing_fields,
            "next_owner": "PLATFORM_AGENT",
            "send_to": "AGENCY_AGENT",
            "record_communication": True,
            "resume_condition":
                "REQUIRED_INFORMATION_COMPLETE",
        }

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
        "expected_traffic":
            request.expected_traffic,
        "traffic_source":
            request.traffic_source,
        "traffic_timestamp":
            request.traffic_timestamp,
        "traffic_information_type":
            request.traffic_information_type.value,
        "engineering_statement":
            request.engineering_statement,
        "engineering_source":
            request.engineering_source,
        "engineering_timestamp":
            request.engineering_timestamp,
        "engineering_information_type":
            request.engineering_information_type.value,
        "record_communication": True,
        "next_owner": "PLATFORM_ENGINEERING",
    }


# ------------------------------------------------------------
# Q3
# Standardize the communication class
# ------------------------------------------------------------

def evaluate_clarification_delegation(
    history: DelegationHistory,
) -> dict:
    """
    Standardization is evaluated at the communication-class
    level, not for one exact sentence or one exact Partner.

    Humans define the communication boundary first.

    After the communication class performs reliably during
    Human Review, routine communication inside that boundary
    may be delegated.
    """

    reliable = (
        history.reviewed_cases >= STANDARDIZATION_REVIEW_CASES
        and history.missing_field_errors == 0
        and history.unauthorized_commitments == 0
        and history.audit_record_errors == 0
    )

    if not reliable:
        return {
            "action": "KEEP_HUMAN_REVIEW",
            "delegation_stage":
                DelegationStage.HUMAN_REVIEW.value,
            "communication_class":
                STANDARD_CLARIFICATION_CLASS,
            "pre_send_human_review": True,
            "reason":
                "STANDARDIZATION_CRITERIA_NOT_YET_MET",
        }

    return {
        "action": "STANDARDIZE_AND_DELEGATE",
        "delegation_stage":
            DelegationStage.PARTIAL_DELEGATION.value,
        "communication_class":
            STANDARD_CLARIFICATION_CLASS,
        "pre_send_human_review": False,
        "reviewed_cases":
            history.reviewed_cases,
        "reason":
            "COMMUNICATION_CLASS_PROVEN_RELIABLE",
    }


def route_standard_clarification(
    topics: Set[str],
    delegation_stage: DelegationStage,
) -> dict:
    """
    Once the communication class is standardized, the Agent
    does not request Human approval for every normal
    clarification.

    Only requests outside the predefined boundary return to
    Human Review.
    """

    detected_human_gate_topics = (
        topics.intersection(HUMAN_GATE_TOPICS)
    )

    if detected_human_gate_topics:
        return {
            "action": "RETURN_TO_HUMAN_REVIEW",
            "workflow_status":
                WorkflowStatus.ESCALATE.value,
            "detected_topics":
                sorted(detected_human_gate_topics),
            "next_owner": "PLATFORM_PARTNER_LEAD",
            "agent_can_send_directly": False,
        }

    if (
        delegation_stage
        == DelegationStage.PARTIAL_DELEGATION
    ):
        return {
            "action": "SEND_STANDARD_CLARIFICATION",
            "workflow_status":
                WorkflowStatus.CONTINUE.value,
            "communication_class":
                STANDARD_CLARIFICATION_CLASS,
            "agent_can_send_directly": True,
            "send_to": "AGENCY_AGENT",
            "record_communication": True,
        }

    return {
        "action": "REQUIRE_PRE_SEND_HUMAN_REVIEW",
        "workflow_status": WorkflowStatus.WAIT.value,
        "next_owner": "PLATFORM_PARTNER_LEAD",
        "agent_can_send_directly": False,
    }


# ------------------------------------------------------------
# Demo
# ------------------------------------------------------------

def main():
    print("=== Q1: Composite Request ===")

    action_a = RequestBranch(
        branch_name="LAUNCH_WINDOW",
        approved=True,
        independent=True,
        requested_rate=500,
        start_time="10:00 JST",
        end_time="12:00 JST",
    )

    action_b = RequestBranch(
        branch_name="Q4_EXTENSION",
        approved=False,
        independent=True,
        requested_rate=500,
        start_time="AFTER_LAUNCH",
        end_time="END_OF_Q4",
    )

    q1 = process_composite_request(
        action_a,
        action_b,
    )

    for key, value in q1.items():
        print("{}: {}".format(key, value))

    print("\n=== Q2: Agent-to-Agent Clarification ===")

    clarification = ClarificationRequest(
        requested_rate=500,
        endpoints=["/applications"],
        start_time="2026-10-21",
        end_time="2026-12-31",

        expected_traffic="420-470 rpm",
        traffic_source="PARTNER_ANALYTICS_EXPORT",
        traffic_timestamp=
            "2026-10-21T13:30:00+09:00",
        traffic_information_type=
            InformationType.VERIFIED_DATA,

        engineering_statement=(
            "Partner Engineering confirmed "
            "500 rpm through Q4"
        ),
        engineering_source="AGENCY_AGENT",
        engineering_timestamp=
            "2026-10-21T13:35:00+09:00",
        engineering_information_type=
            InformationType.AGENT_ATTESTATION,
    )

    q2 = validate_clarification_request(
        clarification
    )

    for key, value in q2.items():
        print("{}: {}".format(key, value))

    print("\n=== Q3: Standardization Decision ===")

    history = DelegationHistory(
        reviewed_cases=5,
        missing_field_errors=0,
        unauthorized_commitments=0,
        audit_record_errors=0,
    )

    q3 = evaluate_clarification_delegation(
        history
    )

    for key, value in q3.items():
        print("{}: {}".format(key, value))

    print(
        "\n--- Standard Clarification After Delegation ---"
    )

    standard_case = route_standard_clarification(
        topics={
            "TRAFFIC_FORECAST",
            "ENDPOINT",
            "TIME_WINDOW",
            "SOURCE",
        },
        delegation_stage=
            DelegationStage.PARTIAL_DELEGATION,
    )

    for key, value in standard_case.items():
        print("{}: {}".format(key, value))

    print("\n--- Outside Standard Boundary ---")

    exception_case = route_standard_clarification(
        topics={
            "TRAFFIC_FORECAST",
            "NEW_COMMITMENT",
        },
        delegation_stage=
            DelegationStage.PARTIAL_DELEGATION,
    )

    for key, value in exception_case.items():
        print("{}: {}".format(key, value))


if __name__ == "__main__":
    main()