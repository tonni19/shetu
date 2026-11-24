# Issue #22: T3, the AI gateway with a replay adapter

- Prepared by: Mohammad Mahadi Hasan, with an AI assistant
- Branch: `feature/22-ai-gateway-replay`
- Date: 2026-11-24

## What was done
Built the AI gateway (board row T3) in `backend/app/ai/`:
- `schemas.py`: the data shapes (Turn, JdLine, DraftDuty, ModelReply, ExtractResult) and `GatewayError`.
- `prompts.py`: the prompt that asks the model for draft duties, with its header comment.
- `adapters.py`: the adapter interface and the replay adapter.
- `gateway.py`: `extract_duties(turns, job_description_lines)`, which the interview route (Maruf, T5) will call.
- `fixtures/replay/banglish_credit_pre_meeting.json`: one recorded reply for one synthetic Banglish answer.
- `backend/tests/test_gateway.py`: 21 tests.

Also added the `ExtractResult` and `DraftDuty` shapes to `docs/API-CONTRACT.md` (section 3), the first section of `docs/CODE-EXPLANATION.md`, two handoff rows on the team board, and the T3 row update.

## Why
Maruf's route (T5) and Nazha's tests need `extract_duties` working before the 26 November progress presentation. The gateway is the only door to a model (rule 10), so every reply is validated here.

## How it works
The route gives `extract_duties` the interview turns and the job description lines. The prompt is built, the adapter returns raw text, the text is parsed as JSON and checked against the schema, and the gateway checks that every cited job description line really exists. The result carries `mode`, set by the adapter and never by the model, so a replay run is never shown as live. The full walkthrough is in `docs/CODE-EXPLANATION.md`.

Which parts are AI: only the adapter call. In replay mode that is a recorded reply, not a model. Everything else is plain Python.

## How it was tested
`python -m pytest backend/tests -v` passes locally: 21 tests, on Python 3.12. They cover the replay path, bad JSON, a code-fenced reply, an extra "reason" field, a `said` duty without a quote, a `suggested` duty with a quote, a model trying to set its own mode, an unknown source line, an error message that must not contain the raw reply, no employee turn, live mode refused, and neutral wording in the prompt and fixture. CI has not run these yet.

## Not finished / known problems
- **No live adapter.** The provider is not chosen. `SHETU_AI_MODE=live` raises `live_not_configured`. Every run is a labelled replay.
- **Depends on #21 for CI.** Nazha's pull request (#21) creates `backend/requirements-dev.txt`, `pytest.ini` and the CI workflow. CI installs only pytest, so these tests need `pydantic` added there. That one line is to be added after #21 is merged. Until then CI on this branch would fail on the missing package.
- The quote test uses a plain `in` check. After #21 is merged it should call Nazha's `check_quote`. Marked `TODO(Mahadi, T3)` in the test file.
- One fixture entry only: unknown answers fail with `replay_no_match`, on purpose.
- Tested on Python 3.12 locally; CI uses 3.13.
- Not yet read through line by line by the member, and not yet reviewed by another member.

## What the next person can rely on
- Maruf (T5): `extract_duties` returns an `ExtractResult` or raises `GatewayError`. Add `id`, `case_id` and `confirmation="pending"` to each DraftDuty to make a Duty, and call `check_quote` on each `said` duty.
- Nazha (T4, T7): the fixture shape can be reused for synthetic cases.

## Stubs
None. Nothing here stands in for another board row. The only unfinished piece is the live adapter, which is a TODO, not a stub.

## AI assistance
Claude Code wrote the code, tests and documents from the contract and the team rules. Mohammad Mahadi Hasan chose the task and the approach. Recorded in `AI-USAGE.md`.
