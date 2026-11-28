# T9: Selenium end-to-end browser test suite

- Author: Nazha Tarannum Roza
- Branch: `feature/selenium-e2e`
- Date: 2026-11-28

## What I did
Added `e2e/` (`e2e/conftest.py`, `e2e/test_user_flows.py`, `e2e/requirements.txt`, `e2e/README.md`) to run automated Selenium browser tests against the real React/Vite frontend and FastAPI backend.

## Why
Backend unit tests check API routes in isolation, and frontend builds check TypeScript types, but neither verifies full-stack browser navigation, session cookies through the Vite proxy, or server-enforced 403 screens rendered in a real browser.

## How it works
`e2e/conftest.py` seeds a throwaway SQLite database via `python -m app.seed`, launches Uvicorn on `127.0.0.1:8000` and Vite on `localhost:5173`, waits for `/healthz`, provides a fresh headless Chrome WebDriver per test, and stops both servers when finished. `e2e/test_user_flows.py` uses Tonni's `data-testid` attributes to verify employee sign-in and Role Map duties (`u-nusrat`), cover colleague empty list plus 403 forbidden screen on `/cases/case-1` (`u-tania`), and HR case list plus sign-out redirect (`u-farhana`). No AI calls are made.

## How I tested it
Ran `python -m pytest e2e -v` (3 passed in 5.72s) and `python -m pytest -q` (80 passed).

## Not finished / known problems
Covers T1/T2 flows (sign-in, case list, Role Map view, 403 check, sign-out). Interview submission and duty confirm/dismiss E2E flows will be added once the T6 frontend interview screen lands.

## AI assistance
Used Gemini to scaffold `e2e/conftest.py` and `e2e/test_user_flows.py`; verified the selectors against `frontend/src/pages/*.tsx`, debugged the immediate demo sign-in redirect, and ran both pytest suites locally.
