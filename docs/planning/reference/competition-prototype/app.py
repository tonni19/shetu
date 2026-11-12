"""Shetu prototype: local web app. Run:  python app.py  then open http://127.0.0.1:5000

Everything runs offline on this laptop. No data leaves the device.
"""
import json
import os
import uuid
from datetime import date
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from engines import catchup, handover, qa, return_plan

ROOT = Path(__file__).parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
app = Flask(__name__)

STATE_FILE = DATA / "state.json"


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(s):
    STATE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")


@app.get("/")
def index():
    return render_template("index.html", state=load_state())


@app.post("/api/transcribe")
def api_transcribe():
    texts = []
    for f in request.files.getlist("audio"):
        p = DATA / f"{uuid.uuid4().hex}{Path(f.filename).suffix}"
        f.save(p)
        texts.append(handover.transcribe(str(p)))
    handover.unload_whisper()
    s = load_state()
    s["transcript"] = "\n".join(texts)
    save_state(s)
    return jsonify(transcript=s["transcript"])


@app.post("/api/handover")
def api_handover():
    transcript = request.json["transcript"]
    h = handover.build_handover(transcript)
    s = load_state()
    s.update(transcript=transcript, handover=h, approved=False)
    save_state(s)
    return jsonify(h)


@app.post("/api/approve")
def api_approve():
    s = load_state()
    s["handover"] = request.json["handover"]
    s["approved"] = True
    s["passages"] = handover.handover_passages(s["handover"])
    save_state(s)
    return jsonify(passages=s["passages"])


@app.post("/api/ask")
def api_ask():
    s = load_state()
    if not s.get("approved"):
        return jsonify(error="The handover must be approved by her first."), 400
    return jsonify(qa.answer(request.json["question"], s["passages"], s.get("manager", "the manager")))


@app.post("/api/plans")
def api_plans():
    s = load_state()
    body = request.json
    tags = s.get("tags") if body.get("reuse_tags") else None
    if not tags:
        tags = return_plan.tag_tasks(s["handover"])
        s["tags"] = tags
    plans = return_plan.build_plans(
        [dict(t) for t in tags], body["answers"], body["team"], date.fromisoformat(body["return_date"])
    )
    s["plans"] = plans
    save_state(s)
    return jsonify(tags=tags, plans=plans)


@app.post("/api/catchup")
def api_catchup():
    return jsonify(catchup.summarise(request.json["updates"]))


if __name__ == "__main__":
    app.run(debug=False, port=5000)
