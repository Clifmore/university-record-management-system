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
    CONCAT(s.first_name, ' ', s.last_name) AS `Name`,
    p.name AS `Program`,
    s.year_of_study AS `Year`
FROM students AS s
JOIN enrolments AS e ON e.student_id = s.student_id
JOIN course_teaching AS ct ON ct.course_code = e.course_code
JOIN lecturers AS l ON l.lecturer_id = ct.lecturer_id
JOIN programs AS p ON p.program_id = s.program_id
WHERE e.course_code = %s
  AND LOWER(l.last_name) = LOWER(%s)
GROUP BY s.student_id, s.first_name, s.last_name, p.name,
    s.year_of_study
ORDER BY s.student_id
"""

LECTURERS_BY_EXPERTISE = """
SELECT
    l.lecturer_id AS `Lecturer ID`,
    CONCAT(l.first_name, ' ', l.last_name) AS `Name`,
    d.name AS `Department`,
    le.expertise_area AS `Expertise Area`
FROM lecturers AS l
JOIN lecturer_expertise AS le ON le.lecturer_id = l.lecturer_id
JOIN departments AS d ON d.department_id = l.department_id
WHERE LOWER(le.expertise_area) LIKE LOWER(%s)
ORDER BY l.lecturer_id, le.expertise_area
"""


def students_in_course_by_lecturer(course_code, lecturer_last_name):
    """Students enrolled in a course taught by a given lecturer.

    Returns the student id, full name, program name and year of
    study for every student enrolled in the course identified by
    ``course_code`` where that course is taught by a lecturer whose
    surname matches ``lecturer_last_name`` (case-insensitive).
    """
    params = (course_code, lecturer_last_name)
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
]
