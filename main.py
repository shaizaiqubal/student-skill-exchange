import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import core
from models import ReportGenerator

class SkillExchangeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Student Skill Exchange")
        self.root.geometry("900x620")
        self.root.minsize(760, 520)
        self.build_window()

    def build_window(self):
        heading = tk.Label(self.root, text="Smart Student Skill Exchange", font=("Arial", 22, "bold"))
        heading.pack(pady=(18, 4))
        subtitle = tk.Label(self.root, text="Peer Learning Management System", font=("Arial", 11))
        subtitle.pack(pady=(0, 14))
        buttons = [
            ("Register Student", self.register_student),
            ("Display Students", self.show_students),
            ("Add Skill", self.add_skill),
            ("Search Skill", self.search),
            ("Add Learning Request", self.add_request),
            ("Find Peer Partner", self.find_partner),
            ("Update Request", self.update_request),
            ("Generate Report", self.report),
            ("Display Statistics", self.statistics),
            ("Generate Graphs", self.graphs),
            ("Exit", self.root.destroy)
        ]
        panel = ttk.Frame(self.root, padding=12)
        panel.pack()
        for index, (label, command) in enumerate(buttons):
            ttk.Button(panel, text=label, command=command, width=24).grid(row=index // 3, column=index % 3, padx=8, pady=8)
        self.output = tk.Text(self.root, height=19, width=100, wrap="word", font=("Consolas", 10))
        self.output.pack(fill="both", expand=True, padx=18, pady=12)
        self.show_text("Welcome! Choose an option above. The project includes sample student records.")

    def show_text(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def ask(self, title, prompt):
        return simpledialog.askstring(title, prompt, parent=self.root)

    def register_student(self):
        name = self.ask("Register Student", "Student name:")
        if not name:
            return
        department = self.ask("Register Student", "Department:")
        semester = self.ask("Register Student", "Semester number:")
        email = self.ask("Register Student", "Email:")
        contact = self.ask("Register Student", "Contact number:")
        teaching = self.ask("Register Student", "Teaching skills (comma separated):")
        learning = self.ask("Register Student", "Learning skills (comma separated):")
        day = self.ask("Register Student", "Available day:")
        time = self.ask("Register Student", "Available time (e.g. 2 PM-4 PM):")
        mode = self.ask("Register Student", "Mode (Offline/Online):")
        try:
            student = {
                "name": name.strip(), "department": department.strip(),
                "semester": int(semester), "email": email.strip(), "contact": contact.strip(),
                "teaching_skills": [item.strip() for item in teaching.split(",") if item.strip()],
                "learning_skills": [item.strip() for item in learning.split(",") if item.strip()],
                "available_day": day.strip(), "available_time": time.strip(), "mode": mode.strip(),
                "skill_levels": {}
            }
            valid, result = core.register_student(student)
            if valid:
                messagebox.showinfo("Success", f"Student registered. ID: {result}")
                self.show_text(f"Student registered successfully.\nStudent ID: {result}")
            else:
                messagebox.showerror("Invalid data", result)
        except (ValueError, AttributeError):
            messagebox.showerror("Invalid data", "Please enter a valid semester and complete all fields.")

    def show_students(self):
        students = core.display_students()
        lines = []
        for student in students:
            lines.append(f'{student["student_id"]} | {student["name"]} | {student["department"]} | Semester {student["semester"]}')
            lines.append(f'  Teaches: {", ".join(student["teaching_skills"])}')
            lines.append(f'  Learns: {", ".join(student["learning_skills"])}')
            lines.append(f'  Available: {student["available_day"]}, {student["available_time"]} ({student["mode"]})')
            lines.append("")
        self.show_text("\n".join(lines) if lines else "No students registered.")

    def add_skill(self):
        name = self.ask("Add Skill", "Skill name:")
        category = self.ask("Add Skill", "Category:")
        level = self.ask("Add Skill", "Level (Beginner/Intermediate/Advanced):")
        if name and category and level:
            if core.add_skill(name.strip(), category.strip(), level.strip()):
                self.show_text(f"Skill added: {name}")
            else:
                messagebox.showwarning("Already exists", "That skill is already in the skill list.")

    def search(self):
        keyword = self.ask("Search", "Enter a skill or available day:")
        if not keyword:
            return
        results = core.search_skill(keyword)
        lines = [f'{item["student_id"]} | {item["name"]} | Teaches: {", ".join(item["teaching_skills"])} | Learns: {", ".join(item["learning_skills"])} | {item["available_day"]}' for item in results]
        self.show_text("\n".join(lines) if lines else "No matching students found.")

    def add_request(self):
        learner_id = self.ask("Learning Request", "Learner ID:")
        skill = self.ask("Learning Request", "Required skill:")
        day = self.ask("Learning Request", "Preferred day:")
        time = self.ask("Learning Request", "Preferred time:")
        mode = self.ask("Learning Request", "Mode (Offline/Online):")
        if all([learner_id, skill, day, time, mode]):
            if core.search_student_recursively(core.display_students(), 0, learner_id) is None:
                messagebox.showerror("Not found", "Learner ID does not exist.")
                return
            request = {"learner_id": learner_id.strip(), "required_skill": skill.strip(),
                       "preferred_day": day.strip(), "preferred_time": time.strip(), "mode": mode.strip()}
            request_id = core.add_learning_request(request)
            self.show_text(f"Learning request created: {request_id}")

    def find_partner(self):
        request_id = self.ask("Find Peer Partner", "Enter request ID:")
        if not request_id:
            return
        request = next((item for item in core.display_learning_requests() if item["request_id"].lower() == request_id.lower()), None)
        if not request:
            messagebox.showerror("Not found", "Request ID does not exist.")
            return
        matches = core.find_peer_partners(request)
        if not matches:
            self.show_text("No peer teacher found for this skill.")
            return
        lines = [f'Results for {request_id} - {request["required_skill"]}', ""]
        for item in matches:
            student = item["student"]
            lines.append(f'{student["student_id"]} | {student["name"]} | Score: {item["score"]}/16 | {item["classification"]}')
            lines.append(f'  Department: {student["department"]} | Available: {student["available_day"]}, {student["available_time"]} | {student["mode"]}')
        self.show_text("\n".join(lines))

    def update_request(self):
        request_id = self.ask("Update Request", "Request ID:")
        if not request_id:
            return
        status = self.ask("Update Request", "New status (Pending, Accepted, Rejected, Session Scheduled, Completed, Cancelled):")
        allowed = ["Pending", "Accepted", "Rejected", "Session Scheduled", "Completed", "Cancelled"]
        if status and status.title() in allowed:
            success = core.update_request_status(request_id, status.title())
            self.show_text("Request status updated." if success else "Request ID not found.")
        else:
            messagebox.showerror("Invalid status", "Please enter one of the listed statuses.")

    def report(self):
        report = core.generate_learning_report()
        self.show_text(ReportGenerator(report).display())

    def statistics(self):
        data = core.display_statistics()
        self.show_text("\n".join(f'{key.replace("_", " ").title()}: {value}' for key, value in data.items()))

    def graphs(self):
        path = core.generate_graphs()
        self.show_text(f"Graphs saved to:\n{path}\n\nOpen the charts folder to view the graph.")

if __name__ == "__main__":
    window = tk.Tk()
    app = SkillExchangeApp(window)
    window.mainloop()
