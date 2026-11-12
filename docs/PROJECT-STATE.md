# Project State

The current picture of the project. **Update this in every pull request.** Keep it short: this is "where are we now", not history. History lives in `docs/worklog/`.

Last updated: 2026-11-12, repository set up with the planning documents (no code yet)

## Milestones

| Checkpoint | Goal | Status |
|---|---|---|
| Proposal, 15 Nov 2026 | Pitch | Preparing |
| Update 1 (30%) | MAP works: interview, Role Map, a forgotten duty found | Not started |
| Update 2 (60%) | HOLD works: a change typed in plain words is understood and re-planned | Not started |
| Final (100%) | All three stages, tests green, AI measured | Not started |

## What works now

No application code yet. The full plan, slides and Excel draft are in `docs/planning/`.

## In progress

| Issue | What | Who | Branch |
|---|---|---|---|
| | | | |

## Next up

1. Proposal presentation on 15 November (slides: `docs/planning/05-Shetu-Proposal-Deck.pptx`).
2. Step 1 of the roadmap (`docs/planning/00-Overview.md`, section 7): assign roles; create the empty FastAPI + React + SQLite app with login; CI; the AI gateway.
3. First six fake test cases, then test the AI models and choose one.

## Known problems and open questions

- Hosted AI provider not chosen (decided by the bake-off).
- Dates of Update 1 and Update 2 not known.
- **`main` cannot be protected:** GitHub branch protection needs a public repo or GitHub Pro. Until then, the rule "no direct pushes to `main`, every change through a reviewed pull request" is kept by agreement. Tonni can get GitHub Pro free through the GitHub Student Developer Pack, which would allow protection.
- Mohammad Mahadi Hasan (`HasanGMS0047`) has not yet accepted the collaborator invitation.
- Member roles are not assigned yet.

## Things every assistant should know right now

- No code exists yet. Do not assume any file or function is there; check.
