# 2026-11-28 — Harden R1 (`check_quote`) with casefolding and minimum word length (T4)

- **Owner:** Nazha (`NazhaTarannum`)
- **Branch:** `feature/t4-quote-check-hardening`
- **What changed:**
  - Updated `_normalize_text` in `backend/app/rules/evidence.py` to apply `.casefold()` after NFC Unicode normalization and whitespace collapsing, so Banglish and English quotes match regardless of capitalization.
  - Added `MIN_QUOTE_WORDS = 3` in `backend/app/rules/evidence.py` so single-word or two-word fragments (such as `"kori"`) are rejected by `check_quote`.
  - Added `test_check_quote_ignores_case_for_banglish_and_english` and `test_check_quote_rejects_quotes_shorter_than_three_words` in `backend/tests/test_evidence.py`.
  - Updated `docs/CODE-EXPLANATION.md`, `docs/TEAM-BOARD.md`, and `AI-USAGE.md`.
- **Verification:** `python -m pytest -v` passes all 82 tests (including T5 interview route tests and T7 synthetic eval cases).
