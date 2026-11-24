# Team Board: who is doing what, and what depends on what

This is the live coordination file for the four members and their AI assistants. It answers three questions before anyone writes code:

1. **What is each person building right now?**
2. **What must exist first** before my part can work?
3. **Has that part actually been merged, or only planned?**

Keep it short and true. If this file disagrees with GitHub, **GitHub wins**: check `origin/main`, open pull requests and Issues, then fix this file.

Last updated: 2026-11-23. The owners below are **confirmed**: all four members accepted their areas on 23 November 2026 (reported by Maruf). The shared contract (`docs/API-CONTRACT.md`) is **agreed** (23 November 2026).

## How to use this file (members and AI assistants)

**Before you start any task**

1. Run `git fetch` and compare with `origin/main`. Your local copy may be old.
2. Find your row in "Work items". Read the **Needs** column.
3. For every item in **Needs**, look at its **Status** *and* confirm it on `origin/main` (is the code or file really there?). A board row can lag; merged code does not.
4. Decide, using the rules in `AGENTS.md`, section "Coordinate before you act":
   - **Everything you need is merged:** build against the real thing.
   - **A thing you need is not merged yet:** do **not** build the other person's part and do **not** guess. Build against the written contract (`docs/API-CONTRACT.md`) using a stub or fixture, mark your row **Blocked on T#** (or **In progress, using a stub for T#**), and tell the owner in the Issue.
   - **The contract is missing something you need:** propose the change (see "Changing a shared interface" in `AGENTS.md`). Never silently invent a field.
5. Set your row to **In progress** (your own pull request).

**While you work.** If your plan changes (a different file, a renamed field, a new dependency), update your row in the same pull request.

**When you finish.** Set the row to **In review** when you open the pull request, and to **Done** after it is merged. Add a line to the Handoff log if someone else is waiting for this. Say in the worklog what the next person can now rely on.

**Status words:** `Not started` · `In progress` · `Blocked` · `In review` · `Done` (merged to `main`).

## People and areas

| Person | Area (primary owner) | May help with | Confirmed? |
|---|---|---|---|
| Sadia Noman Tonni | Frontend and UI/UX (React/Vite) | the API calls; Selenium flows | confirmed |
| Ahmad Maruf Hossain (Maruf) | Full stack: FastAPI, SQLite, sign-in and permissions, routes, wiring everything together | gateway wiring; the frontend's API use; everyone's reviews | confirmed |
| Mohammad Mahadi Hasan | AI: gateway, replay, prompts, evidence extraction, model comparison | the synthetic cases; wiring into the routes | confirmed |
| Nazha Tarannum Roza | Rules and quality: plain-Python rules, pytest, Selenium, CI, synthetic cases | the screens' Selenium; the cases | confirmed |

One person is **primary** for each area. Others may help, but the primary owner decides how their module works and explains it to the instructor.

## Work items

Target: the 10 to 15% progress presentation on **Thursday 26 November 2026**. IDs are stable; never reuse one.

| ID | Work item | Owner | Status | Needs | Produces (what others rely on) | Issue / PR |
|---|---|---|---|---|---|---|
| T1 | Backend skeleton: health route, seeded synthetic accounts, sign-in, `GET /api/cases/{id}` with a permission check (colleague gets 403) | Maruf | Not started | nothing | The running API and the case route in `docs/API-CONTRACT.md` | |
| T2 | Frontend skeleton: login screen and the case page in the Shetu look | Tonni | Not started | the contract (stub until T1 is merged) | A running React app that shows a case | |
| T3 | AI gateway: interface, replay adapter, first prompt and its Pydantic schema, one Banglish fixture | Mahadi | Not started | the Duty shape in the contract | `extract_duties(...)` that works in replay mode | |
| T4 | Rules R1 (quote check) and R2 (confirmation) as plain functions with tests; pytest set-up and a CI workflow | Nazha | Done | the Duty shape in the contract | `check_quote(...)`, `counts_as_fact(...)` / `can_count(...)`, pytest & CI in `backend/app/rules/evidence.py` | branch `feature/t4-evidence-rules` |
| T5 | Interview route: employee reply goes through the gateway, the rules, then SQLite; one audit event on confirm | Maruf | Not started | T1, T3, T4 | `POST /api/cases/{id}/interview/reply` | |
| T6 | Frontend interview screen: reply box, duties with evidence labels, confirm and dismiss | Tonni | Not started | T2, T5 (stub until merged) | The employee MAP screen | |
| T7 | First three synthetic cases with answer keys | Nazha | In review | nothing | `eval/cases/` (English, Banglish, Bangla) + `eval/loader.py` & tests | branch `feature/t7-synthetic-cases` |

When a row needs more than the Thursday scope, add it below with the next free ID.

## Handoff log

Append only; newest at the bottom. One line each: date, who to who, what is now ready or what is needed, link.

| Date | From | To | Note |
|---|---|---|---|
| 2026-11-23 | Maruf | everyone | Board and contract created. |
| 2026-11-23 | Maruf | everyone | All four members accepted their areas; the owners on this board are confirmed. The contract is agreed, as accepted by Maruf for the team. Each owner should still read their part and raise a problem early. |

| 2026-11-24 | Nazha | Maruf, Mahadi | T4 (`check_quote`, `counts_as_fact` / `can_count`, pytest, and CI) merged into `main`. |
| 2026-11-24 | Nazha | Mahadi, Maruf | T7 first three synthetic cases with answer keys (`eval/cases/`, English/Banglish/Bangla) added and tested against real T4 rules in `feature/t7-synthetic-cases` (ready for review). |

## Known conflicts and open questions

- None recorded. Add a line here when two parts disagree (for example two people need different shapes for the same data), with who has to decide.
