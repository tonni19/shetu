# FILE:        backend/app/routes/cases.py
# PURPOSE:     Read one leave case, with its duties, if the signed-in user is allowed to.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  app/security.py (current_user, can_read_case), app/models.py, app/schemas.py
# USED BY:     the React case page (Tonni, T2) and the interview screen later (T6)
# STATUS:      REAL. Everyone allowed sees every duty for now.
#              TODO(Maruf, T5): the manager should see confirmed duties only, without the raw
#              interview, once the interview exists (docs/UPDATE-1-PLAN.md, "fuller MAP slice").
# CONTRACT:    docs/API-CONTRACT.md section 2, "Read a case".
# SECURITY:    The permission check runs on the server for every call (can_read_case).

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.errors import ApiError
from app.models import Case, User
from app.schemas import CaseOut
from app.security import can_read_case, current_user

router = APIRouter(prefix="/api", tags=["cases"])


@router.get("/cases/{case_id}", response_model=CaseOut)
def read_case(case_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)) -> Case:
    """Return the case and its duties.

    Errors: 401 if nobody is signed in (from current_user), 404 "case_not_found" if there is no
    such case, 403 "forbidden" if this user may not see it.
    """
    case = db.get(Case, case_id)
    if case is None:
        raise ApiError(404, "case_not_found", f"There is no case {case_id}.")
    if not can_read_case(user, case):
        raise ApiError(403, "forbidden", "You are not allowed to see this case.")
    return case
