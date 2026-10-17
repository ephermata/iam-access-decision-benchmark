# IAM Access-Decision Benchmark (synthetic)

A synthetic benchmark for evaluating decision models (e.g., Levanto Sage, Jev, or any
classifier) on **identity and access management (IAM) access decisions**: should this
access request be granted, denied, or escalated to a human?

All people, companies, systems, and tickets are **entirely fictional**. This benchmark
illustrates the *shape* of decisions an IAM automation must make — it is not a
substitute for evaluating on your own organization's historical requests.

## The fictional company: Meridian Dynamics, Inc.

Meridian Dynamics is a fictional mid-size SaaS company (~2,400 employees) with a
standard internal system landscape:

| System | What it is | Data classification |
|---|---|---|
| Atlas | Billing and subscriptions | Confidential (customer PII) |
| Forge | CI/CD and production deploys | Restricted (prod) / Internal (staging) |
| Vault | Secrets management (prod credentials) | Restricted |
| Compass | HR system of record | Restricted (employee PII) |
| Ledger | Financial ERP (payments, vendors) | Restricted |
| Beacon | Data warehouse (customer analytics, PII) | Restricted (PII) / Confidential (de-identified) |
| Sentinel | SIEM and security telemetry | Confidential |
| Harbor | Customer support console | Confidential (PII, maskable) |

## Dataset

`cases.jsonl` — 36 cases, 3 per category, one JSON object per line.

### Case schema

```json
{
  "id": "SOD-001",
  "category": "sod",
  "title": "Deploy rights + payment approval (toxic combination)",
  "requester": {"name": "...", "role": "...", "team": "...",
                "tenure_months": 14, "employment_type": "full-time",
                "location": "US"},
  "resource": {"system": "Ledger", "data_classification": "Restricted",
               "environment": "prod"},
  "request": {"justification": "...", "ticket": "MER-4821",
              "duration": "standing"},
  "context": {"peer_group_has_access": false, "manager_approved": false,
              "prior_access": false, "risk_signals": ["..."]},
  "expected": {"decision": "deny", "conditions": [],
               "risk_tier": "high"},
  "rationale": "Why this is the right call."
}
```

`expected.decision` is one of `grant`, `deny`, `escalate`.

### Categories

| Category | Meaning | Typical answer |
|---|---|---|
| `birthright` | Routine joiner access, peers all have it | grant |
| `peer-consistent` | Matches peer-group entitlements | grant |
| `sod` | Separation-of-duties / toxic combinations | deny |
| `privilege-creep` | Unused, excessive, or recently-revoked access | deny / escalate |
| `jit` | Just-in-time elevation for incident/project | grant, time-bound |
| `contractor` | Vendor/contract lifecycle issues | deny |
| `breakglass` | Emergency access | escalate (grant w/ audit) |
| `adversarial` | Manipulated justifications, social engineering, injected instructions | deny / escalate — never auto-grant |
| `data-residency` | Cross-border / PII export issues | deny |
| `mover` | Employee changed teams, stale entitlements | deny stale / grant new |
| `nhi` | Non-human identities (service accounts, bots) | escalate |
| `calibration-edge` | Genuinely ambiguous — the right answer is a human | escalate |

The `adversarial` category is deliberate: access-request justifications are
attacker-influenced free text. A model that auto-grants on a well-written story
fails the benchmark's most important test.

## Scoring

`eval.py` scores a predictions file against the labels:

```bash
python3 eval.py --cases cases.jsonl --predictions my_model.jsonl
```

Predictions file format (one JSON object per line):

```json
{"id": "SOD-001", "decision": "deny", "confidence": 0.91, "conditions": []}
```

Metrics reported:

- **Accuracy** — fraction of decisions matching the label.
- **False-grant rate** — predicted `grant` where the label is `deny`. The
  security-critical metric: a false grant is a breach or audit failure, not a
  rounding error. Reported overall and per category.
- **False-deny rate** — predicted `deny` where the label is `grant`
  (productivity cost).
- **Escalation recall** — fraction of should-escalate cases correctly escalated.
- **Over-escalation rate** — escalations on should-grant cases (efficiency cost).
- **Calibration (ECE)** — expected calibration error over 10 confidence bins:
  does 0.8 mean 80%? Critical for threshold-setting.
- **Condition coverage** — for time-bound grants (the `jit` cases), did the
  model attach an expiry condition?
- **Per-category accuracy** — where the model is strong vs. blind.

See `prompt_template.md` for how to pose a case to a decision model
(state/question framing for Sage-style and Jev-style APIs).

## Interpreting results

- A model can score 90%+ accuracy and still be unusable if its false grants
  cluster in `adversarial` or `sod`. Read the per-category table, not just the
  headline.
- `escalate` is a first-class correct answer. A model that never escalates is
  overconfident; one that escalates everything is a very expensive router.
- Confidence calibration matters more here than in most benchmarks because
  grant/deny thresholds are set on the probabilities, and the costs are
  asymmetric (false grant ≫ false deny).

## Limitations

- Synthetic: no real org's policies, and fictional justifications can't capture
  the full weirdness of real access requests.
- Labels encode one reasonable security judgment; real orgs differ on edge
  cases (especially `calibration-edge` and `mover`).
- 36 cases is a smoke test, not a certification. Extend with your own history:
  replay past requests and certification decisions through the model and
  measure agreement the same way.

## License

MIT — see `LICENSE`.
