# Project State

The current picture of the project. **Update this in every pull request.** Keep it short: this is "where are we now", not history. History lives in `docs/worklog/`.

Last updated: 2026-11-12, after PR #2 was merged (still no code)

## Milestones

| Checkpoint | Goal | Status |
|---|---|---|
| Proposal, 15 Nov 2026 | Pitch | Slides and Excel draft ready in `docs/planning/`; team to review and rehearse |
| Update 1 (30%) | MAP works: interview, Role Map, a forgotten duty found | Not started |
| Update 2 (60%) | HOLD works: a change typed in plain words is understood and re-planned | Not started |
| Final (100%) | All three stages, tests green, AI measured | Not started |

## What works now

No application code yet. The full plan, slides and Excel draft are in `docs/planning/`.

## In progress

| Issue | What | Who | Branch |
|---|---|---|---|
| #3 | Update project state, decisions and worklog after PR #2 | Ahmad Maruf Hossain | `feature/3-update-project-state-after-pr2` (PR waiting for a teammate's review) |

## Next up

1. Proposal presentation on 15 November (slides: `docs/planning/05-Shetu-Proposal-Deck.pptx`). Decide who presents which slides (suggestion in `docs/planning/03-Pitch-Preparation-Pack.md`, section 7.2).
2. Step 1 of the roadmap (`docs/planning/00-Overview.md`, section 7): assign roles; create the empty FastAPI + React + SQLite app with login; CI; the AI gateway.
3. First six fake test cases, then test the AI models and choose one.
4. Stretch, in order: hourglass chart, then voice input (first stretch feature, after HOLD works).

## Known problems and open questions

- Hosted AI provider not chosen (decided by the bake-off).
- Dates of Update 1 and Update 2 not known.
- **`main` cannot be protected yet.** GitHub branch protection on a private repository needs the *owner's* account to have GitHub Pro. The repository is owned by `tonni19`, whose Pro (student pack) is not active yet. `SpicyFalcon619` has Pro, but that does not cover a repository owned by another account. Until this is fixed, the rule "no direct pushes to `main`, every change through a reviewed pull request" is kept by agreement. Options: (A) wait for tonni19's Pro, (B) transfer the repository to an account that has Pro, (C) keep working by agreement. The team has not decided on B.
- Member roles are not assigned yet. Waiting for each member's skills and availability.
- Hosted AI provider, and who holds the API key, not decided.

## Team and access

All four members are collaborators on `tonni19/shetu`: `tonni19` (admin, repository owner), `SpicyFalcon619`, `NazhaTarannum` and `HasanGMS0047` (write). Anyone with write access can review and merge a pull request, but **not their own**, and must use **their own GitHub account** so the history shows who reviewed what. Merge type: **merge commit**, not squash, so each member's own commits stay visible.

## Merged so far

| PR | What | Author | Reviewed and merged by |
|---|---|---|---|
| #2 | Removed an out-of-date line from this file (Issue #1) | HasanGMS0047 | SpicyFalcon619 |

## Things every assistant should know right now

- No code exists yet. Do not assume any file or function is there; check.
