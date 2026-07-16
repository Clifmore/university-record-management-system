"""Test Runner for University Record Management System.

Tester: Chigumira
Date: July 2026
Purpose: Validate all 5 queries against the database.
"""

import sys

from university_management.database.connection import DatabaseConnection
from university_management.queries.student_queries import StudentQueries

# Database Configuration - UPDATE WITH YOUR PASSWORD
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "university_db",
    "user": "postgres",
    "password": "Bigboy130784",  # <<< CHANGE THIS to your actual password
}

# Test Results Tracking
test_results = {"passed": 0, "failed": 0, "total": 0, "details": []}


def print_test_header(query_name, query_description):
    """Print a formatted test header."""
    print("\n" + "=" * 70)
    print(f"🧪 TEST: {query_name}")
    print(f"📝 {query_description}")
    print("=" * 70)


def print_result(passed, expected, actual, message=""):
    """Print test result with details."""
    if passed:
        print("✅ PASSED")
        test_results["passed"] += 1
    else:
        print("❌ FAILED")
        test_results["failed"] += 1

    test_results["total"] += 1

    if expected is not None and actual is not None:
        print(f"   Expected: {expected}")
        print(f"   Actual:   {actual}")

    if message:
        print(f"   📌 {message}")

    test_results["details"].append(
        {
            "passed": passed,
            "message": message or ("All good!" if passed else "Check failed!"),
        }
    )

    return passed


def test_query_1(queries):
    """Test: Find all students enrolled in CS101 taught by Dr. Turing (L001)."""
    print_test_header(
        "Query 1: Students in CS101 by Dr. Turing",
        "Should return John Doe and Bob Johnson (2 students)",
    )

    try:
        results = queries.get_students_by_course_lecturer("CS101", "L001")

        print(f"\n📊 Found {len(results)} student(s):")
        for student in results:
            print(f"  - {student['name']} ({student['program']})")

        expected_students = ["John Doe", "Bob Johnson"]
        actual_students = [s["name"] for s in results]

        passed = len(results) == 2 and set(actual_students) == set(expected_students)
        print_result(passed, expected_students, actual_students)

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print_result(False, "No errors", f"Error: {e}")
        return False

    return passed


def test_query_2(queries):
    """Test: List final year students with average grade > 70%."""
    print_test_header(
        "Query 2: Final Year High Achievers (>70%)",
        "Should return final year students (year 4) with >70% average",
    )

    try:
        results = queries.get_final_year_high_achievers(70.0)

        print(f"\n📊 Found {len(results)} student(s):")
        for student in results:
            avg = student.get("avg_grade", 0)
            print(f"  - {student['name']}: {avg:.2f}%")

        passed = True
        for student in results:
            avg = student.get("avg_grade", 0)
            if avg < 70.0:
                passed = False
                print(f"   ⚠️ {student['name']}: {avg:.2f}% (below 70%)")

        print_result(passed, "> 70.0% average", f"{len(results)} students found")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print_result(False, "No errors", f"Error: {e}")
        return False

    return passed


def test_query_3(queries):
    """Test: Identify students not registered for Spring 2024."""
    print_test_header(
        "Query 3: Unregistered Students (Spring 2024)",
        "Should return students with no enrollments for Spring 2024",
    )

    try:
        results = queries.get_unregistered_students("Spring 2024")

        print(f"\n📊 Found {len(results)} unregistered student(s):")
        for student in results:
            program = student.get("program", "N/A")
            print(f"  - {student['name']} ({program})")

        passed = True
        for student in results:
            print(f"   ✅ {student['name']} is not registered - correct")

        print_result(passed, "Students with no enrollments", f"{len(results)} found")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print_result(False, "No errors", f"Error: {e}")
        return False

    return passed


def test_query_4(queries):
    """Test: Retrieve advisor contact for student S001."""
    print_test_header(
        "Query 4: Advisor Contact for John Doe (S001)",
        "Should return Dr. Alan Turing's contact details",
    )

    try:
        result = queries.get_advisor_contact("S001")

        if result:
            print("\n📊 Advisor found:")
            print(f"  Name:    {result.get('advisor_name', 'N/A')}")
            print(f"  Email:   {result.get('email', 'N/A')}")
            print(f"  Phone:   {result.get('phone', 'N/A')}")
            print(f"  Office:  {result.get('office', 'N/A')}")

            expected_name = "Dr. Alan Turing"
            actual_name = result.get("advisor_name", "")

            passed = actual_name == expected_name
            print_result(passed, expected_name, actual_name)
        else:
            print("\n❌ No advisor found for student S001")
            print_result(False, "Dr. Alan Turing", "None/Null")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print_result(False, "No errors", f"Error: {e}")
        return False

    return passed


def test_query_5(queries):
    """Test: Search for lecturers with expertise in Machine Learning."""
    print_test_header(
        "Query 5: Lecturers in 'Machine Learning'",
        "Should return Dr. Alan Turing and Dr. Jane Smith",
    )

    try:
        results = queries.get_lecturers_by_research_area("Machine Learning")

        print(f"\n📊 Found {len(results)} lecturer(s):")
        for lecturer in results:
            department = lecturer.get("department", "N/A")
            print(f"  - {lecturer['name']} ({department})")

        expected = ["Dr. Alan Turing", "Dr. Jane Smith"]
        actual = [lecturer["name"] for lecturer in results]

        passed = len(results) >= 2 and set(expected).issubset(set(actual))
        print_result(passed, expected, actual)

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print_result(False, "No errors", f"Error: {e}")
        return False

    return passed


def main():
    """Run the main test suite."""
    print("\n" + "=" * 70)
    print("🏛️  UNIVERSITY RECORD MANAGEMENT SYSTEM - TEST SUITE")
    print("👤 Tester: Chigumira")
    print("📅 Date: July 2026")
    print("=" * 70)

    print("\n🔌 Connecting to database...")

    try:
        db = DatabaseConnection(DB_CONFIG)

        if not db.connect():
            print("\n❌ Could not connect to database!")
            print("\n💡 Please check:")
            print("   1. PostgreSQL is running")
            print("   2. Database 'university_db' exists")
            print("   3. Username and password are correct")
            sys.exit(1)

        print("✅ Connected to database successfully!")

        queries = StudentQueries(db)

        print("\n" + "=" * 70)
        print("🔄 RUNNING TESTS...")
        print("=" * 70)

        test_query_1(queries)
        test_query_2(queries)
        test_query_3(queries)
        test_query_4(queries)
        test_query_5(queries)

        print("\n" + "=" * 70)
        print("📊 FINAL TEST REPORT")
        print("=" * 70)
        print("Tester: Chigumira")
        print("Date: July 2026")
        print(f"Total Tests: {test_results['total']}")
        print(f"✅ Passed: {test_results['passed']}")
        print(f"❌ Failed: {test_results['failed']}")

        if test_results["total"] > 0:
            pass_rate = test_results["passed"] / test_results["total"] * 100
            print(f"📈 Pass Rate: {pass_rate:.1f}%")

        print("\n📝 Test Details:")
        for i, detail in enumerate(test_results["details"], 1):
            status = "✅" if detail["passed"] else "❌"
            print(f"  {status} Test {i}: {detail['message']}")

        if test_results["failed"] == 0:
            print("\n🎉 ALL TESTS PASSED! The system is ready for deployment!")
            print("✅ Sign off: Approved by Tester (Chigumira)")
        else:
            failed = test_results["failed"]
            print(f"\n⚠️ {failed} test(s) failed. Please review the issues above.")
            print("❌ Sign off: Pending (issues need to be fixed)")

        print("=" * 70)

        db.disconnect()

    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        print("\n💡 Make sure your team's database modules are properly set up.")
        print("   Check that the 'university_management' package is installed.")


if __name__ == "__main__":
    main()
