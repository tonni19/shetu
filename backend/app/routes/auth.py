# FILE:        backend/app/routes/auth.py
# PURPOSE:     Sign in, sign out, and "who am I". The server keeps who is signed in inside a
#              signed session cookie (SessionMiddleware, app/main.py).
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  app/security.py, app/schemas.py, app/models.py
# USED BY:     the React sign-in screen (Tonni, T2): call with `credentials: "include"` (or via
#              the Vite /api proxy) so the browser keeps the cookie
# STATUS:      REAL. Accounts are seeded synthetic users; there is no sign-up.
# CONTRACT:    docs/API-CONTRACT.md section 2: "Sign in", plus "Sign out" and "Who am I".
# SECURITY:    A wrong user id and a wrong password give the same error, so an attacker cannot
#              learn which user ids exist.

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.errors import ApiError
from app.models import User
from app.schemas import LoginRequest, UserOut
from app.security import current_user, verify_password

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login", response_model=UserOut)
def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)) -> User:
    """Check the user id and password. On success, remember the user in the session cookie and
    return who they are. On failure, 401 "invalid_credentials"."""
    user = db.get(User, body.user_id)
    if user is None or not verify_password(body.password, user.password_hash):
        raise ApiError(401, "invalid_credentials", "The user id or password is wrong.")
    request.session.clear()  # start a clean session, so nothing from an earlier user remains
    request.session["user_id"] = user.id
    return user


@router.post("/logout", status_code=204)
def logout(request: Request) -> None:
    """Forget who is signed in. Safe to call when nobody is signed in."""
    request.session.clear()


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)) -> User:
    """Return the signed-in user, or 401 "not_signed_in". The React app calls this on start-up
    to decide whether to show the sign-in screen."""
    return user
