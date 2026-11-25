# FILE:        backend/app/routes/interview.py
# PURPOSE:     The MAP interview: the employee answers, the AI drafts duties, the rules check them,
#              and the employee confirms or dismisses each one. "AI proposes, rules check, people decide."
# OWNER:       Maruf (board row T5)
# DEPENDS ON:  backend/app/ai/gateway.py (extract_duties, Mahadi T3); backend/app/rules/evidence.py
#              (check_quote R1, counts_as_fact R2, Nazha T4); app/security.py; app/models.py;
#              docs/API-CONTRACT.md section 2 ("Answer the interview", "Confirm or dismiss a duty")
# USED BY:     the React interview screen (Tonni, T6, not built yet); backend/tests/test_interview.py
# STATUS:      REAL, in replay mode only: the gateway has no live model yet (provider not chosen), so
#              every answer comes from a recorded reply and the response says mode = "replay".
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# SECURITY:    Only the employee of the case may call either route (checked on the server). The raw
#              interview text is never stored: only the duties that pass the checks are saved.
# AI NOTE:     The model never decides what is true. Order of checks for every drafted duty:
#              gateway validates the shape -> R1 checks the quote against the EMPLOYEE's own words ->
#              the duty is saved as "pending" -> only the employee can confirm it. A "said" duty whose
#              quote fails R1 is downgraded to "suggested" (a question), never dropped or trusted.

import re
import secrets
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai import gateway
from app.ai.schemas import DraftDuty, GatewayError, JdLine
from app.db import get_db
from app.errors import ApiError
from app.models import AuditEvent, Case, Duty, JobDescriptionLine, User
from app.rules.evidence import check_quote, counts_as_fact
from app.schemas import DecisionRequest, DutyOut, InterviewReplyOut, InterviewRequest
from app.security import current_user

router = APIRouter(prefix="/api", tags=["interview"])

# How a gateway failure is shown to the caller. The detail is always our own sentence: raw model
# text is never put in an error (the gateway guarantees this too).
_BAD_INPUT = {"bad_input"}  # the caller's fault: nothing from the employee to read yet
_NOT_CONFIGURED = {"live_not_configured", "bad_mode"}  # a set-up problem on our side


def _employee_case(case_id: str, user: User, db: Session) -> Case:
    """Load the case and make sure this user is its employee.

    SECURITY: only the employee may answer the interview or confirm their own duties. A manager,
    HR or a colleague gets 403 even though they may read the case. Unknown case: 404.
    """
    case = db.get(Case, case_id)
    if case is None:
        raise ApiError(404, "case_not_found", f"There is no case {case_id}.")
    if not (user.role == "employee" and case.employee_id == user.id):
        raise ApiError(403, "forbidden", "Only the employee of this case can do this.")
    return case


def _same_title(title: str) -> str:
    """A comparison key for duty titles, so "Monthly  Portfolio report" and "monthly portfolio
    report" count as the same duty and are not saved twice."""
    return re.sub(r"\s+", " ", title).strip().casefold()


def _apply_rule_r1(draft: DraftDuty, employee_turns: list[str]) -> tuple[DraftDuty, bool]:
    """R1: a "said" duty must quote the employee's real words. Returns (duty, was_downgraded).

    If the quote is not found in an employee turn, the duty becomes "suggested" with no quote:
    still shown, but only as a question. The model's claim is never trusted.
    """
    if draft.evidence_type == "said" and not check_quote(draft.quote or "", employee_turns):
        return DraftDuty(title=draft.title, evidence_type="suggested", quote=None, source_line_id=None), True
    return draft, False


@router.post("/cases/{case_id}/interview/reply", response_model=InterviewReplyOut)
def interview_reply(
    case_id: str,
    body: InterviewRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Read the interview so far and return the next question and the Role Map as it stands.

    CONTRACT: docs/API-CONTRACT.md, "Answer the interview". The browser keeps the turns; they are sent
    again each time and are NOT stored. Every call may add new duties (as "pending") and never
    changes one a person has already confirmed or dismissed.
    Errors: 401 signed out, 403 not the employee of the case, 404 unknown case, 422 a bad body or no
    employee reply yet, 502 the AI could not give a valid answer, 503 the AI is not configured.
    """
    case = _employee_case(case_id, user, db)

    lines = db.scalars(
        select(JobDescriptionLine).where(JobDescriptionLine.case_id == case.id).order_by(JobDescriptionLine.position)
    ).all()
    jd_lines = [JdLine(id=line.line_id, text=line.text) for line in lines]

    try:
        result = gateway.extract_duties(body.turns, jd_lines)
    except GatewayError as error:
        if error.code in _BAD_INPUT:
            raise ApiError(422, error.code, error.detail) from error
        if error.code in _NOT_CONFIGURED:
            raise ApiError(503, error.code, error.detail) from error
        raise ApiError(502, error.code, error.detail) from error

    employee_turns = [turn.text for turn in body.turns if turn.role == "employee"]
    existing = {_same_title(d.title): d for d in case.duties}
    downgraded: list[str] = []

    for draft in result.duties:
        draft, was_downgraded = _apply_rule_r1(draft, employee_turns)
        if was_downgraded:
            downgraded.append(draft.title)
        known = existing.get(_same_title(draft.title))
        if known is None:
            duty = Duty(
                id=f"duty-{secrets.token_hex(4)}",
                case_id=case.id,
                title=draft.title,
                evidence_type=draft.evidence_type,
                quote=draft.quote,
                source_line_id=draft.source_line_id,
                confirmation="pending",  # a person decides; the model never confirms
                hours_per_week=None,  # only a person fills this in
            )
            db.add(duty)
            case.duties.append(duty)
            existing[_same_title(draft.title)] = duty
        elif known.confirmation == "pending" and known.evidence_type == "suggested" and draft.evidence_type != "suggested":
            # Better evidence arrived for a duty that was only a question: keep it pending, but show why.
            known.evidence_type = draft.evidence_type
            known.quote = draft.quote
            known.source_line_id = draft.source_line_id
        # Otherwise leave it alone: a confirmed or dismissed duty is a person's decision.

    db.commit()
    duties = list(case.duties)
    return {
        "mode": result.mode,
        "next_question": result.next_question,
        "duties": duties,
        "downgraded": downgraded,
        "fact_count": sum(1 for d in duties if counts_as_fact(d)),  # R2
    }


@router.patch("/cases/{case_id}/duties/{duty_id}", response_model=DutyOut)
def decide_duty(
    case_id: str,
    duty_id: str,
    body: DecisionRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> Duty:
    """The employee confirms or dismisses one duty. Writes one audit event.

    CONTRACT: docs/API-CONTRACT.md, "Confirm or dismiss a duty". A person may change their mind, so
    confirming a dismissed duty (or the other way round) is allowed; each change is audited.
    Errors: 401 signed out, 403 not the employee of the case, 404 unknown case or duty, 422 a bad body.
    """
    case = _employee_case(case_id, user, db)
    duty = db.get(Duty, duty_id)
    if duty is None or duty.case_id != case.id:
        raise ApiError(404, "duty_not_found", f"There is no duty {duty_id} in case {case_id}.")

    duty.confirmation = "confirmed" if body.decision == "confirm" else "dismissed"
    db.add(
        AuditEvent(
            case_id=case.id,
            actor_id=user.id,
            action="duty_confirmed" if body.decision == "confirm" else "duty_dismissed",
            duty_id=duty.id,
            at=datetime.now(timezone.utc),
        )
    )
    db.commit()
    return duty
