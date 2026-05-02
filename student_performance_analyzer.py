# Student Performance Analyzer
# Author: Inamdar Mohammad Ali
# An AI-powered system that analyzes student data, predicts at-risk students,
# and generates detailed performance reports with recommendations.

import random
import os
import json
from datetime import datetime

# ─────────────────────────────────────────────
#  DATA LAYER — Simulated Student Database
# ─────────────────────────────────────────────

SUBJECTS = ["Mathematics", "Science", "English", "Computer Science", "History"]

SAMPLE_STUDENTS = [
    {"id": "S001", "name": "Aarav Sharma",    "marks": [88, 92, 75, 95, 70]},
    {"id": "S002", "name": "Priya Mehta",     "marks": [45, 38, 52, 40, 35]},
    {"id": "S003", "name": "Rohan Gupta",     "marks": [72, 68, 80, 74, 65]},
    {"id": "S004", "name": "Sneha Patil",     "marks": [95, 98, 90, 97, 92]},
    {"id": "S005", "name": "Arjun Verma",     "marks": [55, 60, 48, 58, 50]},
    {"id": "S006", "name": "Fatima Khan",     "marks": [30, 25, 40, 35, 28]},
    {"id": "S007", "name": "Rahul Desai",     "marks": [78, 82, 70, 88, 75]},
    {"id": "S008", "name": "Ananya Joshi",    "marks": [62, 58, 66, 70, 60]},
    {"id": "S009", "name": "Kabir Singh",     "marks": [20, 18, 30, 22, 15]},
    {"id": "S010", "name": "Meera Nair",      "marks": [85, 79, 88, 82, 90]},
]

# ─────────────────────────────────────────────
#  ML MODULE — Risk Prediction Engine
# ─────────────────────────────────────────────

def calculate_weighted_score(marks):
    """
    Weighted scoring model:
    - Computer Science & Math weighted higher (AI/ML focus)
    - Penalty for any subject below 40 (fail threshold)
    - Bonus for consistency (low variance = reliable student)
    """
    weights = [0.25, 0.20, 0.15, 0.30, 0.10]  # weights per subject
    weighted = sum(m * w for m, w in zip(marks, weights))

    # Consistency bonus/penalty
    avg = sum(marks) / len(marks)
    variance = sum((m - avg) ** 2 for m in marks) / len(marks)
    consistency_factor = max(0, 1 - (variance / 1000))

    # Fail penalty
    fail_count = sum(1 for m in marks if m < 40)
    fail_penalty = fail_count * 5

    final_score = (weighted * consistency_factor) - fail_penalty
    return round(final_score, 2)

def predict_risk(weighted_score, marks):
    """Multi-factor risk classification"""
    fail_subjects = sum(1 for m in marks if m < 40)

    if weighted_score < 35 or fail_subjects >= 3:
        return "🔴 HIGH RISK", "Immediate intervention required"
    elif weighted_score < 55 or fail_subjects >= 1:
        return "🟡 MEDIUM RISK", "Needs academic support and monitoring"
    elif weighted_score < 75:
        return "🟢 LOW RISK", "Performing adequately, minor improvement needed"
    else:
        return "⭐ EXCELLENT", "Top performer — consider advanced opportunities"

def get_grade(percentage):
    if percentage >= 90: return "A+"
    elif percentage >= 80: return "A"
    elif percentage >= 70: return "B"
    elif percentage >= 60: return "C"
    elif percentage >= 50: return "D"
    else: return "F"

# ─────────────────────────────────────────────
#  ANALYTICS ENGINE
# ─────────────────────────────────────────────

def analyze_student(student):
    marks = student["marks"]
    total = sum(marks)
    avg = total / len(marks)
    weighted = calculate_weighted_score(marks)
    risk_label, risk_msg = predict_risk(weighted, marks)
    grade = get_grade(avg)
    best_subject = SUBJECTS[marks.index(max(marks))]
    weak_subject = SUBJECTS[marks.index(min(marks))]
    fail_subjects = [SUBJECTS[i] for i, m in enumerate(marks) if m < 40]

    return {
        "id": student["id"],
        "name": student["name"],
        "marks": marks,
        "total": total,
        "average": round(avg, 2),
        "weighted_score": weighted,
        "grade": grade,
        "risk_label": risk_label,
        "risk_message": risk_msg,
        "best_subject": best_subject,
        "weak_subject": weak_subject,
        "fail_subjects": fail_subjects,
    }

def generate_recommendations(result):
    recs = []
    for i, (subject, mark) in enumerate(zip(SUBJECTS, result["marks"])):
        if mark < 40:
            recs.append(f"  ❌ URGENT: Failing {subject} ({mark}/100) — Seek tutoring immediately.")
        elif mark < 60:
            recs.append(f"  ⚠️  Weak in {subject} ({mark}/100) — Dedicate extra study time.")
        elif mark >= 90:
            recs.append(f"  ✅ Excellent in {subject} ({mark}/100) — Consider competitions or advanced study.")
    if not recs:
        recs.append("  ✅ Balanced performance across all subjects. Keep it up!")
    return recs

# ─────────────────────────────────────────────
#  REPORT GENERATOR
# ─────────────────────────────────────────────

def ascii_bar(value, max_val=100, width=20):
    filled = int((value / max_val) * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"

def print_student_report(result):
    print("\n" + "═" * 55)
    print(f"  STUDENT REPORT — {result['name']} ({result['id']})")
    print("═" * 55)

    print(f"\n  {'Subject':<20} {'Marks':>6}  {'Bar':>25}")
    print("  " + "─" * 52)
    for subject, mark in zip(SUBJECTS, result["marks"]):
        bar = ascii_bar(mark)
        status = "FAIL" if mark < 40 else ""
        print(f"  {subject:<20} {mark:>5}/100  {bar} {status}")

    print("  " + "─" * 52)
    print(f"  {'Total':<20} {result['total']:>5}/{len(SUBJECTS)*100}")
    print(f"  {'Average':<20} {result['average']:>5}%")
    print(f"  {'Weighted Score':<20} {result['weighted_score']:>5}")
    print(f"  {'Grade':<20} {result['grade']:>5}")
    print(f"\n  Risk Status  : {result['risk_label']}")
    print(f"  Assessment   : {result['risk_message']}")
    print(f"\n  Best Subject : {result['best_subject']}")
    print(f"  Needs Work   : {result['weak_subject']}")

    recs = generate_recommendations(result)
    print(f"\n  RECOMMENDATIONS:")
    for r in recs:
        print(r)
    print("═" * 55)

def print_class_summary(results):
    print("\n" + "═" * 55)
    print("           CLASS PERFORMANCE SUMMARY")
    print("═" * 55)

    averages = [r["average"] for r in results]
    class_avg = sum(averages) / len(averages)
    top = max(results, key=lambda x: x["average"])
    bottom = min(results, key=lambda x: x["average"])

    high_risk = [r for r in results if "HIGH" in r["risk_label"]]
    medium_risk = [r for r in results if "MEDIUM" in r["risk_label"]]
    excellent = [r for r in results if "EXCELLENT" in r["risk_label"]]

    print(f"\n  Total Students   : {len(results)}")
    print(f"  Class Average    : {class_avg:.2f}%")
    print(f"  Top Performer    : {top['name']} ({top['average']}%)")
    print(f"  Needs Most Help  : {bottom['name']} ({bottom['average']}%)")
    print(f"\n  ⭐ Excellent     : {len(excellent)} student(s)")
    print(f"  🟡 Medium Risk   : {len(medium_risk)} student(s)")
    print(f"  🔴 High Risk     : {len(high_risk)} student(s)")

    if high_risk:
        print(f"\n  ⚠️  High Risk Students:")
        for r in high_risk:
            print(f"     - {r['name']} ({r['average']}%) — {r['risk_message']}")

    print(f"\n  SUBJECT-WISE CLASS AVERAGES:")
    print("  " + "─" * 40)
    for i, subject in enumerate(SUBJECTS):
        subj_avg = sum(r["marks"][i] for r in results) / len(results)
        bar = ascii_bar(subj_avg)
        print(f"  {subject:<20} {subj_avg:>5.1f}%  {bar}")

    print("═" * 55)

def save_report(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"performance_report_{timestamp}.json"
    data = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_students": len(results),
        "class_average": round(sum(r["average"] for r in results) / len(results), 2),
        "students": results
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n  ✅ Full report saved to: {filename}")

# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────

def add_custom_student(students):
    print("\n--- Add New Student ---")
    sid = input("Student ID (e.g. S011): ").strip()
    name = input("Student Name: ").strip()
    marks = []
    for subject in SUBJECTS:
        while True:
            try:
                m = float(input(f"Marks for {subject} (0-100): "))
                if 0 <= m <= 100:
                    marks.append(m)
                    break
                else:
                    print("Enter value between 0 and 100.")
            except ValueError:
                print("Invalid input.")
    students.append({"id": sid, "name": name, "marks": marks})
    print(f"\n✅ Student '{name}' added successfully!")
    return students

def main():
    students = [s.copy() for s in SAMPLE_STUDENTS]

    print("╔" + "═" * 53 + "╗")
    print("║       STUDENT PERFORMANCE ANALYZER v1.0        ║")
    print("║     AI-Powered Academic Risk Detection System   ║")
    print("║          Author: Inamdar Mohammad Ali           ║")
    print("╚" + "═" * 53 + "╝")

    while True:
        print("\n  MAIN MENU")
        print("  ─────────────────────────────")
        print("  1. View Class Summary Report")
        print("  2. View Individual Student Report")
        print("  3. View All Students Report")
        print("  4. Identify At-Risk Students")
        print("  5. Add a New Student")
        print("  6. Save Report to File")
        print("  7. Exit")
        print("  ─────────────────────────────")

        choice = input("  Enter choice (1-7): ").strip()

        results = [analyze_student(s) for s in students]

        if choice == "1":
            print_class_summary(results)

        elif choice == "2":
            print("\n  Students:")
            for i, s in enumerate(students, 1):
                print(f"  {i}. {s['name']} ({s['id']})")
            try:
                idx = int(input("  Select student number: ")) - 1
                if 0 <= idx < len(students):
                    print_student_report(results[idx])
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a number.")

        elif choice == "3":
            for result in results:
                print_student_report(result)

        elif choice == "4":
            print("\n" + "═" * 55)
            print("          AT-RISK STUDENT IDENTIFICATION")
            print("═" * 55)
            at_risk = [r for r in results if "HIGH" in r["risk_label"] or "MEDIUM" in r["risk_label"]]
            if not at_risk:
                print("  ✅ No at-risk students found!")
            for r in sorted(at_risk, key=lambda x: x["average"]):
                print(f"\n  {r['risk_label']} — {r['name']} ({r['id']})")
                print(f"  Average: {r['average']}% | Grade: {r['grade']}")
                print(f"  → {r['risk_message']}")
                if r["fail_subjects"]:
                    print(f"  Failing: {', '.join(r['fail_subjects'])}")
            print("═" * 55)

        elif choice == "5":
            students = add_custom_student(students)

        elif choice == "6":
            save_report(results)

        elif choice == "7":
            print("\n  Thank you for using Student Performance Analyzer!")
            print("  Goodbye!\n")
            break

        else:
            print("  Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    main()
