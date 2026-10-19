from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ------------------------------------------------------------
# Human-defined governance rules
# AI may apply these rules but may not change them.
# ------------------------------------------------------------

MAX_PROVISIONAL_REWORK_PERCENT = 20

REVENUE_POINT_UNIT_USD = 10_000
EVIDENCE_COMPLETE_BONUS = 5
DECISION_READY_BONUS = 3
REWORK_PENALTY_PER_10_PERCENT = 1


class WorkflowState(Enum):
    WAIT = "WAIT"
    PROVISIONAL = "PROVISIONAL"
    CONTINUE = "CONTINUE"
    ESCALATE = "ESCALATE"


class DependencyClass(Enum):
    DEPENDENT = "DEPENDENT"
    CONDITIONALLY_DEPENDENT = "CONDITIONALLY_DEPENDENT"
    INDEPENDENT = "INDEPENDENT"


class DelegationStage(Enum):
    HUMAN_REVIEW = "HUMAN_REVIEW"
    PARTIAL_DELEGATION = "PARTIAL_DELEGATION"
    CONTROLLED_AUTONOMY = "CONTROLLED_AUTONOMY"


@dataclass
class Branch:
    name: str
    dependency: DependencyClass
    expected_rework_percent: int
    wait_action: str
    provisional_action: Optional[str]
    continue_action: str
    next_owner: str
    resume_condition: Optional[str] = None


@dataclass
class PartnerCase:
    name: str
    revenue_at_risk: int
    evidence_complete: bool
    decision_ready: bool
    rework_probability_percent: int


# ------------------------------------------------------------
# Q1
# Dependency + rework control
# ------------------------------------------------------------

def evaluate_branch(branch: Branch) -> dict:
    """
    Apply human-defined dependency and rework rules.

    AI does not redefine the dependency class or acceptable
    rework threshold.
    """

    if branch.dependency == DependencyClass.DEPENDENT:
        return {
            "branch": branch.name,
            "action": branch.wait_action,
            "status": WorkflowState.WAIT.value,
            "next_owner": branch.next_owner,
            "resume_condition": branch.resume_condition,
        }

    if branch.dependency == DependencyClass.INDEPENDENT:
        return {
            "branch": branch.name,
            "action": branch.continue_action,
            "status": WorkflowState.CONTINUE.value,
            "next_owner": branch.next_owner,
            "resume_condition": branch.resume_condition,
        }

    if (
        branch.dependency == DependencyClass.CONDITIONALLY_DEPENDENT
        and branch.expected_rework_percent
        <= MAX_PROVISIONAL_REWORK_PERCENT
    ):
        return {
            "branch": branch.name,
            "action": branch.provisional_action,
            "status": WorkflowState.PROVISIONAL.value,
            "next_owner": branch.next_owner,
            "resume_condition": branch.resume_condition,
        }

    return {
        "branch": branch.name,
        "action": branch.wait_action,
        "status": WorkflowState.WAIT.value,
        "next_owner": branch.next_owner,
        "resume_condition": branch.resume_condition,
    }


# ------------------------------------------------------------
# Q2
# Human-defined point model for competing priorities
# ------------------------------------------------------------

def calculate_priority_score(case: PartnerCase) -> dict:
    """
    Demonstration scoring model.

    The weights are defined by humans.
    AI may calculate the score but may not change the model.

    Revenue alone is intentionally not enough to determine priority.
    """

    revenue_points = case.revenue_at_risk // REVENUE_POINT_UNIT_USD

    evidence_points = (
        EVIDENCE_COMPLETE_BONUS
        if case.evidence_complete
        else 0
    )

    decision_ready_points = (
        DECISION_READY_BONUS
        if case.decision_ready
        else 0
    )

    rework_penalty = (
        case.rework_probability_percent // 10
    ) * REWORK_PENALTY_PER_10_PERCENT

    total_score = (
        revenue_points
        + evidence_points
        + decision_ready_points
        - rework_penalty
    )

    return {
        "partner": case.name,
        "revenue_points": revenue_points,
        "evidence_points": evidence_points,
        "decision_ready_points": decision_ready_points,
        "rework_penalty": rework_penalty,
        "total_score": total_score,
    }


def recommend_partner_priority(
    case_a: PartnerCase,
    case_b: PartnerCase,
) -> dict:
    """
    AI calculates the approved scores and recommends a priority.
    """

    score_a = calculate_priority_score(case_a)
    score_b = calculate_priority_score(case_b)

    if score_a["total_score"] > score_b["total_score"]:
        recommendation = case_a.name
    elif score_b["total_score"] > score_a["total_score"]:
        recommendation = case_b.name
    else:
        recommendation = "HUMAN_REVIEW_REQUIRED"

    return {
        "case_a_score": score_a,
        "case_b_score": score_b,
        "recommendation": recommendation,
    }


def apply_delegation_stage(
    stage: DelegationStage,
    recommendation: str,
) -> dict:
    """
    The Platform Partner Lead defines the current delegation stage.

    Agents may not promote themselves to a higher stage.
    """

    if stage == DelegationStage.HUMAN_REVIEW:
        return {
            "recommendation": recommendation,
            "human_review_required": True,
            "auto_execution_allowed": False,
            "next_owner": "PLATFORM_PARTNER_LEAD",
        }

    if stage == DelegationStage.PARTIAL_DELEGATION:
        return {
            "recommendation": recommendation,
            "human_review_required": True,
            "auto_execution_allowed": False,
            "next_owner": "PLATFORM_PARTNER_LEAD",
        }

    return {
        "recommendation": recommendation,
        "human_review_required": False,
        "auto_execution_allowed": True,
        "next_owner": "PLATFORM_AGENT",
    }


# ------------------------------------------------------------
# Q3
# Cross-functional conflict
# ------------------------------------------------------------

def handle_sales_commitment_conflict(
    partner_name: str,
    signed_commitment_verified: bool,
    formally_escalated_by_sales: bool,
) -> dict:
    """
    Sales owns its business commitments.

    Platform does not proactively compensate for missing Sales
    processes or silently override Platform priority.

    Once a verified cross-functional conflict is formally raised,
    the Platform Partner Lead validates and routes the conflict
    to the predefined Decision Owner.
    """

    if signed_commitment_verified and formally_escalated_by_sales:
        return {
            "partner": partner_name,
            "action": "ESCALATE_CROSS_FUNCTIONAL_CONFLICT",
            "workflow_status": WorkflowState.ESCALATE.value,
            "next_owner": "PLATFORM_PARTNER_LEAD",
            "decision_owner": "EXECUTIVE_DECISION_OWNER",
            "platform_priority_auto_changed": False,
            "ai_autonomy_reduced": False,
            "resume_condition":
                "EXECUTIVE_PRIORITY_DECISION_RECORDED",
            "reason":
                "VERIFIED_CROSS_FUNCTIONAL_PRIORITY_CONFLICT",
        }

    return {
        "partner": partner_name,
        "action": "KEEP_CURRENT_PLATFORM_PRIORITY",
        "workflow_status": WorkflowState.CONTINUE.value,
        "next_owner": "PLATFORM_AGENT",
        "decision_owner": None,
        "platform_priority_auto_changed": False,
        "ai_autonomy_reduced": False,
        "resume_condition": None,
        "reason": "NO_FORMAL_VERIFIED_CONFLICT",
    }


# ------------------------------------------------------------
# Demo
# ------------------------------------------------------------

def main():
    print("=== Q1: Branch Control ===")

    branches = [
        Branch(
            name="CAPACITY_REVIEW",
            dependency=DependencyClass.DEPENDENT,
            expected_rework_percent=100,
            wait_action="WAIT_FOR_CAPACITY_EVIDENCE",
            provisional_action=None,
            continue_action="CONTINUE_CAPACITY_REVIEW",
            next_owner="AGENCY_AGENT",
            resume_condition="AUTHORITATIVE_DURATION_VERIFIED",
        ),
        Branch(
            name="PERMISSION_SECURITY_CHECK",
            dependency=DependencyClass.CONDITIONALLY_DEPENDENT,
            expected_rework_percent=40,
            wait_action="WAIT_FOR_PERMISSION_REVIEW",
            provisional_action="PREPARE_PERMISSION_REVIEW",
            continue_action="CONTINUE_PERMISSION_REVIEW",
            next_owner="PLATFORM_AGENT",
            resume_condition="CAPACITY_CONDITION_CONFIRMED",
        ),
        Branch(
            name="PARTNER_COMMUNICATION",
            dependency=DependencyClass.CONDITIONALLY_DEPENDENT,
            expected_rework_percent=10,
            wait_action="WAIT_FOR_COMMUNICATION",
            provisional_action="PREPARE_REUSABLE_COMMUNICATION",
            continue_action="CONTINUE_COMMUNICATION",
            next_owner="PLATFORM_AGENT",
            resume_condition="ENGINEERING_DECISION_CONFIRMED",
        ),
        Branch(
            name="PARTNER_IDENTITY_CHECK",
            dependency=DependencyClass.INDEPENDENT,
            expected_rework_percent=0,
            wait_action="WAIT_FOR_IDENTITY_CHECK",
            provisional_action=None,
            continue_action="CONTINUE_INDEPENDENT_CHECK",
            next_owner="PLATFORM_AGENT",
        ),
    ]

    for branch in branches:
        result = evaluate_branch(branch)

        print(
            f"{result['branch']}: "
            f"{result['action']} "
            f"({result['status']})"
        )

    print("\n=== Q2: Competing Partner Priority ===")

    partner_a = PartnerCase(
        name="PARTNER_A",
        revenue_at_risk=80_000,
        evidence_complete=False,
        decision_ready=False,
        rework_probability_percent=70,
    )

    partner_b = PartnerCase(
        name="PARTNER_B",
        revenue_at_risk=50_000,
        evidence_complete=True,
        decision_ready=True,
        rework_probability_percent=0,
    )

    priority_result = recommend_partner_priority(
        partner_a,
        partner_b,
    )

    score_a = priority_result["case_a_score"]
    score_b = priority_result["case_b_score"]

    print(
        "PARTNER_A score:",
        score_a["total_score"],
        score_a,
    )

    print(
        "PARTNER_B score:",
        score_b["total_score"],
        score_b,
    )

    recommendation = priority_result["recommendation"]

    delegation = apply_delegation_stage(
        DelegationStage.HUMAN_REVIEW,
        recommendation,
    )

    print("AI recommendation:", recommendation)
    print(
        "Human review required:",
        delegation["human_review_required"],
    )
    print(
        "Auto execution allowed:",
        delegation["auto_execution_allowed"],
    )
    print("Next owner:", delegation["next_owner"])

    print("\n=== Q3: Sales Conflict ===")

    conflict = handle_sales_commitment_conflict(
        partner_name="PARTNER_A",
        signed_commitment_verified=True,
        formally_escalated_by_sales=True,
    )

    for key, value in conflict.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()