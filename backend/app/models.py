# FILE:        backend/app/models.py
# PURPOSE:     The database tables, written as Python classes (SQLAlchemy ORM).
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  app/db.py (Base); docs/API-CONTRACT.md section 1 (the Case and Duty shapes)
# USED BY:     app/routes/*, app/security.py, app/seed.py, tests; later the rules (Nazha, T4)
#              and the interview route (Maruf, T5)
# STATUS:      PARTIAL: User, Case, Duty, JobDescriptionLine and AuditEvent exist. Cover assignments
#              come later. Cover assignments and the audit log come later
#              (T5 adds the audit event).
# DATA:        Synthetic only. There is NO column for the reason for leave, and none may be added
#              (AGENTS.md rule 5). No medical or family details anywhere.
# AI NOTE:     Field names follow docs/API-CONTRACT.md exactly. Renaming one is a shared-interface
#              change: follow "Changing a shared interface" in AGENTS.md.

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

# The four kinds of user. Kept as plain strings so they read clearly in the database and in JSON.
ROLES = ("employee", "manager", "hr", "colleague")


class User(Base):
    """A person who can sign in. `role` decides what they may see (see app/security.py)."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(20))  # one of ROLES
    # SECURITY: only a salted hash is stored, never the password itself (app/security.py).
    password_hash: Mapped[str] = mapped_column(String(200))


class Case(Base):
    """One planned leave of one employee. CONTRACT: docs/API-CONTRACT.md, "Case"."""

    __tablename__ = "cases"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    manager_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    leave_start: Mapped[date] = mapped_column(Date)  # inclusive
    leave_end: Mapped[date] = mapped_column(Date)  # inclusive
    stage: Mapped[str] = mapped_column(String(10), default="map")  # "map" | "hold" | "fit"

    duties: Mapped[list["Duty"]] = relationship(back_populates="case", order_by="Duty.id")
    # The two people, so a screen can show a name instead of an id. `foreign_keys` says which column
    # each one follows, because a Case has two links to the users table.
    employee: Mapped["User"] = relationship(foreign_keys=[employee_id])
    manager: Mapped["User"] = relationship(foreign_keys=[manager_id])


class Duty(Base):
    """One duty in the employee's Role Map. CONTRACT: docs/API-CONTRACT.md, "Duty".

    `evidence_type` says where the duty came from; `confirmation` says what a person decided.
    They are separate on purpose: a "suggested" duty that the employee confirmed is still
    honest about having started as a suggestion (rule R2, owned by Nazha in T4).
    """

    __tablename__ = "duties"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    title: Mapped[str] = mapped_column(String(200))
    evidence_type: Mapped[str] = mapped_column(String(12))  # "said" | "documented" | "suggested"
    quote: Mapped[str | None] = mapped_column(Text, nullable=True)  # the employee's exact words
    source_line_id: Mapped[str | None] = mapped_column(String(40), nullable=True)  # job description line
    confirmation: Mapped[str] = mapped_column(String(12), default="pending")  # "pending" | "confirmed" | "dismissed"
    # None means "unknown". AI NOTE: only a person fills this in, never the model.
    hours_per_week: Mapped[float | None] = mapped_column(Float, nullable=True)

    case: Mapped[Case] = relationship(back_populates="duties")


class JobDescriptionLine(Base):
    """One numbered line of a case's (synthetic) job description, so a duty can point at its source.

    The AI gateway receives these lines with each interview answer; a "documented" duty must cite
    one of their ids (`line_id`, for example "jd-3"), or the gateway rejects the reply.
    """

    __tablename__ = "job_description_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    line_id: Mapped[str] = mapped_column(String(20))  # "jd-1", "jd-2", ... becomes Duty.source_line_id
    position: Mapped[int] = mapped_column(Integer)  # order within the job description
    text: Mapped[str] = mapped_column(Text)


class AuditEvent(Base):
    """A permanent record of one human decision: who did what to which duty, and when.

    Only decisions are recorded here (confirm or dismiss). It never holds interview text, and there
    is no reason-for-leave field (AGENTS.md rule 5). The full audit log and the HR view come later.
    """

    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(30))  # "duty_confirmed" | "duty_dismissed"
    duty_id: Mapped[str | None] = mapped_column(ForeignKey("duties.id"), nullable=True)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

