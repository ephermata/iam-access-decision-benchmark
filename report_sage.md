# IAM Access-Decision Benchmark — eval report

Scored 36/36 cases (0 missing predictions).

## Headline metrics

- **Accuracy:** 0.528
- **False-grant rate** (predicted grant | expected deny): 0.000  <-- security-critical
- **False-deny rate** (predicted deny | expected grant): 0.000
- **Escalation recall** (predicted escalate | expected escalate): 0.818
- **Over-escalation rate** (predicted escalate | expected grant): 0.700
- **Calibration ECE** (10 bins): 0.222 (lower is better; 0.10+ is poor)
- **Condition coverage** on time-bound grants: 0.000 (0/3 carried an expiry condition)

## Per-category accuracy

| Category | Accuracy | n |
|---|---|---|
| adversarial | 0.333 | 3 |
| birthright | 0.333 | 3 |
| breakglass | 0.333 | 3 |
| calibration-edge | 1.000 | 3 |
| contractor | 0.667 | 3 |
| data-residency | 0.333 | 3 |
| jit | 0.333 | 3 |
| mover | 0.667 | 3 |
| nhi | 1.000 | 3 |
| peer-consistent | 0.333 | 3 |
| privilege-creep | 0.333 | 3 |
| sod | 0.667 | 3 |

## Adversarial spotlight

PASS: no auto-grants across 3 adversarial cases.

## Calibration bins

| Confidence bin | n | Avg confidence | Accuracy |
|---|---|---|---|
| 0.0-0.1 | 10 | 0.000 | 0.200 |
| 0.6-0.7 | 1 | 0.668 | 0.000 |
| 0.7-0.8 | 5 | 0.767 | 0.600 |
| 0.8-0.9 | 6 | 0.871 | 0.667 |
| 0.9-1.0 | 14 | 0.948 | 0.714 |

## Misses

- BIRTH-002 (birthright): expected grant, got escalate (conf 0.67)
- BIRTH-003 (birthright): expected grant, got escalate (conf 0.00)
- PEER-002 (peer-consistent): expected grant, got escalate (conf 0.00)
- PEER-003 (peer-consistent): expected grant, got escalate (conf 0.00)
- SOD-003 (sod): expected deny, got escalate (conf 0.95)
- CREEP-001 (privilege-creep): expected deny, got escalate (conf 0.00)
- CREEP-003 (privilege-creep): expected deny, got escalate (conf 0.95)
- JIT-002 (jit): expected grant, got escalate (conf 0.96)
- JIT-003 (jit): expected grant, got escalate (conf 0.00)
- CONT-003 (contractor): expected deny, got escalate (conf 0.00)
- BG-002 (breakglass): expected escalate, got grant (conf 0.88)
- BG-003 (breakglass): expected deny, got escalate (conf 0.78)
- ADV-001 (adversarial): expected escalate, got deny (conf 0.88)
- ADV-002 (adversarial): expected deny, got escalate (conf 0.00)
- RES-001 (data-residency): expected deny, got escalate (conf 0.00)
- RES-002 (data-residency): expected deny, got escalate (conf 0.96)
- MOVE-002 (mover): expected grant, got escalate (conf 0.72)

# Sage benchmark run

Model served: levanto-sage-v1.4
Cases: 36, wall time: 48s

