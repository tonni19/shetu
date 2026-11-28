# Code Explanation

How the code works, in plain words, one module at a time. Every member must be able to explain their own modules to the instructor; this file is where they learn and where their AI assistant looks first. **Update the section for a module in the same pull request that changes it** (`AGENTS.md`).

---

## Backend skeleton (board row T1, owner: Maruf)

Added 2026-11-23. Folder: `backend/`. How to run it: `backend/README.md`.

### What it does
A FastAPI app with a SQLite database. Synthetic people can sign in, and a leave case can be read by the people allowed to see it. Nothing here uses AI; it is the foundation the AI parts plug into.

### The files, and why each exists

| File | Job | One line to remember |
|---|---|---|
| `app/main.py` | Builds the app: database, session cookie, CORS, error format, routes | The front door; everything is wired here |
| `app/config.py` | Reads settings from environment variables | No secret ever lives in code |
| `app/db.py` | Connects to SQLite; gives each request its own database session | One request, one session, always closed |
| `app/models.py` | The tables: `User`, `Case`, `Duty` | Names match `docs/API-CONTRACT.md`; no reason field |
| `app/schemas.py` | The JSON shapes in and out (Pydantic) | A promise to the frontend |
| `app/security.py` | Password hashing, "who is signed in", "may this person see this case" | Every permission decision lives here |
| `app/errors.py` | Makes every error `{"code", "detail"}` | The frontend shows any error the same way |
| `app/routes/health.py` | `GET /healthz` | Is the API up and can it reach the database |
| `app/routes/auth.py` | Sign in, sign out, who am I | The cookie remembers you |
| `app/routes/cases.py` | `GET /api/cases/{id}` | 404 if unknown, 403 if not yours |
| `app/seed.py` | Puts the synthetic cast into the database | Same data on every laptop |
| `tests/` | 16 tests with pytest | Each test gets a fresh temporary database |

### How one request travels: the employee opens her case

1. The browser sends `GET /api/cases/case-1` with the **session cookie** it got at sign-in.
2. **SessionMiddleware** checks the cookie's signature with the secret key and reads `user_id` from it. A user cannot change the id, because changing it breaks the signature.
3. FastAPI sees the route needs `current_user` and `get_db` (**dependencies**). `get_db` opens a database session; `current_user` loads the user, or stops with **401** if nobody is signed in.
4. The route loads the case. Unknown id: **404** `case_not_found`.
5. `can_read_case(user, case)` decides: the employee of the case, its manager, and HR may read; everyone else gets **403** `forbidden`.
6. The route returns the SQLAlchemy `Case` object. FastAPI turns it into JSON using `CaseOut` (`response_model`), so only the fields in the contract leave the server. The password hash, for example, can never leak this way.
7. `get_db` closes the database session.

### Which parts are AI and which are ordinary code
All of it is ordinary code. The AI gateway (Mahadi, T3) and the rules (Nazha, T4) will be called from the interview route (Maruf, T5), which is built next.

### Words to know
- **Dependency (FastAPI):** a function a route asks for in its parameters (`Depends(...)`); FastAPI runs it first and passes the result in. We use it for "the database session" and "the signed-in user".
- **Session cookie:** a small piece of data the server gives the browser at sign-in. Ours is **signed**, so the browser can hold it but not change it.
- **Password hash (PBKDF2 with a salt):** we never store a password. We store a one-way scramble of it plus a random salt, and compare scrambles at sign-in.
- **ORM (SQLAlchemy):** tables as Python classes; `db.get(Case, "case-1")` instead of writing SQL.
- **response_model:** the Pydantic shape FastAPI uses to filter and check what a route sends back.

### What an instructor might ask, and the answer
- *Where are permissions checked?* In `app/security.py`, on the server, for every request. The frontend hiding a button is not security.
- *Can a user pretend to be someone else?* No. The user id comes from a cookie signed by the server, not from anything the caller sends.
- *Why do a wrong user id and a wrong password give the same error?* So nobody can find out which accounts exist.
- *Why is there no reason-for-leave field?* By design (rule 5): Shetu never asks why someone is away.
- *Why `hours_per_week` can be empty?* Unknown stays unknown until a person fills it in; the AI never guesses it.
- *How do you know it works?* `python -m pytest`: 16 tests, including 401, 403 and 404 cases, each on a fresh database.

### Update 2026-11-25: names and the case list
Tonni's frontend (Issue #28) asked for two things, so a screen can show people and not just ids:
- **Display names.** `Case` now has two *relationships* (`employee` and `manager`) that point at the `User` table, and `GET /api/cases/{id}` returns `employee_name` and `manager_name`. Only the name leaves the server, never the role or the password hash. A `Case` has two links to `users`, so each relationship says which column it follows (`foreign_keys=[employee_id]`).
- **`GET /api/cases`.** Returns the cases the signed-in user may read. It uses the **same** `can_read_case` function as reading one case, so the list can never show a case the user cannot open (a test checks this). A cover colleague gets an empty list, not an error, because "nothing to show" is not a mistake.
- **Shape.** `CaseSummaryOut` is the row (names, dates, stage). `CaseOut` is the summary plus the duties.

### Known limits (on purpose, for now)
- Cover colleagues cannot read any case yet; they will see their own assignments once assignments exist.
- The manager sees every duty; after the interview exists, the manager should see confirmed duties only.
- No migration tool: change a table, then delete `shetu.db` and re-seed.
- The session key has a development default; set `SHETU_SECRET_KEY` for any deployment.

---

## Evidence rules R1 and R2 (board row T4, owner: Nazha)

Added 2026-11-24. Code: `backend/app/rules/evidence.py`. Tests: `backend/tests/test_evidence.py`.

### Why these rules exist
Shetu builds a Role Map from what an employee says in an interview. An AI model drafts the duties, and a model can invent things, including a "quote" the employee never said. A Role Map is only useful if the manager can trust it. So two small rules, written as ordinary code, sit between the AI and the map. The AI proposes, the rules check, and a person confirms.

### R1: `check_quote(quote, employee_turns)`
**Question it answers:** did the employee really say this?

It returns `True` only if the quote appears inside at least one reply the employee typed.

How it works:
1. It rejects an empty or whitespace-only quote, and an empty list of turns.
2. It normalises both the quote and each reply: Unicode is converted to NFC, runs of spaces, tabs and line breaks are collapsed to one space, and `.casefold()` is applied so case differences in English or Banglish do not cause false mismatches.
3. It requires at least `MIN_QUOTE_WORDS = 3` words in the normalised quote so a stray single word like `"kori"` cannot pass on its own.
4. It checks whether the normalised quote is inside any normalised reply.

**Why only `employee` turns?** The assistant's own questions and the job description also contain words. If they were allowed, the AI could "prove" a quote by pointing at its own text. Evidence has to come from the person.

**Why normalise?** Bangla text can be stored in two ways: one composed character, or a base character plus a mark (NFC and NFD). They look identical but are different strings, so a plain comparison would wrongly fail. The test `test_check_quote_normalizes_bangla_unicode_nfc_vs_nfd` proves the fix. Typing with extra spaces, as in Banglish replies, is handled the same way.

**Example:**
- Employee said: `Protidin   shokal 10tay inventory sheet update kori.`
- Quote `inventory sheet update kori` → `True`
- Quote `monthly tax audit` → `False` (never said, so it is rejected)

### R2: `counts_as_fact(duty)` (also exported as `can_count`)
**Question it answers:** may this duty be treated as a fact on the Role Map?

| Duty | Counts as fact? |
|---|---|
| `dismissed` (any type) | No, never |
| `suggested` and `pending` | No |
| `suggested` and `confirmed` | Yes, only after a person confirms |
| `said` or `documented`, not dismissed | Yes |
| missing or unknown `evidence_type` | No |

**Why?** A `suggested` duty is only the AI's hypothesis. It becomes a fact when a person confirms it. The duty keeps its original `evidence_type` ("suggested"), so the map stays honest about where it came from. It takes either a dict or an object.

### Which parts are AI and which are ordinary code
Both rules are ordinary Python with no AI, database or web imports. The model never decides them, and that is why they are easy to test (8 unit tests, in CI).

### Where they are used
The interview route (Maruf, T5) is planned to run R1 on each duty the AI extracts, and to use R2 whenever it counts duties as facts. Handling a `said` duty whose quote fails R1 is still to be agreed and is not in the API contract yet.

### What an instructor might ask
- *Why check quotes in code and not ask the AI to be careful?* A prompt is a request and a rule is a guarantee. The check runs every time, and a model can ignore a request.
- *Why only the employee's words?* So the AI can't use its own text as proof.
- *What does NFC mean?* A standard form for Unicode text, so the same Bangla word written two ways compares as equal.
- *Can an AI-suggested duty become a fact?* Yes, but only after a person confirms it.
- *How do you know it works?* `python -m pytest`: exact match, a made-up quote, empty input, Bangla NFC/NFD, Banglish with extra spaces, and every R2 case.

### Known limits (on purpose, for now)
- Matching is case-sensitive, so "tuesday" does not match "Tuesday".
- There is no minimum length, so a very short quote such as one word can match by accident.
- It checks that text appears, not that it means the duty.
- Planned: ignore case and add a minimum length, each with a test, agreed with Mahadi and Maruf first so the gateway fixtures still pass.

---

## Synthetic evaluation cases (board row T7, owner: Nazha)

- **Where:** `eval/cases/` (`case_01_english_branch_ops.json`, `case_02_banglish_it_support.json`, `case_03_bangla_accounts.json`), `eval/loader.py`, and `eval/test_eval_cases.py`.
- **What they test:** Three synthetic MAP interviews—one in English (Gulshan branch operations), one in Banglish (IT support), and one in Bangla (accounts payable)—with numbered job description lines (`id: "jd-1"`, etc.), interview turns, and labeled answer keys.
- **Contract and evidence checks:** `eval/test_eval_cases.py` loads every case via `eval.loader.load_all_cases()` and checks that `case` and `duty` match `docs/API-CONTRACT.md` (`hours_per_week` is `null`, no `leave_reason` field), that `said` duties carry a verified employee `quote` (R1) with `source_line_id: null`, that `documented` duties carry a valid JD `source_line_id` with `quote: null`, that `suggested` duties carry neither, and that `counts_as_fact` (R2) matches `expected_fact_ids`.

---

## Guards that keep the project consistent (Maruf)

`backend/tests/test_conventions.py` runs with every test run and in CI. It fails if: a file imports `backend...` instead of `app...`; `backend/__init__.py` exists; a source file lacks the standard header; or a model or schema gains a reason-for-leave style field. `.gitattributes` and `.github/CODEOWNERS` do the same job for line endings, shared logs and review ownership. The rules are in `AGENTS.md`.


---

## AI gateway (Mahadi, board row T3)

**Files:** `backend/app/ai/gateway.py`, `adapters.py`, `prompts.py`, `schemas.py`, the fixture `backend/app/ai/fixtures/replay/banglish_credit_pre_meeting.json`, and tests in `backend/tests/test_gateway.py`.

**What it does.** The interview route gives it the conversation so far and the numbered job description lines. It returns draft duties for the employee's Role Map, each with its evidence, and one follow-up question. It is the only door to an AI model (rule 10).

**How data flows.**
1. `extract_duties(turns, job_description_lines)` checks there is at least one employee turn.
2. `get_adapter()` picks the adapter from the environment variable `SHETU_AI_MODE`. The default is `replay`. `live` is refused for now, because no provider is chosen.
3. `build_prompts` makes the system prompt (fixed rules for the model) and the user prompt (the job description lines, then the interview).
4. The adapter returns raw text. The replay adapter reads it from the JSON fixture, matching on a phrase from the employee's answer.
5. `_parse_reply` turns the text into JSON and validates it against `ModelReply`. Anything that is not exactly the asked-for shape is thrown away as `invalid_reply`.
6. The gateway checks that every `documented` duty points at a line id that was really given.
7. It returns an `ExtractResult` whose `mode` comes from the adapter, never from the model.

**Which parts are AI and which are ordinary code.** Only the adapter's `complete` call is "AI" (and in replay mode it is a recorded reply). Everything else is plain Python: the prompt builder, the JSON parsing, the Pydantic validation, and the line-id check.

**Rules it protects.**
- Rule 1: a `said` duty must carry a quote, a `documented` duty a source line, a `suggested` duty neither.
- Rule 5: replies with any extra field, such as "reason", are rejected.
- Rule 10: replies are validated before anyone sees them. Error messages never repeat the raw reply.
- Rule 11: prompts and fixtures use neutral wording; a test checks it.

**What it does not do.** It does not check that a quote is really in the employee's words. That is rule R1 (`check_quote`, Nazha, `backend/app/rules/evidence.py`), which the route calls. It does not store anything, and it does not decide whether a duty counts: a person confirms each one.

**Not real yet.** There is no live adapter (provider not chosen), so every run is a labelled replay. The fixture has one recorded reply, for one Banglish answer.

**Questions an instructor might ask.**
- *Why a replay adapter?* Real models answer differently each time and need a key and a network. A recorded reply makes tests and offline demos repeatable, and it is labelled as a replay so it is never passed off as live.
- *What stops the AI inventing a quote?* The gateway rejects a `said` duty with no quote. The route then runs rule R1, which checks that the quote really appears in what the employee typed.
- *What if the model returns rubbish?* The gateway raises `GatewayError("invalid_reply")` and nothing from the reply is kept.
- *How would you add a real model?* Write one more adapter in `adapters.py` that sets `mode = "live"`. Nothing else changes, because validation is in the gateway.

---

## Frontend skeleton (board row T2, owner: Tonni)

Added 2026-11-25. Folder: `frontend/`. How to run it: `frontend/README.md`.

### What it does
A React app, written in TypeScript and served by Vite. A synthetic person signs in and sees the leave cases they may read (`GET /api/cases`). Opening one reads it from the real backend (`GET /api/cases/{id}`) and shows the names, its leave dates, its stage (Map, Hold, Fit) and its Role Map: every duty with its evidence and its confirmation. It reads only; confirming and dismissing duties come with the interview screen (T6). No AI runs in the browser.

### The files, and why each exists

| File | Job | One line to remember |
|---|---|---|
| `vite.config.ts` | Dev server and the **proxy** to the backend | One address for the browser, so the cookie just works |
| `src/api/types.ts` | The contract's shapes (`Case`, `Duty`, `User`) as TypeScript types | The checker refuses a field that does not exist, or a forgotten null |
| `src/api/client.ts` | The only place that calls `fetch` | Every failure becomes one `ApiError` with `{code, detail}` |
| `src/session.tsx` | Who is signed in, for the whole app | Asks the server (`GET /api/me`); stores nothing in the browser |
| `src/App.tsx` | The routes and the sign-in guard | Signed out? Go to `/sign-in`, then come back |
| `src/pages/SignInPage.tsx` | Sign-in form and demo-account buttons | Both use the real `POST /api/login` |
| `src/pages/CaseListPage.tsx` | The cases this person may read | The server chooses the list; a colleague's is empty |
| `src/pages/CasePage.tsx` | One case, or the right error screen | 401 sign in again, 403 not allowed, 404 not found |
| `src/components/DutyCard.tsx` | One duty: evidence and confirmation, kept apart | "Suggested" is worded as a question |
| `src/format.ts` | Dates in words and the number of leave days | Computed by code, the same on every laptop |
| `src/styles.css` | The Shetu look | Same colours and font as the learning guide |

### How one request travels: the employee opens their case
1. The browser loads `http://localhost:5173`. `src/session.tsx` calls `GET /api/me`. Vite's proxy forwards it to the backend on port 8000.
2. Nobody is signed in yet, so the backend answers **401**. The guard in `src/App.tsx` sends the browser to `/sign-in` and remembers the page it wanted.
3. The person clicks "Nusrat Jahan". The app sends `POST /api/login` with the user id and the demo password. The backend checks the password hash and answers with the user, and sets a **signed, HttpOnly session cookie**. The browser keeps the cookie; JavaScript cannot read it.
4. The app goes to `/`. `src/pages/CaseListPage.tsx` calls `GET /api/cases`, and the server answers with only the cases this person may read (for the employee, their own). Clicking a case goes to `/cases/case-1`, and `src/pages/CasePage.tsx` calls `GET /api/cases/case-1`. The browser sends the cookie with every call automatically.
5. The backend checks the cookie, then `can_read_case` (the employee, the manager and HR may read). It answers with the case as JSON in the shape of `CaseOut`.
6. The page draws it. `src/format.ts` turns `2027-01-10` into "10 January 2027" and counts the days (both ends included). Each duty goes to `DutyCard`.

### Which parts are AI and which are ordinary code
All of it is ordinary code. The screens show what the backend sends. The AI's work (the gateway, T3) will reach the screens through the interview route (T5) and the interview screen (T6). Even then the browser never calls a model: every model call goes through the backend gateway (`AGENTS.md` rule 10).

### Words to know
- **Component:** a function that returns part of the screen (`DutyCard`, `StageSteps`).
- **State:** a value a component remembers between drawings (`useState`), for example "loading" or "loaded".
- **Effect:** code that runs after drawing (`useEffect`); we use it to fetch the case.
- **Context:** a value shared with every component below it, without passing it by hand. We use it for the signed-in user (`SessionProvider`).
- **Route:** which page belongs to which address (`/cases/:caseId`).
- **Proxy:** Vite forwards `/api` calls to the backend, so the browser sees one site.
- **TypeScript type:** a description of a value's shape. The checker (`npm run typecheck`) compares the code with it before the app runs.

### What an instructor might ask, and the answer
- *Why TypeScript?* The screens and the API must agree on every field. `src/api/types.ts` copies the contract. If a screen uses a field that does not exist, such as a reason for leave, or forgets that `hours_per_week` can be `null`, `npm run typecheck` fails before anyone runs the app. We tried this on purpose, and both mistakes were caught.
- *Where is the password or session stored in the browser?* Nowhere that JavaScript can reach. The server keeps the session in a signed, HttpOnly cookie. The app uses no localStorage or sessionStorage.
- *What stops a cover colleague from seeing a case?* The server. Their list from `GET /api/cases` is empty, and if they type a case address, `GET /api/cases/{id}` answers 403. The page only reports what the server decided. Hiding a button is not security (`AGENTS.md` rule 9).
- *Why does "suggested" look different?* It is an AI guess. It is shown as a question, in amber with a dashed border, and it does not count until the employee confirms it (rule R2).
- *Why "Unknown" and not 0 hours?* Unknown stays unknown until a person fills it in; the AI never guesses it.
- *Why compute the number of days in code?* Dates are computed by code, never by the model (`AGENTS.md` rule 3). The code reads the year, month and day itself, because JavaScript's default date parsing can show the day before in some time zones.
- *How was it tested?* With the type checker, a production build, and a browser run of each flow against the real backend: sign-in, wrong password, the case list for each role, the case, 403, 404, sign-out, an expired session, phone width. The browser run found a bug: after a deliberate sign-out, the next person was sent to the previous person's last page. It is fixed. The checks are listed in the worklog.

### Known limits (on purpose, for now)
- **No automated frontend tests yet.** Vitest is proposed in the Issue for T2. Selenium flows are planned (Nazha).
- **The font:** the app asks for Plus Jakarta Sans and falls back to Segoe UI when it is not installed. Shipping the font file with the app is a possible follow-up.

---

## The interview route (board row T5, owner: Maruf)

Added 2026-11-26. Code: `backend/app/routes/interview.py`. Tests: `backend/tests/test_interview.py` (20). This is where the three parts meet: **Mahadi's AI gateway proposes, Nazha's rules check, and the employee decides.**

### What it does
Two routes, both only for the employee of the case:
- `POST /api/cases/{id}/interview/reply`: the browser sends the conversation so far. The route returns the next question and the Role Map (every duty of the case, each with its evidence).
- `PATCH /api/cases/{id}/duties/{duty_id}`: the employee confirms or dismisses one duty. Each decision writes one audit event.

### How one reply travels
1. **Who is asking?** `current_user` reads the signed cookie. The route then checks the user is *the employee of this case*. A manager, HR or a colleague gets **403**, even though they may read the case.
2. **The job description.** The route loads the case's numbered job description lines from the database (`jd-1`, `jd-2`, ...).
3. **The AI proposes.** It calls `gateway.extract_duties(turns, lines)`. The gateway validates the answer's shape and returns *drafts*, or raises `GatewayError`. Today this is a recorded **replay**, so the response says `mode: "replay"`.
4. **Rule R1 checks.** For every duty marked "said", `check_quote` asks: are these exact words in something the *employee* typed? If not, the duty is not trusted: it becomes "suggested" (a question) and its title goes into `downgraded`.
5. **Saved as pending.** New duties are stored with `confirmation: "pending"`. A duty with the same title is not stored twice. A duty the employee already confirmed or dismissed is never changed or brought back. The raw interview text is **not stored**: only the verified quote, inside its duty.
6. **Rule R2 counts.** `counts_as_fact` decides which duties count as facts. A "suggested" duty only counts after the employee confirms it. The response carries `fact_count`.
7. **The employee decides.** Confirming a duty sets `confirmation: "confirmed"` and writes an `AuditEvent` (who, what, when). Nothing becomes a fact on its own.

### AI or ordinary code?
Only step 3 is AI (and today even that is a recording). Steps 1, 2, 4, 5, 6 and 7 are ordinary code. That is the whole product idea: **AI proposes, rules check, people decide.**

### Why it is built this way (questions an instructor may ask)
- *Why not trust the model's quote?* A model can invent a quote. R1 checks it against the employee's real words, and a failure downgrades the duty instead of hiding it, so nothing silently disappears and nothing false is trusted.
- *Why doesn't the route store the conversation?* It is sensitive and not needed: only the evidence behind each duty is kept (privacy by design).
- *Why can a manager not answer for the employee?* The Role Map is the employee's own account of their job, and nothing counts until they confirm it.
- *Why a 502 and not a 200 when the AI fails?* The caller must know no valid answer exists. The error says our own sentence, never the model's text.
- *Why "replay"?* No hosted model is chosen yet. A recorded answer makes tests and demos repeatable, and the label stops it from being shown as live.
- *How do you know it works?* 20 tests, and each rule was proved by breaking the code on purpose: removing R1, the employee check, the audit event or the de-duplication each made tests fail.

### Words to know
- **Draft duty:** what the model returns: a title, an evidence type, a quote or a source line. It is not yet a duty of the case.
- **Downgrade:** a "said" duty with a failed quote becomes "suggested" (a question).
- **Audit event:** a permanent record of one human decision. It never holds interview text.

### Known limits (on purpose, for now)
- Replay only: one recorded answer. A live model comes when the provider is chosen.
- Each call re-reads the whole conversation; there is no "retry once" on a bad AI answer yet (the gateway's TODO).
- The manager still sees every duty; showing only confirmed duties comes with the manager screen.
- Cover assignments and the full audit log come later.

