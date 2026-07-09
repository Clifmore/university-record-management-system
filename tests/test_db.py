"""Unit tests for the database connection layer.

These tests mock ``mysql.connector.connect`` so they run without a
live MySQL server.
"""
import unittest
from unittest import mock

import mysql.connector

from app import db


def make_connection(rows=None, description=None, execute_error=None):
    """Build a mock connection whose cursor returns canned results.

    :param rows: value returned by ``cursor.fetchall``.
    :param description: value assigned to ``cursor.description``.
    :param execute_error: exception raised by ``cursor.execute``.
    """
    cursor = mock.MagicMock()
    if execute_error is not None:
        cursor.execute.side_effect = execute_error
    cursor.fetchall.return_value = rows or []
    cursor.description = description or []

    connection = mock.MagicMock()
    connection.cursor.return_value = cursor
    return connection, cursor


class RunQueryTests(unittest.TestCase):

    @mock.patch("mysql.connector.connect")
    def test_returns_columns_and_rows(self, connect):
        rows = [(1, "Alice"), (2, "Bob")]
        description = [("id",), ("name",)]
        connection, cursor = make_connection(rows, description)
        connect.return_value = connection

        columns, result = db.run_query("SELECT id, name FROM students")

        self.assertEqual(columns, ["id", "name"])
        self.assertEqual(result, rows)

    @mock.patch("mysql.connector.connect")
    def test_connection_error_becomes_database_error(self, connect):
        connect.side_effect = mysql.connector.Error("host unreachable")

        with self.assertRaises(db.DatabaseError) as ctx:
            db.run_query("SELECT 1")

        message = str(ctx.exception)
        self.assertIn("Could not connect to the database", message)
        self.assertIn("host unreachable", message)

    @mock.patch("mysql.connector.connect")
    def test_resources_closed_when_execute_raises(self, connect):
        error = mysql.connector.Error("bad query")
        connection, cursor = make_connection(execute_error=error)
        connect.return_value = connection

        with self.assertRaises(db.DatabaseError):
            db.run_query("SELECT bad")

        cursor.close.assert_called_once()
        connection.close.assert_called_once()

    @mock.patch("mysql.connector.connect")
    def test_params_passed_through_unchanged(self, connect):
        connection, cursor = make_connection()
        connect.return_value = connection

        params = (42, "final")
        db.run_query("SELECT * FROM students WHERE id=%s AND year=%s",
                     params)

        cursor.execute.assert_called_once_with(
            "SELECT * FROM students WHERE id=%s AND year=%s", params
        )


if __name__ == "__main__":
    unittest.main()
