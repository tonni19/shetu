# FILE:        eval/test_eval_cases.py
# PURPOSE:     Validate synthetic cases (T7) against docs/API-CONTRACT.md and rules R1/R2.
# OWNER:       Nazha (board row T7)
# DEPENDS ON:  eval/loader.py, docs/API-CONTRACT.md; uses STUB(T4) fallback until T4 merges to main
# USED BY:     Local pytest and CI once merged
# STATUS:      PARTIAL: uses inline STUB(T4) rule fallback until PR #19 (T4) merges to main
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     Once T4 is merged to main, replace the STUB(T4) fallback import with direct
#              `from backend.app.rules.evidence import check_quote, counts_as_fact`.

import unicodedata
from eval.loader import load_all_cases

try:
    from backend.app.rules.evidence import check_quote, counts_as_fact
except ImportError:
    # STUB(T4): inline mirror of R1 and R2 while T4 PR #19 awaits merge to main
    def check_quote(quote: str, employee_turns: list[str]) -> bool:
        if not isinstance(quote, str) or not quote.strip() or not employee_turns:
            return False
        norm_quote = " ".join(unicodedata.normalize("NFC", quote).split())
        return any(
            norm_quote in " ".join(unicodedata.normalize("NFC", t).split())
            for t in employee_turns
            if isinstance(t, str) and t.strip()
        )

    def counts_as_fact(duty: dict) -> bool:
        if duty.get("confirmation") == "dismissed":
            return False
        if duty.get("evidence_type") == "suggested":
            return duty.get("confirmation") == "confirmed"
        return duty.get("evidence_type") in ("said", "documented")


REQUIRED_CASE_KEYS = {"id", "employee_id", "manager_id", "leave_start", "leave_end", "stage"}
REQUIRED_DUTY_KEYS = {
    "id",
    "case_id",
    "title",
    "evidence_type",
    "quote",
    "source_line_id",
    "confirmation",
    "hours_per_week",
}


def test_three_synthetic_cases_exist_and_match_contract():
    cases = load_all_cases()
    assert len(cases) >= 3

    for item in cases:
        case_obj = item["case"]
        assert set(case_obj.keys()) == REQUIRED_CASE_KEYS
        assert "leave_reason" not in case_obj
        assert case_obj["stage"] == "map"

        jd_ids = {line["line_id"] for line in item["job_description_lines"]}
        employee_turns = [t["text"] for t in item["turns"] if t["role"] == "employee"]
        assert len(employee_turns) >= 1

        duties = item["answer_key"]["duties"]
        fact_ids = []

        for duty in duties:
            assert set(duty.keys()) == REQUIRED_DUTY_KEYS
            assert duty["case_id"] == case_obj["id"]
            assert duty["hours_per_week"] is None

            if duty["evidence_type"] == "said":
                assert duty["quote"] is not None
                assert check_quote(duty["quote"], employee_turns) is True
            elif duty["evidence_type"] == "documented":
                assert duty["source_line_id"] in jd_ids
                if duty["quote"] is not None:
                    assert check_quote(duty["quote"], employee_turns) is True
            elif duty["evidence_type"] == "suggested":
                assert duty["quote"] is None

            if counts_as_fact(duty):
                fact_ids.append(duty["id"])

        assert fact_ids == item["answer_key"]["expected_fact_ids"]


def test_forbidden_assistant_quotes_are_rejected_by_r1():
    for item in load_all_cases():
        employee_turns = [t["text"] for t in item["turns"] if t["role"] == "employee"]
        for bad_quote in item["answer_key"]["forbidden_quote_substrings"]:
            assert check_quote(bad_quote, employee_turns) is False
