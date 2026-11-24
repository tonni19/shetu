# FILE:        backend/tests/test_gateway.py
# PURPOSE:     Tests for the AI gateway: the replay path, and every way a model reply can be rejected.
# OWNER:       Mahadi (board row T3)
# DEPENDS ON:  backend/app/ai/ (gateway, adapters, schemas, prompts, the replay fixture)
# USED BY:     CI and local pytest runs
# STATUS:      REAL
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     No test here calls a real model. Tests that need a particular reply use FakeAdapter, a plain
#              test double. It is not a STUB(T#): it stands in for nothing on the board.
# AI NOTE:     The quote test uses Nazha's real `check_quote` (rule R1, backend/app/rules/evidence.py). The
#              gateway itself never calls it; the route (Maruf, T5) does. The test only proves that our
#              recorded reply would pass R1.

import json
import re
from pathlib import Path

import pytest

from backend.app.ai.adapters import DEFAULT_REPLAY_FIXTURE, ReplayAdapter
from backend.app.ai.gateway import MODE_ENV_VAR, extract_duties, get_adapter
from backend.app.ai.prompts import SYSTEM_PROMPT, build_prompts
from backend.app.ai.schemas import GatewayError, JdLine, Turn
from backend.app.rules.evidence import check_quote

# The synthetic Banglish answer the replay fixture was written for (also used on slide 4 of the proposal).
BANGLISH_ANSWER = (
    "Protiti Tuesday sondha 6 ta theke 7:30 porjonto credit pre-meeting hoy, "
    "oikhane ami amar clients er loan proposals present kori."
)

JD_LINES = [
    JdLine(id="jd-1", text="Manage a portfolio of corporate clients"),
    JdLine(id="jd-2", text="Present loan proposals every week"),
    JdLine(id="jd-3", text="Submit the monthly portfolio report"),
]

TURNS = [
    Turn(role="assistant", text="Apnar kajer kotha bolun."),
    Turn(role="employee", text=BANGLISH_ANSWER),
]


class FakeAdapter:
    """Test double: returns a fixed raw reply. `mode` can be set to check where the label comes from."""

    def __init__(self, raw_reply: str, mode: str = "replay") -> None:
        self.raw_reply = raw_reply
        self.mode = mode

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        return self.raw_reply


def reply_json(**overrides) -> str:
    """A valid model reply with one 'said' duty; tests change one thing at a time."""
    reply = {
        "next_question": "Ar kono kaj ache?",
        "duties": [
            {
                "title": "Credit pre-meeting",
                "evidence_type": "said",
                "quote": "credit pre-meeting hoy",
                "source_line_id": None,
            }
        ],
    }
    reply.update(overrides)
    return json.dumps(reply)


# ---------- the replay path ----------


def test_replay_returns_three_duties_labelled_replay():
    result = extract_duties(TURNS, JD_LINES)
    assert result.mode == "replay"
    assert [d.evidence_type for d in result.duties] == ["said", "documented", "suggested"]
    assert result.next_question


def test_said_duty_quote_is_inside_the_employee_words():
    result = extract_duties(TURNS, JD_LINES)
    said = [d for d in result.duties if d.evidence_type == "said"]
    assert said, "the fixture should contain a 'said' duty"
    for duty in said:
        assert check_quote(duty.quote, [BANGLISH_ANSWER])


def test_documented_duty_points_at_a_real_line_and_suggested_carries_no_evidence():
    result = extract_duties(TURNS, JD_LINES)
    known = {line.id for line in JD_LINES}
    for duty in result.duties:
        if duty.evidence_type == "documented":
            assert duty.source_line_id in known and duty.quote is None
        if duty.evidence_type == "suggested":
            assert duty.quote is None and duty.source_line_id is None


def test_replay_with_an_unknown_answer_fails_instead_of_inventing_one():
    turns = [Turn(role="employee", text="Ami onno kichu kori.")]
    with pytest.raises(GatewayError) as caught:
        extract_duties(turns, JD_LINES)
    assert caught.value.code == "replay_no_match"


def test_replay_with_a_missing_fixture_file_is_reported():
    adapter = ReplayAdapter(Path("does-not-exist.json"))
    with pytest.raises(GatewayError) as caught:
        extract_duties(TURNS, JD_LINES, adapter=adapter)
    assert caught.value.code == "replay_unavailable"


# ---------- replies the gateway must reject ----------


def test_reply_that_is_not_json_is_rejected():
    with pytest.raises(GatewayError) as caught:
        extract_duties(TURNS, JD_LINES, adapter=FakeAdapter("Sure! Here are the duties..."))
    assert caught.value.code == "invalid_reply"


def test_json_wrapped_in_a_code_fence_is_accepted():
    fenced = "```json\n" + reply_json() + "\n```"
    result = extract_duties(TURNS, JD_LINES, adapter=FakeAdapter(fenced))
    assert len(result.duties) == 1


def test_extra_reason_field_is_rejected():
    # Rule 5: there is no reason field. A reply that adds one must be thrown away.
    reply = json.loads(reply_json())
    reply["duties"][0]["reason"] = "personal"
    with pytest.raises(GatewayError) as caught:
        extract_duties(TURNS, JD_LINES, adapter=FakeAdapter(json.dumps(reply)))
    assert caught.value.code == "invalid_reply"


def test_said_duty_without_a_quote_is_rejected():
    duty = {"title": "X", "evidence_type": "said", "quote": None, "source_line_id": None}
    with pytest.raises(GatewayError) as caught:
        extract_duties(TURNS, JD_LINES, adapter=FakeAdapter(reply_json(duties=[duty])))
    assert caught.value.code == "invalid_reply"


def test_suggested_duty_with_a_quote_is_rejected():
    # A suggestion must never look like the employee's own words.
    duty = {"title": "X", "evidence_type": "suggested", "quote": "made up", "source_line_id": None}
    with pytest.raises(GatewayError) as caught:
        extract_duties(TURNS, JD_LINES, adapter=FakeAdapter(reply_json(duties=[duty])))
    assert caught.value.code == "invalid_reply"


def test_model_cannot_set_its_own_mode():
    reply = json.loads(reply_json())
    reply["mode"] = "live"
    with pytest.raises(GatewayError) as caught:
        extract_duties(TURNS, JD_LINES, adapter=FakeAdapter(json.dumps(reply)))
    assert caught.value.code == "invalid_reply"


def test_documented_duty_citing_an_unknown_line_is_rejected():
    duty = {"title": "X", "evidence_type": "documented", "quote": None, "source_line_id": "jd-99"}
    with pytest.raises(GatewayError) as caught:
        extract_duties(TURNS, JD_LINES, adapter=FakeAdapter(reply_json(duties=[duty])))
    assert caught.value.code == "unknown_source_line"


def test_error_message_never_contains_the_raw_reply():
    with pytest.raises(GatewayError) as caught:
        extract_duties(TURNS, JD_LINES, adapter=FakeAdapter("SECRET-RAW-TEXT"))
    assert "SECRET-RAW-TEXT" not in caught.value.detail


# ---------- input, labels and mode ----------


def test_interview_with_no_employee_turn_is_bad_input():
    turns = [Turn(role="assistant", text="Apnar kajer kotha bolun.")]
    with pytest.raises(GatewayError) as caught:
        extract_duties(turns, JD_LINES)
    assert caught.value.code == "bad_input"


def test_mode_label_comes_from_the_adapter():
    result = extract_duties(TURNS, JD_LINES, adapter=FakeAdapter(reply_json(), mode="live"))
    assert result.mode == "live"


def test_live_mode_is_refused_until_a_provider_exists(monkeypatch):
    monkeypatch.setenv(MODE_ENV_VAR, "live")
    with pytest.raises(GatewayError) as caught:
        get_adapter()
    assert caught.value.code == "live_not_configured"


def test_unknown_mode_is_refused(monkeypatch):
    monkeypatch.setenv(MODE_ENV_VAR, "turbo")
    with pytest.raises(GatewayError) as caught:
        get_adapter()
    assert caught.value.code == "bad_mode"


def test_replay_is_the_default_mode(monkeypatch):
    monkeypatch.delenv(MODE_ENV_VAR, raising=False)
    assert get_adapter().mode == "replay"


# ---------- prompt and fixture hygiene ----------


def test_user_prompt_lists_job_description_ids_and_both_speakers():
    _, user_prompt = build_prompts(TURNS, JD_LINES)
    assert "[jd-3] Submit the monthly portfolio report" in user_prompt
    assert "assistant: Apnar kajer kotha bolun." in user_prompt
    assert f"employee: {BANGLISH_ANSWER}" in user_prompt


def test_prompt_and_fixture_use_neutral_wording():
    # AGENTS.md rule 11: no gendered pronouns in prompts, fixtures or messages.
    gendered = re.compile(r"\b(she|her|hers|he|him|his)\b", re.IGNORECASE)
    texts = [SYSTEM_PROMPT, DEFAULT_REPLAY_FIXTURE.read_text(encoding="utf-8")]
    for text in texts:
        assert not gendered.search(text)


def test_fixture_has_no_reason_field():
    # Rule 5, checked on the recorded data itself.
    assert '"reason"' not in DEFAULT_REPLAY_FIXTURE.read_text(encoding="utf-8")
