#!/usr/bin/env python3
"""Run the IAM benchmark against Laya, the open-weights decision model.

Laya (Convai Innovations, Apache-2.0) is a non-autoregressive System 1
decision model: typed choice/score/yes-no answers in a single forward pass.
Checkpoints: laya (English, 421M), laya-multilingual (322M), and
laya-typed-decisions (fine-tuned on the typed-decisions workflows).

Setup:
    python3 -m venv .venv && . .venv/bin/activate
    pip install laya            # pulls torch; ~2 GB with weights
    # first run downloads the checkpoint from Hugging Face
    # (set HF_HOME to keep weights outside ~/.cache if you prefer)

Usage:
    python3 runners/run_laya.py [--model routed] [--out predictions_laya.jsonl]
                                [--limit 5] [--preload]

--model: checkpoint routing. Default "routed" lets Laya's Router pick per
request (English text -> English checkpoint). Pass "multilingual" to pin
the multilingual checkpoint, or "typed-decisions" for the fine-tuned one.

Honest-limits note (from Laya's own README): the base checkpoints are
near chance zero-shot on business decisions (0.362 vs 0.318 random on
typed-decisions); the 0.766 figure is the fine-tuned checkpoint on its own
training domain. Expect modest zero-shot scores here — that IS the result.
Fine-tuning on your own labeled decisions is where accuracy jumps.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (CRITERIA, INSTRUCTIONS, DECISIONS, main_loop,  # noqa: E402
                    repo_root)


def laya_decide(router, model, state):
    questions = {
        "decision": {
            "type": "choice",
            "instructions": INSTRUCTIONS,
            "criteria": CRITERIA,
        }
    }
    kwargs = {} if model == "routed" else {"model": model}
    result = router.predict(state, questions, **kwargs)
    ans = result["answers"]["decision"]
    decision = ans.get("choice")
    if decision not in DECISIONS:
        raise ValueError(f"unexpected choice {decision!r}; "
                         f"answer keys: {sorted(ans.keys())}")
    confidence = ans.get("confidence")
    if confidence is None:
        confidence = (ans.get("probabilities") or {}).get(decision, 0.5)
    return decision, float(confidence), []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="routed",
                    help="'routed' (default), 'multilingual', 'typed-decisions'")
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--preload", action="store_true",
                    help="load all checkpoints up front")
    args = ap.parse_args()

    try:
        from laya import Router
    except ImportError:
        sys.exit("the 'laya' package is not installed: pip install laya")

    print("[laya] loading router (first run downloads the checkpoint)...",
          flush=True)
    router = Router(preload=args.preload)

    out = args.out or os.path.join(
        repo_root(), f"predictions_laya_{args.model}.jsonl")
    main_loop("laya",
              lambda case, state: laya_decide(router, args.model, state),
              out, limit=args.limit, delay=0.1)


if __name__ == "__main__":
    main()
