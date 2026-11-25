class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class Student(User):
    def __init__(self, user_id, name, department, semester, teaching_skills, learning_skills):
        super().__init__(user_id, name)
        self.department = department
        self.semester = semester
        self.teaching_skills = teaching_skills
        self.learning_skills = learning_skills

class PeerTeacher(Student):
    def __init__(self, user_id, name, department, semester, teaching_skills, learning_skills):
        super().__init__(user_id, name, department, semester, teaching_skills, learning_skills)

class Skill:
    def __init__(self, name, category, level):
        self.name = name
        self.category = category
        self.level = level

class LearningRequest:
    def __init__(self, learner_id, required_skill, preferred_day, preferred_time, mode):
        self.learner_id = learner_id
        self.required_skill = required_skill
        self.preferred_day = preferred_day
        self.preferred_time = preferred_time
        self.mode = mode
        self.status = "Pending"

class ReportGenerator:
    def __init__(self, report):
        self.report = report

    def display(self):
        return "\n".join(f"{key.replace('_', ' ').title()}: {value}" for key, value in self.report.items())


class PeerMatcher:
    def calculate(self, learner, teacher, request):
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
        if teacher.get("skill_levels", {}).get(request["required_skill"], "").lower() == "advanced":
            score += 2
        return score
