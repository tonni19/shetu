# T1: Backend skeleton

- Author: Maruf
- Branch: `feature/t1-backend-skeleton`
- Date: 2026-11-23

## What I did
Created `backend/`: a FastAPI app with SQLite that seeds synthetic people and two leave cases, lets them sign in with a signed session cookie, and returns a case only to the people allowed to see it. Added a health check, one error format for every error, 16 tests, a README and the first section of `docs/CODE-EXPLANATION.md`.

## Why
Every other part (Tonni's screens, Mahadi's gateway, Nazha's rules, the interview route) needs a running API, a database and a permission check to plug into. This is the foundation for the 26 November presentation.

## How it works
`app/main.py` builds the app. A request carries the session cookie; `app/security.py` reads the signed-in user from it and decides access with `can_read_case` (employee, manager, HR; colleagues get 403). Routes return SQLAlchemy objects, which FastAPI converts to JSON through the Pydantic shapes in `app/schemas.py`. No AI is involved yet. Full walk-through: `docs/CODE-EXPLANATION.md`.

## How I tested it
- `python -m pytest -q`: 16 passed (health; sign-in, sign-out, who-am-I; the same error for a wrong id and a wrong password; the error shape for a bad body; passwords stored only as salted hashes; employee, manager and HR can read; a colleague and another employee get 403; signed out gets 401; unknown case gets 404; no reason field; evidence and confirmation kept separate).
- Started the real server and called it over HTTP: health 200, case while signed out 401, as a colleague 403, as the employee 200.

## Interface changes (contract)
Added `POST /api/logout` and `GET /api/me`, and named the error codes (`not_signed_in`, `invalid_credentials`, `forbidden`, `case_not_found`, `invalid_request`). Logged for Tonni on the team board.

## Not finished / known problems
- Cover colleagues cannot read any case until cover assignments exist.
- The manager sees all duties; after the interview exists, the manager should see confirmed duties only (T5).
- No migration tool; changing a table means deleting `shetu.db` and re-seeding.
- The test client prints a deprecation warning from Starlette about `httpx`; harmless for now.
- CI (running these tests on every pull request) is Nazha's T4.
- No stubs in this change.
