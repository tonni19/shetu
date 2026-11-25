# FILE:        backend/tests/test_interview.py
# PURPOSE:     Proves the MAP interview route (board row T5): who may use it, that the AI's draft duties
#              go through rules R1 and R2, that nothing is saved twice or overwritten, that a person's
#              confirm or dismiss is audited, and that a failing AI never leaks raw text or bad data.
# OWNER:       Maruf (board row T5)
# DEPENDS ON:  backend/app/routes/interview.py; the recorded Banglish reply in
#              backend/app/ai/fixtures/replay/banglish_credit_pre_meeting.json (Mahadi, T3);
#              tests/conftest.py (client, login)
# STATUS:      REAL. Every run here is a labelled REPLAY: no live model exists yet.
# AI NOTE:     The replay answer is found by the text "credit pre-meeting hoy" in the interview, so the
#              employee turn below must contain it. To test the failure paths we replace
#              `gateway.extract_duties` with a small fake (monkeypatch); that never touches a real model.

import pytest
from sqlalchemy import select

from app import db as db_module
from app.ai import gateway
from app.ai.schemas import DraftDuty, ExtractResult, GatewayError
from app.models import AuditEvent
from tests.conftest import login

QUOTE = "Protiti Tuesday sondha 6 ta theke 7:30 porjonto credit pre-meeting hoy"
TURNS = [
    {"role": "assistant", "text": "Apnar sprotahik kaj ki ki?"},
    {"role": "employee", "text": QUOTE},
]


def reply(client, case_id="case-2", turns=None):
    return client.post(f"/api/cases/{case_id}/interview/reply", json={"turns": TURNS if turns is None else turns})


def by_title(body):
    return {d["title"]: d for d in body["duties"]}


# ---------------------------------------------------------------- the happy path (replay)

def test_the_recorded_banglish_answer_builds_a_role_map_with_evidence(client):
    login(client, "u-sabbir")
    r = reply(client)
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "replay"  # never shown as live
    assert "Quarter-end" in body["next_question"]
    duties = by_title(body)
    assert set(duties) == {"Credit pre-meeting", "Monthly portfolio report", "Quarter-end loan review"}
    said = duties["Credit pre-meeting"]
    assert said["evidence_type"] == "said" and said["quote"] == QUOTE  # her own words, verified by R1
    documented = duties["Monthly portfolio report"]
    assert documented["evidence_type"] == "documented" and documented["source_line_id"] == "jd-3"
    asked = duties["Quarter-end loan review"]
    assert asked["evidence_type"] == "suggested" and asked["quote"] is None  # only a question
    assert all(d["confirmation"] == "pending" and d["hours_per_week"] is None for d in body["duties"])


def test_rule_r2_counts_only_what_may_be_treated_as_a_fact(client):
    login(client, "u-sabbir")
    body = reply(client).json()
    # said + documented count; the suggested question does not, until the employee confirms it.
    assert body["fact_count"] == 2


def test_asking_twice_does_not_save_a_duty_twice(client):
    login(client, "u-sabbir")
    first = reply(client).json()
    second = reply(client).json()
    assert len(first["duties"]) == len(second["duties"]) == 3
    assert {d["id"] for d in first["duties"]} == {d["id"] for d in second["duties"]}


def test_a_duty_already_on_the_map_is_not_duplicated(client):
    # case-1 already has "Monthly portfolio report" (seed); the AI proposes it again.
    login(client, "u-nusrat")
    body = reply(client, case_id="case-1").json()
    assert [d["title"] for d in body["duties"]].count("Monthly portfolio report") == 1


# ---------------------------------------------------------------- rule R1: the model's claim is not trusted

def _fake_result(duties):
    return lambda turns, jd: ExtractResult(mode="replay", next_question="Next?", duties=duties)


def test_a_said_duty_with_an_invented_quote_is_downgraded_to_a_question(client, monkeypatch):
    invented = DraftDuty(title="Vendor payments", evidence_type="said", quote="I approve every vendor payment")
    monkeypatch.setattr(gateway, "extract_duties", _fake_result([invented]))
    login(client, "u-sabbir")
    body = reply(client).json()
    duty = by_title(body)["Vendor payments"]
    assert duty["evidence_type"] == "suggested" and duty["quote"] is None
    assert body["downgraded"] == ["Vendor payments"]


def test_a_quote_that_only_the_assistant_said_does_not_count(client, monkeypatch):
    # The assistant's question text is not the employee's evidence (R1 checks employee turns only).
    sneaky = DraftDuty(title="Weekly tasks", evidence_type="said", quote="Apnar sprotahik kaj ki ki?")
    monkeypatch.setattr(gateway, "extract_duties", _fake_result([sneaky]))
    login(client, "u-sabbir")
    body = reply(client).json()
    assert by_title(body)["Weekly tasks"]["evidence_type"] == "suggested"


def test_better_evidence_upgrades_a_pending_question_but_never_a_decision(client, monkeypatch):
    login(client, "u-sabbir")
    monkeypatch.setattr(gateway, "extract_duties", _fake_result([DraftDuty(title="Credit pre-meeting", evidence_type="suggested")]))
    first = by_title(reply(client).json())["Credit pre-meeting"]
    assert first["evidence_type"] == "suggested"
    monkeypatch.undo()  # back to the recorded reply, which says "said" with the real quote
    upgraded = by_title(reply(client).json())["Credit pre-meeting"]
    assert upgraded["evidence_type"] == "said" and upgraded["confirmation"] == "pending"
    # Once the employee confirms it, a later answer must not change it.
    client.patch(f"/api/cases/case-2/duties/{upgraded['id']}", json={"decision": "confirm"})
    again = by_title(reply(client).json())["Credit pre-meeting"]
    assert again["confirmation"] == "confirmed"


def test_a_dismissed_duty_does_not_come_back(client):
    login(client, "u-sabbir")
    duty = by_title(reply(client).json())["Quarter-end loan review"]
    assert client.patch(f"/api/cases/case-2/duties/{duty['id']}", json={"decision": "dismiss"}).status_code == 200
    again = by_title(reply(client).json())["Quarter-end loan review"]
    assert again["confirmation"] == "dismissed" and again["id"] == duty["id"]


# ---------------------------------------------------------------- who may use it

def test_only_the_employee_of_the_case_can_answer(client):
    assert reply(client).status_code == 401  # signed out
    for user_id in ("u-shirin", "u-farhana", "u-tania", "u-nusrat"):  # manager, HR, colleague, another employee
        login(client, user_id)
        r = reply(client)
        assert r.status_code == 403, user_id
        assert r.json()["code"] == "forbidden"


def test_unknown_case_is_404(client):
    login(client, "u-sabbir")
    assert reply(client, case_id="case-999").json()["code"] == "case_not_found"


# ---------------------------------------------------------------- bad input and a failing AI

def test_an_empty_or_malformed_body_is_422(client):
    login(client, "u-sabbir")
    assert reply(client, turns=[]).status_code == 422
    r = client.post("/api/cases/case-2/interview/reply", json={"turns": [{"role": "robot", "text": "hi"}]})
    assert r.status_code == 422 and r.json()["code"] == "invalid_request"


def test_a_conversation_with_no_employee_reply_yet_is_422(client):
    login(client, "u-sabbir")
    r = reply(client, turns=[{"role": "assistant", "text": "Apnar sprotahik kaj ki ki?"}])
    assert r.status_code == 422 and r.json()["code"] == "bad_input"


def test_an_interview_the_replay_does_not_know_fails_loudly_and_saves_nothing(client):
    login(client, "u-sabbir")
    r = reply(client, turns=[{"role": "employee", "text": "Something the recording has never seen"}])
    assert r.status_code == 502 and r.json()["code"] == "replay_no_match"
    assert len(client.get("/api/cases/case-2").json()["duties"]) == 0  # nothing invented


@pytest.mark.parametrize("code, status", [("invalid_reply", 502), ("unknown_source_line", 502), ("live_not_configured", 503)])
def test_gateway_failures_become_clean_errors_without_raw_model_text(client, monkeypatch, code, status):
    def failing(turns, jd):
        raise GatewayError(code, "Our own sentence.")

    monkeypatch.setattr(gateway, "extract_duties", failing)
    login(client, "u-sabbir")
    r = reply(client)
    assert r.status_code == status
    assert r.json() == {"code": code, "detail": "Our own sentence."}


def test_the_raw_interview_is_never_stored(client):
    # The employee message holds the quote AND other words. Only the verified quote may be saved,
    # inside its duty; the rest of the message, and the assistant's questions, must not be in the database.
    extra = "ar ami ekta onno kotha bolchi 99999"
    turns = [
        {"role": "assistant", "text": "Apnar sprotahik kaj ki ki?"},
        {"role": "employee", "text": f"{QUOTE} {extra}"},
    ]
    login(client, "u-sabbir")
    assert reply(client, turns=turns).status_code == 200
    with db_module.SessionLocal() as session:
        from app.models import Base

        stored = " ".join(str(value) for table in Base.metadata.sorted_tables for row in session.execute(table.select()).all() for value in row)
    assert QUOTE in stored  # the verified quote is kept, as part of its duty
    assert extra not in stored and "sprotahik" not in stored


# ---------------------------------------------------------------- the employee decides, and it is audited

def _audit(case_id="case-2"):
    with db_module.SessionLocal() as session:
        return session.scalars(select(AuditEvent).where(AuditEvent.case_id == case_id).order_by(AuditEvent.id)).all()


def test_confirming_a_duty_changes_it_and_writes_one_audit_event(client):
    login(client, "u-sabbir")
    duty = by_title(reply(client).json())["Quarter-end loan review"]
    r = client.patch(f"/api/cases/case-2/duties/{duty['id']}", json={"decision": "confirm"})
    assert r.status_code == 200 and r.json()["confirmation"] == "confirmed"
    events = _audit()
    assert len(events) == 1
    assert (events[0].actor_id, events[0].action, events[0].duty_id) == ("u-sabbir", "duty_confirmed", duty["id"])
    assert events[0].at is not None
    # R2: now the former question counts as a fact.
    assert reply(client).json()["fact_count"] == 3


def test_a_person_can_change_their_mind_and_each_change_is_audited(client):
    login(client, "u-sabbir")
    duty = by_title(reply(client).json())["Credit pre-meeting"]
    client.patch(f"/api/cases/case-2/duties/{duty['id']}", json={"decision": "confirm"})
    client.patch(f"/api/cases/case-2/duties/{duty['id']}", json={"decision": "dismiss"})
    assert [e.action for e in _audit()] == ["duty_confirmed", "duty_dismissed"]


def test_only_the_employee_can_decide_and_only_about_a_duty_of_that_case(client):
    login(client, "u-sabbir")
    duty = by_title(reply(client).json())["Credit pre-meeting"]
    for user_id in ("u-shirin", "u-farhana", "u-tania", "u-nusrat"):
        login(client, user_id)
        assert client.patch(f"/api/cases/case-2/duties/{duty['id']}", json={"decision": "confirm"}).status_code == 403
    login(client, "u-sabbir")
    assert client.patch("/api/cases/case-2/duties/duty-nope", json={"decision": "confirm"}).json()["code"] == "duty_not_found"
    # A duty that belongs to another case is "not found" here, not readable through this case.
    assert client.patch("/api/cases/case-2/duties/duty-1", json={"decision": "confirm"}).status_code == 404
    assert client.patch(f"/api/cases/case-2/duties/{duty['id']}", json={"decision": "approve"}).status_code == 422
    assert _audit() == []  # none of the refused attempts left an event
