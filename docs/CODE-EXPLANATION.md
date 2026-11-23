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
