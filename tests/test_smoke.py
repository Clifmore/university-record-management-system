"""Minimal smoke test for the application package."""
import app.db
import app.queries
import app.main


def test_modules_import():
    assert app.db.__doc__
    assert app.queries.__doc__
    assert app.main.__doc__
