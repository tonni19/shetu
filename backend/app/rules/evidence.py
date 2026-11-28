# FILE:        backend/app/rules/evidence.py
# PURPOSE:     Rules R1 and R2 for evidence: is a quote real, does a duty count as a fact.
# OWNER:       Nazha (board row T4)
# DEPENDS ON:  docs/API-CONTRACT.md (Duty shape). Nothing else; these are pure functions.
# USED BY:     backend/app/routes/interview.py (Maruf, T5); backend/tests/test_evidence.py
# STATUS:      REAL
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     Keep these pure standard-library Python functions with zero DB or HTTP imports.
#              Both `counts_as_fact` (API-CONTRACT.md) and `can_count` (TEAM-BOARD.md T4) are exported.

import unicodedata
from typing import Any

MIN_QUOTE_WORDS = 3


def _normalize_text(text: str) -> str:
    """Normalize Unicode to NFC, collapse whitespace, and casefold so Bangla and Banglish compare reliably."""
    normalized = unicodedata.normalize("NFC", text)
    return " ".join(normalized.split()).casefold()


def check_quote(quote: str, employee_turns: list[str]) -> bool:
    """R1: Verify that `quote` actually appears in at least one employee reply.

    Why it exists:
        Prevents AI-hallucinated or overly short single-word quotes from being attached to a Duty
        as employee evidence. Only `employee` turns may be passed here—never assistant prompts
        or job descriptions.

    Inputs:
        quote: Exact substring claimed by the extractor (may be empty or contain Bangla/English).
        employee_turns: List of raw reply strings spoken by the employee during the interview.

    Returns:
        True if the NFC-normalized, whitespace-collapsed, casefolded `quote` has at least
        `MIN_QUOTE_WORDS` words and appears inside any employee turn; False otherwise.
    """
    if not isinstance(quote, str) or not quote.strip():
        return False
    if not employee_turns:
        return False

    norm_quote = _normalize_text(quote)
    if len(norm_quote.split()) < MIN_QUOTE_WORDS:
        return False

    for turn in employee_turns:
        if isinstance(turn, str) and turn.strip():
            if norm_quote in _normalize_text(turn):
                return True

    return False


def counts_as_fact(duty: Any) -> bool:
    """R2: Determine whether a Duty counts as an established fact on the Role Map.

    Why it exists:
        AI-suggested duties are only hypotheses. Under rule R2, a `suggested` duty must never
        be treated as a confirmed responsibility until a person explicitly confirms it.

    Inputs:
        duty: A Duty object (Pydantic model, dataclass, or SimpleNamespace) or dict with
              `evidence_type` ("said" | "documented" | "suggested") and
              `confirmation` ("pending" | "confirmed" | "dismissed").

    Returns:
        False if `confirmation == "dismissed"`.
        True for `evidence_type == "suggested"` ONLY when `confirmation == "confirmed"`.
        True for `evidence_type` in ("said", "documented") unless dismissed.
        False for missing or unknown `evidence_type` values.
    """
    if isinstance(duty, dict):
        evidence_type = duty.get("evidence_type")
        confirmation = duty.get("confirmation")
    else:
        evidence_type = getattr(duty, "evidence_type", None)
        confirmation = getattr(duty, "confirmation", None)

    if confirmation == "dismissed":
        return False

    if evidence_type == "suggested":
        return confirmation == "confirmed"

    return evidence_type in ("said", "documented")


# Alias matching the wording in docs/TEAM-BOARD.md row T4
can_count = counts_as_fact
