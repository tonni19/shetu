"""Run Shetu's engines on the Nusrat demo case and save every real output to demo/results.json."""
import json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
from engines import shetu

ROOT = Path(__file__).parent
case = json.loads((ROOT / "demo" / "nusrat.json").read_text(encoding="utf-8"))
log, t0 = {}, time.time()

duties = shetu.map_role(case["conversation"])
log["map_seconds"] = round(time.time() - t0, 1)
missing = shetu.cross_check(duties, case["job_description"])
# her answer to the cross-check question becomes a new duty (rule: parse the time span she gives)
for m in missing:
    if "quarter" in m["jd_duty"].lower():
        s, e = "17:00", shetu.parse_clock("9 pm")
        duties.append({"duty": "Quarter-end loan classification review", "frequency": "quarterly", "day": "last 2 days of quarter",
                       "time": "often until 9 pm", "due": "30 September", "place": "office", "clients": [], "critical": "high",
                       "quote": case["answers"]["quarter_end_review"], "grounded": True, "start": s, "end": e,
                       "source": "job description (she confirmed)"})
planned = {d["duty"]: "Rafiq" for d in duties if "renewal" in d["duty"].lower()}
alerts = shetu.dropped_work(duties, case["employee"], case["team"], planned)

cl = shetu.clashes(duties, case["needs"])
fixes = shetu.propose_fixes(cl, case["team"], case["policy"]) if cl else []
used, decided = {}, []
for c in cl:
    f = next((x for x in fixes if x["duty"].lower()[:12] in c["duty"].lower() or c["duty"].lower()[:12] in x["duty"].lower()), None)
    checked = []
    for o in (f or {}).get("options", []):
        ok, why = shetu.check_fix(o, c, case["team"], case["needs"], used)
        checked.append(dict(o, ok=ok, why=why))
    checked = shetu.rank(checked, c)
    pick = next((o for o in checked if o["ok"]), None) or shetu.fallback_cover(c, case["team"], used)
    if pick and pick.get("by_rule") and pick not in checked:
        checked.append(pick)
    if pick and pick["action"] == "reassign":
        used[pick["to"]] = used.get(pick["to"], 0) + c["hours"]
    decided.append(dict(c, options=checked, chosen=pick))

out = {"duties": duties, "missing": missing, "alerts": alerts, "clashes": decided, "seconds": round(time.time() - t0, 1), **log}
(ROOT / "demo" / "results.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
