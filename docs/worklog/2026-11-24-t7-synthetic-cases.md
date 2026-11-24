# T7: First three synthetic cases with answer keys (`eval/`)

- Author: Nazha Tarannum Roza
- Branch: feature/t7-synthetic-cases
- Date: 2026-11-24

## What I did
Created the first three synthetic evaluation cases with answer keys in `eval/cases/` (`case_01_english_branch_ops.json`, `case_02_banglish_it_support.json`, and `case_03_bangla_accounts.json`), along with `eval/README.md`, `eval/loader.py`, and schema/rule validation tests in `eval/test_eval_cases.py`.

## Why
Mahadi's AI gateway replay fixtures (T3) and the rules test suite need three deterministic, gender-neutral, privacy-safe cases covering English, Banglish, and Bangla inputs against the `Case` and `Duty` schemas in `docs/API-CONTRACT.md`.

## How it works
Each JSON file defines a `Case` (`stage: "map"`, no leave reason), numbered `job_description_lines`, interview `turns` (`assistant` and `employee`), and an `answer_key` with expected `Duty` objects (`documented`, `said`, and unconfirmed `suggested` items) plus `expected_fact_ids` and `forbidden_quote_substrings`. `eval/test_eval_cases.py` validates every field against `docs/API-CONTRACT.md` and checks R1 (`check_quote`) and R2 (`counts_as_fact`).

## How I tested it
Ran `python3 -m pytest eval/test_eval_cases.py -v`; both validation tests passed.

## Not finished / known problems
- **Stub used:** `STUB(T4)` in `eval/test_eval_cases.py` provides an inline fallback for `check_quote` and `counts_as_fact` while PR #19 (T4) awaits review and merge into `main`. Once T4 merges, remove the inline fallback and import directly from `backend.app.rules.evidence`, and add `eval` to `testpaths` in `pytest.ini`.

## AI assistance
Gemini helped draft the three synthetic JSON scenarios (`eval/cases/`), `eval/loader.py`, and `eval/test_eval_cases.py` against `docs/API-CONTRACT.md`. I checked the schema fields, privacy rules, and Bangla/Banglish text, and ran `pytest` locally.
