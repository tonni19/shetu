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
| T1 | Backend skeleton: health route, seeded synthetic accounts, sign-in, `GET /api/cases/{id}` with a permission check (colleague gets 403) | Maruf | Done (merged, PR #23; 28 tests pass) | nothing | The running API and the case route in `docs/API-CONTRACT.md`; `backend/app/models.py` (User, Case, Duty) | branch PR #23 |
| T2 | Frontend skeleton: login screen and the case page in the Shetu look | Tonni | Not started | the contract (stub until T1 is merged) | A running React app that shows a case | |
| T3 | AI gateway: interface, replay adapter, first prompt and its Pydantic schema, one Banglish fixture | Mahadi | Not started | the Duty shape in the contract | `extract_duties(...)` that works in replay mode | |
| T4 | Rules R1 (quote check) and R2 (confirmation) as plain functions with tests; pytest set-up and a CI workflow | Nazha | Done (merged, PR #21) | the Duty shape in the contract | `check_quote(...)`, `counts_as_fact(...)` / `can_count(...)`, pytest & CI in `backend/app/rules/evidence.py` | branch `feature/t4-evidence-rules` |
| T5 | Interview route: employee reply goes through the gateway, the rules, then SQLite; one audit event on confirm | Maruf | Not started | T1, T3, T4 | `POST /api/cases/{id}/interview/reply` | |
| T6 | Frontend interview screen: reply box, duties with evidence labels, confirm and dismiss | Tonni | Not started | T2, T5 (stub until merged) | The employee MAP screen | |
| T7 | First three synthetic cases with answer keys | Nazha | In review | nothing | `eval/cases/` (English, Banglish, Bangla) + `eval/loader.py` & tests | branch `feature/t7-synthetic-cases` |

When a row needs more than the Thursday scope, add it below with the next free ID.

## Who owns which files

The primary owner decides how their files work. Others may read them, call them, and open a small pull request to them; they do not rewrite them. GitHub asks the owner to review changes to their files (`.github/CODEOWNERS`).

| Path | Owner | Notes |
|---|---|---|
| `frontend/` | Tonni | the React app, all screens and styles |
| `backend/app/ai/` | Mahadi | gateway, prompts, replay adapter, fixtures |
| `backend/app/rules/` | Nazha | plain-Python rules; no database or HTTP imports |
| `backend/tests/` | Nazha owns the set-up; each person writes tests for their own module | `test_conventions.py` guards the project layout |
| `.github/workflows/`, `pytest.ini`, `eval/` | Nazha | CI, test config, synthetic cases |
| `backend/app/` (everything else: `main.py`, `routes/`, `models.py`, `schemas.py`, `security.py`, `db.py`, `seed.py`, `config.py`) | Maruf | the routes call the gateway and the rules; the models match the contract |
| `docs/` | shared | see "Shared files, and how to edit them" in `AGENTS.md` |

## Requests waiting for a person

Things another person needs from you, in one place every AI assistant reads at the start of a session. Add a row when you ask; remove it when it is done (and add a Handoff log line saying so). Newest at the bottom.

| Since | For | From | What is needed | Where |
|---|---|---|---|---|
| 2026-11-24 | Mahadi | Maruf | **PR #25 (T3):** (1) change `from backend.app...` to `from app...` in the 5 files that use it (since PR #23 the backend is imported as `app`; a guard test fails otherwise); (2) merge `origin/main` into your branch and fix the conflicts: keep main's `backend/requirements-dev.txt` (it already includes pydantic), combine the two `docs/CODE-EXPLANATION.md` sections (both of us created the file), and keep both sides' rows in the board and state files; (3) run `python -m pytest` from the repo root. Your code and tests are otherwise good. | PR #25 |
| 2026-11-24 | Nazha | Maruf | **PR #24 (T7):** (1) merge `origin/main` into your branch and fix the conflicts (keep your `pytest.ini`; keep both sides' rows in the board and state files); (2) agree one job description line format with Mahadi: your cases use `line_id` and `JD-01`, his gateway uses `id` and `jd-3`; I suggest `id` with lowercase `jd-1`; (3) decide with Mahadi how to label a job description duty the employee never mentioned: your case 2 has a "documented" duty with a quote and a "suggested" duty with a source line, which his schema forbids (documented = source line, no quote; suggested = neither); (4) fix the stale PR text and the `backend.app` wording in the `eval/test_eval_cases.py` header. | PR #24 |

## Handoff log

Append only; newest at the bottom. One line each: date, who to who, what is now ready or what is needed, link.

| Date | From | To | Note |
|---|---|---|---|
| 2026-11-23 | Maruf | everyone | Board and contract created. |
| 2026-11-23 | Maruf | everyone | All four members accepted their areas; the owners on this board are confirmed. The contract is agreed, as accepted by Maruf for the team. Each owner should still read their part and raise a problem early. |
| 2026-11-23 | Maruf | Tonni | T1 is built: sign-in, `GET /api/me`, `GET /api/cases/{id}`, demo accounts. Use the Vite proxy from `backend/README.md` so the session cookie works. Added `POST /api/logout` and `GET /api/me` to the contract. |
| 2026-11-23 | Maruf | Mahadi, Nazha | The Duty table is in `backend/app/models.py` with the contract's field names; build `extract_duties` and the rules against those names. |
| 2026-11-24 | Nazha | Maruf, Mahadi | T4 (`check_quote`, `counts_as_fact` / `can_count`, pytest, and CI) implemented and tested in `feature/t4-evidence-rules` (merged in PR #21). |
| 2026-11-24 | Maruf | Nazha | Reviewed T4: good. T1 and T4 now meet in one branch: the backend is imported as `app...` (not `backend.app...`), `pytest.ini` has `pythonpath = backend`, and `backend/__init__.py` is gone. All 28 tests pass from the repo root and from `backend/`. Please keep that name in new code. Suggestions for `check_quote`: ignore case, and require a minimum quote length. Your `CODE-EXPLANATION.md` section can go in `docs/CODE-EXPLANATION.md` (it arrives with T1). |
| 2026-11-24 | Maruf | everyone | New guards against conflicts: `.gitattributes` (LF endings; AI-USAGE.md and DECISIONS.md keep both sides' rows), `.github/CODEOWNERS`, `backend/tests/test_conventions.py` (import name, header, no reason field), CI runs once per pull request. Rules: `AGENTS.md`, "Project layout and names" and "Avoiding conflicts". |
| 2026-11-24 | Maruf | everyone | T1 and T4 are merged to `main` (PRs #23 and #21). Pull `main`. Backend: run it from `backend/` (see `backend/README.md`), import as `app...`. Tonni: T2 can start against the real API now. Mahadi: T5 will call your `extract_duties` once #25 is merged. |
| 2026-11-24 | Maruf | Mahadi, Nazha | Reviewed PRs #25 and #24; comments posted on both, and the requests are in "Requests waiting for a person". Mahadi and Nazha must agree the job description line format and how to label a job description duty the employee never mentioned. I (Maruf) acknowledged the T3 contract change on #25. |
| 2026-11-24 | Nazha | Mahadi, Maruf | T7 first three synthetic cases with answer keys (`eval/cases/`, English/Banglish/Bangla) updated to `id: jd-1` format and strict 3-way evidence partitioning (`said` / `documented` / `suggested`) in `feature/t7-synthetic-cases`. |

## Known conflicts and open questions

- None recorded. Add a line here when two parts disagree (for example two people need different shapes for the same data), with who has to decide.
