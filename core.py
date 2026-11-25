import json
from pathlib import Path
from datetime import datetime
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).parent / "data"
TIME_SLOTS = ("9 AM-11 AM", "10 AM-12 PM", "12 PM-2 PM", "1 PM-3 PM", "2 PM-4 PM", "3 PM-5 PM", "4 PM-6 PM", "5 PM-7 PM")
STUDENTS_FILE = DATA_DIR / "students.txt"
REQUESTS_FILE = DATA_DIR / "learning_requests.txt"
SKILLS_FILE = DATA_DIR / "skills.txt"
SESSIONS_FILE = DATA_DIR / "session_records.txt"
REPORTS_FILE = DATA_DIR / "learning_reports.txt"

def read_file(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def write_file(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

def load_students_from_file():
    return read_file(STUDENTS_FILE)

def save_students_to_file(students):
    write_file(STUDENTS_FILE, students)

def load_requests_from_file():
    return read_file(REQUESTS_FILE)

def save_requests_to_file(requests):
    write_file(REQUESTS_FILE, requests)

def load_skills():
    return read_file(SKILLS_FILE)

def save_skills(skills):
    write_file(SKILLS_FILE, skills)

def validate_student_data(student):
    required = ["name", "department", "email", "contact", "teaching_skills", "learning_skills"]
    return all(str(student.get(field, "")).strip() for field in required) and student.get("semester", 0) > 0

def register_student(student):
    students = load_students_from_file()
    student["student_id"] = f"STU{1001 + len(students):04d}"
    student["registered_at"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    if not validate_student_data(student):
        return False, "Please enter all required details."
    students.append(student)
    save_students_to_file(students)
    return True, student["student_id"]

def display_students():
    return load_students_from_file()

def add_skill(name, category, level):
    skills = load_skills()
    if any(item["name"].lower() == name.lower() for item in skills):
        return False
    skills.append({"skill_id": f"SK{len(skills)+1:03d}", "name": name, "category": category, "level": level})
    save_skills(skills)
    return True

def search_skill(keyword):
    keyword = keyword.strip().lower()
    results = []
    for student in load_students_from_file():
        teaches = any(keyword in skill.lower() for skill in student["teaching_skills"])
        learns = any(keyword in skill.lower() for skill in student["learning_skills"])
        day_match = keyword in student["available_day"].lower()
        if teaches or learns or day_match:
            results.append(student)
    return results

def add_learning_request(request):
    requests = load_requests_from_file()
    request["request_id"] = f"REQ{len(requests)+1:03d}"
    request["request_date"] = datetime.now().strftime("%d-%m-%Y")
    request["created_at"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    request["status"] = "Pending"
    requests.append(request)
    save_requests_to_file(requests)
    return request["request_id"]

def display_learning_requests():
    return load_requests_from_file()

def search_student_recursively(students, index, student_id):
    if index == len(students):
        return None
    if students[index]["student_id"].lower() == student_id.lower():
        return students[index]
    return search_student_recursively(students, index + 1, student_id)

def find_common_skills(teacher, learner):
    teacher_skills = set(teacher["teaching_skills"])
    learner_skills = set(learner["learning_skills"])
    return teacher_skills.intersection(learner_skills)

def classify_match(score):
    if score >= 13:
        return "Excellent Match"
    elif score >= 9:
        return "Suitable Match"
    elif score >= 5:
        return "Partially Suitable"
    elif score > 0:
        return "Low Compatibility"
    else:
        return "No Match"

def calculate_match_score(learner, teacher, request):
    score = 0
    if request["required_skill"].lower() in [skill.lower() for skill in teacher["teaching_skills"]]:
        score += 5
    if learner["department"] == teacher["department"]:
        score += 2
    if learner["semester"] == teacher["semester"]:
        score += 1
    if request["preferred_day"].lower() == teacher["available_day"].lower():
        score += 2
    if request["preferred_time"].lower() == teacher["available_time"].lower():
        score += 2
    if request["mode"].lower() == teacher["mode"].lower():
        score += 1
    level = teacher.get("skill_levels", {}).get(request["required_skill"], "")
    if level.lower() == "advanced":
        score += 2
    sessions = read_file(SESSIONS_FILE)
    if any(item.get("learner_id") == learner["student_id"] and item.get("teacher_id") == teacher["student_id"] and item.get("status") == "Completed" for item in sessions):
        score += 1
    return score

def sort_matches(matches):
    matches.sort(key=lambda student: student["score"], reverse=True)
    return matches

def find_peer_partners(request):
    students = load_students_from_file()
    learner = search_student_recursively(students, 0, request["learner_id"])
    if learner is None:
        return []
    matches = []
    for teacher in students:
        if teacher["student_id"] != learner["student_id"]:
            if request["required_skill"].lower() in [skill.lower() for skill in teacher["teaching_skills"]]:
                score = calculate_match_score(learner, teacher, request)
                matches.append({
                    "student": teacher,
                    "score": score,
                    "classification": classify_match(score)
                })
    return sort_matches(matches)

def update_request_status(request_id, status):
    requests = load_requests_from_file()
    sessions = read_file(SESSIONS_FILE)
    for request in requests:
        if request["request_id"].lower() == request_id.lower():
            request["status"] = status
            now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            session = next((item for item in sessions if item.get("request_id") == request["request_id"]), None)
            if status in ["Accepted", "Session Scheduled"]:
                matches = find_peer_partners(request)
                teacher_id = matches[0]["student"]["student_id"] if matches else ""
                if session is None:
                    session = {
                        "session_id": f"SES{len(sessions)+1:03d}",
                        "request_id": request["request_id"],
                        "learner_id": request["learner_id"],
                        "teacher_id": teacher_id,
                        "status": status,
                        "scheduled_at": now,
                        "completed_at": ""
                    }
                    sessions.append(session)
                else:
                    session["teacher_id"] = teacher_id or session.get("teacher_id", "")
                    session["status"] = status
                    session["scheduled_at"] = session.get("scheduled_at") or now
            elif status == "Completed":
                if session is None:
                    matches = find_peer_partners(request)
                    teacher_id = matches[0]["student"]["student_id"] if matches else ""
                    session = {
                        "session_id": f"SES{len(sessions)+1:03d}",
                        "request_id": request["request_id"],
                        "learner_id": request["learner_id"],
                        "teacher_id": teacher_id,
                        "status": "Completed",
                        "scheduled_at": now,
                        "completed_at": now
                    }
                    sessions.append(session)
                else:
                    session["status"] = "Completed"
                    session["completed_at"] = now
            save_requests_to_file(requests)
            write_file(SESSIONS_FILE, sessions)
            return True
    return False

def generate_learning_report():
    students = load_students_from_file()
    requests = load_requests_from_file()
    sessions = read_file(SESSIONS_FILE)
    taught = {}
    requested = {}
    teacher_count = {}
    for student in students:
        for skill in student["teaching_skills"]:
            taught[skill] = taught.get(skill, 0) + 1
    for request in requests:
        requested[request["required_skill"]] = requested.get(request["required_skill"], 0) + 1
    for session in sessions:
        teacher_id = session.get("teacher_id")
        if teacher_id:
            teacher_count[teacher_id] = teacher_count.get(teacher_id, 0) + 1
    report = {
        "generated_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "total_students": len(students),
        "total_skills": len(load_skills()),
        "most_taught_skill": max(taught, key=taught.get) if taught else "N/A",
        "most_requested_skill": max(requested, key=requested.get) if requested else "N/A",
        "total_requests": len(requests),
        "accepted_requests": sum(1 for item in requests if item["status"] in ["Accepted", "Completed"]),
        "completed_sessions": sum(1 for item in requests if item["status"] == "Completed"),
        "most_active_peer_teacher": next((student["name"] for student in students if student["student_id"] == max(teacher_count, key=teacher_count.get)), "N/A") if teacher_count else "N/A"
    }
    old_reports = read_file(REPORTS_FILE)
    old_reports.append(report)
    write_file(REPORTS_FILE, old_reports)
    return report

def display_statistics():
    students = load_students_from_file()
    requests = load_requests_from_file()
    scores = []
    for request in requests:
        matches = find_peer_partners(request)
        if matches:
            scores.append(matches[0]["score"])
    score_array = np.array(scores) if scores else np.array([0])
    deviation = float(stats.tstd(score_array)) if len(score_array) > 1 else 0.0
    return {
        "average_score": float(np.mean(score_array)),
        "highest_score": int(np.max(score_array)),
        "score_deviation": deviation,
        "students": len(students),
        "requests": len(requests)
    }

def generate_graphs():
    students = load_students_from_file()
    requests = load_requests_from_file()
    taught = {}
    requested = {}
    statuses = {}
    for student in students:
        for skill in student["teaching_skills"]:
            taught[skill] = taught.get(skill, 0) + 1
    for request in requests:
        requested[request["required_skill"]] = requested.get(request["required_skill"], 0) + 1
        statuses[request["status"]] = statuses.get(request["status"], 0) + 1
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    axes[0].bar(list(taught.keys())[:8], list(taught.values())[:8])
    axes[0].set_title("Most Taught Skills")
    axes[0].tick_params(axis="x", rotation=45)
    axes[1].bar(list(requested.keys())[:8], list(requested.values())[:8])
    axes[1].set_title("Most Requested Skills")
    axes[1].tick_params(axis="x", rotation=45)
    axes[2].bar(list(statuses.keys()), list(statuses.values()))
    axes[2].set_title("Request Status")
    fig.tight_layout()
    output = Path(__file__).parent / "charts" / "learning_statistics.png"
    output.parent.mkdir(exist_ok=True)
    fig.savefig(output)
    plt.close(fig)
    return output
