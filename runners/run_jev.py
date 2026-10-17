#!/usr/bin/env python3
"""Run the IAM benchmark against TypeSafe's Jev API.

Setup:
    export TYPESAFE_API_KEY=<redacted>   # create at console.typesafe.ai -> API Keys
    # optional: pip install typesafe-sdk (not required; this uses plain REST)

Usage:
    python3 runners/run_jev.py [--model jev-latest] [--out predictions_jev.jsonl]
                               [--limit 5]

API: POST https://api.typesafe.ai/v1/systemone
Body: {"model", "state", "questions": {"decision": {"type": "choice",
       "instructions", "criteria": {"grant","deny","escalate"}}}}
"""

import argparse
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (CRITERIA, INSTRUCTIONS, DECISIONS, main_loop,  # noqa: E402
                    repo_root)

API_URL = "https://api.typesafe.ai/v1/systemone"


def jev_decide(api_key, model, state):
    body = {
        "model": model,
        "state": state,
        "questions": {
            "decision": {
                "type": "choice",
                "instructions": INSTRUCTIONS,
                "criteria": CRITERIA,
            }
        },
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.loads(resp.read())
    ans = payload["answers"]["decision"]
    decision = ans["choice"]
    if decision not in DECISIONS:
        raise ValueError(f"unexpected choice {decision!r}")
    # Confidence: prefer the explicit field, else the chosen option's prob.
    confidence = ans.get("confidence")
    if confidence is None:
        confidence = ans.get("probabilities", {}).get(decision, 0.5)
    return decision, float(confidence), []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="jev-latest",
                    help="e.g. jev-latest, jev-1.14.0 (pin for repro)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    api_key = os.environ.get("TYPESAFE_API_KEY")
    if not api_key:
        sys.exit("TYPESAFE_API_KEY is not set. Create a key at "
                 "console.typesafe.ai -> API Keys.")

    out = args.out or os.path.join(repo_root(),
                                   f"predictions_jev_{args.model}.jsonl")
    main_loop("jev", lambda case, state: jev_decide(api_key, args.model, state),
              out, limit=args.limit)


if __name__ == "__main__":
    main()
