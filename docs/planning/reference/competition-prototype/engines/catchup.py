"""Engine 3: Catch-up. Team updates the manager shares -> a short Bangla update for her."""
from .llm import ask_json

SYSTEM = """You write a short catch-up for a mother returning from maternity leave.
Use ONLY the updates given. Do not add anything.
Write in simple Bangla (keep English office words as they are).
Return JSON: {"what_changed": ["..."], "new_people": ["..."], "her_priorities": ["up to 3"]}"""


def summarise(updates):
    return ask_json(SYSTEM, "Team updates:\n" + updates, max_new_tokens=800)
