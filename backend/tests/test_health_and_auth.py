# FILE:        backend/tests/test_health_and_auth.py
# PURPOSE:     Proves the health check, signing in and out, and the error format work.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  tests/conftest.py (client, login)
# STATUS:      REAL

from app.models import User
from app.security import hash_password, verify_password
from tests.conftest import login


def test_health_reports_database_ok(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "database": "ok"}


def test_login_with_seeded_account_returns_the_user_without_password(client):
    r = login(client, "u-nusrat")
    assert r.status_code == 200
    assert r.json() == {"id": "u-nusrat", "name": "Nusrat Jahan", "role": "employee"}
    assert "password" not in r.text and "hash" not in r.text


def test_wrong_password_and_unknown_user_give_the_same_error(client):
    # SECURITY: the same answer for both, so nobody can find out which user ids exist.
    wrong_password = login(client, "u-nusrat", "nope")
    unknown_user = login(client, "u-nobody", "nope")
    assert wrong_password.status_code == unknown_user.status_code == 401
    assert wrong_password.json() == unknown_user.json() == {
        "code": "invalid_credentials",
        "detail": "The user id or password is wrong.",
    }


def test_me_needs_a_signed_in_user(client):
    r = client.get("/api/me")
    assert r.status_code == 401
    assert r.json()["code"] == "not_signed_in"


def test_me_after_login_and_logout(client):
    login(client, "u-shirin")
    assert client.get("/api/me").json()["role"] == "manager"
    assert client.post("/api/logout").status_code == 204
    assert client.get("/api/me").status_code == 401


def test_bad_request_body_uses_the_contract_error_shape(client):
    r = client.post("/api/login", json={"user_id": "u-nusrat"})  # password missing
    assert r.status_code == 422
    assert r.json()["code"] == "invalid_request"
    assert "password" in r.json()["detail"]


def test_passwords_are_stored_only_as_salted_hashes(client):
    from app import db as db_module

    with db_module.SessionLocal() as session:
        stored = session.get(User, "u-nusrat").password_hash
    assert "shetu-demo" not in stored
    assert verify_password("shetu-demo", stored)
    # The same password hashed twice gives different results because of the random salt.
    assert hash_password("same") != hash_password("same")
