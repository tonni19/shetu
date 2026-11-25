# FILE:        backend/tests/test_case_access.py
# PURPOSE:     Proves who may read a leave case (docs/API-CONTRACT.md, "Read a case"):
#              the employee, their manager and HR may; a cover colleague and another employee get
#              403; nobody signed in gets 401; an unknown case is 404.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  tests/conftest.py, app/seed.py (the synthetic cast)
# STATUS:      REAL

import pytest

from tests.conftest import login


@pytest.mark.parametrize("user_id", ["u-nusrat", "u-shirin", "u-farhana"])
def test_employee_manager_and_hr_can_read_the_case(client, user_id):
    login(client, user_id)
    r = client.get("/api/cases/case-1")
    assert r.status_code == 200
    body = r.json()
    assert body["employee_id"] == "u-nusrat"
    assert body["leave_start"] == "2027-01-10" and body["leave_end"] == "2027-06-30"
    assert [d["id"] for d in body["duties"]] == ["duty-1", "duty-2"]


@pytest.mark.parametrize("user_id", ["u-tania", "u-sabbir"])
def test_a_colleague_or_another_employee_gets_403(client, user_id):
    login(client, user_id)
    r = client.get("/api/cases/case-1")
    assert r.status_code == 403
    assert r.json() == {"code": "forbidden", "detail": "You are not allowed to see this case."}


def test_reading_a_case_needs_sign_in(client):
    assert client.get("/api/cases/case-1").status_code == 401


def test_unknown_case_is_404(client):
    login(client, "u-farhana")
    r = client.get("/api/cases/case-999")
    assert r.status_code == 404
    assert r.json()["code"] == "case_not_found"


def test_the_case_has_no_reason_for_leave(client):
    # AGENTS.md rule 5: there is no reason field, and none may be added.
    login(client, "u-nusrat")
    body = client.get("/api/cases/case-1").json()
    assert set(body) == {"id", "employee_id", "manager_id", "leave_start", "leave_end", "stage", "duties"}


def test_duty_keeps_evidence_and_confirmation_separate(client):
    login(client, "u-nusrat")
    said = client.get("/api/cases/case-1").json()["duties"][1]
    assert said["evidence_type"] == "said" and said["quote"]
    assert said["confirmation"] == "pending"
    assert said["hours_per_week"] is None  # unknown until a person says otherwise
