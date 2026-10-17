#!/usr/bin/env python3
"""Run the IAM access-decision benchmark against Laya (open weights, local).

Uses the real laya package API:
    runner = laya.load()                      # downloads convaiinnovations/laya (421M)
    out = runner.system_one(state, {"q": {"type": "choice",
        "instructions": "...", "criteria": {"grant": "...", "deny": "...", "escalate": "..."}}})
    -> {"answers": {"q": "grant"}, "probabilities": {"q": {...}}, ...}

Zero-shot: no fine-tuning, no per-case calibration. The base checkpoint is expected
to be weak on business decisions (its README says as much) -- that is the baseline
the hosted models are measured against.

Writes predictions_laya.jsonl (same schema as run_jev/run_sage).
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import load_cases, render_state, INSTRUCTIONS, CRITERIA  # noqa: E402

CASES_PATH = os.environ.get("CASES_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cases.jsonl"))
OUT_PATH = os.environ.get("OUT_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "predictions_laya.jsonl"))

QUESTIONS = {
    "decision": {
        "type": "choice",
        "instructions": INSTRUCTIONS,
        "criteria": CRITERIA,
    }
}


def main():
    import laya

    t0 = time.time()
    print("Loading Laya model (first run downloads ~421M params from HF)...", flush=True)
    runner = laya.load()
    print(f"Model loaded in {time.time() - t0:.1f}s", flush=True)

    cases = load_cases(CASES_PATH)
    print(f"Running {len(cases)} cases...", flush=True)

    with open(OUT_PATH, "w") as f:
        for i, case in enumerate(cases):
            state = render_state(case)
            t1 = time.time()
            out = runner.system_one(state, QUESTIONS)
            latency_ms = (time.time() - t1) * 1000.0

            # system_one -> {"answers": {"decision": {"choice": ..., "probabilities": {...}}}, ...}
            ans = (out.get("answers", {}) or {}).get("decision", {}) or {}
            chosen = ans.get("choice")
            prob = None
            pq = ans.get("probabilities") or {}
            if chosen in pq:
                prob = float(pq[chosen])

            if chosen not in ("grant", "deny", "escalate"):
                chosen, prob = "escalate", 0.0
            rec = {
                "id": case["id"],
                "decision": chosen,
                "confidence": round(float(prob), 4) if prob is not None else 0.0,
                "conditions": [],
            }
            f.write(json.dumps(rec) + "\n")
            print(f"  [{i+1}/{len(cases)}] {case['id']}: {chosen} p={prob} ({latency_ms:.0f}ms)", flush=True)

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
