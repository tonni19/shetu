# Code explanation

One section per module, written so a member can explain and change it in front of an instructor, and so the next person's AI assistant can find its way around. When you add or change a module, change its section in the same pull request. Add your section at the end; do not reorder other people's sections.

---

## AI gateway (Mahadi, board row T3)

**Files:** `backend/app/ai/gateway.py`, `adapters.py`, `prompts.py`, `schemas.py`, the fixture `backend/app/ai/fixtures/replay/banglish_credit_pre_meeting.json`, and tests in `backend/tests/test_gateway.py`.

**What it does.** The interview route gives it the conversation so far and the numbered job description lines. It returns draft duties for the employee's Role Map, each with its evidence, and one follow-up question. It is the only door to an AI model (rule 10).

**How data flows.**
1. `extract_duties(turns, job_description_lines)` checks there is at least one employee turn.
2. `get_adapter()` picks the adapter from the environment variable `SHETU_AI_MODE`. The default is `replay`. `live` is refused for now, because no provider is chosen.
3. `build_prompts` makes the system prompt (fixed rules for the model) and the user prompt (the job description lines, then the interview).
4. The adapter returns raw text. The replay adapter reads it from the JSON fixture, matching on a phrase from the employee's answer.
5. `_parse_reply` turns the text into JSON and validates it against `ModelReply`. Anything that is not exactly the asked-for shape is thrown away as `invalid_reply`.
6. The gateway checks that every `documented` duty points at a line id that was really given.
7. It returns an `ExtractResult` whose `mode` comes from the adapter, never from the model.

**Which parts are AI and which are ordinary code.** Only the adapter's `complete` call is "AI" (and in replay mode it is a recorded reply). Everything else is plain Python: the prompt builder, the JSON parsing, the Pydantic validation, and the line-id check.

**Rules it protects.**
- Rule 1: a `said` duty must carry a quote, a `documented` duty a source line, a `suggested` duty neither.
- Rule 5: replies with any extra field, such as "reason", are rejected.
- Rule 10: replies are validated before anyone sees them. Error messages never repeat the raw reply.
- Rule 11: prompts and fixtures use neutral wording; a test checks it.

**What it does not do.** It does not check that a quote is really in the employee's words. That is rule R1 (`check_quote`, Nazha, `backend/app/rules/evidence.py`), which the route calls. It does not store anything, and it does not decide whether a duty counts: a person confirms each one.

**Not real yet.** There is no live adapter (provider not chosen), so every run is a labelled replay. The fixture has one recorded reply, for one Banglish answer.

**Questions an instructor might ask.**
- *Why a replay adapter?* Real models answer differently each time and need a key and a network. A recorded reply makes tests and offline demos repeatable, and it is labelled as a replay so it is never passed off as live.
- *What stops the AI inventing a quote?* The gateway rejects a `said` duty with no quote. The route then runs rule R1, which checks that the quote really appears in what the employee typed.
- *What if the model returns rubbish?* The gateway raises `GatewayError("invalid_reply")` and nothing from the reply is kept.
- *How would you add a real model?* Write one more adapter in `adapters.py` that sets `mode = "live"`. Nothing else changes, because validation is in the gateway.
