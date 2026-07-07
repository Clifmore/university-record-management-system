"""Test script to verify the setup is working correctly."""

import os


def test_imports():
    """Test that all modules import correctly."""
    print("Testing imports...")
    try:
        # Test database connection import
        from university_management.database.connection import DatabaseConnection

        print("✅ DatabaseConnection imported successfully")

        # Test student queries import
        from university_management.queries.student_queries import StudentQueries

        print("✅ StudentQueries imported successfully")

        # Actually use the imported classes to avoid F401 errors
        # This just creates dummy instances to show they work
        print(f"   DatabaseConnection class: {DatabaseConnection.__name__}")
        print(f"   StudentQueries class: {StudentQueries.__name__}")

        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_config():
    """Test that configuration files are present."""
    print("\nTesting configuration files...")

    required_files = [
        ".flake8",
        "pyproject.toml",
        ".pre-commit-config.yaml",
    ]

    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} NOT found")
            all_exist = False

    return all_exist


def main():
    """Run all tests."""
    print("=" * 50)
    print("Testing University Management System Setup")
    print("=" * 50)

    success = True

    if not test_imports():
        success = False

    if not test_config():
        success = False

    if success:
        print("\n🎉 All tests passed! Your setup is working perfectly!")
        print("\nYou can now:")
        print("  - Write PEP-8 compliant code")
        print("  - Use pre-commit hooks automatically")
        print("  - Run 'flake8 .' to check your code")
        print("  - Run 'black .' to format your code")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
