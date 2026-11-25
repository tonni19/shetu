# T1 follow-up: display names and the case list

- Author: Maruf
- Branch: `feature/t1-case-names-and-list`
- Date: 2026-11-25

## What I did
Added what Tonni's Issue #28 asked for: `employee_name` and `manager_name` on a case, and a new route `GET /api/cases` that lists the cases the signed-in user may read. Marked T7 as Done on the team board (it was left as "In review" after #24 merged) and removed Nazha's finished request.

## Why
The frontend could only show user ids, and it had to open a fixed demo case after sign-in. With names and a list it can show who the leave is for and let each person see their own cases.

## How it works
`Case` has two relationships to `User` (employee and manager). The route builds each response from the case plus those two names; only the name is copied out. The list uses the same `can_read_case` function as reading one case, so it can never show a case the user cannot open. A cover colleague gets an empty list. Explanation: `docs/CODE-EXPLANATION.md`, "Update 2026-11-25".

## How I tested it
- `python -m pytest -q`: 39 passed (30 before, 9 new: names, the list for each of the five demo users, rows without duties, sign-in needed, and "every case in my list can be opened").
- Called the real server over HTTP: Nusrat sees `case-1`, the manager sees both cases, a colleague gets `[]`, signed out gets 401, and `case-1` carries both names.

## Interface changes (contract)
`Case` gains `employee_name` and `manager_name`; new route `GET /api/cases`. Both only add things, so existing code keeps working. Logged for Tonni on the team board.

## Not finished / known problems
- The list shows no duty counts or stage detail beyond the summary fields.
- Cover colleagues still see no cases (they will see their assignments later).
- T5 (the interview route) is next.
- No stubs in this change.
