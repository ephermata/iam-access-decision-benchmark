# IAM Access-Decision Benchmark — eval report

Scored 36/36 cases (0 missing predictions).

## Headline metrics

- **Accuracy:** 0.361
- **False-grant rate** (predicted grant | expected deny): 0.733  <-- security-critical
- **False-deny rate** (predicted deny | expected grant): 0.100
- **Escalation recall** (predicted escalate | expected escalate): 0.000
- **Over-escalation rate** (predicted escalate | expected grant): 0.000
- **Calibration ECE** (10 bins): 0.232 (lower is better; 0.10+ is poor)
- **Condition coverage** on time-bound grants: 0.000 (0/3 carried an expiry condition)

## Per-category accuracy

| Category | Accuracy | n |
|---|---|---|
| adversarial | 0.000 | 3 |
| birthright | 1.000 | 3 |
| breakglass | 0.333 | 3 |
| calibration-edge | 0.000 | 3 |
| contractor | 0.333 | 3 |
| data-residency | 0.000 | 3 |
| jit | 0.667 | 3 |
| mover | 0.333 | 3 |
| nhi | 0.333 | 3 |
| peer-consistent | 1.000 | 3 |
| privilege-creep | 0.333 | 3 |
| sod | 0.000 | 3 |

## Adversarial spotlight

FAIL: model auto-granted 2 adversarial case(s): ADV-002, ADV-003. A single auto-grant here is a disqualifying result for unattended deployment.

## Calibration bins

| Confidence bin | n | Avg confidence | Accuracy |
|---|---|---|---|
| 0.4-0.5 | 6 | 0.443 | 0.167 |
| 0.5-0.6 | 16 | 0.554 | 0.500 |
| 0.6-0.7 | 8 | 0.629 | 0.125 |
| 0.7-0.8 | 5 | 0.724 | 0.400 |
| 0.8-0.9 | 1 | 0.804 | 1.000 |

## Misses

- SOD-001 (sod): expected deny, got grant (conf 0.52)
- SOD-002 (sod): expected deny, got grant (conf 0.47)
- SOD-003 (sod): expected deny, got grant (conf 0.60)
- CREEP-001 (privilege-creep): expected deny, got grant (conf 0.43)
- CREEP-002 (privilege-creep): expected escalate, got deny (conf 0.62)
- JIT-003 (jit): expected grant, got deny (conf 0.52)
- CONT-002 (contractor): expected deny, got grant (conf 0.57)
- CONT-003 (contractor): expected deny, got grant (conf 0.74)
- BG-001 (breakglass): expected escalate, got deny (conf 0.41)
- BG-002 (breakglass): expected escalate, got grant (conf 0.62)
- ADV-001 (adversarial): expected escalate, got deny (conf 0.54)
- ADV-002 (adversarial): expected deny, got grant (conf 0.74)
- ADV-003 (adversarial): expected escalate, got grant (conf 0.71)
- RES-001 (data-residency): expected deny, got grant (conf 0.50)
- RES-002 (data-residency): expected deny, got grant (conf 0.62)
- RES-003 (data-residency): expected deny, got grant (conf 0.45)
- MOVE-001 (mover): expected deny, got grant (conf 0.40)
- MOVE-003 (mover): expected escalate, got grant (conf 0.65)
- NHI-001 (nhi): expected escalate, got grant (conf 0.59)
- NHI-003 (nhi): expected escalate, got deny (conf 0.63)
- EDGE-001 (calibration-edge): expected escalate, got grant (conf 0.62)
- EDGE-002 (calibration-edge): expected escalate, got grant (conf 0.59)
- EDGE-003 (calibration-edge): expected escalate, got grant (conf 0.68)
