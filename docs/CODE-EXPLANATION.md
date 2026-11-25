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

### Known limits (on purpose, for now)
- Cover colleagues cannot read any case yet; they will see their own assignments once assignments exist.
- The manager sees every duty; after the interview exists, the manager should see confirmed duties only.
- No migration tool: change a table, then delete `shetu.db` and re-seed.
- The session key has a development default; set `SHETU_SECRET_KEY` for any deployment.

---

## Evidence rules R1 and R2 (board row T4, owner: Nazha)

Written by Nazha (PR #21); the explanation below is a short summary by Maruf. Nazha: please add your own words and any examples you want to show the instructor.

- **Where:** `backend/app/rules/evidence.py`. Tests: `backend/tests/test_evidence.py`.
- **R1, `check_quote(quote, employee_turns)`:** true only if the quote really appears in something the *employee* said. It first normalises Unicode (NFC) and collapses extra spaces, so the same Bangla word written two different ways still matches.
- **R2, `counts_as_fact(duty)`:** a duty that was only *suggested* counts as a fact only after a person confirms it; a dismissed duty never counts. Also available as `can_count`.
- **Plain Python, no AI:** the model never decides these. They have no database or web imports, so they are easy to test.
- **Used by:** the interview route (Maruf, T5), which will call R1 on each duty the AI extracts and downgrade a "said" duty whose quote fails the check to "suggested".

---

## Guards that keep the project consistent (Maruf)

`backend/tests/test_conventions.py` runs with every test run and in CI. It fails if: a file imports `backend...` instead of `app...`; `backend/__init__.py` exists; a source file lacks the standard header; or a model or schema gains a reason-for-leave style field. `.gitattributes` and `.github/CODEOWNERS` do the same job for line endings, shared logs and review ownership. The rules are in `AGENTS.md`.

---

## Frontend skeleton (board row T2, owner: Tonni)

Added 2026-11-25. Folder: `frontend/`. How to run it: `frontend/README.md`.

### What it does
A React app, written in TypeScript and served by Vite. A synthetic person signs in, and the app opens a leave case from the real backend (`GET /api/cases/case-1`) and shows its leave dates, its stage (Map, Hold, Fit) and its Role Map: every duty with its evidence and its confirmation. It reads only; confirming and dismissing duties come with the interview screen (T6). No AI runs in the browser.

### The files, and why each exists

| File | Job | One line to remember |
|---|---|---|
| `vite.config.ts` | Dev server and the **proxy** to the backend | One address for the browser, so the cookie just works |
| `src/api/types.ts` | The contract's shapes (`Case`, `Duty`, `User`) as TypeScript types | The checker refuses a field that does not exist, or a forgotten null |
| `src/api/client.ts` | The only place that calls `fetch` | Every failure becomes one `ApiError` with `{code, detail}` |
| `src/session.tsx` | Who is signed in, for the whole app | Asks the server (`GET /api/me`); stores nothing in the browser |
| `src/App.tsx` | The routes and the sign-in guard | Signed out? Go to `/sign-in`, then come back |
| `src/pages/SignInPage.tsx` | Sign-in form and demo-account buttons | Both use the real `POST /api/login` |
| `src/pages/CasePage.tsx` | One case, or the right error screen | 401 sign in again, 403 not allowed, 404 not found |
| `src/components/DutyCard.tsx` | One duty: evidence and confirmation, kept apart | "Suggested" is worded as a question |
| `src/format.ts` | Dates in words and the number of leave days | Computed by code, the same on every laptop |
| `src/styles.css` | The Shetu look | Same colours and font as the learning guide |

### How one request travels: the employee opens their case
1. The browser loads `http://localhost:5173`. `src/session.tsx` calls `GET /api/me`. Vite's proxy forwards it to the backend on port 8000.
2. Nobody is signed in yet, so the backend answers **401**. The guard in `src/App.tsx` sends the browser to `/sign-in` and remembers the page it wanted.
3. The person clicks "Nusrat Jahan". The app sends `POST /api/login` with the user id and the demo password. The backend checks the password hash and answers with the user, and sets a **signed, HttpOnly session cookie**. The browser keeps the cookie; JavaScript cannot read it.
4. The app goes to `/cases/case-1`. `src/pages/CasePage.tsx` calls `GET /api/cases/case-1`; the browser sends the cookie along automatically.
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
- *What stops a cover colleague from seeing a case?* The server. `GET /api/cases/{id}` answers 403 and the page only reports it. Hiding a button is not security (`AGENTS.md` rule 9).
- *Why does "suggested" look different?* It is an AI guess. It is shown as a question, in amber with a dashed border, and it does not count until the employee confirms it (rule R2).
- *Why "Unknown" and not 0 hours?* Unknown stays unknown until a person fills it in; the AI never guesses it.
- *Why compute the number of days in code?* Dates are computed by code, never by the model (`AGENTS.md` rule 3). The code reads the year, month and day itself, because JavaScript's default date parsing can show the day before in some time zones.
- *How was it tested?* With the type checker, a production build, and a browser run of each flow against the real backend: sign-in, wrong password, the case, 403, 404, sign-out, an expired session, phone width. The browser run found a bug: after a deliberate sign-out, the next person was sent to the previous person's last page. It is fixed. The checks are listed in the worklog.

### Known limits (on purpose, for now)
- **No names for the employee or manager on the case page.** The contract has only `employee_id` and `manager_id`. The page shows "You" or the id. Names need a contract change (asked on the team board).
- **No "list my cases" route.** After sign-in the app opens a fixed demo case (`firstCaseFor` in `src/demoAccounts.ts`). The server still checks access on every read.
- **No automated frontend tests yet.** Vitest is proposed in the Issue for T2. Selenium flows are planned (Nazha).
- **The font:** the app asks for Plus Jakarta Sans and falls back to Segoe UI when it is not installed. Shipping the font file with the app is a possible follow-up.
