# T7: First three synthetic cases with answer keys (`eval/`)

- Author: Nazha Tarannum Roza
- Branch: feature/t7-synthetic-cases
- Date: 2026-11-24

## What I did
Created the first three synthetic evaluation cases with answer keys in `eval/cases/` (`case_01_english_branch_ops.json`, `case_02_banglish_it_support.json`, and `case_03_bangla_accounts.json`), along with `eval/README.md`, `eval/loader.py`, and schema/rule validation tests in `eval/test_eval_cases.py`. Merged `origin/main` after T4 landed, removed the temporary `STUB(T4)` fallback, and wired `eval` into `pytest.ini`.

## Why
Mahadi's AI gateway replay fixtures (T3) and the rules test suite need three deterministic, gender-neutral, privacy-safe cases covering English, Banglish, and Bangla inputs against the `Case` and `Duty` schemas in `docs/API-CONTRACT.md`.

## How it works
Each JSON file defines a `Case` (`stage: "map"`, no leave reason), numbered `job_description_lines`, interview `turns` (`assistant` and `employee`), and an `answer_key` with expected `Duty` objects (`documented`, `said`, and unconfirmed `suggested` items) plus `expected_fact_ids` and `forbidden_quote_substrings`. `eval/test_eval_cases.py` validates every field against `docs/API-CONTRACT.md` and imports `check_quote` (R1) and `counts_as_fact` (R2) directly from `backend.app.rules.evidence`.

## How I tested it
Ran `python3 -m pytest -v` locally; all 10 tests (8 in `backend/tests/test_evidence.py` and 2 in `eval/test_eval_cases.py`) passed.

## Not finished / known problems
None for T7. Gateway replay tests will connect to these fixtures once T3 lands.

## AI assistance
Gemini helped draft the three synthetic JSON scenarios (`eval/cases/`), `eval/loader.py`, and `eval/test_eval_cases.py` against `docs/API-CONTRACT.md`. I checked the schema fields, privacy rules, and Bangla/Banglish text, resolved the `origin/main` merge, and ran `pytest` locally.
