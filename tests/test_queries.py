"""Unit tests for query functions.

These tests mock ``app.db.run_query`` so they run without a live
database. They verify that each query function calls ``run_query`` with
the expected SQL statement and parameters, and returns its result
unchanged.
"""
from unittest import mock

from app import queries


@mock.patch("app.db.run_query")
def test_final_year_high_average_uses_no_params(run_query):
    run_query.return_value = (["Student ID"], [(1001,)])

    columns, rows = queries.students_final_year_high_average()

    run_query.assert_called_once_with(queries.FINAL_YEAR_HIGH_AVERAGE)
    assert columns == ["Student ID"]
    assert rows == [(1001,)]


def test_final_year_high_average_registered_in_menu():
    titles = [entry["title"] for entry in queries.QUERIES]

    assert "Final-year students with an average grade above 70%" in titles
    entry = next(
        entry for entry in queries.QUERIES
        if entry["func"] is queries.students_final_year_high_average
    )
    assert entry["params"] == []


def test_final_year_high_average_sql_targets_real_schema():
    sql = queries.FINAL_YEAR_HIGH_AVERAGE

    assert "AVG(e.grade)" in sql
    assert "s.year_of_study = p.duration_years" in sql
    assert "HAVING AVG(e.grade) > 70" in sql


@mock.patch("app.db.run_query")
def test_not_registered_passes_semester_param(run_query):
    run_query.return_value = (["Student ID"], [(1008,), (1009,)])

    columns, rows = queries.students_not_registered_this_semester("2026-S1")

    run_query.assert_called_once_with(
        queries.STUDENTS_NOT_REGISTERED_THIS_SEMESTER, ("2026-S1",)
    )
    assert rows == [(1008,), (1009,)]


def test_not_registered_registered_in_menu():
    entry = next(
        entry for entry in queries.QUERIES
        if entry["func"] is queries.students_not_registered_this_semester
    )
    assert entry["params"] == [("Semester (e.g. 2026-S1): ", "semester")]


def test_not_registered_sql_uses_anti_join():
    sql = queries.STUDENTS_NOT_REGISTERED_THIS_SEMESTER

    assert "NOT EXISTS" in sql
    assert "e.semester = %s" in sql


@mock.patch("app.db.run_query")
def test_advisor_contact_passes_wildcarded_name(run_query):
    run_query.return_value = (["Student"], [("Amira Khalil",)])

    columns, rows = queries.student_advisor_contact("Amira")

    run_query.assert_called_once_with(
        queries.STUDENT_ADVISOR_CONTACT, ("%Amira%",)
    )
    assert rows == [("Amira Khalil",)]


def test_advisor_contact_registered_in_menu():
    entry = next(
        entry for entry in queries.QUERIES
        if entry["func"] is queries.student_advisor_contact
    )
    assert entry["params"] == [("Student name (e.g. Amira): ", "student_name")]


def test_advisor_contact_sql_joins_advisor():
    sql = queries.STUDENT_ADVISOR_CONTACT

    assert "l.lecturer_id = s.advisor_id" in sql
    assert "LOWER(s.name) LIKE LOWER(%s)" in sql


@mock.patch("app.db.run_query")
def test_courses_in_department_passes_dept_param(run_query):
    run_query.return_value = (["Lecturer"], [("Dr Sara Haddad",)])

    columns, rows = queries.courses_taught_in_department("Computer Science")

    run_query.assert_called_once_with(
        queries.COURSES_TAUGHT_IN_DEPARTMENT, ("Computer Science",)
    )
    assert rows == [("Dr Sara Haddad",)]


def test_courses_in_department_registered_in_menu():
    entry = next(
        entry for entry in queries.QUERIES
        if entry["func"] is queries.courses_taught_in_department
    )
    assert entry["params"] == [
        ("Department name (e.g. Computer Science): ", "dept_name"),
    ]


def test_courses_in_department_sql_joins_teaching():
    sql = queries.COURSES_TAUGHT_IN_DEPARTMENT

    assert "teaching_assignments" in sql
    assert "LOWER(d.dept_name) = LOWER(%s)" in sql


@mock.patch("app.db.run_query")
def test_staff_in_department_passes_dept_param_twice(run_query):
    run_query.return_value = (["Name"], [("Dr Sara Haddad",)])

    columns, rows = queries.staff_in_department("Computer Science")

    run_query.assert_called_once_with(
        queries.STAFF_IN_DEPARTMENT,
        ("Computer Science", "Computer Science"),
    )
    assert rows == [("Dr Sara Haddad",)]


def test_staff_in_department_registered_in_menu():
    entry = next(
        entry for entry in queries.QUERIES
        if entry["func"] is queries.staff_in_department
    )
    assert entry["params"] == [
        ("Department name (e.g. Computer Science): ", "dept_name"),
    ]


def test_staff_in_department_sql_unions_both_staff_tables():
    sql = queries.STAFF_IN_DEPARTMENT

    assert "UNION ALL" in sql
    assert "FROM lecturers" in sql
    assert "FROM non_academic_staff" in sql


@mock.patch("app.db.run_query")
def test_research_supervisors_passes_program_param(run_query):
    run_query.return_value = (["Supervisor"], [("Dr Sara Haddad",)])

    columns, rows = queries.research_supervisors_in_program(
        "Computer Science"
    )

    run_query.assert_called_once_with(
        queries.RESEARCH_SUPERVISORS_IN_PROGRAM, ("Computer Science",)
    )
    assert rows == [("Dr Sara Haddad",)]


def test_research_supervisors_registered_in_menu():
    entry = next(
        entry for entry in queries.QUERIES
        if entry["func"] is queries.research_supervisors_in_program
    )
    assert entry["params"] == [
        ("Program name (e.g. Computer Science): ", "program_name"),
    ]


def test_research_supervisors_sql_counts_pi_and_project_lecturers():
    sql = queries.RESEARCH_SUPERVISORS_IN_PROGRAM

    assert "pi_lecturer_id" in sql
    assert "project_lecturers" in sql
    assert "project_students" in sql
    assert "LOWER(p.program_name) = LOWER(%s)" in sql
