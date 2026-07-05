# Team Guide and Ways of Working

**Group C, CSCK542 Databases**

This document sets out how the team works together and how to get a local
environment running. It supports ticket CSC-7. Read it before your first
commit.

## 1. Roles

| Member | Role |
|---|---|
| Ahmed Tayel | Project Manager (also contributes to design, engineering and testing) |
| Adam Ayad | Database Designer / Engineer |
| Awni Almoughrabi | Software Engineer |
| Clifmore Chigumira | Tester |

## 2. Tools

- **Code:** this GitHub repository (University of Liverpool account).
- **Planning:** Linear project "University Record Management System", two sprints.
- **Communication:** Microsoft Teams.
- **Files and report:** shared SharePoint / OneDrive folder.

## 3. Working in Linear

- Every piece of work has a ticket. If it is not on the board, it does not exist.
- Move your ticket through the states as you go: Backlog to Todo to In Progress
  to In Review to Done.
- Reference the ticket id in your branch name and pull request (for example
  `CSC-14`), so work and tracking stay linked.
- If a ticket is unclear or blocked, comment on it and flag it in Teams rather
  than leaving it silent.

## 4. Git workflow

- `main` is protected and always working. Never commit directly to `main`.
- Create a branch per ticket:
  ```bash
  git checkout -b csc-14-db-connection-layer
  ```
- Commit in small, focused steps with clear messages:
  ```
  Add MySQL connection context manager (CSC-14)
  ```
- Open a pull request into `main` when the ticket is ready. At least one other
  member reviews and approves before merge.
- Keep your branch up to date with `main` to avoid large conflicts:
  ```bash
  git checkout main && git pull
  git checkout your-branch && git merge main
  ```

## 5. Code standards

- Python code follows **PEP 8**. Run the linter before opening a pull request:
  ```bash
  flake8 .
  ```
- All database access uses **parameterised queries**. Never build SQL by string
  concatenation (this prevents SQL injection and keeps queries readable).
- Keep functions small and files focused. Handle errors explicitly; do not let
  them pass silently.

## 6. Definition of done

A ticket is done when:

1. The code works and has been run locally.
2. It passes `flake8` with no errors.
3. Any query returns correct results against the dummy data.
4. It has been reviewed and merged into `main`.
5. The Linear ticket is moved to Done.

## 7. Environment setup

You need **Python 3.10+**, **Git**, and a local **MySQL 8** server.

```bash
# 1. clone the repository
git clone https://github.com/ahmed-osama-tayel/university-record-management-system.git
cd university-record-management-system

# 2. create and activate a virtual environment
python -m venv .venv
source .venv/Scripts/activate        # Windows (Git Bash)
# source .venv/bin/activate          # macOS / Linux
pip install -r requirements.txt

# 3. create the database (once the schema is ready)
mysql -u root -p < db/schema.sql
mysql -u root -p < db/seed.sql

# 4. configure your local credentials
cp .env.example .env                 # then edit .env with your MySQL user / password

# 5. run the application
python -m app.main
```

Never commit your `.env` file or any real credentials. `.env` is already listed
in `.gitignore`.

## 8. Meetings

The team meets or reports at three milestones during the project. Minutes are
recorded for each meeting, agreed by all members, and stored in the shared
folder. The minutes form part of the final submission, so please respond within
the agreed window even if you cannot attend live.
