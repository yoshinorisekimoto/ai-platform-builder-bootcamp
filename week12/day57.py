
過去のメッセージを読み込み中…



















































































































"""Day 57 — Agent Communication Failure & Business Continuity.

Synthetic PPM operating-model scenarios, not a network messaging implementation.
"""

import json
from dataclasses import asdict, dataclass
from typing import Optional, List, Set


@dataclass
class PartnerCase:
    name: str
    scenario: str
    communication_available: bool
    production_incident: bool = False
    users_affected: bool = False
    launch_approved: bool = False
    launch_soon: bool = False
    clarification_needed: bool = False
    human_contact_available: bool = True
    approval_record_available: bool = False
    human_notification_recorded: bool = False


@dataclass
class Outcome:
    case: str
    action: str
    status: str
    next_owner: str
    reason: str
    resume_condition: Optional[str]
    human_approval_bypassed: bool = False


def route(case: PartnerCase) -> Outcome:
    """Route business work; never grant technical or launch approval."""
    if case.production_incident and case.users_affected:
        return Outcome(
            case=case.name,
            action="ROUTE_TO_INCIDENT_RESPONSE",
            status="CONTINUE",
            next_owner="PLATFORM_ENGINEERING_AND_PARTNER_LEAD",
            reason="Production user impact takes priority; the human incident route remains available.",
            resume_condition="INCIDENT_STATUS_RECORDED",
        )

    if case.communication_available:
        if case.human_notification_recorded:
            return Outcome(
                case=case.name,
                action="RECONCILE_HUMAN_HANDOFF",
                status="CONTINUE",
                next_owner="PLATFORM_AGENT",
                reason="Confirm the recorded human action before resuming Agent coordination; do not repeat the notification.",
                resume_condition="HANDOFF_RECORD_VERIFIED",
            )
        return Outcome(
            case=case.name,
            action="CONTINUE_AUTHORIZED_AGENT_COORDINATION",
            status="CONTINUE",
            next_owner="PLATFORM_AGENT",
            reason="Communication is available; existing authorization boundaries still apply.",
            resume_condition=None,
        )

    if case.launch_approved and case.approval_record_available and case.human_contact_available:
        return Outcome(
            case=case.name,
            action="HANDOFF_APPROVED_LAUNCH_NOTICE_TO_HUMAN",
            status="CONTINUE",
            next_owner="PLATFORM_PARTNER_LEAD",
            reason="Formal approval is recorded; a human can notify the partner without waiting for Agent connectivity.",
            resume_condition="PARTNER_NOTIFICATION_RECORDED",
        )

    if case.launch_soon and not case.launch_approved:
        return Outcome(
            case=case.name,
            action="CONTINUE_ENGINEERING_LAUNCH_REVIEW",
            status="WAIT",
            next_owner="PLATFORM_ENGINEERING",
            reason="The internal review can continue; launch is not approved until Engineering decides.",
            resume_condition="ENGINEERING_LAUNCH_DECISION_RECORDED",
        )

    if case.clarification_needed:
        return Outcome(
            case=case.name,
            action="HOLD_AGENT_CLARIFICATION",
            status="WAIT",
            next_owner="PLATFORM_AGENT",
            reason="External Agent clarification is unavailable; record the outstanding question and monitor the deadline.",
            resume_condition="COMMUNICATION_RESTORED_OR_HUMAN_FALLBACK_AUTHORIZED",
        )

    return Outcome(
        case=case.name,
        action="RECORD_COMMUNICATION_OUTAGE",
        status="WAIT",
        next_owner="PLATFORM_AGENT",
        reason="No approved alternative action is available; preserve the current business state.",
        resume_condition="COMMUNICATION_RESTORED_OR_HUMAN_DIRECTION_RECORDED",
    )


def demo() -> None:
    cases: List[PartnerCase] = [
        PartnerCase("partner_c_incident", "live incident", False, production_incident=True, users_affected=True),
        PartnerCase("partner_a_review", "launch tomorrow", False, launch_soon=True),
        PartnerCase("partner_b_clarification", "launch next week", False, clarification_needed=True),
        PartnerCase("partner_a_human_notice", "approval recorded during outage", False, launch_approved=True,
                    approval_record_available=True, human_contact_available=True),
        PartnerCase("partner_a_recovery", "communication restored after human notice", True,
                    launch_approved=True, approval_record_available=True, human_notification_recorded=True),
    ]
    for case in cases:
        result = route(case)
        assert not result.human_approval_bypassed
        print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    demo()



