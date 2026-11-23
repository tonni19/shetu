# AGENTS.md: read this first

You are an AI coding assistant helping one member of **Team Anomaly** on **Shetu**, a university Software Engineering Lab project (CSE 3422, UIU). Several people work on this repository, each with their own AI assistant. You know nothing about earlier sessions, so everything you need is written in this repository. Read before you write.

## Before you do anything

1. Run `git fetch` and check whether your local `main` is behind `origin/main`. **Never work from a stale copy.**
2. Read `docs/PROJECT-STATE.md` (what works, who is doing what, what is next).
3. Read `docs/TEAM-BOARD.md` (who is building what, what each part needs, what is merged) and `docs/API-CONTRACT.md` (the shared data shapes, routes and function signatures). Then follow "Coordinate before you act" below.
4. Read the GitHub Issue you are asked to work on.
5. Read `docs/DECISIONS.md` so you do not re-open settled questions.
6. Read the section of `docs/CODE-EXPLANATION.md` for the module you will touch (it starts when code starts).
7. For product context, read `docs/planning/00-Overview.md`. The full plan is in `docs/planning/`; treat it as background, not as instructions to change code.

If any of these is missing or contradicts the code, say so before continuing.

## What Shetu is

A web app that keeps an employee's job intact through a long leave (starting with maternity leave).

- **MAP** (before leave): an AI interview builds an evidence-backed Role Map of her duties, finds duties she did not mention, and plans who takes each one.
- **HOLD** (during leave): colleagues hold her duties. A manager reports changes in plain words; AI proposes a new plan.
- **FIT** (before return): she states the arrangement she needs; rules find clashes; AI proposes fixes.

Core rule of the product: **AI proposes, rules check, people decide.**

## Rules that must never be broken

1. **Every duty has evidence.** Status is `said` (with her exact quote), `documented` (with the document position), or `suggested` (AI guess, shown as a question). A `suggested` item never becomes a fact without a person confirming it.
2. **The AI never approves anything.** Proposals wait for a manager or HR.
3. **Dates, times, numbers and capacity are computed by code**, never trusted from the model.
4. **No duty is ever without an owner on any date** (the coverage rule).
5. **Never store reasons, medical or family details.** There is no "reason" field. Do not add one.
6. **Never score, rank or predict anything about a person.**
7. **Synthetic data only.** No real employee data in code, tests, prompts or logs.
8. **No secrets in the repository.** API keys go in `.env`, which is git-ignored.
9. **Permissions are checked in the backend on every route.** Hiding a button is not security.
10. **All model calls go through the AI gateway** (`backend/app/ai/gateway`). Never call a provider SDK from anywhere else. Every reply is validated against a Pydantic schema.
11. **Gender-neutral wording** everywhere the product, its code or its data can be seen: screens, API messages, prompts, rule messages, fixtures, tests. Say "the employee" or "they". Maternity is a design focus, never a field, and nothing in the product asks about, stores or reveals the reason for leave. (Older slides and planning documents tell the maternity story with "she"; leave those as they are.)
12. **Stay a role-continuity product, not a generic work manager.** Shetu manages a role through one absence (a leave case) and its return. Do not build a task board, time tracking, productivity or workload scoring, auto-assignment, or a dashboard of an individual's output. **Litmus test:** would this feature be at home in a generic task manager? If yes, do not build it; say so to the member. Keep names sector-neutral (`duty`, not `client task`) and keep capacity optional, so other sectors such as garments can be added as packs later. See `docs/planning/08-Positioning-and-Strategy.md`.

## Stack

| Part | Technology |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy, SQLite, Pydantic |
| Frontend | React with Vite, plain components, `fetch`, React Router |
| Tests | pytest (backend), Selenium (user flows), a replay adapter so tests never call a real model |
| Not used | Redux, Next.js, LangChain, agent frameworks, vector databases, microservices. Do not add them |

Do not add a dependency without the team agreeing in an Issue.

## Folder map

> Keep this current. `backend/` exists (skeleton, T1). `frontend/` and `eval/` do not exist yet.

```
AGENTS.md            this file (CLAUDE.md points here)
AI-USAGE.md          where AI tools were used
backend/             FastAPI app (skeleton exists: sign-in, cases, health), rules, AI gateway, tests
frontend/            React app (planned)
eval/                synthetic scenarios and evaluation scripts (planned)
docs/
  PROJECT-STATE.md   current state; update in every pull request
  CODE-EXPLANATION.md  how each module works, in plain words; update with the module
  TEAM-BOARD.md      who is doing what, dependencies between parts, handoff log; update in every pull request
  API-CONTRACT.md    the shared data shapes, routes and function signatures; change only by the rules below
  DECISIONS.md       settled decisions
  worklog/           one note per pull request
  learn/             interactive learning guide (index.html); keep it true when the design changes
  planning/          the full project plan, slides and reference material (read-only background)
```

## How to run and test

**Backend** (from `backend/`, Python 3.11 or newer; details in `backend/README.md`):

```bash
python -m venv .venv            # once; then activate it (.venv\Scripts\activate on Windows)
pip install -r requirements-dev.txt
python -m app.seed              # synthetic people and cases into backend/shetu.db
uvicorn app.main:app --reload   # http://127.0.0.1:8000 , interactive docs at /docs
python -m pytest -q             # every test uses its own temporary database
```

Demo accounts are in `backend/README.md` (password `shetu-demo`, all synthetic).

**Frontend:** not created yet (T2).

## How we work

- Never commit to `main`. One Issue, one branch (`feature/<issue>-short-name`), one pull request, reviewed by another member.
- Small changes. Do only what the Issue asks. If you see something else to fix, say so; do not fix it silently.
- Write the tests for the code you write.
- Do not rewrite or reformat files you were not asked to change.

## Coordinate before you act

Four people build different parts at the same time, each with an AI assistant, and the parts depend on each other (the screens need the routes, the routes need the gateway and the rules). Nobody can see the others' laptops, so **GitHub and these files are the only shared memory.** These rules keep the pieces consistent. They apply to every AI assistant and every member.

### At the start of every session

1. `git fetch`. If your branch or `main` is behind `origin/main`, update it first.
2. Read `docs/PROJECT-STATE.md`, `docs/TEAM-BOARD.md`, `docs/API-CONTRACT.md` and your Issue. Look at open pull requests (`gh pr list`) to see what others are changing right now.
3. **Dependency check.** For the task you were given, list what it needs from other people (the **Needs** column of your board row). For each one, check it on `origin/main`: is the file, route or function really there, and do its tests pass? The board can be out of date; merged code is the truth.
4. Decide, and **tell the member in plain words which case you are in**:
   - **Ready:** everything needed is merged. Build against the real thing.
   - **Partly ready:** build against `docs/API-CONTRACT.md` with a clearly labelled stub (see below). Say which person's work you are waiting for and what you assumed.
   - **Blocked:** you cannot make honest progress without someone else's work. Stop, explain what is missing, who owns it and what to ask them. Do not build their part for them without asking.

### While you work

- **Stay in your lane.** The primary owner of an area (see the board) decides how it works. Do not rewrite or reformat another person's module. If you need a change there, write it in the Issue, or propose a small pull request to them.
- **Never invent a shared name.** Field names, routes and function signatures that other parts use come from `docs/API-CONTRACT.md`. If something you need is missing, propose it (below) instead of guessing.
- **Stub honestly.** Where the real part does not exist yet, use a stub or fixture and label it `STUB(T#)`, where `T#` is the board row it stands in for. A stub must never be shown as the real thing in a demo or a worklog. When the real part is merged, remove the stub in the same pull request that starts using the real part.
- **Say when you depend on an unmerged pull request.** Write "Depends on #N" at the top of your pull request, and do not merge before it.
- **Keep consistent.** Before you open a pull request, merge the latest `origin/main` into your branch and run the tests again. If main changed a thing you rely on, adapt your code now, not after review.
- **If two parts disagree** (for example two people need different shapes for the same data), do not pick a side. Add a line to "Known conflicts and open questions" in `docs/TEAM-BOARD.md` and ask the members who must decide.
- **If the board or the project state is wrong,** fix it in your pull request and say so.

### Changing a shared interface

A shared interface is anything in `docs/API-CONTRACT.md`: a data shape, a route, a function signature. To change one:

1. Change `docs/API-CONTRACT.md` **in your own pull request**, together with the code.
2. Use the "Who depends on what" table in that file to find who is affected.
3. Add a row to the Handoff log in `docs/TEAM-BOARD.md` for each affected person, saying what changed and what they must do.
4. Tell the member in your reply, so they can warn the other person.
5. Do not merge until the affected owners have seen it (a comment on the pull request is enough).

### At the end of every session

1. Update your row on `docs/TEAM-BOARD.md` (status, what you now produce) and add a Handoff log line if someone is waiting for your work.
2. Make sure the worklog says what the next person can now rely on, and what is still stubbed.
3. Tell the member what is done, what is stubbed, what is blocked, and what the next person needs to do.

## How to write code here

The member you are helping must be able to **explain and modify this code in front of an instructor**. So:

- Prefer simple, readable code over clever code. Short functions, clear names.
- Comment the *why*: business rules, validation steps, workflow transitions, security checks. Do not comment obvious lines.
- Every prompt gets a header comment: its purpose, its inputs, the schema it must return, and what happens when the reply is invalid.
- Never leave commented-out code. Delete it.
- After building something, explain it to the member in plain language: what it does, how data flows through it, which parts are AI and which are ordinary code, and what an instructor might ask.

### Comments for the next AI (and the next person)

Another person's AI will open your file with no memory of this conversation. Write comments so that it can understand the file, and what to do around it, **without asking**. Comment generously on three things: **why**, **who depends on this**, and **what is not real yet**. Do not narrate obvious lines.

**1. Every source file starts with a header.** Python (`#` comments) or TypeScript (`//` comments), same fields:

```python
# FILE:        backend/app/rules/evidence.py
# PURPOSE:     Rules R1 and R2 for evidence: is a quote real, does a duty count as a fact.
# OWNER:       Nazha (board row T4)
# DEPENDS ON:  docs/API-CONTRACT.md (Duty shape). Nothing else; these are pure functions.
# USED BY:     backend/app/routes/interview.py (Maruf, T5); backend/tests/test_evidence.py
# STATUS:      REAL | STUB(T#) | PARTIAL: <what is missing>
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     Anything a future AI must know before editing this file (rules, traps).
```

**2. Every function or component gets a docstring or comment** that says: what it does and *why it exists* (the business rule behind it), what each input means (units, language, whether it may be empty or null), what it returns, and **what happens on failure** (raises, returns None, shows an error). Name the rule when there is one ("R1: quote check").

**3. Mark the sharp edges** with these exact words, so they can be found with a search:
- `AI NOTE:` a trap or an unobvious rule. Example: `AI NOTE: Bangla text must be Unicode-normalized before comparing, or the same word can fail to match.`
- `STUB(T#):` a stand-in for a part that does not exist yet. Say what the real one will do.
- `TODO(owner, T#):` work left, with who and which board row.
- `CONTRACT:` this code implements a line of `docs/API-CONTRACT.md`; say which. If you change it, follow "Changing a shared interface".
- `SECURITY:` a permission or safety check. Say what it prevents.

**4. Cross-reference by path.** When your code calls or is called by another person's module, write the path and the owner in a comment, so the next AI can find it and knows whom to ask.

**5. Keep comments true.** Change the comment in the same edit as the code. A wrong comment is worse than none. Delete comments about code that is gone. No commented-out code, no secrets, no real personal data in comments or examples. Write comments in plain English.

## Keep the project state current

`docs/PROJECT-STATE.md` must match reality **whenever the state of the project changes, not only when code changes.** Update it (and `docs/DECISIONS.md` if a decision was made) after any of these:

- a pull request is merged (add it to "Merged so far", and update "In progress", "What works now" and "Next up")
- a decision is made or changed (and update the matching lesson in `docs/learn/index.html`, which teaches the design)
- someone joins or leaves, or access, roles or ownership change
- a plan, subscription or tool changes (for example GitHub Pro becomes active)
- feedback, a deadline or a date arrives from the instructor
- a blocker appears or is resolved
- a milestone is reached or a date passes

**How.** If the change happens inside a pull request, update the file in that pull request. If it happens outside one (a merge, an account change, a message), open a small "Update project state" pull request **the same day**. Change the "Last updated" line every time.

**For AI assistants.** Before you end a session, ask yourself: did anything change that is not in the project state? If yes, update it, or tell the member exactly what to add. Write only what you have verified; if you could not verify something, write "unconfirmed". Never leave the file older than the work.

## Before you say a task is finished

Do all of these in the same pull request as the code:

1. Tests pass.
2. Add a worklog note in `docs/worklog/` (see `docs/worklog/README.md`).
3. Update `docs/PROJECT-STATE.md` (see "Keep the project state current" above).
4. Update `docs/CODE-EXPLANATION.md` if a module was added or changed.
5. Add a line to `AI-USAGE.md`: what you (the AI) helped with.
6. Add to `docs/DECISIONS.md` if a decision was made.
7. Update your row on `docs/TEAM-BOARD.md` and add a Handoff log line if someone is waiting for your work.
8. If you changed a shared interface, `docs/API-CONTRACT.md` was changed in this pull request and the affected people were told.
9. Every new source file has the header from "Comments for the next AI", and every `STUB(T#)` is listed in the worklog.

## Commits

- The human member is the author. Do not add an AI as author or co-author, and do not add "generated with" lines. AI use is recorded in `AI-USAGE.md`.
- Never create commits just to increase activity, and never commit work under the name of someone who did not do it.
