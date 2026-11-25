# Shetu backend (FastAPI + SQLite)

The API that the React app talks to. Owner: Maruf (board row T1). How it works, file by file: [`docs/CODE-EXPLANATION.md`](../docs/CODE-EXPLANATION.md).

## Run it (first time)

From the `backend/` folder. You need Python 3.11 or newer.

```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements-dev.txt
python -m app.seed                 # creates backend/shetu.db with the synthetic people and cases
uvicorn app.main:app --reload      # http://127.0.0.1:8000
```

Then open http://127.0.0.1:8000/docs for the interactive API page (FastAPI makes it from the code), or http://127.0.0.1:8000/healthz to check it is up.

If you use `uv`: `uv venv .venv` then `uv pip install -p .venv -r requirements-dev.txt`.

## Run the tests

```bash
python -m pytest -q
```

Every test uses its own temporary database, so your `shetu.db` is never touched.

## Demo accounts (synthetic)

All passwords are `shetu-demo`. Nobody here is a real person.

| User id | Name | Role | Can read |
|---|---|---|---|
| `u-nusrat` | Nusrat Jahan | employee | `case-1` (her own) |
| `u-sabbir` | Sabbir Rahman | employee | `case-2` (his own) |
| `u-shirin` | Shirin Akter | manager | `case-1`, `case-2` |
| `u-farhana` | Farhana Islam | hr | every case |
| `u-tania`, `u-rafiq`, `u-imran` | cover colleagues | colleague | no case yet (403) |

**To try the interview** (replay mode): sign in as `u-sabbir` (employee of `case-2`, who starts with an empty Role Map) and POST this to `/api/cases/case-2/interview/reply` from the interactive page at `/docs`:

```json
{"turns": [{"role": "assistant", "text": "Apnar sprotahik kaj ki ki?"},
           {"role": "employee", "text": "Protiti Tuesday sondha 6 ta theke 7:30 porjonto credit pre-meeting hoy"}]}
```

The answer says `"mode": "replay"`: it is a recorded reply, not a live model, and must be called that in any demo.

## Routes so far

| Route | What it does |
|---|---|
| `GET /healthz` | `{"status": "ok", "database": "ok"}` when the API and database are up |
| `POST /api/login` | body `{"user_id": "...", "password": "..."}`; sets the session cookie; returns the user |
| `POST /api/logout` | clears the session |
| `GET /api/me` | the signed-in user, or 401 |
| `GET /api/cases` | the cases you may read (each with `employee_name` and `manager_name`, no duties); an empty list if none |
| `POST /api/cases/{case_id}/interview/reply` | the employee's interview: send `{"turns": [...]}`, get the next question and the Role Map (every duty, with evidence); only the case's employee may call it |
| `PATCH /api/cases/{case_id}/duties/{duty_id}` | the employee confirms or dismisses a duty (`{"decision": "confirm"\|"dismiss"}`); audited |
| `GET /api/cases/{case_id}` | the case, its two names and its duties; 401 if signed out, 403 if not allowed, 404 if unknown |

Errors always look like `{"code": "forbidden", "detail": "You are not allowed to see this case."}`.

## For the React app (Tonni, T2)

Use a Vite proxy, so the browser sees one address and the session cookie just works. In `frontend/vite.config.js`:

```js
server: { proxy: { "/api": "http://127.0.0.1:8000", "/healthz": "http://127.0.0.1:8000" } }
```

Then call `fetch("/api/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ user_id, password }) })`. Without the proxy, add `credentials: "include"` to every `fetch`.

## Settings

| Environment variable | Default | Meaning |
|---|---|---|
| `SHETU_DATABASE_URL` | `sqlite:///./shetu.db` | where the database file lives |
| `SHETU_SECRET_KEY` | a development key (a warning is printed) | signs the session cookie; set a real one for any deployment |
| `SHETU_CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | browser origins allowed without the proxy |

If you change a table in `app/models.py`, delete `shetu.db` and run `python -m app.seed` again (no migration tool yet).

**After you pull new code, run `python -m app.seed` again.** It only adds what is missing, so it is safe. Without it, an older `shetu.db` has no job description lines, and the interview route answers `502 unknown_source_line`. (The server creates new tables by itself; the seed fills them.)
