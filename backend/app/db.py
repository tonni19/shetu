# FILE:        backend/app/db.py
# PURPOSE:     Connects to the SQLite database and hands each request its own database session.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  app/config.py (database address)
# USED BY:     app/models.py (Base), every route through the `get_db` dependency, app/seed.py, tests
# STATUS:      REAL
# DATA:        Synthetic only.
# AI NOTE:     A "session" here is a SQLAlchemy database session (a unit of work), not the login
#              session cookie. Each request gets a fresh one and it is always closed afterwards.

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Parent class of every table in app/models.py."""


def make_engine(url: str) -> Engine:
    """Create the database engine.

    `check_same_thread=False` is needed for SQLite because FastAPI may handle one request on a
    different thread from the one that opened the connection. It is safe here because every
    request uses its own session.
    """
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args)


# Filled in by app/main.py when the app is created (and by tests with a temporary database).
SessionLocal: sessionmaker[Session] = sessionmaker(autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """FastAPI dependency: open a database session for one request, and always close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
