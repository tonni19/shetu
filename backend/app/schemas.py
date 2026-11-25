# FILE:        backend/app/schemas.py
# PURPOSE:     The exact JSON shapes the API accepts and returns (Pydantic models).
#              The React app (Tonni, T2) reads these shapes; they must match docs/API-CONTRACT.md.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  docs/API-CONTRACT.md sections 1 and 2
# USED BY:     app/routes/*, tests; the frontend through the JSON it receives
# STATUS:      REAL for sign-in and reading a case. Interview shapes come with T5.
# DATA:        No reason-for-leave field, and no password in any response.
# AI NOTE:     A model here is a promise to the frontend. Changing a field name or type is a
#              shared-interface change (AGENTS.md, "Changing a shared interface").

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    """Body of POST /api/login. Accounts are seeded synthetic users (see app/seed.py)."""

    user_id: str
    password: str


class UserOut(BaseModel):
    """Who is signed in. Never includes the password hash."""

    model_config = ConfigDict(from_attributes=True)  # lets Pydantic read a SQLAlchemy object

    id: str
    name: str
    role: Literal["employee", "manager", "hr", "colleague"]


class DutyOut(BaseModel):
    """CONTRACT: docs/API-CONTRACT.md, "Duty"."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    case_id: str
    title: str
    evidence_type: Literal["said", "documented", "suggested"]
    quote: str | None
    source_line_id: str | None
    confirmation: Literal["pending", "confirmed", "dismissed"]
    hours_per_week: float | None


class CaseSummaryOut(BaseModel):
    """One row of the case list (GET /api/cases). CONTRACT: docs/API-CONTRACT.md, "List my cases".

    Only the names and dates a list screen needs. It has no duties; the full case has them.
    """

    id: str
    employee_id: str
    employee_name: str
    manager_id: str
    manager_name: str
    leave_start: date
    leave_end: date
    stage: Literal["map", "hold", "fit"]


class CaseOut(CaseSummaryOut):
    """CONTRACT: docs/API-CONTRACT.md, "Case": the summary plus the duties the caller may see."""

    duties: list[DutyOut]


class ErrorOut(BaseModel):
    """CONTRACT: every error the API returns has this shape: a machine code and a human sentence."""

    code: str
    detail: str
