# FILE:        eval/test_eval_cases.py
# PURPOSE:     Validate synthetic cases (T7) against docs/API-CONTRACT.md and rules R1/R2.
# OWNER:       Nazha (board row T7)
# DEPENDS ON:  eval/loader.py, backend/app/rules/evidence.py, docs/API-CONTRACT.md
# USED BY:     Local pytest and CI (.github/workflows/ci.yml)
# STATUS:      REAL
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     Imports real R1/R2 rules directly from backend.app.rules.evidence.

from app.rules.evidence import check_quote, counts_as_fact
from eval.loader import load_all_cases


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
