#!/usr/bin/env python3
"""Run the IAM benchmark against Levanto's Sage API.

Setup:
    export LEVANTO_API_KEY=<redacted>  # Sage console -> Decision model -> API keys

Usage:
    python3 runners/run_sage.py [--out predictions_sage.jsonl] [--limit 5]

API: POST https://sage.levanto.ai/decide
Auth: Authorization: Bearer <key> (key looks like lv_live_...)
Body: {"content": "<state>", "question": {"kind": "choice", "id": "decision",
       "instructions": "<task>",
       "options": [{"option": "grant", "description": "<meaning>"}, ...]}}
Response: {"result": {"chosen": "deny"|null, "probability": 0.9|null, ...},
           "meta": {"model": "levanto-sage-v1.4", ...}}

A null probability means Sage abstained ("route null to a human"); this
runner maps abstentions to escalate at 0.0 confidence.

Note: Cloudflare in front of sage.levanto.ai rejects Python-urllib's
default user agent (403 error 1010); this script sets a browser UA.
"""

import argparse
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (CRITERIA, INSTRUCTIONS, DECISIONS, main_loop,  # noqa: E402
                    repo_root)

API_URL = "https://sage.levanto.ai/decide"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def sage_decide(api_key, state):
    body = {
        "content": state,
        "question": {
            "kind": "choice",
            "id": "decision",
            "instructions": INSTRUCTIONS,
            "options": [{"option": d, "description": CRITERIA[d]}
                        for d in DECISIONS],
        },
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json",
                 "User-Agent": UA},
        method="POST",
    )
    with urllib.request.build_opener(NoRedirect()).open(req,
                                                        timeout=180) as resp:
        payload = json.loads(resp.read())
    result = payload["result"]
    prob = result["probability"]
    if prob is None:
        # Sage abstained: route to a human.
        return "escalate", 0.0, []
    decision = result["chosen"]
    if decision not in DECISIONS:
        raise ValueError(f"unexpected choice {decision!r}")
    return decision, float(prob), []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    api_key = os.environ.get("LEVANTO_API_KEY")
    if not api_key:
        sys.exit("LEVANTO_API_KEY is not set. Create a key in the Sage "
                 "console under Decision model -> API keys.")

    out = args.out or os.path.join(repo_root(), "predictions_sage.jsonl")
    main_loop("sage", lambda case, state: sage_decide(api_key, state),
              out, limit=args.limit)


if __name__ == "__main__":
    main()
