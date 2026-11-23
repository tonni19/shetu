# Project State

The current picture of the project. Keep it short: this is "where are we now", not history. History lives in `docs/worklog/` and in GitHub's pull request list.

**Update this file whenever the state of the project changes, not only when code changes.** The triggers and the routine are in `AGENTS.md`, section "Keep the project state current". If this file looks old, assume it is wrong and check GitHub.

Last updated: 2026-11-23, after pull requests #2 to #20 and the first application code (the backend skeleton, T1, on a branch waiting for review). **Thursday 26 November 2026 is the final date for the 10 to 15% progress presentation (online, every member present).** The [progress plan](UPDATE-1-PLAN.md) has the scope and the confirmed split of work (Tonni frontend and UI/UX, Maruf full stack, Mahadi AI, Nazha rules and quality); `docs/TEAM-BOARD.md` shows who is doing what now.

## Milestones

| Checkpoint | Goal | Status |
|---|---|---|
| Proposal, 15 Nov 2026 | Pitch | **Done.** Presented on 15 November; the deck (`05-Shetu-Proposal-Deck.pptx`) was submitted to the portal on 14 November. Feedback, asked in both places we presented: *why only for mothers, when anyone could use it? Where is the niche? Isn't it just a work planner?* The instructor also mentioned tokenization and vectorization (embeddings). Our answers are not agreed yet (see Next up). Not recorded here: whether the Excel sheet was entered in the faculty's Google Sheet |
| Progress, 26 Nov 2026 (online) | Show about 10 to 15%: GitHub set up, every member present, group discussion of the features | Plan drafted in `docs/UPDATE-1-PLAN.md`: a running skeleton and the first thin MAP slice. Not started. Time and format unconfirmed |
| Update 1 (30%) | MAP works: interview, Role Map, a forgotten duty found, initial cover check | Not started. Date unknown |
| Update 2 (60%) | HOLD works: a change typed in plain words is understood and re-planned | Not started |
| Final (100%) | All three stages, tests green, AI measured | Not started |

## What works now

**The backend skeleton (T1)** is built and tested on the branch `feature/t1-backend-skeleton`, not yet merged: FastAPI and SQLite, seeded synthetic accounts, sign-in with a signed session cookie, `GET /api/me`, `GET /api/cases/{id}` with a server-side permission check (employee, manager and HR may read; a colleague gets 403), `GET /healthz`, and 16 passing tests. How to run it: `backend/README.md`. How it works: `docs/CODE-EXPLANATION.md`. No frontend, AI or rules code yet. The full plan, slides and Excel draft are in `docs/planning/`; the learning guide is online at https://tonni19.github.io/shetu/.

## In progress

| Issue | What | Who | Branch |
|---|---|---|---|
| | Nothing in progress. The next work starts after the proposal presentation | | |

## Next up

1. **Thursday 26 November: the 10 to 15% progress presentation.** Follow the schedule at the top of the [progress plan](UPDATE-1-PLAN.md). Take ideas, not stacks, from the Congress build (decided 23 November). The owners are confirmed and the shared contract (`docs/API-CONTRACT.md`) is agreed. Agree how to answer the instructor and record settled product decisions in `docs/DECISIONS.md`. Record confirmed roles here and in `CONTRIBUTIONS.md`.
2. Get the FastAPI, React/Vite and SQLite foundation running, including sign-in, CI and the AI gateway with replay. Then connect interview, evidence, confirmation, and dated cover approval as one flow.
3. Write the first six synthetic cases in parallel. Compare live model candidates on those cases and prepare a labeled replay for the checkpoint. Attempt the HOLD change-parsing spike once the MAP path is working.
4. Stretch, in order: hourglass chart, then voice input (first stretch feature, after HOLD works).

## Known problems and open questions

- Hosted AI provider not chosen (decided by the bake-off).
- The faculty's later checkpoint dates (Update 1 at 30%, Update 2) are unknown. Maruf confirmed that Thursday 26 November is the final date for the 10 to 15% presentation; an earlier note about Sunday 29 November is dropped.
- A separate, public **Congress** build of Shetu exists (`SpicyFalcon619/shetu-congress`, Next.js and PostgreSQL, made by Maruf and Tonni for the AI Builders Congress 2026; its team page also lists Rowshonur Rahman Rizvy, who is not on the lab team, so credit him when adapting ideas). Our proposal answers called the earlier work "a one-case prototype". The team has to decide how to tell the instructor. This lab project stays a new build here, and anything adapted from Congress is credited in the worklog.
- The learning guide on GitHub Pages is **public** (anyone with the link), even though the repository is private. Only `docs/learn` is published. Never put names with student IDs, emails, keys or course PDFs in `docs/learn`.
- Member roles are **confirmed** (all four accepted on 23 November 2026, reported by Maruf): Tonni frontend and UI/UX, Maruf full stack, Mahadi AI, Nazha rules and quality. Details: `docs/TEAM-BOARD.md`. `CONTRIBUTIONS.md` is not created yet; add it when the first work lands.
- Hosted AI provider, and who holds the API key, not decided.
- Task tracking: GitHub Issues with a Projects board is proposed instead of Jira. Not decided.
- No review is recorded on pull requests #4 to #15 (merged before `main` was protected). From now on every pull request needs an approval from another member.

## Team and access

All four members are collaborators on `tonni19/shetu`: `tonni19` (admin, repository owner), `SpicyFalcon619`, `NazhaTarannum` and `HasanGMS0047` (write). Anyone with write access can review and merge a pull request, but **not their own**, and must use **their own GitHub account** so the history shows who reviewed what. Merge type: **merge commit**, not squash, so each member's own commits stay visible.

**`main` is protected** (since 16 November 2026, when `tonni19`'s GitHub Pro became active): no direct pushes, no force pushes, and every pull request needs **one approving review from a member who is not the author** before it can be merged. This also applies to the owner. **Learning guide online:** https://tonni19.github.io/shetu/ (published by `.github/workflows/learn-guide.yml` whenever `docs/learn` changes on `main`; the workflow publishes only that folder. First published on 16 November 2026 and checked live).

Three of the accounts (`SpicyFalcon619`, `tonni19`, `NazhaTarannum`) are signed in on Maruf's computer. At the team's request, some pull requests were pushed or merged from it under one of them. The worklog notes and the table below say which. Commits are authored under the name of the person who wrote them.

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
| #16 | Learning guide online with GitHub Pages; six "Deeper, in plain words" lessons; presentation feedback; decision 23 | SpicyFalcon619 (commits by Ahmad Maruf Hossain) | tonni19, **approved by tonni19** (the first reviewed pull request under branch protection) |
| #17 | Project state after #16 | SpicyFalcon619 (commits by Ahmad Maruf Hossain) | tonni19, approved by tonni19 |
| #18 | Plan for the 26 November progress presentation; decision 24 (ideas, not stacks, from Congress) | NazhaTarannum (commits by Ahmad Maruf Hossain) | SpicyFalcon619, approved by SpicyFalcon619 |
| #19 | Project state after #18, wording tidy-ups | SpicyFalcon619 (commits by Ahmad Maruf Hossain) | tonni19 |
| #20 | Team board, shared contract, coordination rules, positioning answers; decisions 25 to 28 | NazhaTarannum (commits by Ahmad Maruf Hossain) | SpicyFalcon619, approved by SpicyFalcon619 |

## Things every assistant should know right now

- **Positioning (working answer, decision 28).** Shetu is role-continuity software, not a generic work manager: it manages a role through one absence and its return. Do not build task boards, time tracking, productivity scoring or auto-assignment (`AGENTS.md` rule 12). Wording is gender-neutral (rule 11). Details: `docs/planning/08-Positioning-and-Strategy.md`.
- **Coordinate before you act.** Read `docs/TEAM-BOARD.md` and `docs/API-CONTRACT.md` at the start of every session, check on `origin/main` that the parts you depend on are really merged, and use labelled stubs (`STUB(T#)`) rather than guessing or building someone else's part. The rules are in `AGENTS.md`, section "Coordinate before you act".
- Only the backend skeleton exists (T1). Do not assume any other file or function is there; check `origin/main` and `docs/TEAM-BOARD.md`.
- Voice input is a **stretch** feature (decision 16), not cut and not in the first version.
- Speaker scripts exist for all ten slides (decision 22). **Tonni's parts (the elevator speech, slides 2 and 3) are exactly as she wrote them: never edit or "improve" them.** The scripts for slides 4 to 10 are drafts that Mahadi, Maruf and Nazha edit into their own words, so those may change.
- The deck wording fixes 1 to 5 are applied (decision 19). The bank statistic is a net fall in the count, never "women who left".
- `main` is protected: a pull request cannot be merged without an approving review from another member. Do not try to bypass it.
- Do not push, pull, merge or open issues or pull requests unless the member asks, and ask which GitHub account to use each time.
