---
name: iiot-reliability-calc
description: >
  Calculates industrial maintenance KPIs (MTBF, MTTF). Triggers when the user asks to evaluate reliability, failure history, or calculate maintenance metrics.
---
# IIoT Reliability Calculator

## Quick Start
```bash
python .agents/skills/iiot-reliability-calc/scripts/calc_kpi.py --input failures.csv
```

## Procedural Workflow
1. Analyze failure history data.
2. Run `calc_kpi.py` to get exact metrics.
3. Provide technical recommendations based on the MTBF/MTTF output.
