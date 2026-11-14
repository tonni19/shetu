# Project State

The current picture of the project. Keep it short: this is "where are we now", not history. History lives in `docs/worklog/` and in GitHub's pull request list.

**Update this file whenever the state of the project changes, not only when code changes.** The triggers and the routine are in `AGENTS.md`, section "Keep the project state current". If this file looks old, assume it is wrong and check GitHub.

Last updated: 2026-11-14 (evening), after the deck wording fixes and pull requests #8 to #12. Still no application code.

## Milestones

| Checkpoint | Goal | Status |
|---|---|---|
| Proposal, 15 Nov 2026 | Pitch | Slides (10, wording fixes 1 to 5 applied on 14 Nov) and the Excel draft are ready in `docs/planning/`. The instructor replied to our feedback request: the idea is approved to proceed, and some questions may come after the presentation. The elevator pitch is being rewritten by a teammate; until it is ready the current text stands (workbook cell E3, pitch pack section 2). Not recorded here: whether the Excel sheet has been entered in the faculty's Google Sheet |
| Update 1 (30%) | MAP works: interview, Role Map, a forgotten duty found | Not started |
| Update 2 (60%) | HOLD works: a change typed in plain words is understood and re-planned | Not started |
| Final (100%) | All three stages, tests green, AI measured | Not started |

## What works now

No application code yet. The full plan, slides and Excel draft are in `docs/planning/`. An interactive learning guide for the whole team is in `docs/learn/index.html` (open it in a browser; it works offline).

## In progress

| Issue | What | Who | Branch |
|---|---|---|---|
| | Deck wording fixes 1 to 5 and this refresh. Pull request waiting for a teammate's review | Ahmad Maruf Hossain | `feature/deck-fixes-and-state` |
| | A new elevator pitch. Nothing in the repository yet | A teammate (name not recorded here) | |

## Next up

1. Proposal presentation on 15 November (slides: `docs/planning/05-Shetu-Proposal-Deck.pptx`). Decide who presents which slides (suggestion in `docs/planning/03-Pitch-Preparation-Pack.md`, section 7.2). Optional deck polish, items 6 to 9 in `docs/planning/06-Slide-Deck-Change-Proposals.md`, is undecided.
2. When the new elevator pitch is ready, update the workbook cell E3, the pitch pack (section 2) and the notes of slide 3 together.
3. Agree the work division. A proposal exists (not agreed): each member owns a layer and one feature end to end: A frontend + MAP, B backend + ownership and approvals, C AI + HOLD re-planning, D testing + FIT. Needs each member's skills and free time. See `docs/planning/01-Investigation-Report.md`, section 25.2.
4. Step 1 of the roadmap (`docs/planning/00-Overview.md`, section 7): create the empty FastAPI + React + SQLite app with login; CI; the AI gateway.
5. First six fake test cases, then test the AI models and choose one.
6. When `tonni19`'s GitHub Pro is active: turn on branch protection for `main`, and publish the learning guide with GitHub Pages using a workflow that publishes only `docs/learn` (never the whole `docs/` folder, which holds course PDFs). The workflow must be pushed from an account whose login has the `workflow` permission (`SpicyFalcon619` or `NazhaTarannum`; not `tonni19`).
7. Stretch, in order: hourglass chart, then voice input (first stretch feature, after HOLD works).

## Known problems and open questions

- Hosted AI provider not chosen (decided by the bake-off).
- Dates of Update 1 and Update 2 not known.
- **`main` cannot be protected yet.** GitHub branch protection on a private repository needs the *owner's* account to have GitHub Pro. The repository is owned by `tonni19`, whose Pro is not active yet (checked 14 November). Her student application was approved on 12 November 2026, and GitHub says the benefits become available 72 hours after approval (about 15 November). She should claim GitHub Pro from `github.com/education` once it appears, and must **not** pay on the upgrade page. `SpicyFalcon619` has Pro, but that does not cover a repository owned by another account. Until `tonni19`'s Pro is active, the rule "no direct pushes to `main`, every change through a reviewed pull request" is kept by agreement. Moving the repository to another account is not planned.
- Member roles are not assigned yet. Waiting for each member's skills and availability.
- Hosted AI provider, and who holds the API key, not decided.
- Task tracking: GitHub Issues with a Projects board is proposed instead of Jira. Not decided.
- No review is recorded on pull requests #4 to #12. They were merged by a teammate or from Ahmad's computer without a written review.

## Team and access

All four members are collaborators on `tonni19/shetu`: `tonni19` (admin, repository owner), `SpicyFalcon619`, `NazhaTarannum` and `HasanGMS0047` (write). Anyone with write access can review and merge a pull request, but **not their own**, and must use **their own GitHub account** so the history shows who reviewed what. Merge type: **merge commit**, not squash, so each member's own commits stay visible.

Three of the accounts (`SpicyFalcon619`, `tonni19`, `NazhaTarannum`) are signed in on Ahmad's computer. At the team's request, some pull requests were pushed or merged from it under one of them. The worklog notes and the table below say which. Commits are authored under the name of the person who wrote them.

## Merged so far

This list lags by one: the pull request that updates this file cannot list itself, so the next update records it.

| PR | What | Author | Merged by |
|---|---|---|---|
| #2 | Removed an out-of-date line from this file (Issue #1) | HasanGMS0047 | SpicyFalcon619 (approved and merged) |
| #4 | Project state, decisions 14 and 15, worklog (Issue #3) | SpicyFalcon619 | tonni19. No review recorded |
| #6 | Voice input is a stretch feature everywhere; slides rebuilt; decision 16 (Issue #5) | SpicyFalcon619 | tonni19. No review recorded |
| #8 | Refreshed this file and added the rule that keeps it current; decision 17 (Issue #7) | tonni19 (commits by Ahmad Maruf Hossain) | SpicyFalcon619. No review recorded |
| #9 | Recorded that the instructor email was sent | SpicyFalcon619 | tonni19. No review recorded |
| #10 | Interactive learning guide; decision 18 | tonni19 (commits by Ahmad Maruf Hossain) | SpicyFalcon619. No review recorded |
| #12 | Workbook tidied, shorter elevator pitch, deck change proposals (Issue #11) | HasanGMS0047 | NazhaTarannum. No review recorded |

## Things every assistant should know right now

- No code exists yet. Do not assume any file or function is there; check.
- Voice input is a **stretch** feature (decision 16), not cut and not in the first version.
- The deck wording fixes 1 to 5 are applied (decision 19). The bank statistic is a net fall in the count, never "women who left".
- Do not push, pull, merge or open issues or pull requests unless the member asks, and ask which GitHub account to use each time.
