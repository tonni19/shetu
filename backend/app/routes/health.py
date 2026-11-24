# FILE:        backend/app/routes/health.py
# PURPOSE:     GET /healthz: a quick "is the API up, and can it reach the database?" check.
#              Useful before a demo, and for anyone setting up the project on a new laptop.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  app/db.py
# USED BY:     people and scripts; no login needed
# STATUS:      REAL
# CONTRACT:    docs/API-CONTRACT.md section 2, "Health".

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz(db: Session = Depends(get_db)) -> JSONResponse:
    """Return 200 with {"status": "ok", "database": "ok"} when the database answers,
    or 503 with "database": "unreachable" when it does not. Never raises."""
    try:
        db.execute(text("SELECT 1"))
        return JSONResponse({"status": "ok", "database": "ok"})
    except Exception:  # any database problem means "not healthy"; the detail is not leaked
        return JSONResponse({"status": "degraded", "database": "unreachable"}, status_code=503)
