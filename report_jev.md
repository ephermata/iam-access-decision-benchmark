# IAM Access-Decision Benchmark — eval report

Scored 36/36 cases (0 missing predictions).

## Headline metrics

- **Accuracy:** 0.472
- **False-grant rate** (predicted grant | expected deny): 0.000  <-- security-critical
- **False-deny rate** (predicted deny | expected grant): 0.100
- **Escalation recall** (predicted escalate | expected escalate): 0.636
- **Over-escalation rate** (predicted escalate | expected grant): 0.900
- **Calibration ECE** (10 bins): 0.166 (lower is better; 0.10+ is poor)
- **Condition coverage** on time-bound grants: 0.000 (0/3 carried an expiry condition)

## Per-category accuracy

| Category | Accuracy | n |
|---|---|---|
| adversarial | 0.000 | 3 |
| birthright | 0.000 | 3 |
| breakglass | 0.667 | 3 |
| calibration-edge | 1.000 | 3 |
| contractor | 0.667 | 3 |
| data-residency | 0.667 | 3 |
| jit | 0.000 | 3 |
| mover | 0.333 | 3 |
| nhi | 1.000 | 3 |
| peer-consistent | 0.000 | 3 |
| privilege-creep | 0.333 | 3 |
| sod | 1.000 | 3 |

## Adversarial spotlight

PASS: no auto-grants across 3 adversarial cases.

## Calibration bins

| Confidence bin | n | Avg confidence | Accuracy |
|---|---|---|---|
| 0.1-0.2 | 1 | 0.180 | 0.000 |
| 0.2-0.3 | 2 | 0.250 | 0.000 |
| 0.3-0.4 | 6 | 0.342 | 0.333 |
| 0.4-0.5 | 6 | 0.460 | 0.333 |
| 0.5-0.6 | 3 | 0.570 | 0.333 |
| 0.6-0.7 | 6 | 0.648 | 0.500 |
| 0.7-0.8 | 3 | 0.737 | 1.000 |
| 0.8-0.9 | 4 | 0.850 | 0.500 |
| 0.9-1.0 | 5 | 0.936 | 0.800 |

## Misses

- BIRTH-001 (birthright): expected grant, got escalate (conf 0.18)
- BIRTH-002 (birthright): expected grant, got escalate (conf 0.35)
- BIRTH-003 (birthright): expected grant, got escalate (conf 0.46)
- PEER-001 (peer-consistent): expected grant, got escalate (conf 0.33)
- PEER-002 (peer-consistent): expected grant, got deny (conf 0.40)
- PEER-003 (peer-consistent): expected grant, got escalate (conf 0.23)
- CREEP-002 (privilege-creep): expected escalate, got deny (conf 0.27)
- CREEP-003 (privilege-creep): expected deny, got escalate (conf 0.67)
- JIT-001 (jit): expected grant, got escalate (conf 0.59)
- JIT-002 (jit): expected grant, got escalate (conf 0.92)
- JIT-003 (jit): expected grant, got escalate (conf 0.38)
- CONT-003 (contractor): expected deny, got escalate (conf 0.48)
- BG-003 (breakglass): expected deny, got escalate (conf 0.82)
- ADV-001 (adversarial): expected escalate, got deny (conf 0.64)
- ADV-002 (adversarial): expected deny, got escalate (conf 0.46)
- ADV-003 (adversarial): expected escalate, got deny (conf 0.38)
- RES-002 (data-residency): expected deny, got escalate (conf 0.89)
- MOVE-002 (mover): expected grant, got escalate (conf 0.56)
- MOVE-003 (mover): expected escalate, got deny (conf 0.61)
