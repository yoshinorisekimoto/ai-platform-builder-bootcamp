"""Day 59 — Standard Work, Exception Tickets, and Human Authorization.

Synthetic Commerce SaaS operating-model exercise; no live Agent communication.
"""

import json
from dataclasses import asdict, dataclass
from typing import Optional, List, Set

ALLOWED_STATUSES: Set[str] = {"WAIT", "PROVISIONAL", "CONTINUE"}
ALLOWED_PRIORITIES: Set[str] = {"NORMAL", "URGENT", "CRITICAL"}


@dataclass
class Request:
    case: str
    standard_work_authorized: bool = True
    exception_requested: bool = False
    ticket_submitted_by_partner_human: bool = False
    declared_priority: str = "NORMAL"
    business_context_complete: bool = False
    previous_similar_exception_approved: bool = False
    repeated_pattern: bool = False
    case_specific_human_approval: bool = False


@dataclass
class Result:
    case: str
    action: str
    status: str
    next_owner: str
    reason: str
    resume_condition: str
    standard_work_status: str
    exception_status: str
    declared_priority: str
    human_decision_required: bool
    commitment_made_by_agent: bool = False


def route(request: Request) -> Result:
    if request.declared_priority not in ALLOWED_PRIORITIES:
        raise ValueError("Partner priority must be NORMAL, URGENT, or CRITICAL")

    # Standard tasks are a separate branch: an exception need not block them.
    standard_status = "CONTINUE" if request.standard_work_authorized else "WAIT"
    if not request.standard_work_authorized:
        result = Result(
            request.case, "ROUTE_STANDARD_WORK_AUTHORIZATION", "WAIT",
            "PLATFORM_PARTNER_LEAD", "Standard tasks lack prior authorization.",
            "STANDARD_WORK_AUTHORIZED", standard_status, "WAIT",
            request.declared_priority, True,
        )
    elif not request.exception_requested:
        result = Result(
            request.case, "CONTINUE_AUTHORIZED_STANDARD_WORK", "CONTINUE",
            "PLATFORM_AGENT", "Only pre-approved standard API and authentication work is requested.",
            "STANDARD_WORK_RECORDED", standard_status, "CONTINUE",
            request.declared_priority, False,
        )
    elif not request.ticket_submitted_by_partner_human:
        result = Result(
            request.case, "DIRECT_PARTNER_TO_EXCEPTION_TICKET", "WAIT",
            "PARTNER_HUMAN", "An exception requires a separate human-submitted ticket.",
            "EXCEPTION_TICKET_SUBMITTED", standard_status, "WAIT",
            request.declared_priority, True,
        )
    elif not request.business_context_complete:
        result = Result(
            request.case, "ROUTE_TICKET_FOR_HUMAN_ASSESSMENT", "WAIT",
            "PLATFORM_PARTNER_LEAD", "The business impact is incomplete; Human follow-up is required.",
            "BUSINESS_IMPACT_ASSESSED_BY_HUMAN", standard_status, "WAIT",
            request.declared_priority, True,
        )
    elif request.case_specific_human_approval:
        result = Result(
            request.case, "PREPARE_APPROVED_EXCEPTION_NOTICE", "CONTINUE",
            "PLATFORM_PARTNER_LEAD", "Case-specific Human approval is recorded; the Lead owns notice.",
            "PARTNER_NOTICE_RECORDED", standard_status, "CONTINUE",
            request.declared_priority, False,
        )
    elif request.repeated_pattern:
        result = Result(
            request.case, "PROPOSE_STANDARDIZATION_FOR_HUMAN_REVIEW", "PROVISIONAL",
            "PLATFORM_PARTNER_LEAD", "Repeated cases suggest a possible rule, not automatic delegation.",
            "HUMAN_POLICY_AND_CASE_DECISIONS_RECORDED", standard_status, "WAIT",
            request.declared_priority, True,
        )
    else:
        reason = (
            "Past approval is reference Evidence only; Partner B needs its own decision."
            if request.previous_similar_exception_approved else
            "Partner-declared urgency is advisory; business priority needs Human judgment."
        )
        result = Result(
            request.case, "PREPARE_HUMAN_EXCEPTION_DECISION", "WAIT",
            "PLATFORM_PARTNER_LEAD", reason,
            "PLATFORM_ENGINEERING_AND_PARTNER_LEAD_DECISIONS_RECORDED",
            standard_status, "WAIT", request.declared_priority, True,
        )

    assert result.status in ALLOWED_STATUSES
    assert result.standard_work_status in ALLOWED_STATUSES
    assert result.exception_status in ALLOWED_STATUSES
    assert not result.commitment_made_by_agent
    return result


def demo() -> None:
    cases: List[Request] = [
        Request(case="standard_only"),
        Request(case="ticket_needed", exception_requested=True),
        Request(case="ticket_missing_impact", exception_requested=True,
                ticket_submitted_by_partner_human=True, declared_priority="CRITICAL"),
        Request(case="ticket_ready_for_review", exception_requested=True,
                ticket_submitted_by_partner_human=True, business_context_complete=True,
                declared_priority="CRITICAL"),
        Request(case="similar_prior_approval", exception_requested=True,
                ticket_submitted_by_partner_human=True, business_context_complete=True,
                previous_similar_exception_approved=True),
        Request(case="repeated_exception_pattern", exception_requested=True,
                ticket_submitted_by_partner_human=True, business_context_complete=True,
                repeated_pattern=True),
        Request(case="case_specific_approval", exception_requested=True,
                ticket_submitted_by_partner_human=True, business_context_complete=True,
                case_specific_human_approval=True),
        Request(case="standard_not_authorized", standard_work_authorized=False),
    ]
    for case in cases:
        print(json.dumps(asdict(route(case)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    demo()
