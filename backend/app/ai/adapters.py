# FILE:        backend/app/ai/adapters.py
# PURPOSE:     The "model adapter" interface, and the replay adapter that serves recorded replies.
# OWNER:       Mahadi (board row T3)
# DEPENDS ON:  backend/app/ai/schemas.py (GatewayError); fixtures in backend/app/ai/fixtures/replay/.
# USED BY:     backend/app/ai/gateway.py, backend/tests/test_gateway.py
# STATUS:      PARTIAL: the replay adapter is real. There is NO live adapter yet, because the hosted
#              provider has not been chosen (docs/PROJECT-STATE.md, "Known problems").
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     An adapter only turns a prompt into raw text. It does no validation. Validation happens in
#              gateway.py, so every adapter, replay or live, is held to the same checks.
# TODO(Mahadi, T3): add a hosted adapter here once the provider is chosen by the bake-off. It must set
#              mode = "live" and must be the only file that imports a provider SDK.

import json
from pathlib import Path
from typing import Literal, Protocol

from backend.app.ai.schemas import GatewayError

DEFAULT_REPLAY_FIXTURE = (
    Path(__file__).parent / "fixtures" / "replay" / "banglish_credit_pre_meeting.json"
)


class ModelAdapter(Protocol):
    """Anything that can answer a prompt with raw text. The gateway works with any of them."""

    # "replay" means a recorded reply; "live" means a real provider was called. The gateway copies this
    # into ExtractResult.mode, so a replay run can never be shown as live.
    mode: Literal["replay", "live"]

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Return the model's raw text reply, or raise GatewayError if it cannot answer."""
        ...


class ReplayAdapter:
    """Serves recorded replies from a JSON fixture, so tests and offline demos are repeatable.

    Why it exists: real models give different answers each time and need a key and a network.
    A recorded reply makes a test or a demo give the same answer every run, and it is always labelled
    as a replay (mode = "replay"), never as live.

    Fixture format: {"label": "...", "entries": [{"match": "<text>", "reply": {...}}]}. The first entry
    whose "match" text appears in the user prompt is used.
    """

    mode: Literal["replay", "live"] = "replay"

    def __init__(self, fixture_path: Path = DEFAULT_REPLAY_FIXTURE) -> None:
        self._fixture_path = fixture_path

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Return the recorded reply whose "match" text is in `user_prompt`, as JSON text.

        Raises GatewayError("replay_unavailable") if the fixture cannot be read, and
        GatewayError("replay_no_match") if no recorded reply fits. It never invents a reply: an
        unknown question must fail loudly, not pass with made-up data.
        """
        try:
            fixture = json.loads(self._fixture_path.read_text(encoding="utf-8"))
            entries = fixture["entries"]
        except (OSError, ValueError, KeyError) as error:
            raise GatewayError(
                "replay_unavailable", "The recorded replies could not be read."
            ) from error

        for entry in entries:
            if entry["match"] in user_prompt:
                return json.dumps(entry["reply"], ensure_ascii=False)

        raise GatewayError(
            "replay_no_match", "No recorded reply fits this interview, so the replay cannot answer."
        )
