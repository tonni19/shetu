# FILE:        backend/app/ai/schemas.py
# PURPOSE:     The data shapes that go into and come out of the AI gateway, checked by Pydantic.
# OWNER:       Mahadi (board row T3)
# DEPENDS ON:  docs/API-CONTRACT.md (Duty shape, section 1; ExtractResult, section 3).
# USED BY:     backend/app/ai/gateway.py, backend/app/ai/adapters.py, backend/tests/test_gateway.py;
#              the interview route (Maruf, T5) reads ExtractResult.
# STATUS:      REAL
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     Every model here forbids extra fields (extra="forbid"). That is deliberate: it is how
#              rule 5 is enforced. If a model reply contains a "reason" field, or anything else we did
#              not ask for, validation fails and the reply is thrown away. Do not loosen this.
# AI NOTE:     A DraftDuty is NOT a full Duty. It has no id, case_id, confirmation or hours_per_week.
#              The route adds id, case_id and confirmation="pending". hours_per_week is only ever
#              filled in by a person (contract), so the model is not allowed to return it.

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

# CONTRACT: the three evidence types in docs/API-CONTRACT.md, Duty table.
EvidenceType = Literal["said", "documented", "suggested"]


class GatewayError(Exception):
    """Raised when the gateway cannot give back a validated result.

    It carries the same two fields as the contract's Error shape ({"code", "detail"}) so a route can
    turn it into a response without inventing text. `code` is a stable machine word (for example
    "invalid_reply"); `detail` is one human sentence. Raw model text is never put in `detail`.
    """

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


class Turn(BaseModel):
    """One message in the interview. Only `employee` turns can be quoted as evidence."""

    model_config = ConfigDict(extra="forbid")

    role: Literal["assistant", "employee"]
    text: str


class JdLine(BaseModel):
    """One numbered line of the (synthetic) job description, so a duty can point at its source."""

    model_config = ConfigDict(extra="forbid")

    id: str  # for example "jd-2"; becomes Duty.source_line_id
    text: str


class DraftDuty(BaseModel):
    """A duty the model proposes. It is a draft: a person must still confirm it.

    The evidence fields must agree with the evidence type (AGENTS.md rule 1):
      said       -> `quote` is required (the employee's exact words); no source_line_id
      documented -> `source_line_id` is required (a job description line); no quote
      suggested  -> neither: it is only a question for the employee, never a fact
    """

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=120)
    evidence_type: EvidenceType
    quote: str | None = Field(default=None, max_length=500)
    source_line_id: str | None = None

    @model_validator(mode="after")
    def evidence_fields_match_type(self) -> "DraftDuty":
        if self.evidence_type == "said":
            if not self.quote or not self.quote.strip():
                raise ValueError("a 'said' duty needs the employee's exact quote")
            if self.source_line_id is not None:
                raise ValueError("a 'said' duty must not carry a source_line_id")
        elif self.evidence_type == "documented":
            if not self.source_line_id:
                raise ValueError("a 'documented' duty needs a source_line_id")
            if self.quote is not None:
                raise ValueError("a 'documented' duty must not carry a quote")
        else:  # suggested
            if self.quote is not None or self.source_line_id is not None:
                raise ValueError("a 'suggested' duty is only a question: no quote, no source_line_id")
        return self


class ModelReply(BaseModel):
    """Exactly what we ask the model to return, and nothing more.

    `mode` is deliberately absent: whether a run was replay or live is decided by the adapter, so the
    model can never claim to be live. Any extra field in the reply makes validation fail.
    """

    model_config = ConfigDict(extra="forbid")

    next_question: str = Field(min_length=1, max_length=500)
    duties: list[DraftDuty]


class ExtractResult(BaseModel):
    """What `extract_duties` returns to the route.

    CONTRACT: matches `{"next_question": "...", "duties": [...]}` of the interview reply route, plus
    `mode`, so a demo can say plainly whether the answer came from a recorded replay or a live model.
    """

    model_config = ConfigDict(extra="forbid")

    mode: Literal["replay", "live"]
    next_question: str
    duties: list[DraftDuty]
