import json, time, sys
from datetime import date
sys.stdout.reconfigure(encoding="utf-8")
from engines import handover, qa, return_plan
tr = open("samples/dev/card1_dev_transcript.txt", encoding="utf-8").read()
t=time.time(); h = handover.build_handover(tr); print("handover s", round(time.time()-t,1))
print(json.dumps(h, ensure_ascii=False, indent=1))
P = handover.handover_passages(h)
card = json.load(open("eval/job_cards.json", encoding="utf-8"))["cards"][0]
for q in card["questions"]:
    t=time.time(); r = qa.answer(q["q"], P)
    print(f"[{'A' if q['answerable'] else 'U'}] {q['q']} -> answered={r['answered']} best={r['best_score']:.3f} gate={r.get('gate')} | {r['answer'][:110]} ({time.time()-t:.1f}s)")
t=time.time(); tags = return_plan.tag_tasks(h); print("tags s", round(time.time()-t,1))
print(json.dumps(tags, ensure_ascii=False, indent=1))
plans = return_plan.build_plans(tags, {"office_days":3,"leave_by":"16:00","feeding_breaks":True,"childcare":"09:00-17:00"}, [{"name":"Colleague A","spare_hours":6},{"name":"Colleague B","spare_hours":4}], date(2027,3,1))
for p in plans: print("==", p["name"], p["reasons"])
