"""Shetu engines: Map (AI extraction + AI cross-check + dropped-work rule),
Fit (rule clash check + AI fix proposals + rule capacity/policy check).

AI: local Qwen3-4B via llama.cpp (engines/llm.py). Everything else is plain rules.
"""
import re
from datetime import date
from difflib import SequenceMatcher

from .llm import ask_json
from .return_plan import parse_clock

# ---------------------------------------------------------------- Map: AI extraction
MAP_SYSTEM = """You turn an employee's spoken description of her job (Bangla, English or Banglish) into a Role Map.
Use ONLY what she said. Never invent duties, times or names.
For each duty give:
- "duty": short English name
- "frequency": daily / weekly / monthly / quarterly / one-off
- "day": weekday if said, else null
- "time": the time span as she said it (e.g. "6 to 7:30 in the evening"), else null
- "due": a date if she gave one (e.g. "10 April"), else null
- "place": "office", "home possible" or "travel"
- "clients": list of client letters/names if she named them, else []
- "critical": "high", "medium" or "low" (deadlines, money and clients are high)
- "quote": the exact words she used (copy them, original language)
Return JSON: {"duties": [ ... ]}"""

CROSS_SYSTEM = """You compare an employee's Role Map with her official job description.
List job-description duties that are NOT covered by any Role Map duty. Be strict: only list a duty if nothing
in the Role Map matches it. For each, write one short, friendly question to ask her about it (when it happens,
how long it takes, whether it runs late).
Return JSON: {"missing": [{"jd_duty": "", "question": ""}]}"""


def map_role(conversation):
    text = "\n".join(f"Q: {t['q']}\nA: {t['a']}" for t in conversation)
    duties = ask_json(MAP_SYSTEM, text, max_new_tokens=1800)["duties"]
    answers = " ".join(t["a"] for t in conversation)
    for d in duties:
        d["grounded"] = _found(d.get("quote", ""), answers) >= 0.6
        d["start"], d["end"] = _span(d.get("time"))
        d["source"] = "conversation"
        # rule: keep only client codes she actually said (e.g. "client C" -> "C")
        d["clients"] = sorted({m for c in d.get("clients", []) for m in re.findall(r"\b([A-Z])\b", str(c))})
    return duties


def cross_check(duties, job_description):
    rm = "\n".join(f"- {d['duty']} ({d.get('frequency')})" for d in duties)
    jd = "\n".join(f"- {j}" for j in job_description)
    missing = ask_json(CROSS_SYSTEM, f"Role Map:\n{rm}\n\nJob description:\n{jd}", max_new_tokens=700)["missing"]

    # Rule check on the AI: drop any "missing" duty that clearly matches a Role Map duty (2+ shared key words)
    def words(t):
        return {w.rstrip("s") for w in re.findall(r"[a-z]+", t.lower()) if len(w) > 3} - STOP
    have = [words(d["duty"]) for d in duties]
    return [m for m in missing if not any(len(words(m["jd_duty"]) & h) >= 2 for h in have)]


STOP = {"with", "from", "that", "this", "assigned", "complete", "manage", "prepare", "proces", "submit", "needed",
        "weekly", "monthly", "client", "portfolio", "follow"}


def _found(quote, text):
    q = (quote or "").strip()
    if len(q) < 6:
        return 0.0
    m = SequenceMatcher(None, text, q, autojunk=False).find_longest_match(0, len(text), 0, len(q))
    lo = max(0, m.a - m.b)
    return SequenceMatcher(None, text[lo:lo + len(q) + 10], q, autojunk=False).ratio()


def _span(t):
    """'6 to 7:30 in the evening' -> ('18:00', '19:30') by rule."""
    if not t:
        return None, None
    parts = re.split(r"\s*(?:to|till|until|-|–|theke|porjonto)\s*", t, maxsplit=1)
    cue = t
    start = parse_clock(_as_time(parts[0]) + " " + cue)
    end = parse_clock(_as_time(parts[1]) + " " + cue) if len(parts) > 1 else None
    return start, end


def _as_time(s):
    s = s.strip()
    return s + " o'clock" if re.fullmatch(r"\d{1,2}(:\d{2})?", s) else s


# ---------------------------------------------------------------- Map: dropped-work rule
MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                      "september", "october", "november", "december"], 1)}


def parse_due(s, year):
    if not s:
        return None
    m = re.search(r"(\d{1,2})\s*([A-Za-z]+)|([A-Za-z]+)\s*(\d{1,2})", s)
    if not m:
        return None
    day, mon = (m.group(1), m.group(2)) if m.group(1) else (m.group(4), m.group(3))
    mi = next((v for k, v in MONTHS.items() if k.startswith(mon.lower()[:3])), None)
    return date(year, mi, int(day)) if mi else None


def dropped_work(duties, emp, team, planned_cover):
    """Rule: a critical duty due during the leave whose planned cover doesn't know the clients."""
    start, end = date.fromisoformat(emp["leave_start"]), date.fromisoformat(emp["leave_end"])
    alerts = []
    for d in duties:
        due = parse_due(d.get("due"), start.year)
        if not due or not (start <= due <= end) or d.get("critical") != "high":
            continue
        cover = planned_cover.get(d["duty"])
        mate = next((t for t in team if t["name"] == cover), None)
        unknown = [c for c in d.get("clients", []) if not mate or c not in mate["knows_clients"]]
        if unknown:
            better = [t["name"] for t in team if all(c in t["knows_clients"] for c in d["clients"]) and t["role"] != "Manager"]
            alerts.append({"duty": d["duty"], "due": due.isoformat(), "planned_cover": cover,
                           "reason": f"{cover} has never handled clients {', '.join(unknown)}",
                           "suggest": better[0] if better else None})
    return alerts


# ---------------------------------------------------------------- Fit: clash rules
def clashes(duties, needs):
    out = []
    lb = needs["leave_by"]
    for d in duties:
        if d.get("end") and d["end"] > lb:
            out.append({"duty": d["duty"], "type": "time", "detail": f"runs until {d['end']}, after her {lb} finish",
                        "hours": 2})
        if d.get("place") == "travel":
            out.append({"duty": d["duty"], "type": "travel", "detail": "needs travel; she has no travel until December",
                        "hours": 4})
    return out


FIX_SYSTEM = """You help a manager fix clashes between a returning mother's job and the arrangement she needs.
For each clash, propose 2 or 3 short, specific options. Use only these action types:
- "move_time": move a meeting earlier; give "new_time" as HH:MM-HH:MM (24h)
- "reassign": give the duty to a colleague; give "to" (a colleague's name)
- "start_earlier": start the work earlier so she finishes on time; give "days_earlier" (number)
- "remote": she joins by video
Return JSON: {"fixes": [{"duty": "", "options": [{"action": "", "new_time": null, "to": null, "days_earlier": null, "text": ""}]}]}"""


def propose_fixes(clash_list, team, policy):
    team_txt = ", ".join(f"{t['name']} ({t['role']})" for t in team)
    cl = "\n".join(f"- {c['duty']}: {c['detail']}" for c in clash_list)
    return ask_json(FIX_SYSTEM, f"Colleagues: {team_txt}\nPolicy: meetings must end by {policy['latest_meeting_end']}.\n"
                                f"Clashes:\n{cl}", max_new_tokens=1200)["fixes"]


def check_fix(opt, clash, team, needs, used):
    """Rules decide which AI options are allowed. Returns (ok, reason)."""
    a = opt.get("action")
    meeting = any(w in clash["duty"].lower() for w in ("meeting", "call", "huddle"))
    if a == "move_time" and not meeting:
        return False, "it is a piece of work, not a meeting"
    if a == "start_earlier" and clash["type"] == "travel":
        return False, "starting earlier doesn't remove the travel"
    if a == "move_time":
        nt = opt.get("new_time") or ""
        m = re.findall(r"(\d{1,2}):(\d{2})", nt)
        if len(m) < 2:
            return False, "no valid time given"
        end = f"{int(m[1][0]):02d}:{m[1][1]}"
        return (end <= needs["leave_by"], "ends before her finish" if end <= needs["leave_by"] else f"still ends at {end}")
    if a == "reassign":
        mate = next((t for t in team if t["name"].lower() == str(opt.get("to")).lower()), None)
        if not mate:
            return False, "no such colleague"
        left = mate["spare_hours"] - used.get(mate["name"], 0)
        if left < clash["hours"]:
            return False, f"{mate['name']} is near his limit ({left} h spare)" if mate["name"] == "Rafiq" else f"{mate['name']} has only {left} h spare"
        return True, f"{mate['name']} has {left} h spare"
    if a == "start_earlier":
        return True, "she can sign off within her hours"
    if a == "remote":
        return (clash["type"] != "travel", "fine for meetings" if clash["type"] != "travel" else "a site visit needs someone there")
    return False, "unknown action"


def fallback_cover(clash, team, used):
    """Rule-made option when every AI option failed: the colleague with the most spare hours."""
    mates = sorted((t for t in team if t["role"] != "Manager"), key=lambda t: t["spare_hours"] - used.get(t["name"], 0), reverse=True)
    for t in mates:
        if t["spare_hours"] - used.get(t["name"], 0) >= clash["hours"]:
            return {"action": "reassign", "to": t["name"], "text": f"{t['name']} takes the {clash['duty'].lower()} until December",
                    "ok": True, "why": f"{t['name']} has {t['spare_hours'] - used.get(t['name'], 0)} h spare", "by_rule": True}
    return None


KEEP = ("move_time", "start_earlier", "remote")


def rank(options, clash):
    """Rule: prefer fixes that keep her own duty with her (protects her role), then reassignments."""
    opts = list(options)
    if clash["type"] == "time" and not any(w in clash["duty"].lower() for w in ("meeting", "call"))             and not any(o["action"] == "start_earlier" and o["ok"] for o in opts):
        opts.append({"action": "start_earlier", "days_earlier": 3, "ok": True, "by_rule": True,
                     "text": "Start 3 days earlier so she signs off by 17:00", "why": "keeps the duty in her name"})
    return sorted(opts, key=lambda o: (not o["ok"], o["action"] not in KEEP))
