from dataclasses import dataclass
from enum import Enum


# ------------------------------------------------------------
# Human-defined governance
# AI applies these rules but cannot change them.
# ------------------------------------------------------------

REGULATORY_DEADLINE_MONTHS = 12
INTERNAL_SAFETY_BUFFER_MONTHS = 1
PLATFORM_MIGRATION_DEADLINE_MONTHS = (
    REGULATORY_DEADLINE_MONTHS - INTERNAL_SAFETY_BUFFER_MONTHS
)


class WorkflowStatus(Enum):
    CONTINUE = "CONTINUE"
    WAIT = "WAIT"
    ESCALATE = "ESCALATE"


class ModelDecision(Enum):
    HOLD_MODEL_CHANGE = "HOLD_MODEL_CHANGE"
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"


class MigrationMode(Enum):
    EARLY_INDIVIDUAL_PLANNING = "EARLY_INDIVIDUAL_PLANNING"
    QUARTERLY_MIGRATION_WAVE = "QUARTERLY_MIGRATION_WAVE"


@dataclass
class ModelReview:
    total_cases: int
    matched_cases: int
    mismatched_cases: int
    mismatches_from_missing_input: int
    rubric_defined: bool
    alternative_model_tested: bool


@dataclass
class PartnerMigration:
    partner_name: str
    is_large_partner: bool
    migration_owner: str
    required_change: str
    target_quarter: str
    test_date_defined: bool
    production_deadline_defined: bool


# ------------------------------------------------------------
# Q1
# Scoring model governance
# ------------------------------------------------------------

def review_scoring_model_change(review: ModelReview) -> dict:
    """
    A poor output does not automatically mean the model is wrong.

    First separate:
    - missing input
    - scoring rubric problems
    - scoring weight problems

    AI may analyze and back-test.
    Human approves scoring-model changes.
    """

    missing_input_explains_all_mismatches = (
        review.mismatched_cases > 0
        and review.mismatched_cases
        == review.mismatches_from_missing_input
    )

    if (
        missing_input_explains_all_mismatches
        or not review.rubric_defined
        or not review.alternative_model_tested
    ):
        return {
            "action": ModelDecision.HOLD_MODEL_CHANGE.value,
            "workflow_status": WorkflowStatus.WAIT.value,
            "next_owner": "PLATFORM_PARTNER_LEAD",
            "ai_can_change_weights": False,
            "reason": "MODEL_CHANGE_NOT_YET_JUSTIFIED",
            "resume_condition":
                "RUBRIC_DEFINED_AND_BACKTEST_COMPLETED",
        }

    return {
        "action": ModelDecision.READY_FOR_HUMAN_REVIEW.value,
        "workflow_status": WorkflowStatus.CONTINUE.value,
        "next_owner": "PLATFORM_PARTNER_LEAD",
        "ai_can_change_weights": False,
        "reason": "MODEL_CHANGE_EVIDENCE_AVAILABLE",
        "resume_condition": "HUMAN_APPROVAL",
    }


# ------------------------------------------------------------
# Q2
# Compliance guardrail
# ------------------------------------------------------------

def classify_compliance_work(
    affected_integrations: int,
    regulatory_requirement_mandatory: bool,
) -> dict:
    """
    Mandatory regulatory work does not compete with normal
    revenue prioritization for whether it must be completed.

    Business and technical factors may still determine
    migration sequence inside the allowed window.
    """

    if not regulatory_requirement_mandatory:
        return {
            "action": "USE_NORMAL_PRIORITY_MODEL",
            "workflow_status": WorkflowStatus.CONTINUE.value,
        }

    return {
        "action": "CREATE_MANDATORY_MIGRATION_PROGRAM",
        "workflow_status": WorkflowStatus.CONTINUE.value,
        "affected_integrations": affected_integrations,
        "regulatory_deadline_month":
            REGULATORY_DEADLINE_MONTHS,
        "platform_deadline_month":
            PLATFORM_MIGRATION_DEADLINE_MONTHS,
        "safety_buffer_months":
            INTERNAL_SAFETY_BUFFER_MONTHS,
        "normal_revenue_override_allowed": False,
        "next_owner": "PLATFORM_PARTNER_LEAD",
    }


def plan_partner_migration(
    partner: PartnerMigration,
) -> dict:
    """
    Large Partners may need earlier individual planning because
    their Engineering roadmaps can already be committed.

    This is different from business-tier classification.
    """

    if partner.is_large_partner:
        mode = MigrationMode.EARLY_INDIVIDUAL_PLANNING
    else:
        mode = MigrationMode.QUARTERLY_MIGRATION_WAVE

    required_fields_complete = all(
        [
            bool(partner.migration_owner),
            bool(partner.required_change),
            bool(partner.target_quarter),
            partner.test_date_defined,
            partner.production_deadline_defined,
        ]
    )

    if not required_fields_complete:
        status = WorkflowStatus.WAIT
        action = "COMPLETE_MIGRATION_PLAN"
    else:
        status = WorkflowStatus.CONTINUE
        action = "TRACK_MIGRATION"

    return {
        "partner": partner.partner_name,
        "planning_mode": mode.value,
        "action": action,
        "workflow_status": status.value,
        "next_owner": "PLATFORM_AGENT",
    }


# ------------------------------------------------------------
# Q3
# Safety buffer and exception governance
# ------------------------------------------------------------

 # ------------------------------------------------------------
# Q3
# Safety buffer and exception governance
# ------------------------------------------------------------

def handle_extension_request(
    partner_name: str,
    requested_extension_months: int,
    platform_deadline_at_risk: bool,
) -> dict:
    """
    The internal safety buffer is not a negotiable external deadline.

    A Partner request does not automatically consume the buffer.

    If the Partner later risks missing the Platform deadline,
    the Platform Partner Lead may trigger the predefined
    exception-review process.

    The Migration Program Owner may approve use of the internal
    safety buffer but cannot extend the regulatory deadline.
    """

    if not platform_deadline_at_risk:
        return {
            "partner": partner_name,
            "action": "KEEP_STANDARD_PLATFORM_DEADLINE",
            "workflow_status": WorkflowStatus.CONTINUE.value,
            "requested_extension_months":
                requested_extension_months,
            "extension_approved": False,
            "internal_buffer_disclosed_as_extension": False,
            "next_owner": "PLATFORM_PARTNER_LEAD",
            "reason": "NO_CONFIRMED_NEED_FOR_EXCEPTION",
        }

    return {
        "partner": partner_name,
        "action": "ESCALATE_BUFFER_EXCEPTION_REVIEW",
        "workflow_status": WorkflowStatus.ESCALATE.value,
        "requested_extension_months":
            requested_extension_months,
        "extension_approved": False,
        "internal_buffer_disclosed_as_extension": False,
        "next_owner": "PLATFORM_PARTNER_LEAD",
        "decision_owner": "MIGRATION_PROGRAM_OWNER",
        "compliance_review_required": True,
        "resume_condition":
            "EXCEPTION_DECISION_RECORDED",
        "reason": "PLATFORM_DEADLINE_AT_RISK",
    }

# ------------------------------------------------------------
# Demo
# ------------------------------------------------------------

def main():
    print("=== Q1: Scoring Model Governance ===")

    model_review = ModelReview(
        total_cases=20,
        matched_cases=17,
        mismatched_cases=3,
        mismatches_from_missing_input=3,
        rubric_defined=False,
        alternative_model_tested=False,
    )

    q1 = review_scoring_model_change(model_review)

    for key, value in q1.items():
        print(f"{key}: {value}")

    print("\n=== Q2: Compliance Guardrail ===")

    program = classify_compliance_work(
        affected_integrations=40,
        regulatory_requirement_mandatory=True,
    )

    for key, value in program.items():
        print(f"{key}: {value}")

    print("\n--- Large Partner Migration ---")

    large_partner = PartnerMigration(
        partner_name="PARTNER_X",
        is_large_partner=True,
        migration_owner="PLATFORM_PARTNER_LEAD",
        required_change="ENABLE_CONSENT_ENFORCEMENT",
        target_quarter="Q2",
        test_date_defined=True,
        production_deadline_defined=True,
    )

    large_partner_plan = plan_partner_migration(
        large_partner
    )

    for key, value in large_partner_plan.items():
        print(f"{key}: {value}")

    print("\n--- Standard Partner Migration ---")

    standard_partner = PartnerMigration(
        partner_name="PARTNER_Y",
        is_large_partner=False,
        migration_owner="PARTNER_MANAGER",
        required_change="ENABLE_CONSENT_ENFORCEMENT",
        target_quarter="Q3",
        test_date_defined=True,
        production_deadline_defined=True,
    )

    standard_partner_plan = plan_partner_migration(
        standard_partner
    )

    for key, value in standard_partner_plan.items():
        print(f"{key}: {value}")

    print("\n=== Q3: Safety Buffer Request ===")

    initial_request = handle_extension_request(
        partner_name="PARTNER_X",
        requested_extension_months=1,
        platform_deadline_at_risk=False,
    )

    for key, value in initial_request.items():
        print(f"{key}: {value}")

    print("\n--- If Partner Later Falls Behind ---")

    exception_case = handle_extension_request(
        partner_name="PARTNER_X",
        requested_extension_months=1,
        platform_deadline_at_risk=True,
    )

    for key, value in exception_case.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()