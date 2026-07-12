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
