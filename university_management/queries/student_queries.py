"""
Student queries module for the University Management System.

This module contains all database queries related to student operations
including enrollment, grades, and advisor information.
"""

from typing import Dict, List, Optional

from university_management.database.connection import DatabaseConnection


class StudentQueries:
    """
    Handles all student-related database queries.

    This class provides methods for querying student information including
    course enrollments, academic performance, and advisor details.

    Attributes:
        db: DatabaseConnection instance for executing queries

    Example:
        >>> db = DatabaseConnection(config)
        >>> db.connect()
        >>> queries = StudentQueries(db)
        >>> students = queries.get_students_by_course_lecturer('CS101', 'L001')
    """

    def __init__(self, db: DatabaseConnection) -> None:
        """
        Initialize the student queries with a database connection.

        Args:
            db: DatabaseConnection instance

        Raises:
            RuntimeError: If the database connection is not active
        """
        self.db = db
        if not db.conn:
            raise RuntimeError("Database connection must be established first")

    def get_students_by_course_lecturer(
        self, course_code: str, lecturer_id: str
    ) -> List[Dict[str, str]]:
        """
        Get all students enrolled in a specific course taught by a lecturer.

        This query finds all students enrolled in a particular course
        that is taught by a specific lecturer.

        Args:
            course_code: The course code (e.g., 'CS101')
            lecturer_id: The lecturer identifier (e.g., 'L001')

        Returns:
            List of student dictionaries with student details

        Example:
            >>> students = queries.get_students_by_course_lecturer('CS101', 'L001')
            >>> for s in students:
            ...     print(f"{s['name']} - {s['email']}")
            John Doe - john@example.com
            Jane Smith - jane@example.com
        """
        query = """
            SELECT
                s.student_id,
                s.name,
                s.email,
                s.program,
                s.year_of_study
            FROM students s
            JOIN course_enrollments ce ON s.student_id = ce.student_id
            JOIN courses c ON ce.course_id = c.course_id
            WHERE c.course_code = %s AND c.lecturer_id = %s
            ORDER BY s.name
        """

        results = self.db.execute_query(query, (course_code, lecturer_id))

        return [
            {
                "student_id": row[0],
                "name": row[1],
                "email": row[2],
                "program": row[3],
                "year_of_study": row[4],
            }
            for row in results
        ]

    def get_final_year_high_achievers(
        self, min_grade: float = 70.0
    ) -> List[Dict[str, float]]:
        """
        Get final year students with average grade above a threshold.

        This query identifies high-performing students in their final year
        who have maintained an average grade above the specified threshold.

        Args:
            min_grade: Minimum average grade threshold (default: 70.0)

        Returns:
            List of student dictionaries with their average grade

        Example:
            >>> achievers = queries.get_final_year_high_achievers(75.0)
            >>> for s in achievers:
            ...     print(f"{s['name']}: {s['avg_grade']:.2f}%")
            Mary Johnson: 92.50%
            David Wilson: 88.75%
        """
        query = """
            SELECT
                s.student_id,
                s.name,
                s.email,
                AVG(g.grade) as avg_grade,
                COUNT(g.course_id) as courses_taken
            FROM students s
            JOIN grades g ON s.student_id = g.student_id
            WHERE s.year_of_study = 4
            GROUP BY s.student_id, s.name, s.email
            HAVING AVG(g.grade) > %s
            ORDER BY avg_grade DESC
        """

        results = self.db.execute_query(query, (min_grade,))

        return [
            {
                "student_id": row[0],
                "name": row[1],
                "email": row[2],
                "avg_grade": float(row[3]) if row[3] else 0.0,
                "courses_taken": int(row[4]) if row[4] else 0,
            }
            for row in results
        ]

    def get_unregistered_students(self, semester: str) -> List[Dict[str, str]]:
        """
        Get students not registered for the specified semester.

        This query identifies students who have no course enrollments
        for a particular semester.

        Args:
            semester: Semester identifier (e.g., 'Spring 2024')

        Returns:
            List of student dictionaries with basic information

        Example:
            >>> unregistered = queries.get_unregistered_students('Spring 2024')
            >>> for s in unregistered:
            ...     print(f"{s['name']} is not registered for Spring 2024")
        """
        query = """
            SELECT
                s.student_id,
                s.name,
                s.email,
                s.program
            FROM students s
            WHERE NOT EXISTS (
                SELECT 1
                FROM course_enrollments ce
                JOIN courses c ON ce.course_id = c.course_id
                WHERE ce.student_id = s.student_id
                AND c.semester = %s
            )
            ORDER BY s.name
        """

        results = self.db.execute_query(query, (semester,))

        return [
            {"student_id": row[0], "name": row[1], "email": row[2], "program": row[3]}
            for row in results
        ]

    def get_advisor_contact(self, student_id: str) -> Optional[Dict[str, str]]:
        """
        Get contact information for a student's faculty advisor.

        This query retrieves the advisor's contact details for a specific student.

        Args:
            student_id: The student identifier

        Returns:
            Dictionary with advisor details or None if not found

        Example:
            >>> advisor = queries.get_advisor_contact('S001')
            >>> if advisor:
            ...     print(f"Advisor: {advisor['advisor_name']}")
            ...     print(f"Email: {advisor['email']}")
            Advisor: Dr. Sarah Johnson
            Email: sarah.johnson@university.edu
        """
        query = """
            SELECT
                l.name as advisor_name,
                l.email,
                l.phone,
                l.office,
                l.department
            FROM lecturers l
            JOIN advisor_assignments aa ON l.lecturer_id = aa.lecturer_id
            WHERE aa.student_id = %s
        """

        results = self.db.execute_query(query, (student_id,))
        if not results:
            return None

        row = results[0]
        return {
            "advisor_name": row[0],
            "email": row[1],
            "phone": row[2],
            "office": row[3],
            "department": row[4],
        }

    def get_lecturers_by_research_area(
        self, research_area: str
    ) -> List[Dict[str, str]]:
        """
        Get lecturers with expertise in a specific research area.

        This query finds all lecturers who have research interests
        matching the given research area.

        Args:
            research_area: Research area to search for (supports partial match)

        Returns:
            List of lecturer dictionaries with their research area

        Example:
            >>> lecturers = queries.get_lecturers_by_research_area('Machine Learning')
            >>> for l in lecturers:
            ...     print(f"{l['name']} - {l['department']}")
            Dr. Alan Turing - Computer Science
            Dr. Ada Lovelace - Computer Science
        """
        query = """
            SELECT DISTINCT
                l.lecturer_id,
                l.name,
                l.department,
                l.email,
                r.research_area
            FROM lecturers l
            JOIN research_interests r ON l.lecturer_id = r.lecturer_id
            WHERE r.research_area ILIKE %s
            ORDER BY l.name
        """

        results = self.db.execute_query(query, (f"%{research_area}%",))

        return [
            {
                "lecturer_id": row[0],
                "name": row[1],
                "department": row[2],
                "email": row[3],
                "research_area": row[4],
            }
            for row in results
        ]
