"""Local language model (runs offline on the laptop GPU).

Qwen3-4B-Instruct (6-bit GGUF) served by llama.cpp's llama-server on this machine.
All engines call `ask_json`; the server is told to reply in JSON only, so replies
always parse. Nothing is sent over the internet.
"""
import json
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "tools" / "llama" / "llama-server.exe"
MODEL = ROOT / "models" / "Qwen3-4B-Instruct-2507-Q6_K.gguf"
MODEL_NAME = "Qwen3-4B-Instruct-2507 (Q6_K, local)"
PORT = 8081
URL = f"http://127.0.0.1:{PORT}"

_proc = None


def _alive():
    try:
        with urllib.request.urlopen(URL + "/health", timeout=2) as r:
            return r.status == 200
    except (urllib.error.URLError, OSError):
        return False


def start():
    """Start llama-server if it is not already running."""
    global _proc
    if _alive():
        return
    _proc = subprocess.Popen(
        [str(SERVER), "-m", str(MODEL), "-ngl", "99", "-c", "8192", "--port", str(PORT), "--no-webui"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    for _ in range(180):
        if _alive():
            return
        time.sleep(1)
    raise RuntimeError("llama-server did not start")


def _chat(system, user, max_new_tokens, json_mode):
    start()
    body = {
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0,
        "max_tokens": max_new_tokens,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    req = urllib.request.Request(URL + "/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def generate(system, user, max_new_tokens=1500):
    return _chat(system, user, max_new_tokens, json_mode=False)


def ask_json(system, user, max_new_tokens=1500):
    reply = _chat(system, user, max_new_tokens, json_mode=True)
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        reply = _chat(system, user + "\n\nReply with valid JSON only.", max_new_tokens, json_mode=True)
        return json.loads(reply)
