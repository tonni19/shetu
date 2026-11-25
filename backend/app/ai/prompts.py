# FILE:        backend/app/ai/prompts.py
# PURPOSE:     The prompt that asks the model for draft duties, built from the interview so far.
# OWNER:       Mahadi (board row T3)
# DEPENDS ON:  backend/app/ai/schemas.py (Turn, JdLine, and the ModelReply shape the prompt asks for).
# USED BY:     backend/app/ai/gateway.py
# STATUS:      REAL
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     If you change the JSON the prompt asks for, change ModelReply in schemas.py and the
#              replay fixture in the same edit, or every reply will fail validation.
# AI NOTE:     Interview text is untrusted input. It is placed in the user message, never in the system
#              message, and the model's answer is validated no matter what the text says.

from app.ai.schemas import JdLine, Turn

# PROMPT: extract draft duties for the employee's Role Map.
#   Purpose:  turn the interview so far into draft duties with evidence, and pick one follow-up question.
#   Inputs:   the interview turns and the numbered job description lines (see build_prompts).
#   Returns:  one JSON object matching ModelReply: {"next_question": str, "duties": [DraftDuty]}.
#   If the reply is invalid (not JSON, extra field, evidence that does not fit its type): the gateway
#   raises GatewayError("invalid_reply"). Nothing from the bad reply is kept or shown.
SYSTEM_PROMPT = """You help draft a Role Map for a leave handover. You read an interview and the numbered \
lines of a job description. Reply with ONE JSON object and nothing else, in exactly this shape:

{"next_question": "<one short question>",
 "duties": [{"title": "<short name>", "evidence_type": "said|documented|suggested",
             "quote": "<text or null>", "source_line_id": "<id or null>"}]}

Rules:
- "said": the employee described this duty. "quote" must be copied EXACTLY, character for character, \
from one employee message. "source_line_id" must be null.
- "documented": the duty appears in a job description line. "source_line_id" is that line's id. \
"quote" must be null.
- "suggested": you think a duty may be missing and want to ask about it. It is a question, not a fact. \
"quote" and "source_line_id" must both be null.
- Never add other fields. Do not return hours, dates or times: people fill those in.
- Never ask about, guess or write the reason for the leave, or any health or family detail.
- Use neutral wording: "the employee" or "they".
- "next_question" asks about ONE thing still missing, in the language the employee used (Bangla, English \
or Banglish).
- If you find no duties, return an empty "duties" list."""


def build_prompts(turns: list[Turn], job_description_lines: list[JdLine]) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) for one extraction call.

    `turns` is the interview so far, oldest first. `job_description_lines` may be empty. The user
    prompt lists the job description lines with their ids first, then the interview, so the model can
    cite a line id for a "documented" duty and quote an employee message for a "said" duty.
    """
    if job_description_lines:
        jd_block = "\n".join(f"[{line.id}] {line.text}" for line in job_description_lines)
    else:
        jd_block = "(no job description provided)"

    interview_block = "\n".join(f"{turn.role}: {turn.text}" for turn in turns)

    user_prompt = f"JOB DESCRIPTION LINES:\n{jd_block}\n\nINTERVIEW SO FAR:\n{interview_block}"
    return SYSTEM_PROMPT, user_prompt
