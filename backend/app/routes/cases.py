# FILE:        backend/app/routes/cases.py
# PURPOSE:     List the leave cases the signed-in user may read, and read one case with its duties.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  app/security.py (current_user, can_read_case), app/models.py, app/schemas.py
# USED BY:     the React case list and case page (Tonni, T2) and the interview screen later (T6)
# STATUS:      REAL. Everyone allowed sees every duty for now.
#              TODO(Maruf, T5): the manager should see confirmed duties only, without the raw
#              interview, once the interview exists (docs/UPDATE-1-PLAN.md, "fuller MAP slice").
# CONTRACT:    docs/API-CONTRACT.md section 2: "List my cases" and "Read a case".
# SECURITY:    The permission check runs on the server for every call (can_read_case). The list
#              is filtered with the same function, so it never shows a case the user cannot open.

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.errors import ApiError
from app.models import Case, User
from app.schemas import CaseOut, CaseSummaryOut
from app.security import can_read_case, current_user

router = APIRouter(prefix="/api", tags=["cases"])


def _summary_fields(case: Case) -> dict:
    """The fields the list and the single case share, including the two display names.

    The names come from the users table through Case.employee and Case.manager. Only the name is
    copied out: nothing else about a person (role, password hash) leaves through a case.
    """
    return {
        "id": case.id,
        "employee_id": case.employee_id,
        "employee_name": case.employee.name,
        "manager_id": case.manager_id,
        "manager_name": case.manager.name,
        "leave_start": case.leave_start,
        "leave_end": case.leave_end,
        "stage": case.stage,
    }


@router.get("/cases", response_model=list[CaseSummaryOut])
def list_cases(user: User = Depends(current_user), db: Session = Depends(get_db)) -> list[dict]:
    """Return the cases this user may read, oldest id first.

    Each person gets a different list: an employee sees their own case, a manager the cases they
    manage, HR every case, and a cover colleague an empty list (not an error: nothing to show).
    Errors: 401 if nobody is signed in (from current_user).
    """
    cases = db.scalars(select(Case).order_by(Case.id)).all()
    return [_summary_fields(case) for case in cases if can_read_case(user, case)]


@router.get("/cases/{case_id}", response_model=CaseOut)
def read_case(case_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict:
    """Return the case and its duties.

    Errors: 401 if nobody is signed in (from current_user), 404 "case_not_found" if there is no
    such case, 403 "forbidden" if this user may not see it.
    """
    case = db.get(Case, case_id)
    if case is None:
        raise ApiError(404, "case_not_found", f"There is no case {case_id}.")
    if not can_read_case(user, case):
        raise ApiError(403, "forbidden", "You are not allowed to see this case.")
    return {**_summary_fields(case), "duties": case.duties}
