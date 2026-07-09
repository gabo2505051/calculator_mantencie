# Industrial Reliability Calculator (IIoT Reliability Calc) - v2.0

![Status](https://img.shields.io/badge/Status-v2.0_Professional-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas)
![Tests](https://img.shields.io/badge/Tests-22_Passing-brightgreen)

> 🌐 **Language / Idioma:** You are reading the English version. | [Leer en Español → READMEES.md](READMEES.md)

This project is part of my **IIoT Portfolio** and consists of an advanced Reliability Engineering tool designed to optimize decision-making in industrial environments. The application automates the calculation of key performance indicators (KPIs) and provides strategic recommendations based on the historical behavior of assets.

## 📌 Problem Statement

In many industrial plants, maintenance management remains reactive due to:
- **Lack of visibility:** Failure data is often scattered across unstructured spreadsheets or manual logs.
- **Subjectivity:** Decision-making relies on staff intuition rather than precise engineering metrics.
- **"Bad Actors":** Difficulty in quickly identifying which equipment consumes the most resources or fails most frequently.
- **Hidden Costs:** Extended downtime due to lack of maintainability analysis (MTTR).

## 💡 Solution

This calculator addresses these challenges through:
1. **Data Normalization:** Transforms historical records into a clean data structure ready for analysis.
2. **World-Class KPIs:** Automatically calculates **MTBF** (Reliability), **MTTR** (Maintainability), and **MTTF** (Mean Time To First Failure).
3. **Availability Analysis:** Identifies the percentage availability of each asset compared to corporate targets.
4. **Maintenance Intelligence:** A rules engine translates KPIs into concrete technical recommendations, enabling a shift from corrective to preventive and predictive maintenance.

## 🚀 What's New in Version 2.0 (5-Star Improvements)

- **`ReliabilityEngine` Class:** Object-oriented architecture ready for AI agent integration (MantOS).
- **MTTF Implemented:** Calculation of Mean Time To First Failure for non-repairable assets.
- **Trend Detection:** Real Condition D — automatically identifies sustained increases in failure rate (wear indicator).
- **Configurable Thresholds:** `ReliabilityThresholds` class with `dataclass` to adapt criteria without modifying code.
- **Professional Logging:** Timestamp-based logging system replacing all `print()`.
- **Type Hints:** Type annotations on all functions and methods.
- **Test Suite:** 22 unit tests with `pytest` validating formulas, recommendations, and visualization.
- **Organized Output:** Charts saved in the `reports/` folder instead of the project root.

## 🛠️ Key Features

- **Automated KPI Calculation:** Precise computation of MTBF, MTTR, MTTF, and Operational Availability.
- **Recommendations Engine:** Expert system with 5 conditions (Critical, Alert, Improvement, Degradation, Optimal).
- **Synthetic Data Generator:** Ability to simulate complex industrial scenarios (infant mortality, wear, critical assets).
- **Visual Dashboard:** 4 panels including MTBF vs MTTR, Availability, MTTF, and the **Bathtub Curve**.

## 🛠️ Technologies Used

- **Python 3.11+**
- **Pandas:** Time series processing and data cleaning.
- **Matplotlib:** Dashboard generation and technical visualizations.
- **Numpy:** Statistical calculations and failure curve simulations.
- **Pytest:** Unit test automation.

## 📁 Project Structure

```text
cal_mant/
├── reliability_calculator.py  # Main engine (ReliabilityEngine class)
├── generate_dataset.py        # Synthetic industrial data generator
├── tests/                     # Unit test suite
│   └── test_reliability.py    # 22 automated tests
├── reports/                   # Generated dashboard (created automatically)
├── requirements.txt           # Project dependencies
├── PROYECTO_2_PLAN.md         # Development plan documentation
└── README.md
```

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/iiot-reliability-calc.git
   cd iiot-reliability-calc
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the test dataset (Optional):**
   ```bash
   python generate_dataset.py
   ```

4. **Run the calculator:**
   ```bash
   python reliability_calculator.py
   ```

## 🧪 Unit Tests

To verify the integrity of formulas and the recommendations engine:
```bash
pytest tests/ -v
```

## 📊 Results Visualization

The script automatically generates a dashboard at `reports/analisis_confiabilidad_completo.png` that includes:
1. Reliability (MTBF) vs Maintainability (MTTR) comparison.
2. Availability level per equipment with color-coded alerts.
3. MTTF: Mean Time To First Failure per equipment.
4. Bathtub Curve representation to identify lifecycle stages.

---
**Author:** Gabriel Castro - Automation & IIoT Specialist.
