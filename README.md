# Smart Student Skill Exchange and Peer Learning Management System

In a university, students have different skills and interests. One student may be good at Python, another student may be good at graphic design, while another student may be good at communication, mathematics or web development. However, students often do not have a proper platform to exchange their knowledge with one another.
This Python-based Smart Student Skill Exchange and Peer Learning Management System stores student details, teaching skills, learning requirements, available time slots and peer-learning requests. The system compares student skills and suggest suitable peer-learning partners using predefined rules.
It uses rule-based matching, text-file storage, basic OOP and inheritance, recursion, lambda sorting, NumPy, SciPy and Matplotlib.

## Features

- Register and display students
- Add skills and search students by skill or available day
- Create learning requests
- Find peer teachers using the scoring rules from the project brief
- Update request status
- Generate a text-based learning report
- Display basic statistics and save charts
- Sample data for 30 students, 20 skills and 15 requests

## Requirements

- Python 3.10 or newer
- Tkinter (usually included with Python)
- NumPy, SciPy and Matplotlib

## Run

Open a terminal in this project folder and install the packages:

```bash
python -m pip install -r requirements.txt
```

Then start the application:

```bash
python main.py
```

## Project files

- `main.py` - Tkinter interface
- `core.py` - functions, file handling, matching and reports
- `models.py` - classes and inheritance
- `data/` - sample data stored as text files
- `charts/` - shows matplotlib chart

## Main Features
- Register and display students
- Add and search skills
- Create and update learning requests
- Find peer teachers using rule-based matching
- Calculate compatibility scores out of 16
- Generate learning reports
- Display NumPy and SciPy statistics
- Generate Matplotlib charts
- Save information in local text files

## Project Files
- `main.py`: Tkinter graphical interface
- `core.py`: Functions, matching rules and file handling
- `models.py`: Classes and inheritance
- `data/students.txt`: Sample student records
- `data/skills.txt`: Sample skills
- `data/learning_requests.txt`: Sample requests
- `data/session_records.txt`: Sample learning sessions
- `data/learning_reports.txt`: Five sample reports
- `charts/`: Generated graph image

## Sample Data
The project contains 30 students, 20 skills, 15 learning requests, 5 departments and 8 time slots. The 15 requests include 5 completed requests, 5 accepted requests and 5 unmatched pending requests. Therefore, 10 requests have an accepted outcome when completed requests are included.

The assignment lists 15 total requests, 10 accepted requests, 5 completed requests and 5 unmatched requests. These counts overlap if completed requests are counted as previously accepted; this sample treats the 5 completed requests as part of the 10 accepted outcomes.
