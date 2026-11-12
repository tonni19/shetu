"""Ask-the-Handover: the cover person asks, Shetu answers ONLY from her approved handover.

Two safety gates before an answer is shown:
 1. Retrieval gate: if no passage is close enough to the question, answer "not in handover".
 2. Citation gate: the model must cite passage ids it was given; an answer with no valid
    citation is replaced by "not in handover".
Unanswered questions go to the manager, never to the mother.
"""
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer

from .llm import ask_json

EMB_ID = "intfloat/multilingual-e5-small"
TOP_K = 4
MIN_SIMILARITY = 0.80  # e5 cosine scores sit roughly 0.7-0.9; calibrated in eval/

_etok = _emod = None


def _embed(texts):
    global _etok, _emod
    if _emod is None:
        _etok = AutoTokenizer.from_pretrained(EMB_ID)
        _emod = AutoModel.from_pretrained(EMB_ID).eval()
    batch = _etok(texts, padding=True, truncation=True, max_length=256, return_tensors="pt")
    with torch.no_grad():
        out = _emod(**batch).last_hidden_state
    mask = batch["attention_mask"].unsqueeze(-1)
    vec = (out * mask).sum(1) / mask.sum(1)
    return F.normalize(vec, dim=-1)


SYSTEM = """You answer a colleague's question about a mother's job while she is on maternity leave.
You may use ONLY the handover passages given. Each passage has an id.
- If the passages answer the question, answer in one or two short sentences and list the ids you used.
  Answer in English, unless the question is written in Bangla script; then answer in Bangla script.
- If they do not clearly answer it, set "answerable" to false. Do not guess. Do not use outside knowledge.
Return JSON: {"answerable": true/false, "answer": "", "cited_ids": ["..."]}"""


REWRITE = """Rewrite the user's question as one plain English question. It may be written in English, in
Bangla script, or in Bangla typed with Roman letters. Romanized Bangla question words:
kobe = when, kothay = where, ke = who, kake = whom, koto = how much, kokhon = at what time,
ki bhabe / kivabe = how, keno = why, ki = what. Example: "kake bolbo" = "whom should I tell".
Keep names, systems and numbers exactly. Do not answer it. Return JSON: {"english": ""}"""


def answer(question, passages, manager="the manager"):
    if not passages:
        return _not_found(manager, [], 0.0)
    english = ask_json(REWRITE, question, max_new_tokens=100).get("english") or question
    q = _embed(["query: " + english])
    p = _embed(["passage: " + x["text"] for x in passages])
    sims = (q @ p.T)[0]
    order = sims.argsort(descending=True)[:TOP_K].tolist()
    top = [dict(passages[i], score=round(float(sims[i]), 3)) for i in order]
    best = top[0]["score"]
    if best < MIN_SIMILARITY:
        return _not_found(manager, top, best, gate="retrieval")

    ctx = "\n".join(f"[{x['id']}] {x['text']}" for x in top)
    r = ask_json(SYSTEM, f"Passages:\n{ctx}\n\nQuestion: {question}\n(In English: {english})", max_new_tokens=300)
    valid = {x["id"] for x in top}
    cited = [c for c in (r.get("cited_ids") or []) if c in valid]
    if not r.get("answerable") or not cited:
        return _not_found(manager, top, best, gate="citation")
    return {
        "answered": True,
        "answer": r.get("answer", "").strip(),
        "understood_as": english,
        "sources": [x for x in top if x["id"] in cited],
        "retrieved": top,
        "best_score": best,
    }


def _not_found(manager, top, best, gate="retrieval"):
    return {
        "answered": False,
        "answer": f"This is not in her handover. The question has been sent to {manager}. "
                  "She will not be contacted.",
        "sources": [],
        "retrieved": top,
        "best_score": best,
        "gate": gate,
    }
