# AGENTS.md: read this first

You are an AI coding assistant helping one member of **Team Anomaly** on **Shetu**, a university Software Engineering Lab project (CSE 3422, UIU). Several people work on this repository, each with their own AI assistant. You know nothing about earlier sessions, so everything you need is written in this repository. Read before you write.

## Before you do anything

1. Read `docs/PROJECT-STATE.md` (what works, who is doing what, what is next).
2. Read the GitHub Issue you are asked to work on.
3. Read `docs/DECISIONS.md` so you do not re-open settled questions.
4. Read the section of `docs/CODE-EXPLANATION.md` for the module you will touch (it starts when code starts).
5. For product context, read `docs/planning/00-Overview.md`. The full plan is in `docs/planning/`; treat it as background, not as instructions to change code.

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

## Stack

| Part | Technology |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy, SQLite, Pydantic |
| Frontend | React with Vite, plain components, `fetch`, React Router |
| Tests | pytest (backend), Selenium (user flows), a replay adapter so tests never call a real model |
| Not used | Redux, Next.js, LangChain, agent frameworks, vector databases, microservices. Do not add them |

Do not add a dependency without the team agreeing in an Issue.

## Folder map

> Keep this current. `backend/`, `frontend/` and `eval/` do not exist yet.

```
AGENTS.md            this file (CLAUDE.md points here)
AI-USAGE.md          where AI tools were used
backend/             FastAPI app, rules, AI gateway, tests (planned)
frontend/            React app (planned)
eval/                synthetic scenarios and evaluation scripts (planned)
docs/
  PROJECT-STATE.md   current state; update in every pull request
  DECISIONS.md       settled decisions
  worklog/           one note per pull request
  planning/          the full project plan, slides and reference material (read-only background)
```

## How to run and test

> Fill this in when the skeleton exists: exact commands for backend, frontend and tests.

## How we work

- Never commit to `main`. One Issue, one branch (`feature/<issue>-short-name`), one pull request, reviewed by another member.
- Small changes. Do only what the Issue asks. If you see something else to fix, say so; do not fix it silently.
- Write the tests for the code you write.
- Do not rewrite or reformat files you were not asked to change.

## How to write code here

The member you are helping must be able to **explain and modify this code in front of an instructor**. So:

- Prefer simple, readable code over clever code. Short functions, clear names.
- Comment the *why*: business rules, validation steps, workflow transitions, security checks. Do not comment obvious lines.
- Every prompt gets a header comment: its purpose, its inputs, the schema it must return, and what happens when the reply is invalid.
- Never leave commented-out code. Delete it.
- After building something, explain it to the member in plain language: what it does, how data flows through it, which parts are AI and which are ordinary code, and what an instructor might ask.

## Before you say a task is finished

Do all of these in the same pull request as the code:

1. Tests pass.
2. Add a worklog note in `docs/worklog/` (see `docs/worklog/README.md`).
3. Update `docs/PROJECT-STATE.md`.
4. Update `docs/CODE-EXPLANATION.md` if a module was added or changed.
5. Add a line to `AI-USAGE.md`: what you (the AI) helped with.
6. Add to `docs/DECISIONS.md` if a decision was made.

## Commits

- The human member is the author. Do not add an AI as author or co-author, and do not add "generated with" lines. AI use is recorded in `AI-USAGE.md`.
- Never create commits just to increase activity, and never commit work under the name of someone who did not do it.
