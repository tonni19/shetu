# FILE:        backend/app/ai/gateway.py
# PURPOSE:     The one door to the AI model: ask for draft duties, get back a validated result or an error.
# OWNER:       Mahadi (board row T3)
# DEPENDS ON:  docs/API-CONTRACT.md (section 3, extract_duties); backend/app/ai/prompts.py,
#              backend/app/ai/adapters.py, backend/app/ai/schemas.py.
# USED BY:     backend/app/routes/interview.py (Maruf, T5, not merged yet); backend/tests/test_gateway.py
# STATUS:      PARTIAL: works in replay mode only. SHETU_AI_MODE=live raises GatewayError until a hosted
#              adapter exists (provider not chosen).
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     AGENTS.md rule 10: this is the only module the app calls to reach a model, and every reply
#              is validated against a Pydantic schema before anyone sees it. Raw model text is never
#              returned and never put in an error message.
# AI NOTE:     This module does NOT check that a quote really appears in the employee's words. That is
#              rule R1 (`check_quote`, Nazha, backend/app/rules/evidence.py), and the route (Maruf, T5)
#              calls it on each "said" duty. Do not copy that rule in here.

import json
import os

from app.ai.adapters import ModelAdapter, ReplayAdapter
from app.ai.prompts import build_prompts
from app.ai.schemas import ExtractResult, GatewayError, JdLine, ModelReply, Turn

# Environment variable that picks the adapter. Default is replay, so nothing calls a real model by accident.
MODE_ENV_VAR = "SHETU_AI_MODE"


def get_adapter() -> ModelAdapter:
    """Pick the adapter from SHETU_AI_MODE ("replay" by default).

    Raises GatewayError("live_not_configured") for "live" and GatewayError("bad_mode") for anything
    else. We refuse to quietly fall back to replay when live was asked for: that would let a recorded
    answer be shown as a live one.
    """
    mode = os.environ.get(MODE_ENV_VAR, "replay").strip().lower()
    if mode == "replay":
        return ReplayAdapter()
    if mode == "live":
        # TODO(Mahadi, T3): return the hosted adapter here once the provider is chosen.
        raise GatewayError("live_not_configured", "No live model is configured yet. Use replay mode.")
    raise GatewayError("bad_mode", f"{MODE_ENV_VAR} must be 'replay' or 'live'.")


def _strip_code_fence(raw: str) -> str:
    """Remove a surrounding ```json ... ``` fence, which models often add around JSON."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]  # drop the opening fence line, for example "```json"
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def _parse_reply(raw: str) -> ModelReply:
    """Turn raw model text into a validated ModelReply, or raise GatewayError("invalid_reply").

    Why: the model is not trusted. Anything that is not exactly the JSON shape we asked for (bad
    JSON, an extra field such as "reason", a "said" duty with no quote) is rejected. The error says
    what kind of problem it was but never repeats the raw text.
    """
    try:
        data = json.loads(_strip_code_fence(raw))
    except ValueError as error:
        raise GatewayError("invalid_reply", "The model's reply was not valid JSON.") from error
    try:
        return ModelReply.model_validate(data)
    except ValueError as error:
        raise GatewayError(
            "invalid_reply", "The model's reply did not match the required shape."
        ) from error


def extract_duties(
    turns: list[Turn],
    job_description_lines: list[JdLine],
    *,
    adapter: ModelAdapter | None = None,
) -> ExtractResult:
    """Ask the model (or the replay fixture) for draft duties and one follow-up question.

    CONTRACT: `extract_duties` in docs/API-CONTRACT.md, section 3. Always returns a validated
    ExtractResult or raises GatewayError. It never returns raw model text.

    Inputs:
        turns: the interview so far, oldest first. Must contain at least one `employee` turn.
        job_description_lines: numbered lines of the job description; may be empty.
        adapter: for tests only. Normally left out, and the adapter is picked from SHETU_AI_MODE.

    Returns:
        ExtractResult with `mode` ("replay" or "live", set by the adapter, never by the model),
        `next_question`, and the draft duties. Drafts only: the route sets confirmation="pending", and a
        person confirms or dismisses each one.

    Raises:
        GatewayError with one of these codes:
          bad_input             no employee turn to read
          bad_mode / live_not_configured / replay_unavailable / replay_no_match   adapter problems
          invalid_reply         the reply did not match the schema
          unknown_source_line   a "documented" duty cites a line id that was not in the input
    """
    if not any(turn.role == "employee" for turn in turns):
        raise GatewayError("bad_input", "There is no employee reply to read yet.")

    chosen_adapter = adapter if adapter is not None else get_adapter()
    system_prompt, user_prompt = build_prompts(turns, job_description_lines)
    raw_reply = chosen_adapter.complete(system_prompt, user_prompt)
    reply = _parse_reply(raw_reply)

    # A "documented" duty must point at a line we actually gave the model, or the evidence is invented.
    known_line_ids = {line.id for line in job_description_lines}
    for duty in reply.duties:
        if duty.evidence_type == "documented" and duty.source_line_id not in known_line_ids:
            raise GatewayError(
                "unknown_source_line", "A duty cites a job description line that does not exist."
            )

    return ExtractResult(
        mode=chosen_adapter.mode, next_question=reply.next_question, duties=reply.duties
    )
