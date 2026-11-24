# FILE:        backend/tests/test_conventions.py
# PURPOSE:     Automatic guards for the team's conventions (AGENTS.md, "Project layout" and
#              "Comments for the next AI"), so a mistake is caught by the test run in CI instead of
#              by a merge conflict or a confused teammate.
# OWNER:       Maruf (added with T1); Nazha owns the test set-up and CI as a whole (T4)
# DEPENDS ON:  the files under backend/app and backend/tests
# USED BY:     CI and local pytest runs
# STATUS:      REAL
# AI NOTE:     If a guard fails, fix the code, not the guard. If a rule really must change, change
#              AGENTS.md and this file in the same pull request and tell the team.

import re
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]  # the backend/ folder
SOURCES = [p for p in (BACKEND / "app").rglob("*.py")] + [p for p in (BACKEND / "tests").rglob("*.py")]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_nothing_imports_the_backend_by_its_folder_name():
    # The backend is always imported as `app...` (the name uvicorn uses). `from backend.app...`
    # works on one person's laptop and breaks the others'. This was a real merge problem on 24 Nov.
    bad = [str(p.relative_to(BACKEND)) for p in SOURCES if re.search(r"^\s*(from|import)\s+backend\b", _text(p), re.M)]
    assert not bad, f"Import as `app...`, not `backend...`: {bad}"


def test_backend_folder_is_not_a_package():
    # A backend/__init__.py would make `backend` a package and invite `from backend.app...`.
    assert not (BACKEND / "__init__.py").exists()


def test_every_non_empty_source_file_has_the_agents_md_header():
    # AGENTS.md, "Comments for the next AI": each file starts with FILE, PURPOSE, OWNER, STATUS.
    missing = []
    for p in SOURCES:
        text = _text(p)
        if not text.strip():
            continue  # empty __init__.py files are fine
        head = "\n".join(text.splitlines()[:15])
        if not all(tag in head for tag in ("# FILE:", "# PURPOSE:", "# OWNER:", "# STATUS:")):
            missing.append(str(p.relative_to(BACKEND)))
    assert not missing, f"Add the standard header (AGENTS.md) to: {missing}"


def test_no_reason_for_leave_field_in_the_models_or_schemas():
    # AGENTS.md rule 5: there is no reason field, and none may be added.
    for name in ("models.py", "schemas.py"):
        text = _text(BACKEND / "app" / name).lower()
        # Only look at code lines, so a comment that explains the rule does not trip the guard.
        code = "\n".join(line for line in text.splitlines() if not line.strip().startswith("#"))
        assert not re.search(r"\b(reason|diagnosis|medical|pregnan\w*)\b\s*[:=]", code), f"{name} must not have a reason or medical field"
