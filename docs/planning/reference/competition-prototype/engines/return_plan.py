"""Engine 2: Return Plan.

Step 1 (AI): the language model tags each task from her approved handover:
            fixed time or flexible, office or remote, movable to a colleague or not.
Step 2 (rules): transparent rules combine the tags with her four private answers and the
            team's spare hours to build 2-3 plans. Every decision carries a written reason,
            so a manager can see why a plan looks the way it does.
"""
from datetime import timedelta
from difflib import SequenceMatcher

import re

from .handover import normalize_numbers
from .llm import ask_json

HOURS_PER_DAY = 8
FULL_WEEK = 40

SYSTEM = """You tag work tasks to help plan a mother's return from maternity leave.
For each task decide, using only what the description says (if unclear, choose the safer option):
- "time": "fixed" if it must happen at a set time (e.g. a weekly meeting at 6pm), else "flexible"
- "fixed_time": always null (clock times are read by a separate rule)
- "place": "office" if it needs physical presence, else "remote"
- "movable": true if a colleague could reasonably take it over or stand in for a few months (meetings can
  usually have a stand-in), false if it needs her specific authority, such as approving payments
- "hours_per_week": a number greater than 0; keep the given value if present, otherwise a cautious estimate
  from the frequency (daily work is several hours a week; a monthly report is about 1 hour a week)
- "reason": one short sentence explaining the tags
Return JSON: {"tasks": [{"task": "", "time": "", "fixed_time": null, "place": "", "movable": true, "hours_per_week": 0, "reason": ""}]}"""


def tag_tasks(handover):
    tasks = handover.get("recurring_tasks") or []
    lines = "\n".join(
        f"- {t.get('task')} (frequency: {t.get('frequency')}; when: {t.get('when')}; "
        f"hours/week: {t.get('hours_per_week')})"
        for t in tasks
    )
    tags = ask_json(SYSTEM, "Tasks:\n" + lines, max_new_tokens=1500)["tasks"]
    def source(tag):  # the handover task this tag came from (the model may reorder)
        return max(tasks, key=lambda t: SequenceMatcher(None, str(t.get("task")), str(tag.get("task"))).ratio())

    # Rule step: the clock time is read from her own words, not from the model.
    for tag in tags:
        src = source(tag)
        tag["fixed_time"] = parse_clock(f"{src.get('when') or ''} {src.get('quote') or ''}")
        if tag["fixed_time"]:
            tag["time"] = "fixed"
        tag["hours_estimated"] = not src.get("hours_per_week")
        if not tag.get("hours_per_week"):
            tag["hours_per_week"] = 1
    return tags


_PM = re.compile(r"evening|afternoon|night|pm|p\.m\.|সন্ধ্যা|বিকাল|বিকেল|রাত|দুপুর", re.I)
_TIME = re.compile(r"(?<!\d)(\d{1,2})(?:[:.](\d{2}))?\s*(?:টায়|টার|o'clock|am|pm|a\.m\.|p\.m\.)", re.I)


def parse_clock(text):
    """'Thursday evening 6 o'clock' / 'সন্ধ্যা 6টায়' / '11am' -> '18:00' / '18:00' / '11:00'. None if no time."""
    text = normalize_numbers(text or "")
    m = _TIME.search(text) or re.search(r"(?<!\d)(\d{1,2}):(\d{2})", text)
    if not m:
        return None
    hour, minute = int(m.group(1)), int(m.group(2) or 0)
    if hour > 23 or minute > 59:
        return None
    if hour < 12 and _PM.search(text) and not (hour < 4 and "রাত" in text):
        hour += 12
    return f"{hour:02d}:{minute:02d}"


def _hm(s):
    h, m = (s or "0:0").split(":")
    return int(h) * 60 + int(m)


def _clashes(t, a):
    """Why this task clashes with her answers, or None."""
    if t["time"] == "fixed" and t.get("fixed_time") and _hm(t["fixed_time"]) >= _hm(a["leave_by"]):
        return f"starts at {t['fixed_time']}, after she must leave ({a['leave_by']})"
    return None


def _assign_cover(moved, team):
    """Greedy: biggest task first, to the colleague with most spare hours left.
    A task may be split between colleagues; whatever is left is a cover gap."""
    spare = {m["name"]: float(m["spare_hours"]) for m in team}
    out, gap = [], 0.0
    for t in sorted(moved, key=lambda x: -x["hours_per_week"]):
        need, who = t["hours_per_week"], []
        while need > 0 and spare and max(spare.values()) > 0:
            name = max(spare, key=spare.get)
            take = min(need, spare[name])
            spare[name] -= take
            need -= take
            who.append(f"{name} {take:g} h")
        if need > 0:
            gap += need
            who.append(f"temporary cover {need:g} h")
        out.append(dict(t, cover=", ".join(who)))
    return out, gap


def _office_check(kept, a):
    need = sum(t["hours_per_week"] for t in kept if t["place"] == "office")
    per_day = HOURS_PER_DAY - (1 if a["feeding_breaks"] else 0)
    have = a["office_days"] * per_day
    return need, have


def build_plans(tags, answers, team, return_date):
    a = answers
    review = (return_date + timedelta(weeks=12)).isoformat()
    for t in tags:
        t["hours_per_week"] = float(t.get("hours_per_week") or 0)
    plans = []

    # Plan A: phased return (60% -> 80% -> 100% over 12 weeks)
    keep_order = sorted(tags, key=lambda t: (t["movable"], -t["hours_per_week"]))
    workload = sum(t["hours_per_week"] for t in tags) or FULL_WEEK
    phases = []
    for label, pct in (("Weeks 1-4", 0.6), ("Weeks 5-8", 0.8), ("Weeks 9-12", 1.0)):
        cap = workload * pct
        kept, moved, used = [], [], 0.0
        for t in keep_order:
            if t["movable"] and _clashes(t, a):
                moved.append(t)
            elif not t["movable"] or used + t["hours_per_week"] <= cap:
                kept.append(t)
                used += t["hours_per_week"]
            else:
                moved.append(t)
        cover, gap = _assign_cover(moved, team)
        phases.append({"label": label, "her_hours": round(min(used, cap), 1), "kept": kept,
                       "moved": cover, "gap_hours": gap})
    plans.append({
        "name": "Phased return",
        "summary": "Starts at 60% of hours, rising to full time by week 12.",
        "phases": phases,
        "reasons": [
            "Tasks only she can do (not movable) are kept from day one.",
            "Movable tasks are handed to colleagues with spare hours until her hours rise.",
            "Tasks that clash with her hours stay with colleagues throughout.",
        ],
        "review_date": review,
    })

    # Plan B: flexible hours (same job, office work on office days, the rest from home)
    need, have = _office_check(tags, a)
    clashing = [dict(t, why=_clashes(t, a)) for t in tags if _clashes(t, a)]
    reasons = [f"Office-only work needs {need:g} h/week; her {a['office_days']} office days give {have:g} h."]
    if a["feeding_breaks"]:
        reasons.append("One hour per office day is protected for feeding breaks.")
    reasons += [f"\"{c['task']}\" {c['why']}: it needs a new time or a stand-in." for c in clashing]
    plans.append({
        "name": "Flexible hours",
        "summary": f"Full job; {a['office_days']} office days, remote tasks done from home within childcare hours ({a['childcare']}).",
        "kept": tags,
        "moved": [],
        "fits": need <= have and not clashing,
        "open_points": clashing,
        "reasons": reasons,
        "review_date": review,
    })

    # Plan C: move only the tasks that clash
    moved = [t for t in tags if _clashes(t, a) and t["movable"]]
    stuck = [t for t in tags if _clashes(t, a) and not t["movable"]]
    if moved or stuck:
        cover, gap = _assign_cover(moved, team)
        kept = [t for t in tags if t not in moved]
        plans.append({
            "name": "Move the clashing tasks",
            "summary": "Her normal job, except the few tasks that clash with her limits go to colleagues.",
            "kept": kept,
            "moved": cover,
            "gap_hours": gap,
            "reasons": [f"\"{t['task']}\" moves: {_clashes(t, a)}." for t in moved]
                       + [f"\"{t['task']}\" clashes but cannot move ({t['reason']}); the manager must change its time." for t in stuck],
            "review_date": review,
        })
    return plans
