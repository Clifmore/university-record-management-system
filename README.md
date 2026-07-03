# University Record Management System

**CSCK542 Databases**

**Group C**

## About

A relational database and Python application for managing the records of a university. The system models the core entities a university depends on: students, lecturers, non-academic staff, courses, departments, programs, and research projects, together with the relationships between them (enrolments, advising, teaching, headships, and project supervision).

The database is implemented in MySQL and normalised to third normal form, so plural attributes such as grades, disciplinary records, academic qualifications, prerequisites, and publications live in their own tables rather than in a single cell. A Python command line interface lets a user run a set of predefined queries against the underlying database.

## Entities

| Entity | Summary |
|---|---|
| Students | ID, name, date of birth, contact details, program, year, grades, graduation status, disciplinary records |
| Lecturers | ID, name, department, qualifications, expertise, course load, research interests, publications |
| Non-Academic Staff | ID, name, job title, department, employment type, contract, salary, emergency contact |
| Courses | Code, name, description, department, level, credits, prerequisites, schedule, lecturers, enrolments, materials |
| Departments | Name, faculty, research areas, courses offered, staff members |
| Programs | Name, degree awarded, duration, course requirements, enrolment details |
| Research Projects | Title, principal investigator, funding, team members, publications, outcomes |

## Queries

The application runs at least five distinct queries, including:

1. Students enrolled in a specific course taught by a particular lecturer.
2. Students with an average grade above 70% who are in their final year.
3. Students who have not registered for any courses in the current semester.
4. Contact information for the faculty advisor of a given student.
5. Lecturers with expertise in a particular research area.
6. Courses taught by lecturers in a specific department.
7. Lecturers who have supervised the most student research projects.
8. Staff employed in a specific department.

## Tech Stack

- MySQL (database)
- Python 3 with `mysql-connector-python` (application + queries)
- `pytest` (tests), `flake8` (PEP-8 compliance)

## Project Structure

```
university-record-management-system/
├── db/
│   ├── schema.sql            # DDL: tables, keys, constraints
│   ├── seed.sql              # dummy data
│   └── college_backup.sql    # full dump (schema + data)
├── app/
│   ├── main.py               # entry point / CLI menu
│   ├── db.py                 # connection layer
│   └── queries.py            # query functions
├── tests/                    # pytest test suite
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

```bash
# 1. clone
git clone https://github.com/ahmed-osama-tayel/university-record-management-system.git
cd university-record-management-system

# 2. create a virtual environment
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt

# 3. create the database (MySQL running locally)
mysql -u root -p < db/schema.sql
mysql -u root -p < db/seed.sql

# 4. configure credentials (copy and edit)
cp .env.example .env

# 5. run
python -m app.main
```

## Team

| Member | Role |
|---|---|
| Ahmed Tayel | Project Manager |
| Adam Ayad | Database Designer / Engineer |
| Awni Almoughrabi | Software Engineer |
| Clifmore Chigumira | Tester |

## Project Management

Work is tracked in Linear across two sprints (30 June to 20 July 2026). Meeting minutes are recorded for each milestone and included in the final submission.
