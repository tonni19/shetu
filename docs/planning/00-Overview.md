# Shetu: Quick Overview for the Team

Read this first. It is the short version of everything in this folder. Last updated 12 November 2026.

## 1. What we are building

**Shetu** is a web app that helps a company handle an employee's long leave, starting with maternity leave.

The problem: when someone goes on leave, nobody really knows everything she does. So work gets dropped, the cover plan breaks when something changes, and she comes back to a job that no longer fits her life.

Shetu works in three stages:

| Stage | When | What Shetu does |
|---|---|---|
| **MAP** | Before leave | AI interviews her (Bangla, English or Banglish), builds a list of her real duties, finds duties she forgot, and plans who takes each one |
| **HOLD** | During leave | Colleagues hold her duties. If something changes, the manager types it in plain words and AI proposes a new plan |
| **FIT** | Before return | She says what arrangement she needs. Shetu finds clashes with her job and proposes fixes |

The main rule of the whole product: **AI proposes, rules check, people decide.** The AI never approves anything by itself.

## 2. Two ideas that hold it together

**The Role Map.** One list of her duties. Every duty shows where it came from:

- **Said**: she said it (we keep her exact words)
- **Documented**: a document says it
- **Suggested**: the AI thinks it may be missing. This is only a question until she confirms it

**The Hourglass.** This is the shape of a leave, and it is how the three stages fit together. It is **not** a fourth set of stages. Picture an hourglass on its side:

| Part of the hourglass | Stage | What happens to her duties |
|---|---|---|
| Wide, then narrowing | **MAP** (before leave) | Her duties are mapped, then handed over to colleagues one by one, each on an agreed date |
| The narrow middle | **HOLD** (during leave) | Colleagues hold her duties. If something changes, the plan is repaired. She is not contacted |
| Narrow, then widening | **FIT** (before and after return) | Her duties come back to her one by one, around the arrangement she needs |

**How it works in the app.** Every duty in the Role Map has an owner on every date. Her workload at any moment is simply the duties she owns on that date, so the hourglass is what the plan looks like when drawn over time. Two rules: no duty is ever left without an owner, and no change takes effect without a person's approval.

**What we decided about it:**

- **No fixed percentages.** An earlier idea had six phases with set workload percentages. We dropped it: every person and every job is different, so each handover and return date is agreed individually.
- **No extra stages.** It stays inside MAP, HOLD and FIT, so the product has one structure, not two.
- **How AI helps.** It proposes the order and dates of each handover and return. Rules check the proposals against team workload and policy, and a person approves.
- **In the build.** The ownership timeline and the "no duty without an owner" rule are in the core version. The hourglass chart is a next priority. The slide deck shows it on the "Our solution" slide.

We found no written record of the original six-phase version in the project files, so this follows what we discussed. If anyone has the original notes, tell me and I'll compare them.

## 3. Why this counts as an AI project

Without AI, Shetu would only be a form. A form cannot understand Banglish, notice what is missing, compare her words with a document, or understand "Tania is away for three weeks". AI is used in all three stages.

Example we will demo: the manager types *"Tania will be unavailable for three weeks, and the quarterly report deadline has moved to April 2."* Shetu understands it, finds the affected duties, proposes a new plan, checks it against workload rules, and waits for the manager's approval.

## 4. What exists today

The old competition prototype (GP FutureMakers) only works on **one scripted example**. It has no login, no database, no data entry and no tests. Some of its AI parts are real and useful, and some of its screens are fake.

So for this lab we are doing a **new, proper build**. The faculty already knows about the competition and is fine with it. We must always be honest about what is old, what is planned, and what we actually built. Right now, nothing has been built for the lab.

## 5. Decisions we have made

| Topic | Decision |
|---|---|
| Direction | "Shetu Evidence Map": Map, Hold, Fit around one evidence-backed Role Map |
| AI model | Hosted API is the main one. Our local Qwen model is the backup. Google Colab is for experiments only, never for the demo |
| Which hosted model | **Not chosen yet.** We will test a few on the same test cases and pick the best. A Gemini Flash model is the likely choice |
| Switching models | The app talks to the AI through one small "gateway", so we can change the model without rewriting the app |
| Cost | Free on Gemini's free tier. If we pay, roughly $40 to $135 for the whole term on a mid-level model, and much less on small ones |
| Data | **Fake (synthetic) data only.** Never real employee data |
| Tech stack | Backend: Python with FastAPI. Frontend: React. Database: SQLite. Tests: pytest and Selenium. GitHub for teamwork. This follows our teacher's advice |
| Not using | Microservices, vector databases, AI agents, LangChain, Redux, Next.js. They add complexity we do not need |
| Real companies | For the lab we use a hosted AI with fake data. For a real company, the same app can run on a model inside their own servers, so employee data never leaves the building |
| Team | Team Anomaly: Sadia Noman Tonni, Nazha Tarannum Roza, Ahmad Maruf Hossain, Mohammad Mahadi Hasan |

## 6. What we will build, and what we will not

**We commit to (core version):**

1. Login with four roles: employee, manager, cover colleague, HR
2. AI interview and Role Map that the employee confirms
3. AI compares her words with her job description and asks about gaps
4. AI proposes who covers each duty; rules check workload; manager approves
5. Manager reports a change in plain words; AI re-plans; manager approves
6. Return planning: clashes found, fixes proposed, approved
7. HR approval list and a log of every decision
8. Tests, and a proper way to measure the AI

**Only if time allows:** hourglass chart, question-answering for cover colleagues, file upload, deleting data after a case closes, and **voice input** (first in line once HOLD works; typed Banglish already gives us the AI interview, so voice is an extra way to talk to it, not a new AI capability).

**We will not build:** calendar or email integration, AI that acts alone, anything that scores or predicts people, payments.

**Honest warning:** the core version needs about 183 to 269 hours, plus about 20 to 35 more because we use React and FastAPI. Four people over seven weeks have about 170 to 225 hours. So three simplifications apply **from day one**:

- FIT checks **time clashes only**, with one policy rule.
- The AI compares her words with **her job description only**, not other documents.
- HR gets a **simple approval list**, not a full dashboard.

If we fall behind further, the next cuts are listed in the report (section 21.4). We never cut the evidence on each duty, the "no duty without an owner" rule, the HOLD re-planning, the AI tests, or the automatic tests.

## 7. Roadmap (final plan, agreed 12 November)

The dates of Update 1, Update 2 and the final are not announced yet, so the plan follows the checkpoints. Each step ends with something we can **show working live**, not just screens.

| Step | When | What we build | What we can show |
|---|---|---|---|
| **0. Proposal** | 15 November | Nothing. Slides and Excel sheet only | The plan |
| **1. Setup** | First week after the proposal | GitHub repo set up with the starter files; roles assigned; empty FastAPI + React + SQLite app with login; automatic tests on every pull request; the AI gateway; the first 6 fake test cases; **test the AI models and choose one** | Each member can log in on their own laptop; we know which AI we use |
| **2. MAP** | By **Update 1 (30%)** | AI interview; Role Map with evidence (said, documented, suggested); she confirms it; AI compares it with her job description and asks about missing duties; every duty gets an owner on every date. Plus a quick test: can the AI understand a change like "Tania is away for three weeks"? | She describes her job in Banglish, Shetu finds a duty she forgot, she confirms her Role Map |
| **3. HOLD** | Between Update 1 and Update 2 | AI proposes who covers each duty; rules check workload; manager approves. Manager types a change in plain words; AI understands it; rules find what is affected; AI proposes a new plan; manager approves | The "Tania" example end to end |
| **4. Check** | By **Update 2 (60%)** | Decision log visible; all AI measurements running; permission tests | MAP and HOLD on two cases in different languages, plus our first AI test results |
| **5. FIT** | After Update 2 | She states her return needs; rules find time clashes; AI proposes fixes; manager approves; HR approval list. Then extras if time allows, the hourglass chart first | Her return plan with zero open issues |
| **6. Finish** | By the **final (100%)** | Fix bugs; full browser tests; security checks; documentation | All three stages on a new case, typed live; tests passing; GitHub history; AI results |
| **7. Report** | Lab 12 | The written project report | |

**Why this order:** the two things most likely to go wrong are the AI's quality on Banglish and understanding changes in plain words. So both are tested before Update 1, not left to the end. FIT comes last because it reuses what HOLD already built, so it is the safest part to simplify if time runs short.

## 8. How we check the AI works

We write fake test cases in Bangla, English and Banglish, each with a correct answer written in advance. Then we measure things like: how many real duties the AI found, how many it made up, and whether it refuses questions it cannot answer.

We have **no results yet**. We will never claim real-world accuracy from fake test data.

## 9. How we work as a team

- Everyone uses their **own GitHub account**. One teammate has already created the repository.
- One task = one Issue = one branch = one Pull Request. Another teammate reviews it before it joins `main`. `main` must always work.
- Each person owns one feature **from start to finish**, including its tests, and must be able to explain it.
- Four work areas (not assigned yet): frontend, backend and database, AI and evaluation, testing and documentation.
- No fake or tiny commits just to raise numbers.
- We keep three files in the repo: `AI-USAGE.md` (where we used AI tools), `CODE-EXPLANATION.md` (how the code works), `CONTRIBUTIONS.md` (who did what).
- **Shared memory for our AI tools.** We all code with AI, and each AI only knows what it reads. So the repo holds `AGENTS.md` (the briefing every AI reads first) and `docs/PROJECT-STATE.md` (what is done, in progress and next). **Every pull request must add a short worklog note and update the project state.** Start every session by pulling `main` and telling your AI to read those files. These files are at the root of our repository.
- Claude is a **mentor and helper**. It explains, suggests and reviews. We write, understand and commit our own code.

## 10. For the presentation on 15 November

The faculty asked for: clean slides (Canva or PPTX, full-screen), an elevator pitch, clear features, a USP, a clear architecture and tech stack, all members present, full formal dress with formal shoes and belt.

Ready now: the Excel sheet draft, fully filled (`04-Workbook-Submission-Draft.xlsx`), and the slide deck (`05-Shetu-Proposal-Deck.pptx`): 10 slides, about 6 to 7 minutes, no appendix. A suggested split of slides between the four of us is in the pitch pack, section 7.2.

**Elevator pitch (30 seconds):**

> When someone goes on maternity leave, her work has to pass to others and come back to her later, and today nobody manages that properly. Shetu's AI interviews her in Bangla, English or Banglish, builds an evidence-backed map of her real job, and finds the duties nobody listed. It plans who takes each duty and when, re-plans when a colleague becomes unavailable or a deadline moves, and plans her return around the arrangement she needs. AI proposes, rules check, people decide.

## 11. What we still need to decide

**Before 15 November**

1. Review the slide deck and send corrections.
2. Paste the Excel draft into the faculty's Google Sheet.
3. Decide who presents which slide, and rehearse.

**Before we start coding**

4. Which hosted AI can we get a key for?
5. Each member's skills and free time, so we can assign the four areas
6. The GitHub repository link, and what is already in it
7. The report format and the dates of the two updates (ask the instructor)

Already decided: the direction, the core features and the roadmap (agreed 12 November), the team name and members, and FastAPI with React.

No coding starts until the team says so.

## 12. Where to find the details

| File | What is inside |
|---|---|
| `01-Investigation-Report.md` | Everything in full: audit of the old prototype, AI design, costs, hourglass, scope, roadmap, evaluation, team workflow |
| `02-Requirements-Traceability-Checklist.md` | Every requirement from the faculty and from us, with its status |
| `03-Pitch-Preparation-Pack.md` | All presentation and Excel content, and the slide plan |
| `04-Workbook-Submission-Draft.xlsx` | The faculty Excel sheet, filled in as a draft |
| `05-Shetu-Proposal-Deck.pptx` | The slides for 15 November (10 slides; a PDF copy sits beside it) |
| `reference/` | Course documents, competition materials, logos, and the old prototype code |
| `README.md`, `AGENTS.md` | Start-here guide for people, and context for AI assistants opening this folder |
| `CHANGELOG.md` | What changed between versions |
