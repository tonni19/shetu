# Shetu Update 1 plan

**Checkpoint:** Sunday, 29 November 2026, as confirmed by Ahmad on 22 November. The time and submission details still need checking. **Status:** Implementation plan drafted. Ownership, scope choices and instructor answers below are proposed for the team to confirm.

## First: the 10 to 15% progress presentation, Thursday 26 November 2026 (online)

The faculty's requirements, as Ahmad received them: present project progress at 10 to 15%; GitHub should be set up; the teams hold group discussions to get a better idea of the features; **every team member must be present**. The time and the exact format are unconfirmed.

**It is not clear how this relates to the 29 November date below.** Ahmad has given both dates. Treat 26 November as the next hard deadline, and the 29 November scope (the whole MAP slice) as the target after it. Confirm with the faculty which one is the "Update 1" checkpoint.

**What "10 to 15%" means for us.** We have no percentage rule from the faculty, so we show only what exists and say what it is. Planning, the proposal and the GitHub set-up are done. The new part is a running foundation and the first thin slice of MAP.

**What can honestly be shown on 26 November (screen share from a laptop, with a recorded backup):**
1. **GitHub set up** (already true): private repository with all four members, protected `main`, pull requests with real reviews, Issues, worklog and decision records, AI-use log, the learning guide online.
2. **A running skeleton:** the FastAPI backend and the React/Vite frontend start on every member's laptop; a seeded synthetic account signs in; the employee opens a leave case that comes from SQLite through the API.
3. **The AI gateway with replay:** one Banglish interview answer goes in and a draft Role Map duty comes out with the employee's own quote as evidence, validated by Pydantic. Say clearly that this run is a labelled replay unless a provider was really called.
4. **Tests that pass:** pytest for the evidence check and the access check (a colleague gets 403), run by CI on a pull request.
5. **The group discussion:** each member says what they own and one decision from the discussion (the niche answer, embeddings yes or no, who owns what). The decisions go in `docs/DECISIONS.md` the same day.

**Not on 26 November:** the manager coverage screen, the second case, Selenium flows, a live model comparison, HOLD, FIT. They stay in the plan for 29 November and later.

| By | What |
|---|---|
| **Mon 23 Nov (today)** | Confirm owners and the shared contract (case, duty, assignment). Write one Issue per owner. Everyone clones the repository and checks they can run Python and Node. |
| **Tue 24 Nov** | Backend skeleton merged: health route, seeded accounts, sign-in, `GET /api/cases/{id}` with a permission check. Frontend skeleton merged: login screen and the case page. Gateway interface with the replay adapter and one fixture. First pytest run in CI. |
| **Wed 25 Nov** | The frontend reads the real case from the API. The interview reply route returns draft duties with evidence (replay). Evidence and 403 tests pass. Rehearse the demo twice, record a backup video, agree who says what. |
| **Thu 26 Nov** | Present, online. Everyone attends. Each member shows or explains their own part. Afterwards: update the project state and decisions the same day. |

**Who does what for 26 November** (proposed, matching the ownership table below):
- **Tonni:** the React/Vite shell, the sign-in screen and the case page, in the Shetu look.
- **Ahmad:** the FastAPI/SQLite skeleton, seeded accounts, sign-in and permissions, the case route and the interview route; joins the pieces and runs the demo.
- **Mahadi:** the AI gateway with the replay adapter, the first prompt and its Pydantic schema, one fixture for the Banglish answer.
- **Nazha:** pytest set-up, the evidence and access tests, the CI workflow, and the first three synthetic cases with answer keys.

If time runs short, protect this order: (1) sign-in and a case from the API, (2) the replay interview returning a duty with evidence, (3) a passing test run. Cut anything else.

## What to tell the instructor

**Why maternity first?** Shetu is for planned long absences. Maternity leave is our first design case because it exercises preparation, extended cover and a return that may need new arrangements. The same workflow can handle study leave with different dates and duties. We can show that with two synthetic cases using the same code, and the app can work without a field for the reason for leave.

**Where is the niche?** The unit of work is a leave case. The employee confirms a map of what they actually do, the manager approves who covers each duty and when, and the team accounts for what changed before the employee returns. The manager runs the process, the employee confirms what the job involves, and HR oversees it.

**Why use Shetu alongside a work planner or chatbot?** The signal is the evidence and the checks. The interview can surface work nobody entered as a task. Shetu keeps the source, asks the employee to verify it, checks for a gap in cover, and records who approved the plan. In Update 1, demonstrate that a missing owner prevents approval. Later, compare the pre-leave Role Map with what comes back and ask for explicit agreement if a duty stays elsewhere.

**How do tokens and vectors fit?** A hosted model tokenizes the interview text internally. An embedding represents a passage as a vector so we can compare meaning across wording and languages. For Update 1, send the short job description alongside the interview and check the evidence behind the model's output. Track token use by language when the provider reports it. If the baseline misses paraphrased matches, test whether embeddings improve recall on the same synthetic cases without adding false matches. Any match still needs a source and human confirmation.

## What the Congress version teaches us

**Disclosure.** The Congress build is a separate, public repository made by Team Anomaly for the AI Builders Congress 2026 (created 19 November, so after our proposal). It uses Next.js and PostgreSQL, so it is a different stack from this lab project. Our proposal answers say "a one-case prototype from the GP FutureMakers competition"; they did not mention the Congress build. The team decides how to tell the instructor (see the Q&A answer in the pitch pack). The lab project stays a new build in this repository, and anything adapted from Congress is credited in the worklog.

The Congress build at `34c08bb` has synthetic maternity and study cases, an adaptive interview, an evidence-tagged Role Map, checked cover proposals, change reports and a return guard. Its request flow is a useful model. A route checks permissions, a service handles the use case, the gateway validates the AI response, and plain Python rules check it before a transaction saves the result and its audit event. Its 31 local API and rule tests passed in replay mode with temporary SQLite on 22 November. The public frontend and API health endpoint responded too. The live interview was outside this check. [Congress repository](https://github.com/SpicyFalcon619/shetu-congress) · [Congress demo](https://shetu-congress.vercel.app/)

| Bring into the lab design | Where to look in Congress | Lab decision for this checkpoint |
|---|---|---|
| One question at a time, work stated in the user's language, confirmation before cover | `apps/api/src/shetu_api/ai/prompts/` and `services.py` | Make the missing job-description duty explicit. Link a documented duty to the actual source line. Check a claimed quote against employee turns, and keep the employee's ability to confirm or dismiss it. |
| Code checks dated cover and approval | `domain/rules.py` and `routes.py` under `apps/api/src/shetu_api/` | Start with a small manager form, known colleague IDs, date coverage and human-confirmed effort. Keep AI cover proposals for HOLD. |
| Return guard and decision history | `check_return` in `domain/rules.py` and the return functions in `services.py` | Build a real before/after comparison later. FIT in the lab still has to check time clashes. Congress exercises its return route with a demo fast-forward helper. |
| Repeatable test runs | `apps/api/tests/` and `apps/api/fixtures/replay/` | Use clearly labeled, case-specific responses for Selenium and replay. Evaluate live model quality separately. |

Write the lab implementation in FastAPI, SQLAlchemy, SQLite and React/Vite with pytest and Selenium. The Congress persona header identifies a demo user by a caller-supplied value. The lab should establish identity through sign-in and enforce both role and case access on the server. Congress also lets its extractor estimate hours and can clear coverage when approving a change. For the lab, keep unknown effort unknown until a person supplies it, and validate replacement coverage before committing a future HOLD change. Treat the Congress app, stack, tests and deployment as reference material and credit any adapted idea or code in the relevant worklog.

## What has to run on 29 November

1. A synthetic employee signs in and opens their leave case. They answer a short adaptive interview, including a Banglish answer. The Role Map shows a real quote from their reply and a follow-up about a duty found in the synthetic job description. The employee can confirm or dismiss items.
2. A manager opens the confirmed map and assigns cover for a date range. Leave one day uncovered first. The API blocks approval and the UI shows which duty and date need cover. Fix the gap, approve, and reload to show that the plan and approval persisted.
3. A cover colleague who can see their assignments gets HTTP 403 if they try to approve the plan. The manager can see confirmed duties and their checked sources. Keep raw interview text out of the manager view and persist only validated work evidence for the first slice. Use synthetic data throughout and keep personal reasons and medical or family details out of fields, fixtures and logs.
4. Open a second synthetic case, for study leave, through the same MAP flow. Show a short alternate test if the demo slot is tight. Have a labeled replay ready if the hosted model is unavailable. Only describe a run as live if it actually called a provider.

**First engineering agreement.** Freeze a small shared contract before separate branches diverge. The case has employee and manager IDs and a leave window. A duty has a title, evidence type, quote or job-description reference where applicable, and a separate confirmation state. A cover assignment has a confirmed duty ID, colleague ID and date range. Use ISO dates and propose inclusive ranges, then test the first day, last day and a one-day gap. Pydantic validates shape, Python validates references and rules, and SQLite records the approved changes. Known work estimates come from structured human input.

This is a starting API sketch for the issue, with names and payloads open for review.

| Action | Proposed route and fields |
|---|---|
| Sign in and open a case | `POST /api/login` with a seeded account, then `GET /api/cases/{case_id}` with a server-established session. The employee sees the draft Role Map and the manager sees confirmed duties. |
| Answer the interview | `POST /api/cases/{case_id}/interview/reply` with a short sequence of labelled interview turns kept in memory by the employee's page. Return the next question and the draft duties. Validate quotes against employee turns only. The API provides numbered job-description lines to the model and checks returned line IDs and source excerpts. Save verified duty evidence in SQLite without saving the raw conversation. |
| Resolve a proposed duty | `PATCH /api/cases/{case_id}/duties/{duty_id}` with `decision` set to `confirm` or `dismiss`. Return the updated duty. A human confirmation is recorded separately from the original evidence type. |
| Check and approve cover | `PUT /api/cases/{case_id}/cover` with assignments containing `duty_id`, `colleague_id`, `start_date` and `end_date`. Return the draft and findings. `POST /api/cases/{case_id}/cover/approve` rechecks the stored draft before committing. For a gap, return HTTP 409 with findings containing a code, the duty ID and the first uncovered date. |

**Evidence for the checkpoint.** Add six synthetic cases with an answer key, two each in Bangla, English and Banglish. Include a planted missing duty, a misleading or absent quote and a case with no gap. Use pytest for evidence, approval, date boundaries and permissions. Use Selenium for employee confirmation and manager gap rejection followed by approval. When a live provider is available, compare candidates on the same inputs and report the actual number of cases, duties found, invented duties, verified quotes and missed-duty questions. Aim for at least one fresh live Banglish run and one quick HOLD change-parsing spike. HOLD re-planning, FIT, dashboards, voice, uploads and integrations come after the MAP checkpoint.

## Proposed ownership

Agreed by Ahmad on 23 November 2026; the other three members still need to confirm it. Each person owns a working feature, its tests, and a short explanation of it. **Primary** means one person is responsible for it; others can and should help.

| Person | Primary: owns, tests and explains | Helps with |
|---|---|---|
| **Sadia Noman Tonni** | **Frontend and UI/UX.** The React/Vite app: design and layout, sign-in screen, the employee MAP screen (interview, evidence labels, confirm and dismiss), and the manager coverage screen with its error states. Connects every screen to the real API | Ahmad on the API calls and the shared contract; Nazha on the Selenium flows |
| **Ahmad Maruf Hossain** | **Full stack.** The FastAPI and SQLite foundation: database tables, seeded sign-in, roles and case-level permissions, the routes in the contract below, the approval transaction and audit events. Wires the frontend, rules and AI together, owns the demo script, and follows one request from the screen to the database | Mahadi on calling the gateway from the routes; Tonni on the API; everyone's pull requests |
| **Mohammad Mahadi Hasan** | **AI.** The AI gateway with replay and one hosted adapter once chosen, the interview questions, evidence extraction and reference checks, and the model comparison on the synthetic cases. Next: HOLD change understanding | Nazha on writing the synthetic cases and answer keys; Ahmad on wiring the gateway into the routes |
| **Nazha Tarannum Roza** | **Rules and quality.** The plain-Python rules (dated coverage, date boundaries, approval checks), pytest, Selenium, the CI run on every pull request, and the six synthetic cases with answer keys. Next: FIT's return-time clash check | Tonni on Selenium for the screens; Mahadi on the cases; Ahmad on calling the rules from the routes |

**Review rotation (starting point):** Ahmad reviews Tonni's and Mahadi's pull requests, Tonni reviews Nazha's, Nazha and Mahadi review Ahmad's. Each person opens their own pull request under their own account and explains it to the reviewer. Have one short walkthrough where each owner explains their module, then one where Ahmad traces a complete request from the React screen to the database and back. Ask each owner to explain one failure case live.

## Working backward from Sunday

| By | What should be demonstrable |
|---|---|
| **Mon 23 Nov** | Confirm owners. Agree the minimal case/duty/assignment contract and write the four issue descriptions from the table above. Check the presentation time and submission instructions. |
| **Tue 24 Nov** | Everyone can run the FastAPI and Vite shells. Seed one case and accounts. Demo sign-in and one round trip from the UI to the API with replay. Start fixtures and CI in parallel. |
| **Wed 25 Nov** | Interview, evidence, missing-duty follow-up and confirmation work against SQLite. Try the first live Banglish case and record the result or its blocker. |
| **Thu 26 Nov** | Manager screen can show a failed coverage check, correct the gap and approve. Verify the forbidden approval and the second case. |
| **Fri 27 Nov** | Run pytest and Selenium. Record the first evaluation counts, attempt the small HOLD parsing spike, and record what ran live versus in replay. |
| **Sat 28 Nov** | Rehearse from a clean checkout, assign speaking parts, and preserve a labeled replay backup. Fix failing core checks before adding presentation polish. |
| **Sun 29 Nov** | Show the fresh MAP case, the rejected then approved plan, a brief study-leave example, and the test evidence. Acknowledge any checkpoint item that remains unfinished. |

If the schedule slips, protect the interview-to-confirmation and failed-then-approved cover path. Keep the second case short and report any incomplete evaluation or spike. Avoid trading away evidence, permissions or coverage checks to add more screens.

## Notes for the next session

Start with [AGENTS.md](../AGENTS.md), [PROJECT-STATE.md](PROJECT-STATE.md), this plan and [DECISIONS.md](DECISIONS.md), then the Issue for the work. As of this planning pass, the lab has no application implementation. The suggested first Issue is **Start the FastAPI/SQLite app and seed a signed-in employee case**. Ahmad is the proposed owner. Acceptance is a locally runnable API with a seeded case, authenticated case read and a pytest check for access denial. Tonni scaffolds the React/Vite app against the agreed case response in parallel, and Mahadi starts the gateway with replay. `docs/CODE-EXPLANATION.md` starts with the first code. Record confirmed roles and evidence of real contributions in `CONTRIBUTIONS.md` as work lands.

Use one GitHub Issue, branch and peer-reviewed PR per task. Each owner adds a [worklog](worklog/README.md), updates the project state, explains their module, and adds their actual AI use and human verification to [AI-USAGE.md](../AI-USAGE.md). Record an agreed product or design decision in [DECISIONS.md](DECISIONS.md) and update the corresponding lesson in the learning guide. The guide's embeddings lesson used to say the team will use embeddings; it now says the team may, and will test first. Keep the spoken answer conditional until there is a decision.

For Claude Code, the immediate instruction is: **Read the files above, tell me what is verified, explain the proposed API contract back to me, and start only the agreed Issue. After each change, walk me through data flow, one failure, and what we actually tested.**
