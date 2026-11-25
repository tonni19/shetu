# FILE:        eval/loader.py
# PURPOSE:     Load and validate synthetic evaluation cases and answer keys in eval/cases/.
# OWNER:       Nazha (board row T7)
# DEPENDS ON:  docs/API-CONTRACT.md (Case and Duty shapes).
# USED BY:     eval/test_eval_cases.py; Mahadi's replay fixtures (T3)
# STATUS:      REAL
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     Keep standard-library only so both backend tests and standalone eval scripts can import it.

import json
from pathlib import Path
from typing import Any

CASES_DIR = Path(__file__).resolve().parent / "cases"


def load_all_cases(cases_dir: Path = CASES_DIR) -> list[dict[str, Any]]:
    """Load all synthetic JSON cases sorted by filename.

    Inputs:
        cases_dir: Directory containing `case_*.json` files.

    Returns:
        List of parsed case dicts, each containing `case`, `job_description_lines`,
        `turns`, and `answer_key`.

    Raises:
        FileNotFoundError: If `cases_dir` does not exist or contains no case files.
    """
    paths = sorted(cases_dir.glob("case_*.json"))
    if not paths:
        raise FileNotFoundError(f"No synthetic case files found in {cases_dir}")
    return [json.loads(p.read_text(encoding="utf-8")) for p in paths]
