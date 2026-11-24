# FILE:        backend/tests/conftest.py
# PURPOSE:     Shared test set-up: every test gets a brand-new temporary SQLite database with the
#              synthetic seed data, and a client that talks to the API without starting a server.
# OWNER:       Maruf (board row T1). Nazha (T4) owns the test set-up and CI as a whole; this file
#              is the backend's part of it.
# DEPENDS ON:  app/main.py (create_app), app/seed.py
# USED BY:     every test in backend/tests/
# STATUS:      REAL
# AI NOTE:     The environment variable is set BEFORE `app` is imported, so importing app.main
#              never creates or touches the developer's backend/shetu.db during tests.

import os
import tempfile

os.environ.setdefault("SHETU_DATABASE_URL", "sqlite:///" + os.path.join(tempfile.gettempdir(), "shetu-import-only.db"))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app import db as db_module  # noqa: E402
from app.main import create_app  # noqa: E402
from app.seed import DEMO_PASSWORD, seed  # noqa: E402


@pytest.fixture()
def client(tmp_path) -> TestClient:
    """A test client backed by a fresh database file in pytest's temporary folder."""
    app = create_app(database_url=f"sqlite:///{tmp_path / 'test.db'}")
    with db_module.SessionLocal() as session:
        seed(session)
    return TestClient(app)


def login(client: TestClient, user_id: str, password: str = DEMO_PASSWORD):
    """Sign in as a seeded user. The client keeps the session cookie for the next requests."""
    return client.post("/api/login", json={"user_id": user_id, "password": password})
