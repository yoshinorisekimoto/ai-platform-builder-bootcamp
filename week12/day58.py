"""Day 58 — Partner Requirements Alignment (synthetic Commerce SaaS case).

Operating-model routing demonstration, not a live Agent integration.
"""

import json
from dataclasses import asdict, dataclass
from typing import Optional, List, Set

ALLOWED_STATUSES: Set[str] = {"WAIT", "PROVISIONAL", "CONTINUE"}


@dataclass
class Request:
    case: str
    business_need_known: bool = False
    impact_evidence_complete: bool = False
    standard_option_available: bool = True
    five_minute_guarantee_required: bool = False
    exception_requested: bool = False
    approved_clarification: bool = True
    product_decision_recorded: bool = False


@dataclass
class Result:
    case: str
    action: str
    status: str
    next_owner: str
    reason: str
    resume_condition: str
    human_decision_required: bool
    commitment_made_by_agent: bool = False


def route(request: Request) -> Result:
    # An exception or new delivery guarantee cannot be promised by an Agent.
    if request.exception_requested or request.five_minute_guarantee_required:
        result = Result(
            request.case, "PREPARE_HUMAN_EXCEPTION_REVIEW", "WAIT",
            "PLATFORM_PARTNER_LEAD", "A new guarantee or exception requires human review.",
            "HUMAN_EXCEPTION_DECISION_RECORDED", True,
        )
    elif not request.approved_clarification:
        result = Result(
            request.case, "ROUTE_CLARIFICATION_AUTHORIZATION", "WAIT",
            "PLATFORM_PARTNER_LEAD", "Clarification is outside the approved boundary.",
            "CLARIFICATION_AUTHORIZED", True,
        )
    elif not request.business_need_known:
        result = Result(
            request.case, "REQUEST_BUSINESS_NEED", "WAIT",
            "PLATFORM_AGENT_AND_AGENCY_AGENT", "Clarify the outcome before discussing solutions.",
            "BUSINESS_NEED_RECORDED", False,
        )
    elif not request.impact_evidence_complete:
        result = Result(
            request.case, "COLLECT_BUSINESS_IMPACT_EVIDENCE", "WAIT",
            "PLATFORM_AGENT_AND_AGENCY_AGENT", "Impact and value are not yet decision-ready.",
            "BUSINESS_IMPACT_EVIDENCE_RECORDED", False,
        )
    elif request.product_decision_recorded:
        result = Result(
            request.case, "COMMUNICATE_RECORDED_PRODUCT_DECISION", "CONTINUE",
            "PLATFORM_PARTNER_LEAD", "A human Product decision is recorded; the Platform Partner Lead owns partner communication.",
            "PARTNER_COMMUNICATION_RECORDED", False,
        )
    elif request.standard_option_available:
        result = Result(
            request.case, "PREPARE_STANDARD_OPTION_AND_PRODUCT_BRIEF", "PROVISIONAL",
            "PLATFORM_PARTNER_LEAD", "Standard webhook is available without a five-minute guarantee; the Platform Partner Lead evaluates product-wide value.",
            "PRODUCT_DECISION_RECORDED", True,
        )
    else:
        result = Result(
            request.case, "PREPARE_PRODUCT_ENGINEERING_REVIEW", "WAIT",
            "PLATFORM_PARTNER_LEAD", "No standard option meets the documented business need.",
            "PRODUCT_AND_ENGINEERING_DECISIONS_RECORDED", True,
        )

    assert result.status in ALLOWED_STATUSES
    assert not result.commitment_made_by_agent
    return result


def demo() -> None:
    cases: List[Request] = [
        Request(case="unknown_need"),
        Request(case="impact_missing", business_need_known=True),
        Request(case="standard_option", business_need_known=True, impact_evidence_complete=True),
        Request(case="new_guarantee", business_need_known=True, five_minute_guarantee_required=True),
        Request(case="unauthorized_clarification", approved_clarification=False),
        Request(case="product_decision", business_need_known=True, impact_evidence_complete=True,
                product_decision_recorded=True),
    ]
    for case in cases:
        print(json.dumps(asdict(route(case)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    demo()
