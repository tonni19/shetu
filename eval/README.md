# Synthetic Evaluation Cases (`eval/`)

- **Owner:** Nazha Tarannum Roza (board row **T7**)
- **Used by:** Mahadi (T3 AI gateway replay fixtures & model bake-off), Nazha (pytest eval suite)
- **Data rules:** 100% synthetic, gender-neutral, no reason for leave, no medical or family details (`AGENTS.md` rules 11–12).

## Cases

| File | Language | Role | What it tests |
|---|---|---|---|
| `cases/case_01_english_branch_ops.json` | English | Branch Operations Coordinator | Exact substring `said` quote, `documented` JD line (`JD-02`), and unconfirmed `suggested` duty |
| `cases/case_02_banglish_it_support.json` | Banglish | IT Support & Asset Coordinator | Mixed Bangla-English (`Banglish`) reply extraction, `documented` JD line (`JD-01`), and `suggested` duty |
| `cases/case_03_bangla_accounts.json` | Bangla | Accounts & Vendor Reconciliation Officer | Native Bangla script quotes (Unicode NFC/NFD safe), `documented` JD line (`JD-03`), and `suggested` duty |

## JSON Structure

Each file contains:
- `case`: Matches `Case` in `docs/API-CONTRACT.md` (`id`, `employee_id`, `manager_id`, `leave_start`, `leave_end`, `stage`).
- `job_description_lines`: Numbered `{"line_id": "JD-01", "text": "..."}` entries.
- `turns`: Conversation array `[{"role": "assistant" | "employee", "text": "..."}]`.
- `answer_key`:
  - `duties`: List of expected `Duty` dicts matching `docs/API-CONTRACT.md` (`hours_per_week` is always `null` before human entry).
  - `expected_fact_ids`: Duty IDs that must count as established facts under Rules R1 and R2.
  - `forbidden_quote_substrings`: Assistant-only phrases that must never be cited as employee `quote` evidence.
