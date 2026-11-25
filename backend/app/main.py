# FILE:        backend/app/main.py
# PURPOSE:     Builds the FastAPI application: database, session cookie, CORS, error format and
#              routes. Start it with: `uvicorn app.main:app --reload` from the backend/ folder.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  app/config.py, app/db.py, app/errors.py, app/routes/*
# USED BY:     uvicorn (development server), tests (create_app with a temporary database)
# STATUS:      REAL
# SECURITY:    The session cookie is signed with settings.secret_key, so it cannot be edited by
#              the browser. In development the key is a known default and a warning is printed.
# AI NOTE:     Tables are created with Base.metadata.create_all (no migration tool: Alembic is not
#              in the agreed stack). If you change a table, delete backend/shetu.db and re-seed.
#              New routers are added in the "Routes" block below.

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app import db as db_module
from app.config import DEV_SECRET, settings
from app.errors import register_error_handlers
from app.routes import auth, cases, health, interview

log = logging.getLogger("shetu")


def create_app(database_url: str | None = None) -> FastAPI:
    """Create the app. Tests pass their own `database_url` so they never touch backend/shetu.db."""
    engine = db_module.make_engine(database_url or settings.database_url)
    db_module.SessionLocal.configure(bind=engine)
    # Import the models so their tables are registered on Base before create_all runs.
    from app import models  # noqa: F401

    db_module.Base.metadata.create_all(engine)

    if settings.secret_key == DEV_SECRET:
        log.warning("Using the development session key. Set SHETU_SECRET_KEY before any real deployment.")

    app = FastAPI(title="Shetu API", version="0.1.0", description="Role continuity for planned leave. Synthetic data only.")

    # Order matters: CORS wraps everything; the session cookie is read before any route runs.
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, same_site="lax", https_only=False, max_age=8 * 60 * 60)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,  # the browser may send the session cookie
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_error_handlers(app)

    # Routes
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(cases.router)
    app.include_router(interview.router)
    return app


# The object uvicorn serves: `uvicorn app.main:app`.
app = create_app()
