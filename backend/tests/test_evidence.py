# FILE:        backend/tests/test_evidence.py
# PURPOSE:     Unit tests for evidence validation rules R1 (check_quote) and R2 (counts_as_fact).
# OWNER:       Nazha (board row T4)
# DEPENDS ON:  backend/app/rules/evidence.py, docs/API-CONTRACT.md
# USED BY:     CI (.github/workflows/ci.yml) and local pytest runs
# STATUS:      REAL
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     Add new edge cases here whenever R1 or R2 behavior changes.

import unicodedata
from types import SimpleNamespace

from app.rules.evidence import can_count, check_quote, counts_as_fact


# --- Rule R1: check_quote ---

def test_check_quote_matches_exact_substring():
    turns = [
        "I reconcile the branch cash ledger every Thursday afternoon.",
        "Also I approve petty cash vouchers up to 5,000 BDT.",
    ]
    assert check_quote("branch cash ledger every Thursday", turns) is True


def test_check_quote_rejects_missing_or_hallucinated_quote():
    turns = ["I reconcile the branch cash ledger every Thursday afternoon."]
    assert check_quote("monthly tax audit", turns) is False


def test_check_quote_rejects_empty_and_whitespace_inputs():
    turns = ["I handle client onboarding."]
    assert check_quote("", turns) is False
    assert check_quote("   \n\t  ", turns) is False
    assert check_quote("handle client onboarding", []) is False


def test_check_quote_normalizes_bangla_unicode_nfc_vs_nfd():
    # Decomposed (NFD) vs composed (NFC) Bangla characters must match after normalization
    turn_nfc = unicodedata.normalize("NFC", "আমি প্রতি সপ্তাহে রিপোর্ট তৈরি করি।")
    quote_nfd = unicodedata.normalize("NFD", "প্রতি সপ্তাহে রিপোর্ট")

    assert turn_nfc != quote_nfd
    assert check_quote(quote_nfd, [turn_nfc]) is True


def test_check_quote_handles_banglish_and_extra_whitespace():
    turns = ["Protidin   shokal 10tay\n  inventory sheet update kori."]
    assert check_quote("inventory sheet update kori", turns) is True


def test_check_quote_ignores_case_for_banglish_and_english():
    turns = ["Protiti Tuesday sondha 6 ta theke credit pre-meeting hoy."]
    assert check_quote("protiti tuesday sondha", turns) is True
    assert check_quote("CREDIT PRE-MEETING HOY", turns) is True


def test_check_quote_rejects_quotes_shorter_than_three_words():
    turns = ["Protidin shokal 10tay inventory sheet update kori."]
    assert check_quote("kori", turns) is False
    assert check_quote("update kori", turns) is False
    assert check_quote("sheet update kori", turns) is True


# --- Rule R2: counts_as_fact / can_count ---

def test_suggested_duty_counts_only_when_confirmed():
    assert counts_as_fact({"evidence_type": "suggested", "confirmation": "pending"}) is False
    assert counts_as_fact({"evidence_type": "suggested", "confirmation": "dismissed"}) is False
    assert counts_as_fact({"evidence_type": "suggested", "confirmation": "confirmed"}) is True


def test_said_and_documented_duties_count_unless_dismissed():
    assert counts_as_fact({"evidence_type": "said", "confirmation": "pending"}) is True
    assert counts_as_fact({"evidence_type": "documented", "confirmation": "pending"}) is True
    assert counts_as_fact({"evidence_type": "said", "confirmation": "confirmed"}) is True
    assert counts_as_fact({"evidence_type": "documented", "confirmation": "dismissed"}) is False


def test_counts_as_fact_accepts_object_attributes_and_alias():
    duty_obj = SimpleNamespace(evidence_type="suggested", confirmation="confirmed")
    assert counts_as_fact(duty_obj) is True
    assert can_count(duty_obj) is True
