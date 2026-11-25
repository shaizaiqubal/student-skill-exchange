# Smart Student Skill Exchange and Peer Learning Management System

## Requirements
- Python 3
- NumPy
- SciPy
- Matplotlib
- Tkinter

## Setup

Open a terminal in this folder and install the libraries:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

On Windows, you can also double-click `run_windows.bat`.
On macOS or Linux, run `bash run_mac_linux.command`.

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

## Notes
All matching is based on predefined conditions. The project does not use AI, machine learning, databases, SQL or external APIs. Data is stored locally in JSON-formatted text files.
