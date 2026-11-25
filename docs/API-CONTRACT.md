# Shared contract: data shapes, routes and function signatures

**Status: AGREED on 2026-11-23.** Maruf accepted this contract for the whole team that day, because the team is new to this kind of design and wanted to start building. It is the shared reference now. It is still not frozen: if a real need appears, change it by the protocol in `AGENTS.md` ("Changing a shared interface"): edit this file in your own pull request, log a handoff for everyone affected, and do not merge until they have seen it.

Why this file exists: Tonni's screens, Maruf's routes, Mahadi's gateway and Nazha's rules must fit together without waiting for each other. Everyone builds against this file. If the code and this file disagree, one of them is wrong: fix it in the same pull request and tell the people listed under "Used by".

Conventions: JSON field names are `snake_case`. Dates are ISO `YYYY-MM-DD`, ranges are inclusive. IDs are strings. Everything is synthetic data. There is **no field for the reason for leave**, and none may be added.

## 1. Data shapes

### Case
| Field | Type | Notes |
|---|---|---|
| `id` | string | |
| `employee_id`, `manager_id` | string | user IDs |
| `employee_name`, `manager_name` | string | display names, read from the users table (added 2026-11-25 at the request of Issue #28) |
| `leave_start`, `leave_end` | date | inclusive; no reason field |
| `stage` | `"map"` \| `"hold"` \| `"fit"` | only `"map"` is used first |

### Duty
| Field | Type | Notes |
|---|---|---|
| `id` | string | |
| `case_id` | string | |
| `title` | string | short, in the employee's words |
| `evidence_type` | `"said"` \| `"documented"` \| `"suggested"` | **said** needs `quote`; **documented** needs `source_line_id`; **suggested** is only a question |
| `quote` | string or null | exact words from the employee's reply; checked by rule R1 |
| `source_line_id` | string or null | numbered line of the job description |
| `confirmation` | `"pending"` \| `"confirmed"` \| `"dismissed"` | set by a person, kept **separate** from `evidence_type` |
| `hours_per_week` | number or null | **null means unknown**; only a person fills it in, never the AI |

Rule: a `suggested` duty never counts as a fact until `confirmation` is `"confirmed"` (rule R2).

### Error
`{"code": "<machine_code>", "detail": "<human sentence>"}`. Not signed in returns HTTP 401 (`not_signed_in`), a wrong user id or password 401 (`invalid_credentials`), permission problems 403 (`forbidden`), a missing case 404 (`case_not_found`), a request body of the wrong shape 422 (`invalid_request`), a failed rule 409.

## 2. Routes (T1 and T5)

| Action | Route | Who may call it |
|---|---|---|
| Sign in | `POST /api/login` with `{"user_id", "password"}` for a seeded synthetic account (list in `backend/README.md`); the server sets a signed session cookie and returns `{"id", "name", "role"}` | anyone |
| Sign out | `POST /api/logout` (204) | anyone |
| Who am I | `GET /api/me` returns `{"id", "name", "role"}`, or 401 | a signed-in user |
| Health | `GET /healthz` returns `{"status": "ok", "database": "ok"}` | anyone |
| List my cases | `GET /api/cases` returns a list of case summaries (the Case fields without `duties`), only the cases this user may read: the employee's own, the manager's, every case for HR, and an empty list for a cover colleague (added 2026-11-25) | a signed-in user |
| Read a case | `GET /api/cases/{case_id}` returns the Case, including `employee_name` and `manager_name`, with a `duties` list | the employee, the manager, HR. A cover colleague gets **403** until cover assignments exist (then: only their own assignments). Anyone else gets **403** |
| Answer the interview | `POST /api/cases/{case_id}/interview/reply` with `{"turns": [{"role": "assistant"\|"employee", "text": "..."}]}`. Returns `{"next_question": "...", "duties": [Duty]}`. Quotes are checked against `employee` turns only; raw turns are **not** stored | the employee of that case |
| Confirm or dismiss a duty | `PATCH /api/cases/{case_id}/duties/{duty_id}` with `{"decision": "confirm"\|"dismiss"}`. Writes one audit event | the employee of that case |

The cover routes (`PUT .../cover`, `POST .../cover/approve`) are described in `docs/UPDATE-1-PLAN.md` and come after Thursday.

## 3. Python signatures

These let Mahadi, Nazha and Maruf write and test their parts without waiting.

```python
# backend/app/ai/gateway.py   (owner: Mahadi)  used by: routes (Maruf), tests (Nazha)
def extract_duties(turns: list[Turn], job_description_lines: list[JdLine]) -> ExtractResult:
    """Ask the model (or replay fixture) for draft duties. Always returns a validated
    ExtractResult or raises GatewayError. Never returns raw model text."""

# backend/app/rules/evidence.py   (owner: Nazha)  used by: routes (Maruf)
def check_quote(quote: str, employee_turns: list[str]) -> bool:
    """R1: True only if `quote` really appears in an employee turn, after Unicode
    normalization (so Bangla text compares correctly)."""

def counts_as_fact(duty: Duty) -> bool:
    """R2: a suggested duty counts only once a person has confirmed it."""
```

## 4. Who depends on what

| If this changes | Tell | Because |
|---|---|---|
| A Duty or Case field | everyone | all four parts read it |
| A route or its response | Tonni, Maruf | the screens call it |
| `extract_duties` or `ExtractResult` | Maruf, Nazha | routes call it, tests replay it |
| `check_quote` or `counts_as_fact` | Maruf, Mahadi | routes call them, the gateway output feeds them |

Add a row to the Handoff log in `docs/TEAM-BOARD.md` whenever you change something in this table.
