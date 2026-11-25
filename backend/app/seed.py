# FILE:        backend/app/seed.py
# PURPOSE:     Puts a small set of SYNTHETIC people and leave cases into the database, so everyone
#              can sign in and see the same thing on their laptop. Run: `python -m app.seed`
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  app/models.py, app/security.py (hash_password), app/main.py (create_app)
# USED BY:     developers, the demo, and tests (tests/conftest.py calls seed())
# STATUS:      REAL
# DATA:        Every name and date here is invented. Nobody is a real person.
#              There is NO reason for leave anywhere: case-1 is our maternity story and case-2
#              a different kind of planned leave, but the database cannot tell them apart, on
#              purpose (AGENTS.md rules 5 and 11).
# AI NOTE:     The demo password is public on purpose (it is synthetic demo data). Real accounts
#              would never be seeded like this. Running the seed twice is safe: it skips rows
#              that already exist.

from datetime import date

from sqlalchemy.orm import Session

from app.models import Case, Duty, User
from app.security import hash_password

DEMO_PASSWORD = "shetu-demo"

# (id, name, role). The cover colleagues are the cast of our slides (Tania, Rafiq, Imran).
USERS = [
    ("u-nusrat", "Nusrat Jahan", "employee"),  # case-1, the employee going on leave
    ("u-sabbir", "Sabbir Rahman", "employee"),  # case-2, a second employee, a different planned leave
    ("u-shirin", "Shirin Akter", "manager"),  # manages both cases
    ("u-farhana", "Farhana Islam", "hr"),
    ("u-tania", "Tania Akter", "colleague"),
    ("u-rafiq", "Rafiq Ahmed", "colleague"),
    ("u-imran", "Imran Hossain", "colleague"),
]

CASES = [
    ("case-1", "u-nusrat", "u-shirin", date(2027, 1, 10), date(2027, 6, 30)),
    ("case-2", "u-sabbir", "u-shirin", date(2027, 2, 1), date(2027, 3, 31)),
]

# Two sample duties so the case page has something to show before the interview (T5) exists.
# One comes from the job description, one from the employee's own words.
DUTIES = [
    ("duty-1", "case-1", "Monthly portfolio report", "documented", None, "jd-3", "pending", None),
    (
        "duty-2",
        "case-1",
        "Tuesday credit meeting",
        "said",
        "Tuesday credit meeting ta 6 tay shuru hoy, 7:30 porjonto chole",
        None,
        "pending",
        None,
    ),
]


def seed(db: Session) -> None:
    """Add the synthetic users, cases and duties that are not there yet, then commit."""
    for uid, name, role in USERS:
        if db.get(User, uid) is None:
            db.add(User(id=uid, name=name, role=role, password_hash=hash_password(DEMO_PASSWORD)))
    for cid, emp, mgr, start, end in CASES:
        if db.get(Case, cid) is None:
            db.add(Case(id=cid, employee_id=emp, manager_id=mgr, leave_start=start, leave_end=end, stage="map"))
    for did, cid, title, evidence, quote, line, conf, hours in DUTIES:
        if db.get(Duty, did) is None:
            db.add(
                Duty(
                    id=did,
                    case_id=cid,
                    title=title,
                    evidence_type=evidence,
                    quote=quote,
                    source_line_id=line,
                    confirmation=conf,
                    hours_per_week=hours,
                )
            )
    db.commit()


if __name__ == "__main__":
    # Build the app once so the tables exist and SessionLocal points at the configured database.
    from app.db import SessionLocal
    from app.main import create_app

    create_app()
    with SessionLocal() as session:
        seed(session)
    print(f"Seeded {len(USERS)} synthetic users and {len(CASES)} cases. Demo password: {DEMO_PASSWORD}")
