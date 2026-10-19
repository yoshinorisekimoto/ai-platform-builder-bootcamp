from dataclasses import dataclass
from enum import Enum


# ------------------------------------------------------------
# Governance rules
# These values are defined by humans, not by the AI.
# ------------------------------------------------------------

MAX_PROVISIONAL_REWORK_PERCENT = 20


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
    reusable_percent: int


@dataclass
class PartnerCase:
    name: str
    revenue_at_risk: int
    evidence_complete: bool
    rework_probability_percent: int


# ------------------------------------------------------------
# Q1
# Dependency + rework control
# ------------------------------------------------------------

def decide_branch_state(branch: Branch) -> WorkflowState:
    """
    AI applies a process already defined by humans.
    AI does not redefine the dependency rules.
    """

    if branch.dependency == DependencyClass.DEPENDENT:
        return WorkflowState.WAIT

    if branch.dependency == DependencyClass.INDEPENDENT:
        return WorkflowState.CONTINUE

    if (
        branch.dependency == DependencyClass.CONDITIONALLY_DEPENDENT
        and branch.expected_rework_percent <= MAX_PROVISIONAL_REWORK_PERCENT
    ):
        return WorkflowState.PROVISIONAL

    return WorkflowState.WAIT


# ------------------------------------------------------------
# Q2
# Competing priorities
# ------------------------------------------------------------

def recommend_partner_priority(
    case_a: PartnerCase,
    case_b: PartnerCase,
) -> str:
    """
    Simplified recommendation logic for this learning case.

    In a real system, the scoring model and weights must be
    predefined and approved by humans.
    """

    if (
        case_b.revenue_at_risk > case_a.revenue_at_risk
        and case_b.evidence_complete
        and not case_a.evidence_complete
    ):
        return case_b.name

    return case_a.name


def delegation_control(
    stage: DelegationStage,
    recommendation: str,
) -> dict:
    """
    Delegation increases only after reliability has been demonstrated.
    """

    if stage == DelegationStage.HUMAN_REVIEW:
        return {
            "recommendation": recommendation,
            "human_review_required": True,
            "auto_execution_allowed": False,
        }

    if stage == DelegationStage.PARTIAL_DELEGATION:
        return {
            "recommendation": recommendation,
            "human_review_required": True,
            "auto_execution_allowed": False,
        }

    return {
        "recommendation": recommendation,
        "human_review_required": False,
        "auto_execution_allowed": True,
    }


# ------------------------------------------------------------
# Q3
# Cross-functional conflict
# ------------------------------------------------------------

def handle_sales_escalation(
    signed_commitment_verified: bool,
    formally_escalated_by_sales: bool,
) -> dict:
    """
    Platform does not proactively compensate for missing Sales process.

    If Sales formally raises verified evidence that conflicts with
    the current Platform priority, the conflict is escalated to the
    predefined decision owner.

    The Platform Lead does not silently override the existing process.
    """

    if signed_commitment_verified and formally_escalated_by_sales:
        return {
            "action": "ESCALATE_CROSS_FUNCTIONAL_CONFLICT",
            "workflow_status": WorkflowState.ESCALATE.value,
            "next_owner": "EXECUTIVE_DECISION_OWNER",
            "platform_priority_auto_changed": False,
            "ai_autonomy_reduced": False,
            "reason": "VERIFIED_CROSS_FUNCTIONAL_PRIORITY_CONFLICT",
        }

    return {
        "action": "KEEP_CURRENT_PLATFORM_PRIORITY",
        "workflow_status": WorkflowState.CONTINUE.value,
        "next_owner": "PLATFORM_AGENT",
        "platform_priority_auto_changed": False,
        "ai_autonomy_reduced": False,
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
            reusable_percent=0,
        ),
        Branch(
            name="PERMISSION_SECURITY_CHECK",
            dependency=DependencyClass.CONDITIONALLY_DEPENDENT,
            expected_rework_percent=40,
            reusable_percent=60,
        ),
        Branch(
            name="PARTNER_COMMUNICATION",
            dependency=DependencyClass.CONDITIONALLY_DEPENDENT,
            expected_rework_percent=20,
            reusable_percent=80,
        ),
    ]

    for branch in branches:
        state = decide_branch_state(branch)
        print(f"{branch.name}: {state.value}")

    print("\n=== Q2: Partner Priority ===")

    partner_a = PartnerCase(
        name="PARTNER_A",
        revenue_at_risk=50_000,
        evidence_complete=False,
        rework_probability_percent=70,
    )

    partner_b = PartnerCase(
        name="PARTNER_B",
        revenue_at_risk=80_000,
        evidence_complete=True,
        rework_probability_percent=0,
    )

    recommendation = recommend_partner_priority(
        partner_a,
        partner_b,
    )

    delegation = delegation_control(
        DelegationStage.HUMAN_REVIEW,
        recommendation,
    )

    print("AI recommendation:", recommendation)
    print("Human review required:", delegation["human_review_required"])
    print(
        "Auto execution allowed:",
        delegation["auto_execution_allowed"],
    )

    print("\n=== Q3: Sales Conflict ===")

    conflict = handle_sales_escalation(
        signed_commitment_verified=True,
        formally_escalated_by_sales=True,
    )

    for key, value in conflict.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()