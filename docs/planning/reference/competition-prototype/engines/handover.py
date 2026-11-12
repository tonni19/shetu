"""Engine 1: Handover.

voice notes -> transcript (Whisper, Bangla) -> structured handover (LLM)
-> grounding check: every item must quote a line that is really in the
transcript; items whose quote cannot be found are flagged for her to check.
"""
import re
from difflib import SequenceMatcher

from .llm import ask_json

# Office words Bangladeshi professionals mix into Bangla speech.
# Given to Whisper as a hint so it spells them correctly.
OFFICE_VOCAB = (
    "Handover notes. KPI, deadline, vendor, invoice, payroll, approval, report, "
    "Excel, Google Drive, SharePoint, Outlook, email, meeting, client, budget, "
    "audit, procurement, HR, finance, manager, team lead, dashboard, follow-up."
)

_whisper = None


def transcribe(path, model_size="large-v3"):
    global _whisper
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    segments, info = _whisper.transcribe(
        path, language="bn", initial_prompt=OFFICE_VOCAB, vad_filter=True, beam_size=5
    )
    return " ".join(s.text.strip() for s in segments).strip()


def unload_whisper():
    """Free video memory before the language model loads."""
    global _whisper
    _whisper = None
    import gc, torch
    gc.collect()
    torch.cuda.empty_cache()


SECTIONS = ["recurring_tasks", "deadlines", "contacts", "systems", "file_locations", "open_issues"]

SYSTEM = """You turn a mother's spoken work notes (Bangla, English or mixed) into a structured
handover for the colleague who covers her job during maternity leave.

Rules:
- Use ONLY what the notes say. Never invent names, dates, numbers or tasks.
- If something is not mentioned, leave the list empty or write null.
- Write fields in clear English, but keep names of systems and files exactly as spoken.
- Write people's names in the usual Roman spelling and keep Bangla honorifics untranslated:
  রফিক ভাই -> "Rafiq bhai", নাসরিন আপা -> "Nasrin apa". Never write "brother" or "sister".
- Copy dates, amounts and times exactly as said. Do not convert or guess them.
- hours_per_week: a work week is 5 days, so "2 hours every day" is 10. Use null if no time was said.
- For every item, "quote" must be the exact words from the notes that support it (copy them, in the original language).

Return JSON with exactly these keys:
{
 "role_summary": "one sentence",
 "recurring_tasks": [{"task": "", "frequency": "", "when": "day/time if said, else null", "hours_per_week": number or null, "quote": ""}],
 "deadlines": [{"item": "", "date": "", "quote": ""}],
 "contacts": [{"name": "", "role": "", "contact_for": "", "quote": ""}],
 "systems": [{"name": "", "used_for": "", "quote": ""}],
 "file_locations": [{"what": "", "where": "", "quote": ""}],
 "open_issues": [{"issue": "", "next_step": "", "quote": ""}]
}"""


def _quote_found(quote, transcript):
    """Fuzzy check that the quote really appears in the transcript."""
    q = (quote or "").strip()
    if len(q) < 4:
        return 0.0
    m = SequenceMatcher(None, transcript, q, autojunk=False)
    best = m.find_longest_match(0, len(transcript), 0, len(q))
    # compare the quote with the window of transcript where its longest match sits
    lo = max(0, best.a - best.b)
    window = transcript[lo: lo + len(q) + 10]
    return SequenceMatcher(None, window, q, autojunk=False).ratio()


BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
BN_NUMBER_WORDS = {
    "এক": 1, "দুই": 2, "তিন": 3, "চার": 4, "পাঁচ": 5, "ছয়": 6, "সাত": 7, "আট": 8, "নয়": 9, "দশ": 10,
    "এগারো": 11, "বারো": 12, "তেরো": 13, "চৌদ্দ": 14, "পনেরো": 15, "ষোলো": 16, "সতেরো": 17, "আঠারো": 18,
    "উনিশ": 19, "বিশ": 20, "একুশ": 21, "বাইশ": 22, "তেইশ": 23, "চব্বিশ": 24, "পঁচিশ": 25, "ছাব্বিশ": 26,
    "সাতাশ": 27, "আঠাশ": 28, "উনত্রিশ": 29, "ত্রিশ": 30, "একত্রিশ": 31,
}
EN_NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
    "sixteen seventeen eighteen nineteen twenty".split())}


def numbers_in(text):
    """Every number in a text: digits (Latin or Bangla) and spoken number words."""
    text = (text or "").translate(BN_DIGITS)
    found = {int(n) for n in re.findall(r"\d+", text)}
    for word in re.findall(r"[ঀ-৿]+|[A-Za-z]+", text):
        lw = word.lower()
        if lw in EN_NUMBER_WORDS:
            found.add(EN_NUMBER_WORDS[lw])
        # Bangla suffixes stick to the word (ছয়টায় = at six), so match the longest prefix
        for bn in sorted(BN_NUMBER_WORDS, key=len, reverse=True):
            if word.startswith(bn):
                found.add(BN_NUMBER_WORDS[bn])
                break
    found.discard(0)
    return found


_UNIT = (r"January|February|March|April|May|June|July|August|September|October|November|December|"
         r"জানুয়ারি|ফেব্রুয়ারি|মার্চ|এপ্রিল|মে|জুন|জুলাই|আগস্ট|সেপ্টেম্বর|অক্টোবর|নভেম্বর|ডিসেম্বর|"
         r"তারিখ|লাখ|হাজার|কোটি|টাকা|ঘণ্টা|দিন|সপ্তাহ|মাস|বছর|জন")
_NUM_WORD = "|".join(sorted(BN_NUMBER_WORDS, key=len, reverse=True))
_BEFORE_UNIT = re.compile(rf"(?<![ঀ-৿])({_NUM_WORD})(টা|টি)?(\s+)(?=(?:{_UNIT}))")
_CLOCK = re.compile(rf"(?<![ঀ-৿])({_NUM_WORD})(টায়|টার)(?![ঀ-৿])")


def normalize_numbers(text):
    """Rule step before the AI reads the notes: spoken Bangla numbers next to a date, time or
    amount become digits ("পনেরো January" -> "15 January", "ছয়টায়" -> "6টায়")."""
    text = text.translate(BN_DIGITS)
    text = _BEFORE_UNIT.sub(lambda m: f"{BN_NUMBER_WORDS[m.group(1)]}{m.group(2) or ''}{m.group(3)}", text)
    return _CLOCK.sub(lambda m: f"{BN_NUMBER_WORDS[m.group(1)]}{m.group(2)}", text)


def _check_item(it, transcript, section=""):
    """Grounding check. Returns None if fine, else the reason she should check it."""
    if _quote_found(it.get("quote"), transcript) < 0.6:
        return "could not match this to her words"
    # every number written in the item (dates, amounts, times) must be in the quoted words;
    # hours_per_week is excluded because it is calculated (2 hours a day -> 10 a week)
    said = numbers_in(it.get("quote"))
    written = set()
    for k, v in it.items():
        if k not in ("quote", "hours_per_week", "grounded", "check") and isinstance(v, str):
            written |= numbers_in(v)
    extra = written - said
    if extra:
        return "number " + ", ".join(map(str, sorted(extra))) + " is not in her words"
    # dates must keep the day she said (catches "15 January" becoming "mid-January")
    if section == "deadlines":
        missing = {n for n in said if 1 <= n <= 31} - written
        if missing:
            return "she said " + ", ".join(map(str, sorted(missing))) + " but the date written here does not"
    return None


def build_handover(transcript):
    transcript = normalize_numbers(transcript)
    h = ask_json(SYSTEM, "Work notes:\n" + transcript, max_new_tokens=2000)
    h["_transcript"] = transcript
    flagged = 0
    for sec in SECTIONS:
        items = h.get(sec) or []
        for it in items:
            problem = _check_item(it, transcript, sec)
            it["grounded"] = problem is None
            it["check"] = problem
            flagged += problem is not None
        h[sec] = items
    h["_flagged"] = flagged
    return h


def handover_passages(h):
    """Flatten an approved handover into short passages for Ask-the-Handover."""
    out = []
    def add(kind, text):
        out.append({"id": f"{kind[0].upper()}{len(out) + 1}", "kind": kind, "text": text})
    if h.get("role_summary"):
        add("role", "Role: " + h["role_summary"])
    for t in h.get("recurring_tasks", []):
        add("task", f"Task: {t.get('task')}. Frequency: {t.get('frequency')}. When: {t.get('when')}.")
    for d in h.get("deadlines", []):
        add("deadline", f"Deadline: {d.get('item')} is due {d.get('date')}.")
    for c in h.get("contacts", []):
        add("contact", f"Contact: {c.get('name')} ({c.get('role')}) for {c.get('contact_for')}.")
    for s in h.get("systems", []):
        add("system", f"System: {s.get('name')} is used for {s.get('used_for')}.")
    for f in h.get("file_locations", []):
        add("file", f"File: {f.get('what')} is kept in {f.get('where')}.")
    for o in h.get("open_issues", []):
        add("issue", f"Open issue: {o.get('issue')}. Next step: {o.get('next_step')}.")
    return out
