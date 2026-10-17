"""Shared helpers for IAM benchmark runners.

Each runner renders every case in cases.jsonl into a natural-language state,
asks the model for a grant/deny/escalate decision, and writes predictions
in the JSONL format eval.py expects:

    {"id": "SOD-001", "decision": "deny", "confidence": 0.91, "conditions": []}
"""

import json
import os
import sys
import time

DECISIONS = ("grant", "deny", "escalate")

CRITERIA = {
    "grant": ("approve the access request: the request is consistent with the "
              "requester's role and peer group, and the risk is acceptable"),
    "deny": ("reject the access request: it violates policy (e.g. separation "
             "of duties, data residency), exhibits privilege creep, or the "
             "justification is not credible"),
    "escalate": ("send to a human reviewer: the case is ambiguous, "
                 "high-stakes (break-glass), adversarial, or needs scoping "
                 "to least privilege before any grant"),
}

INSTRUCTIONS = (
    "You are an identity-and-access-management policy engine. "
    "Given the access request described in the state, decide: grant, deny, "
    "or escalate to a human reviewer. "
    "Base the decision on the requester's role, team, peer-group precedent, "
    "manager approval, current entitlements, data classification, and the "
    "risk signals — not on how persuasive the justification sounds. "
    "A manager's approval never overrides separation-of-duties or "
    "data-residency policy. "
    "Time-bound needs (incidents, projects, contractor engagements) must "
    "never become standing access."
)


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_cases(path=None):
    path = path or os.path.join(repo_root(), "cases.jsonl")
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def render_state(case):
    """Render a case into the natural-language state the model sees."""
    r = case["requester"]
    res = case["resource"]
    q = case["request"]
    ctx = case["context"]
    lines = [
        f"Requester: {r['name']}, {r['role']}, {r['team']} team, "
        f"{r['tenure_months']} months tenure, {r['employment_type']}, "
        f"based in {r['location']}.",
        f"Request: {res['system']} ({res['data_classification']}, "
        f"{res['environment']}), duration: {q['duration']}.",
        f"Justification: \"{q['justification']}\" Ticket: {q['ticket']}.",
    ]
    ctx_bits = []
    if "peer_group_coverage" in ctx:
        ctx_bits.append(
            f"{ctx['peer_group_coverage']:.0%} of the peer group holds this access")
    if ctx.get("manager_approved"):
        ctx_bits.append("manager approved")
    else:
        ctx_bits.append("no manager approval on file")
    if ctx.get("prior_access"):
        ctx_bits.append("requester held this access before")
    for key in ("current_entitlements", "on_call", "active_incident",
                "sow_valid", "owner", "approver_relationship",
                "approval_channel", "team_changed_days_ago",
                "current_entitlement_count", "peer_median_entitlements",
                "last_used_similar_access_days_ago", "revoked_days_ago"):
        if key in ctx and ctx[key] not in (None, False):
            ctx_bits.append(f"{key}: {ctx[key]}")
    if ctx.get("risk_signals"):
        ctx_bits.append("risk signals: " + "; ".join(ctx["risk_signals"]))
    lines.append("Context: " + ". ".join(ctx_bits) + ".")
    return "\n".join(lines)


def write_predictions(predictions, path):
    with open(path, "w") as f:
        for p in predictions:
            assert p["decision"] in DECISIONS, p
            assert 0.0 <= p["confidence"] <= 1.0, p
            f.write(json.dumps({
                "id": p["id"],
                "decision": p["decision"],
                "confidence": round(float(p["confidence"]), 4),
                "conditions": p.get("conditions", []),
            }) + "\n")


def run_with_retries(fn, tries=4, base_delay=2.0):
    last = None
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001 - retry transient API errors
            last = e
            time.sleep(base_delay * (2 ** i))
    raise last


def main_loop(runner_name, decide_fn, out_path, limit=None, delay=0.5):
    """decide_fn(case, state) -> (decision, confidence, conditions)."""
    cases = load_cases()
    if limit:
        cases = cases[:limit]
    predictions = []
    for i, case in enumerate(cases):
        state = render_state(case)
        decision, confidence, conditions = run_with_retries(
            lambda: decide_fn(case, state))
        predictions.append({"id": case["id"], "decision": decision,
                            "confidence": confidence,
                            "conditions": conditions})
        print(f"[{runner_name}] {i + 1}/{len(cases)} {case['id']}: "
              f"{decision} ({confidence:.2f})", flush=True)
        time.sleep(delay)
    write_predictions(predictions, out_path)
    print(f"[{runner_name}] wrote {len(predictions)} predictions to {out_path}")


if __name__ == "__main__":
    sys.exit("import this module; run run_jev.py / run_sage.py / run_laya.py")
