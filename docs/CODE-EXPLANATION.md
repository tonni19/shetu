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

Added 2026-11-24. Code: `backend/app/rules/evidence.py`. Tests: `backend/tests/test_evidence.py`.

### Why these rules exist
Shetu builds a Role Map from what an employee says in an interview. An AI model drafts the duties, and a model can invent things, including a "quote" the employee never said. A Role Map is only useful if the manager can trust it. So two small rules, written as ordinary code, sit between the AI and the map. The AI proposes, the rules check, and a person confirms.

### R1: `check_quote(quote, employee_turns)`
**Question it answers:** did the employee really say this?

It returns `True` only if the quote appears inside at least one reply the employee typed.

How it works:
1. It rejects an empty or whitespace-only quote, and an empty list of turns.
2. It normalises both the quote and each reply. Unicode is converted to NFC, and runs of spaces, tabs and line breaks are collapsed to one space.
3. It checks whether the normalised quote is inside any normalised reply.

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

