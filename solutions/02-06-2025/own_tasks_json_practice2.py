import json


def solution(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    best_score = max(student["score"] for student in data["students"])
    best_students = [student["name"] for student in data["students"] if student["score"] == best_score]

    if len(best_students) == 1:
        return f"Top student: {best_students[0]} ({best_score})"
    else:
        names = ", ".join(best_students)
        return f"Top students: {names} ({best_score})"

