"""Test the engines on team-recorded samples.

Put each member's recordings in  prototype/samples/card1/, card2/, card3/  (any audio format).
Run:  python eval/run_eval.py
Writes eval/results/<card>.json and eval/results/summary.md.

Scores are first matched automatically (embedding similarity), then a person reviews
eval/results/review.csv and corrects any wrong match before numbers are quoted.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engines import handover, qa  # noqa: E402

CARDS = json.loads((ROOT / "eval" / "job_cards.json").read_text(encoding="utf-8"))["cards"]
OUT = ROOT / "eval" / "results"
OUT.mkdir(exist_ok=True)
AUDIO = {".m4a", ".mp3", ".ogg", ".opus", ".wav", ".aac", ".flac", ".webm", ".mp4"}
MATCH = 0.86


def item_text(sec, it):
    return " ".join(str(v) for k, v in it.items() if k not in ("quote", "grounded") and v)


def best_match(text, candidates):
    if not candidates:
        return None, 0.0
    a = qa._embed(["query: " + text])
    b = qa._embed(["query: " + c for c in candidates])
    s = (a @ b.T)[0]
    i = int(s.argmax())
    return i, float(s[i])


def main(only=None):
    rows, summary = [], []
    # 1. transcribe everything first, then free the GPU for the language model
    transcripts = {}
    for card in CARDS:
        if only and card["id"] != only:
            continue
        files = sorted(p for p in (ROOT / "samples" / card["id"]).glob("*") if p.suffix.lower() in AUDIO)
        if not files:
            print("no audio for", card["id"])
            continue
        transcripts[card["id"]] = "\n".join(handover.transcribe(str(f)) for f in files)
        print("transcribed", card["id"], len(files), "files")
    handover.unload_whisper()

    for card in CARDS:
        tr = transcripts.get(card["id"])
        if tr is None:
            continue
        h = handover.build_handover(tr)
        found, missed = 0, 0
        total_items = sum(len(h.get(s) or []) for s in handover.SECTIONS)
        matched_items = set()
        for sec, facts in card["facts"].items():
            items = h.get(sec) or []
            texts = [item_text(sec, it) for it in items]
            for fact in facts:
                i, score = best_match(fact, texts)
                ok = i is not None and score >= MATCH
                found += ok
                missed += not ok
                if ok:
                    matched_items.add((sec, i))
                rows.append([card["id"], "fact", sec, fact, texts[i] if i is not None else "", f"{score:.3f}", "yes" if ok else "no"])
        extra = total_items - len(matched_items)

        passages = handover.handover_passages(h)
        qa_res = []
        for q in card["questions"]:
            r = qa.answer(q["q"], passages, "the manager")
            if q["answerable"]:
                _, sc = best_match(q["a"], [r["answer"]]) if r["answered"] else (None, 0.0)
                verdict = "correct" if r["answered"] and sc >= 0.84 else ("refused" if not r["answered"] else "check")
            else:
                verdict = "correct refusal" if not r["answered"] else "MADE-UP ANSWER"
            qa_res.append({**q, "got": r["answer"], "answered": r["answered"], "verdict": verdict,
                           "best_score": r["best_score"]})
            rows.append([card["id"], "question", "answerable" if q["answerable"] else "unanswerable",
                         q["q"], r["answer"], f"{r['best_score']:.3f}", verdict])

        (OUT / f"{card['id']}.json").write_text(json.dumps(
            {"transcript": tr, "handover": h, "qa": qa_res}, ensure_ascii=False, indent=1), encoding="utf-8")
        ans = [x for x in qa_res if x["answerable"]]
        una = [x for x in qa_res if not x["answerable"]]
        summary.append({
            "card": card["id"],
            "facts_found": f"{found}/{found + missed}",
            "extra_items": extra,
            "flagged_items": h["_flagged"],
            "answerable_correct": f"{sum(x['verdict'] == 'correct' for x in ans)}/{len(ans)}",
            "answerable_refused": sum(x["verdict"] == "refused" for x in ans),
            "unanswerable_refused": f"{sum(x['verdict'] == 'correct refusal' for x in una)}/{len(una)}",
            "made_up": sum(x["verdict"] == "MADE-UP ANSWER" for x in una),
        })
        print(summary[-1])

    with open(OUT / "review.csv", "w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerows([["card", "type", "section", "expected / question", "system output", "score", "auto verdict"]] + rows)
    lines = ["| Card | Facts found | Extra items | Flagged | Answerable correct | Wrongly refused | Unanswerable refused | Made-up answers |",
             "|---|---|---|---|---|---|---|---|"]
    lines += [f"| {s['card']} | {s['facts_found']} | {s['extra_items']} | {s['flagged_items']} | {s['answerable_correct']} | "
              f"{s['answerable_refused']} | {s['unanswerable_refused']} | {s['made_up']} |" for s in summary]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n\nAuto-scored; review review.csv before quoting.\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
