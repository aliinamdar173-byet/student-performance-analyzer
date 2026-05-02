# 🎓 Student Performance Analyzer — AI-Powered Academic Risk Detection

A sophisticated Python system that analyzes student academic data, predicts at-risk students using a custom weighted ML scoring model, and generates detailed visual reports with personalized recommendations.

> Built with pure Python — no external libraries required.

---

## 🚀 Features

- **AI Risk Engine** — Custom weighted scoring model classifies students into risk levels (High / Medium / Low / Excellent)
- **Multi-factor Analysis** — Considers subject weights, performance consistency (variance), and fail penalties
- **Visual ASCII Reports** — Bar charts for each subject with colour-coded risk indicators
- **Class Summary Dashboard** — Overview of class averages, top/bottom performers, risk distribution
- **Individual Student Reports** — Deep-dive report per student with personalized recommendations
- **At-Risk Detection** — Instantly identifies students needing immediate academic intervention
- **Add Custom Students** — Input your own student data at runtime
- **Export to JSON** — Save complete analysis report with timestamp

---

## 📊 Risk Classification System

| Risk Level   | Weighted Score | Description                          |
|--------------|---------------|--------------------------------------|
| ⭐ Excellent  | 75+           | Top performer                        |
| 🟢 Low Risk  | 55–74         | Performing adequately                |
| 🟡 Medium Risk| 35–54        | Needs monitoring and support         |
| 🔴 High Risk | Below 35      | Immediate intervention required      |

---

## 🧠 How the ML Scoring Works

```
Weighted Score = Σ(mark × subject_weight) × consistency_factor − fail_penalty
```

**Subject Weights:**
| Subject          | Weight |
|------------------|--------|
| Computer Science | 30%    |
| Mathematics      | 25%    |
| Science          | 20%    |
| English          | 15%    |
| History          | 10%    |

- **Consistency Factor** — Rewards students with stable marks across subjects
- **Fail Penalty** — Deducts 5 points per failed subject (below 40)

---

## 🖥️ Menu Options

```
1. View Class Summary Report
2. View Individual Student Report
3. View All Students Report
4. Identify At-Risk Students
5. Add a New Student
6. Save Report to File (JSON)
7. Exit
```

---

## ▶️ How to Run

```bash
python student_performance_analyzer.py
```

No installation needed — works with Python 3.x out of the box.

---

## 📁 Output Example

```
╔══════════════════════════════════════════════════════╗
║       STUDENT PERFORMANCE ANALYZER v1.0             ║
║     AI-Powered Academic Risk Detection System        ║
╚══════════════════════════════════════════════════════╝

  Subject              Marks   Bar
  ────────────────────────────────────────────────────
  Mathematics           88/100  [█████████████████░░░]
  Science               92/100  [██████████████████░░]
  English               75/100  [███████████████░░░░░]
  Computer Science      95/100  [███████████████████░]
  History               70/100  [██████████████░░░░░░]

  Risk Status  : ⭐ EXCELLENT
  Grade        : A
```

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Concepts:** Weighted scoring algorithm, variance analysis, risk classification, data analysis, JSON export, modular programming, OOP-style design

---

## 👨‍💻 Author

**Inamdar Mohammad Ali**
B.E. Computer Science (AI & ML) — M.H. Saboo Siddiq College of Engineering, Mumbai
📧 Aliinamdar173@gmail.com
