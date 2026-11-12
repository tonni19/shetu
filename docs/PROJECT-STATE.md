# Project State

The current picture of the project. Keep it short: this is "where are we now", not history. History lives in `docs/worklog/` and in GitHub's pull request list.

**Update this file whenever the state of the project changes, not only when code changes.** The triggers and the routine are in `AGENTS.md`, section "Keep the project state current". If this file looks old, assume it is wrong and check GitHub.

Last updated: 2026-11-12 (evening), after PRs #4 and #6 were merged. Still no code.

## Milestones

| Checkpoint | Goal | Status |
|---|---|---|
| Proposal, 15 Nov 2026 | Pitch | Slides (10) and Excel draft ready in `docs/planning/`; team to review and rehearse. A feedback request for the instructor is prepared (one PDF, kept outside GitHub); whether it has been sent is not recorded here |
| Update 1 (30%) | MAP works: interview, Role Map, a forgotten duty found | Not started |
| Update 2 (60%) | HOLD works: a change typed in plain words is understood and re-planned | Not started |
| Final (100%) | All three stages, tests green, AI measured | Not started |

## What works now

No application code yet. The full plan, slides and Excel draft are in `docs/planning/`.

## In progress

| Issue | What | Who | Branch |
|---|---|---|---|
| 7 | Refresh this file and add the rule that keeps it current | Ahmad Maruf Hossain (pushed as tonni19) | `feature/7-refresh-project-state` |

## Next up

1. Proposal presentation on 15 November (slides: `docs/planning/05-Shetu-Proposal-Deck.pptx`). Decide who presents which slides (suggestion in `docs/planning/03-Pitch-Preparation-Pack.md`, section 7.2).
2. Agree the work division. A proposal exists (not agreed): each member owns a layer and one feature end to end: A frontend + MAP, B backend + ownership and approvals, C AI + HOLD re-planning, D testing + FIT. Needs each member's skills and free time. See `docs/planning/01-Investigation-Report.md`, section 25.2.
3. Step 1 of the roadmap (`docs/planning/00-Overview.md`, section 7): create the empty FastAPI + React + SQLite app with login; CI; the AI gateway.
4. First six fake test cases, then test the AI models and choose one.
5. Stretch, in order: hourglass chart, then voice input (first stretch feature, after HOLD works).

## Known problems and open questions

- Hosted AI provider not chosen (decided by the bake-off).
- Dates of Update 1 and Update 2 not known.
- **`main` cannot be protected yet.** GitHub branch protection on a private repository needs the *owner's* account to have GitHub Pro. The repository is owned by `tonni19`, whose Pro is not active yet. Her student application was approved on 12 November 2026, and GitHub says the benefits become available 72 hours after approval (about 15 November). She should claim GitHub Pro from `github.com/education` once it appears, and must **not** pay on the upgrade page. `SpicyFalcon619` has Pro, but that does not cover a repository owned by another account. Until `tonni19`'s Pro is active, the rule "no direct pushes to `main`, every change through a reviewed pull request" is kept by agreement. When Pro is active, turn protection on for `main` (require a pull request and one approving review). Moving the repository to another account is not planned.
- Member roles are not assigned yet. Waiting for each member's skills and availability.
- Hosted AI provider, and who holds the API key, not decided.
- Task tracking: GitHub Issues with a Projects board is proposed instead of Jira. Not decided.

## Team and access

All four members are collaborators on `tonni19/shetu`: `tonni19` (admin, repository owner), `SpicyFalcon619`, `NazhaTarannum` and `HasanGMS0047` (write). Anyone with write access can review and merge a pull request, but **not their own**, and must use **their own GitHub account** so the history shows who reviewed what. Merge type: **merge commit**, not squash, so each member's own commits stay visible.

## Merged so far

This list lags by one: the pull request that updates this file cannot list itself, so the next update records it.

| PR | What | Author | Reviewed and merged by |
|---|---|---|---|
| #2 | Removed an out-of-date line from this file (Issue #1) | HasanGMS0047 | SpicyFalcon619 (approved and merged) |
| #4 | Project state, decisions 14 and 15, worklog (Issue #3) | SpicyFalcon619 | Merged by tonni19. No review recorded |
| #6 | Voice input is a stretch feature everywhere; slides rebuilt; decision 16 (Issue #5) | SpicyFalcon619 | Merged by tonni19. No review recorded |

## Things every assistant should know right now

- No code exists yet. Do not assume any file or function is there; check.
- Voice input is a **stretch** feature (decision 16), not cut and not in the first version.
- Do not push, pull, merge or open issues or pull requests unless the member asks, and ask which GitHub account to use each time.
