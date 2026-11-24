# T4: Evidence validation rules (R1 and R2), pytest setup, and CI workflow

- Author: Nazha Tarannum Roza
- Branch: feature/t4-evidence-rules
- Date: 2026-11-24

## What I did
Implemented the pure-Python evidence validation module (`backend/app/rules/evidence.py`) with `check_quote` (Rule R1) and `counts_as_fact` / `can_count` (Rule R2) matching `docs/API-CONTRACT.md`. Added unit tests (`backend/tests/test_evidence.py`), pytest configuration (`pytest.ini`, `backend/requirements-dev.txt`), and a GitHub Actions CI workflow (`.github/workflows/ci.yml`).

## Why
The interview route (T5) and AI gateway tests (T3) need deterministic rules to verify that quotes actually appear in employee replies (including Bangla Unicode text) and that AI-suggested duties never count as facts unless confirmed by a person.

## How it works
Both functions are deterministic, standard-library Python functions with zero AI or database calls. `check_quote` normalizes Unicode to NFC and collapses whitespace before checking substring membership across `employee_turns` only. `counts_as_fact` inspects `evidence_type` and `confirmation` on a Duty dict or object, returning `True` for `suggested` duties only when `confirmation == "confirmed"`.

## How I tested it
Ran `python3 -m pytest -v` locally against 8 unit tests covering exact matches, hallucinated quotes, empty/whitespace inputs, Bangla NFC vs. NFD Unicode normalization, Banglish text, and R2 confirmation rules across dicts and objects.

## Not finished / known problems
Synthetic eval cases (T7) and gateway replay tests (once T3 lands) are next.

## AI assistance
Gemini helped scaffold `backend/app/rules/evidence.py`, `backend/tests/test_evidence.py`, `pytest.ini`, and `.github/workflows/ci.yml` against `docs/API-CONTRACT.md` and `AGENTS.md`. I set up the local environment, ran pytest, and reviewed the code and tests.
