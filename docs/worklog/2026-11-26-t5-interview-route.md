# T5: The interview route

- Author: Maruf
- Branch: `feature/t5-interview-route`
- Date: 2026-11-26

## What I did
Built the MAP interview in the backend: `POST /api/cases/{id}/interview/reply` (the employee answers, the AI proposes duties, the rules check them) and `PATCH /api/cases/{id}/duties/{duty_id}` (the employee confirms or dismisses; one audit event each). Added two tables (`job_description_lines`, `audit_events`), a short synthetic job description for each case, new request and response shapes, and 20 tests.

## Why
This is where the three parts meet and the product idea becomes real: the AI proposes (Mahadi's gateway), the rules check (Nazha's R1 and R2), and the employee decides. It is the heart of the 10 to 15% presentation.

## How it works
See `docs/CODE-EXPLANATION.md`, "The interview route". Short version: only the case's employee may call it; the route loads the job description lines, calls the gateway, runs R1 on every "said" duty (a failed quote is downgraded to "suggested"), saves new duties as "pending" without duplicating or overwriting, never stores the raw interview, and reports `fact_count` using R2. Gateway errors become 422, 502 or 503 with our own sentence.

## How I tested it
- `python -m pytest -q`: 80 passed (60 before, 20 new).
- Proved the tests catch real bugs: I removed R1, the employee check, the audit event and the de-duplication one at a time, and each made tests fail. Then restored the code.
- Called the real server over HTTP as `u-sabbir`: reply 200 with `mode: replay`, three duties (said, documented with `jd-3`, suggested), `fact_count` 2; after confirming the question, `fact_count` 3; the manager got 403.

## Interface changes (contract)
The reply carries `mode`, `downgraded` and `fact_count`; error codes are mapped; the confirm route returns the updated Duty and a 404 `duty_not_found`. Logged for Tonni (T6), Mahadi and Nazha on the team board.

## Found while checking before the push
- An older local `shetu.db` has no job description lines, so the interview route answers `502 unknown_source_line` until `python -m app.seed` is run again (it only adds what is missing). Tested both ways; documented in `backend/README.md` and in the board handoff for Tonni.
- Ran the tests the way CI does, in a fresh environment installed only from `backend/requirements-dev.txt`: 80 passed from the repo root, 78 from `backend/`.

## Not finished / known problems
- Replay only: one recorded answer; no live model until the provider is chosen.
- No retry on a bad AI answer yet (the gateway's TODO).
- The manager still sees every duty.
- `CODE-EXPLANATION.md` and the rest are updated in this pull request.
- No stubs: T3 and T4 are the real merged code.
