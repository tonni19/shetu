# Project State

The current picture of the project. Keep it short: this is "where are we now", not history. History lives in `docs/worklog/` and in GitHub's pull request list.

**Update this file whenever the state of the project changes, not only when code changes.** The triggers and the routine are in `AGENTS.md`, section "Keep the project state current". If this file looks old, assume it is wrong and check GitHub.

Last updated: 2026-11-16, after the proposal presentation, tonni19's GitHub Pro becoming active, and pull requests #2 to #15. Still no application code.

## Milestones

| Checkpoint | Goal | Status |
|---|---|---|
| Proposal, 15 Nov 2026 | Pitch | **Done.** Presented on 15 November; the deck (`05-Shetu-Proposal-Deck.pptx`) was submitted to the portal on 14 November. Feedback, asked in both places we presented: *why only for mothers, when anyone could use it? Where is the niche? Isn't it just a work planner?* The instructor also mentioned tokenization and vectorization (embeddings). Our answers are not agreed yet (see Next up). Not recorded here: whether the Excel sheet was entered in the faculty's Google Sheet |
| Update 1 (30%) | MAP works: interview, Role Map, a forgotten duty found | Not started |
| Update 2 (60%) | HOLD works: a change typed in plain words is understood and re-planned | Not started |
| Final (100%) | All three stages, tests green, AI measured | Not started |

## What works now

No application code yet. The full plan, slides and Excel draft are in `docs/planning/`. An interactive learning guide for the whole team is in `docs/learn/index.html` (open it in a browser; it works offline).

## In progress

| Issue | What | Who | Branch |
|---|---|---|---|
| | Nothing in progress. The next work starts after the proposal presentation | | |

## Next up

1. Answer the presentation feedback: agree how we explain the niche (why maternity first, how it differs from a work planner) and whether embeddings have a place in the design. Record the outcome in `docs/DECISIONS.md`.
2. Assign the roles: one primary owner per area, others may help. Record it in this file and in `CONTRIBUTIONS.md`.
3. Agree the work division. A proposal exists (not agreed): each member owns a layer and one feature end to end: A frontend + MAP, B backend + ownership and approvals, C AI + HOLD re-planning, D testing + FIT. Needs each member's skills and free time. See `docs/planning/01-Investigation-Report.md`, section 25.2.
4. Step 1 of the roadmap (`docs/planning/00-Overview.md`, section 7): create the empty FastAPI + React + SQLite app with login; CI; the AI gateway.
5. First six fake test cases, then test the AI models and choose one.
6. Done: `main` is protected and the learning guide is published (see Team and access).
7. Stretch, in order: hourglass chart, then voice input (first stretch feature, after HOLD works).

## Known problems and open questions

- Hosted AI provider not chosen (decided by the bake-off).
- Dates of Update 1 and Update 2 not known.
- The learning guide on GitHub Pages is **public** (anyone with the link), even though the repository is private. Only `docs/learn` is published. Never put names with student IDs, emails, keys or course PDFs in `docs/learn`.
- Member roles are not assigned yet. Waiting for each member's skills and availability.
- Hosted AI provider, and who holds the API key, not decided.
- Task tracking: GitHub Issues with a Projects board is proposed instead of Jira. Not decided.
- No review is recorded on pull requests #4 to #15 (merged before `main` was protected). From now on every pull request needs an approval from another member.

## Team and access

All four members are collaborators on `tonni19/shetu`: `tonni19` (admin, repository owner), `SpicyFalcon619`, `NazhaTarannum` and `HasanGMS0047` (write). Anyone with write access can review and merge a pull request, but **not their own**, and must use **their own GitHub account** so the history shows who reviewed what. Merge type: **merge commit**, not squash, so each member's own commits stay visible.

**`main` is protected** (since 16 November 2026, when `tonni19`'s GitHub Pro became active): no direct pushes, no force pushes, and every pull request needs **one approving review from a member who is not the author** before it can be merged. This also applies to the owner. **Learning guide online:** https://tonni19.github.io/shetu/ (published by `.github/workflows/learn-guide.yml` whenever `docs/learn` changes on `main`; the workflow publishes only that folder).

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
| #13 | Final elevator speech in the workbook, pitch pack and slide notes; speaker split; decisions 20 and 21 | NazhaTarannum (commits by Ahmad Maruf Hossain) | SpicyFalcon619. No review recorded |
| #14 | Speaker scripts for all ten slides (`docs/planning/07-Speaker-Scripts.md`); decision 22 | tonni19 (commits by Ahmad Maruf Hossain) | NazhaTarannum. No review recorded |
| #15 | Project state brought up to date after #14 | SpicyFalcon619 (commits by Ahmad Maruf Hossain) | tonni19. No review recorded |

## Things every assistant should know right now

- No code exists yet. Do not assume any file or function is there; check.
- Voice input is a **stretch** feature (decision 16), not cut and not in the first version.
- Speaker scripts exist for all ten slides (decision 22). **Tonni's parts (the elevator speech, slides 2 and 3) are exactly as she wrote them: never edit or "improve" them.** The scripts for slides 4 to 10 are drafts that Mahadi, Ahmad and Nazha edit into their own words, so those may change.
- The deck wording fixes 1 to 5 are applied (decision 19). The bank statistic is a net fall in the count, never "women who left".
- `main` is protected: a pull request cannot be merged without an approving review from another member. Do not try to bypass it.
- Do not push, pull, merge or open issues or pull requests unless the member asks, and ask which GitHub account to use each time.
