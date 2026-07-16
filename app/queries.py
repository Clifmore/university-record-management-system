"""Query functions for the university database.

This module defines the ``QUERIES`` registry consumed by the CLI in
``app.main``. Each entry is a dictionary with three keys:

``title``
    Short, human-readable description shown as a numbered menu item.
``params``
    A list of ``(prompt_text, param_name)`` tuples, in the order they
    should be collected from the user. ``prompt_text`` is passed to
    ``input()`` and the value the user types is passed to ``func`` as
    the keyword argument named ``param_name``. Use an empty list for a
    query that needs no parameters.
``func``
    A callable accepting the parameters named above as keyword
    arguments and returning a ``(columns, rows)`` tuple, matching the
    shape returned by ``app.db.run_query``.

For example, once implemented, an entry might look like::

    {
        "title": "Students enrolled in a course taught by a lecturer",
        "params": [
            ("Course code: ", "course_code"),
            ("Lecturer id: ", "lecturer_id"),
        ],
        "func": students_by_course_and_lecturer,
    }

``QUERIES`` is intentionally empty here; a later ticket populates it
with the application's actual query functions.
"""
from app import db

STUDENTS_IN_COURSE_BY_LECTURER = """
SELECT
    s.student_id AS `Student ID`,
    s.name AS `Name`,
    p.program_name AS `Program`,
    s.year_of_study AS `Year`
FROM students AS s
JOIN enrolments AS e ON e.student_id = s.student_id
JOIN teaching_assignments AS ta
    ON ta.course_code = e.course_code
    AND ta.semester = e.semester
JOIN lecturers AS l ON l.lecturer_id = ta.lecturer_id
JOIN programs AS p ON p.program_id = s.program_id
WHERE e.course_code = %s
  AND LOWER(l.name) LIKE LOWER(%s)
GROUP BY s.student_id, s.name, p.program_name, s.year_of_study
ORDER BY s.student_id
"""

LECTURERS_BY_EXPERTISE = """
SELECT
    l.lecturer_id AS `Lecturer ID`,
    l.name AS `Name`,
    d.dept_name AS `Department`,
    le.expertise_area AS `Expertise Area`
FROM lecturers AS l
JOIN lecturer_expertise AS le ON le.lecturer_id = l.lecturer_id
JOIN departments AS d ON d.dept_id = l.dept_id
WHERE LOWER(le.expertise_area) LIKE LOWER(%s)
ORDER BY l.lecturer_id, le.expertise_area
"""

FINAL_YEAR_HIGH_AVERAGE = """
SELECT
    s.student_id            AS `Student ID`,
    s.name                  AS `Name`,
    p.program_name          AS `Program`,
    s.year_of_study         AS `Year`,
    ROUND(AVG(e.grade), 2)  AS `Average Grade`
FROM students AS s
JOIN programs AS p ON p.program_id = s.program_id
JOIN enrolments AS e ON e.student_id = s.student_id
WHERE s.graduation_status = 'Enrolled'
  AND s.year_of_study = p.duration_years
  AND e.grade IS NOT NULL
GROUP BY s.student_id, s.name, p.program_name, s.year_of_study
HAVING AVG(e.grade) > 70
ORDER BY `Average Grade` DESC, s.student_id
"""

STUDENTS_NOT_REGISTERED_THIS_SEMESTER = """
SELECT
    s.student_id     AS `Student ID`,
    s.name           AS `Name`,
    p.program_name   AS `Program`,
    s.year_of_study  AS `Year`
FROM students AS s
JOIN programs AS p ON p.program_id = s.program_id
WHERE s.graduation_status = 'Enrolled'
  AND NOT EXISTS (
      SELECT 1
      FROM enrolments AS e
      WHERE e.student_id = s.student_id
        AND e.semester = %s
  )
ORDER BY s.student_id
"""


LECTURER_MOST_STUDENT_PROJECTS = """
SELECT
    l.lecturer_id AS `Lecturer ID`,
    l.name        AS `Name`,
    COUNT(DISTINCT sup.project_id) AS `Student Projects Supervised`
FROM lecturers AS l
JOIN (
    SELECT pi_lecturer_id AS lecturer_id, project_id
    FROM research_projects
    UNION
    SELECT lecturer_id, project_id
    FROM project_lecturers
) AS sup ON sup.lecturer_id = l.lecturer_id
JOIN project_students AS ps ON ps.project_id = sup.project_id
GROUP BY l.lecturer_id, l.name
ORDER BY `Student Projects Supervised` DESC, l.name
"""

STUDENT_ADVISOR_CONTACT = """
SELECT
    s.student_id  AS `Student ID`,
    s.name        AS `Student`,
    l.name        AS `Advisor`,
    l.email       AS `Advisor Email`,
    d.dept_name   AS `Advisor Department`
FROM students AS s
JOIN lecturers AS l ON l.lecturer_id = s.advisor_id
JOIN departments AS d ON d.dept_id = l.dept_id
WHERE LOWER(s.name) LIKE LOWER(%s)
ORDER BY s.student_id
"""

COURSES_TAUGHT_IN_DEPARTMENT = """
SELECT DISTINCT
    l.name        AS `Lecturer`,
    c.course_code AS `Course Code`,
    c.course_name AS `Course`,
    ta.semester   AS `Semester`
FROM departments AS d
JOIN lecturers AS l ON l.dept_id = d.dept_id
JOIN teaching_assignments AS ta ON ta.lecturer_id = l.lecturer_id
JOIN courses AS c ON c.course_code = ta.course_code
WHERE LOWER(d.dept_name) = LOWER(%s)
ORDER BY l.name, ta.semester, c.course_code
"""

STAFF_IN_DEPARTMENT = """
SELECT
    l.name       AS `Name`,
    'Lecturer'   AS `Role`,
    d.dept_name  AS `Department`
FROM lecturers AS l
JOIN departments AS d ON d.dept_id = l.dept_id
WHERE LOWER(d.dept_name) = LOWER(%s)
UNION ALL
SELECT
    ns.name       AS `Name`,
    ns.job_title  AS `Role`,
    d.dept_name   AS `Department`
FROM non_academic_staff AS ns
JOIN departments AS d ON d.dept_id = ns.dept_id
WHERE LOWER(d.dept_name) = LOWER(%s)
ORDER BY `Role`, `Name`
"""

RESEARCH_SUPERVISORS_IN_PROGRAM = """
SELECT DISTINCT
    l.name         AS `Supervisor`,
    l.email        AS `Email`,
    p.program_name AS `Program`
FROM (
    SELECT pi_lecturer_id AS lecturer_id, project_id
    FROM research_projects
    UNION
    SELECT lecturer_id, project_id
    FROM project_lecturers
) AS sup
JOIN project_students AS ps ON ps.project_id = sup.project_id
JOIN students AS s ON s.student_id = ps.student_id
JOIN programs AS p ON p.program_id = s.program_id
JOIN lecturers AS l ON l.lecturer_id = sup.lecturer_id
WHERE LOWER(p.program_name) = LOWER(%s)
ORDER BY l.name
"""


def students_in_course_by_lecturer(course_code, lecturer_last_name):
    """Students enrolled in a course taught by a given lecturer.

    Returns the student id, full name, program name and year of study
    for every student enrolled in the course identified by
    ``course_code`` in a semester where that course was taught by a
    lecturer whose name contains ``lecturer_last_name`` (matched
    case-insensitively as a substring, since lecturer names are stored
    in a single ``name`` column).
    """
    params = (course_code, "%{0}%".format(lecturer_last_name))
    return db.run_query(STUDENTS_IN_COURSE_BY_LECTURER, params)


def lecturers_by_expertise(research_area):
    """Lecturers whose expertise matches a research area.

    Returns the lecturer id, full name, department name and the
    matching expertise area for every lecturer with an expertise
    entry containing ``research_area`` as a case-insensitive
    substring.
    """
    params = ("%{0}%".format(research_area),)
    return db.run_query(LECTURERS_BY_EXPERTISE, params)


def students_final_year_high_average():
    """Final-year students whose average grade is above 70%.

    Returns the student id, name, program name, year of study and
    rounded average grade for every currently enrolled student who is
    in the final year of their program (``year_of_study`` equal to the
    program's ``duration_years``) and whose mean grade across all
    completed enrolments exceeds 70. In-progress enrolments (NULL
    grade) are ignored when computing the average. Takes no
    parameters.
    """
    return db.run_query(FINAL_YEAR_HIGH_AVERAGE)


def students_not_registered_this_semester(semester):
    """Enrolled students with no course registration in a semester.

    Returns the student id, name, program name and year of study for
    every currently enrolled student who has no enrolment row for the
    given ``semester`` (for example ``2026-S1``). Uses a ``NOT EXISTS``
    anti-join so students with any registration in that semester are
    excluded.
    """
    params = (semester,)
    return db.run_query(STUDENTS_NOT_REGISTERED_THIS_SEMESTER, params)


def lecturer_most_student_projects():
    """Lecturers ranked by student research projects supervised.

    A lecturer supervises a project if they are its principal
    investigator (``research_projects.pi_lecturer_id``) or a listed
    project lecturer (``project_lecturers``). Only projects that
    involve at least one student (``project_students``) are counted,
    and each project is counted once per lecturer. Results are ordered
    so the lecturer who has supervised the most student research
    projects appears first. Takes no parameters.
    """
    return db.run_query(LECTURER_MOST_STUDENT_PROJECTS)


def student_advisor_contact(student_name):
    """Contact details for a student's academic advisor.

    Returns the student id, student name, and the name, email and
    department of that student's advisor, for every student whose name
    contains ``student_name`` (matched case-insensitively as a
    substring). Students with no advisor assigned are not shown.
    """
    params = ("%{0}%".format(student_name),)
    return db.run_query(STUDENT_ADVISOR_CONTACT, params)


def courses_taught_in_department(dept_name):
    """Courses taught by the lecturers of a given department.

    Returns the lecturer name, course code, course name and semester
    for every teaching assignment held by a lecturer who belongs to
    the department named ``dept_name`` (matched case-insensitively).
    """
    params = (dept_name,)
    return db.run_query(COURSES_TAUGHT_IN_DEPARTMENT, params)


def staff_in_department(dept_name):
    """All staff working in a given department.

    Returns the name, role and department of every member of staff in
    the department named ``dept_name`` (matched case-insensitively),
    combining academic staff (lecturers) and non-academic staff via a
    ``UNION``. Lecturers are shown with the role ``Lecturer``;
    non-academic staff are shown with their job title.
    """
    params = (dept_name, dept_name)
    return db.run_query(STAFF_IN_DEPARTMENT, params)


def research_supervisors_in_program(program_name):
    """Lecturers who supervise research students in a program.

    Returns the name, email and program for every lecturer who
    supervises at least one research student enrolled in the program
    named ``program_name`` (matched case-insensitively). A lecturer
    supervises a project if they are its principal investigator
    (``research_projects.pi_lecturer_id``) or a listed project lecturer
    (``project_lecturers``) -- the same definition used elsewhere in
    this module. Results are de-duplicated so each supervisor appears
    once.
    """
    params = (program_name,)
    return db.run_query(RESEARCH_SUPERVISORS_IN_PROGRAM, params)


QUERIES = [
    {
        "title": "Students enrolled in a course taught by a lecturer",
        "params": [
            ("Course code (e.g. CS101): ", "course_code"),
            ("Lecturer surname: ", "lecturer_last_name"),
        ],
        "func": students_in_course_by_lecturer,
    },
    {
        "title": "Lecturers with expertise in a research area",
        "params": [
            ("Research area (e.g. machine learning): ", "research_area"),
        ],
        "func": lecturers_by_expertise,
    },
    {
        "title": "Final-year students with an average grade above 70%",
        "params": [],
        "func": students_final_year_high_average,
    },
    {
        "title": "Students not registered for any course this semester",
        "params": [
            ("Semester (e.g. 2026-S1): ", "semester"),
        ],
        "func": students_not_registered_this_semester,
    },
    {
        "title": "Lecturer who has supervised the most student research "
                 "projects",
        "params": [],
        "func": lecturer_most_student_projects,
    },
    {
        "title": "Contact details for a student's advisor",
        "params": [
            ("Student name (e.g. Amira): ", "student_name"),
        ],
        "func": student_advisor_contact,
    },
    {
        "title": "Courses taught by lecturers in a department",
        "params": [
            ("Department name (e.g. Computer Science): ", "dept_name"),
        ],
        "func": courses_taught_in_department,
    },
    {
        "title": "Staff working in a department",
        "params": [
            ("Department name (e.g. Computer Science): ", "dept_name"),
        ],
        "func": staff_in_department,
    },
    {
        "title": "Lecturers who supervise research students in a program",
        "params": [
            ("Program name (e.g. Computer Science): ", "program_name"),
        ],
        "func": research_supervisors_in_program,
    },
]
