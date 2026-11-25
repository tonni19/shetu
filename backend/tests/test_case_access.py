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
    assert set(body) == {"id", "employee_id", "employee_name", "manager_id", "manager_name", "leave_start", "leave_end", "stage", "duties"}


def test_duty_keeps_evidence_and_confirmation_separate(client):
    login(client, "u-nusrat")
    said = client.get("/api/cases/case-1").json()["duties"][1]
    assert said["evidence_type"] == "said" and said["quote"]
    assert said["confirmation"] == "pending"
    assert said["hours_per_week"] is None  # unknown until a person says otherwise


# ---- display names and the case list (board row T1 follow-up, requested by Tonni's Issue #28)

def test_case_shows_the_names_of_the_employee_and_the_manager(client):
    login(client, "u-nusrat")
    body = client.get("/api/cases/case-1").json()
    assert body["employee_name"] == "Nusrat Jahan"
    assert body["manager_name"] == "Shirin Akter"


@pytest.mark.parametrize(
    "user_id, expected_ids",
    [
        ("u-nusrat", ["case-1"]),  # the employee sees only their own case
        ("u-sabbir", ["case-2"]),
        ("u-shirin", ["case-1", "case-2"]),  # the manager sees every case they manage
        ("u-farhana", ["case-1", "case-2"]),  # HR sees every case
        ("u-tania", []),  # a cover colleague has no case yet: an empty list, not an error
    ],
)
def test_the_list_holds_only_the_cases_that_user_may_read(client, user_id, expected_ids):
    login(client, user_id)
    r = client.get("/api/cases")
    assert r.status_code == 200
    assert [c["id"] for c in r.json()] == expected_ids


def test_list_rows_have_names_and_dates_but_no_duties(client):
    login(client, "u-shirin")
    row = client.get("/api/cases").json()[0]
    assert set(row) == {"id", "employee_id", "employee_name", "manager_id", "manager_name", "leave_start", "leave_end", "stage"}
    assert row["employee_name"] == "Nusrat Jahan"


def test_the_list_needs_sign_in(client):
    assert client.get("/api/cases").status_code == 401


def test_every_case_in_my_list_can_be_opened(client):
    # The list and the single case use the same permission function, so they can never disagree.
    login(client, "u-nusrat")
    for row in client.get("/api/cases").json():
        assert client.get(f"/api/cases/{row['id']}").status_code == 200

