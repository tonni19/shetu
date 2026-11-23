# FILE:        backend/app/security.py
# PURPOSE:     Passwords, "who is signed in", and "may this person see this case".
#              Every permission decision in the backend goes through this file.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  app/models.py (User, Case), app/db.py (get_db), app/errors.py (ApiError)
# USED BY:     app/routes/auth.py, app/routes/cases.py; later every route
# STATUS:      REAL for reading a case. Cover colleagues get no case access yet:
#              TODO(Maruf, T5+): let a colleague read only their own cover assignments, once
#              assignments exist (docs/API-CONTRACT.md, "Read a case").
# DATA:        Synthetic accounts only.
# SECURITY:    The rules here are enforced on the server for every request. Hiding a button in
#              React is not security (AGENTS.md rule 9). The user id is read from the signed
#              session cookie, never from a header or a field the caller could fake.

import hashlib
import hmac
import secrets

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.errors import ApiError
from app.models import Case, User

_ITERATIONS = 200_000  # slows down password guessing; standard library only, no extra dependency


def hash_password(password: str) -> str:
    """Return "salt$hash" using PBKDF2-SHA256. A new random salt each time, so two users with the
    same password still get different hashes."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), _ITERATIONS).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    """True if `password` matches the stored "salt$hash". Uses a constant-time comparison so the
    time taken does not leak how many characters were right."""
    try:
        salt, digest = stored.split("$", 1)
    except ValueError:
        return False
    check = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), _ITERATIONS).hex()
    return hmac.compare_digest(check, digest)


def current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """FastAPI dependency: the signed-in user, or a 401 error.

    The session cookie is signed by the server (SessionMiddleware in app/main.py), so the
    caller cannot change the user id inside it.
    """
    user_id = request.session.get("user_id")
    user = db.get(User, user_id) if user_id else None
    if user is None:
        raise ApiError(401, "not_signed_in", "Please sign in first.")
    return user


def can_read_case(user: User, case: Case) -> bool:
    """SECURITY: who may read a leave case (docs/API-CONTRACT.md, "Read a case").

    - the employee whose case it is
    - the manager of that case
    - HR (they oversee every case)
    Everyone else, including cover colleagues for now, may not.
    """
    if user.role == "hr":
        return True
    if user.role == "employee" and case.employee_id == user.id:
        return True
    if user.role == "manager" and case.manager_id == user.id:
        return True
    return False
