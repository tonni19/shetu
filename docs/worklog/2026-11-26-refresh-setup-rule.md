# After you pull: refresh your local setup (rule)

- Author: Maruf
- Branch: `feature/refresh-setup-rule`
- Date: 2026-11-26

## What I did
Added a rule to `AGENTS.md` (start of every session): after pulling new code, run `pip install -r requirements-dev.txt` and `python -m app.seed` in `backend/`, `npm install` in `frontend/`, then the tests. Added a request row for everyone on the team board, and decision 33.

## Why
PR #32 added job description lines. An older local `shetu.db` does not have them, so the interview route answers `502 unknown_source_line` until the seed is run again. A written rule for the AI assistants means nobody has to remember. The same message was also posted as a comment on PR #32 with @mentions.

## How I tested it
Documentation only. The failure and the fix were tested in the #32 check: an old database gave 502, and after re-running the seed it gave 200.

## Not finished / known problems
- The rule only helps an AI that reads `AGENTS.md` at the start of a session.
- A migration tool would remove the need, but it is not in the agreed stack.
