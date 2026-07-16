"""Database connection layer.

Centralises configuration loading, connection handling and query
execution against the MySQL database. All connector level errors are
translated into :class:`DatabaseError` so callers deal with a single,
friendly exception type.
"""
import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DEFAULTS = {
    "host": "127.0.0.1",
    "port": "3306",
    "user": "root",
    "password": "",
    "database": "university_db",
}


class DatabaseError(Exception):
    """Raised when a database operation fails.

    Carries a human-readable message suitable for showing to a user.
    """


def load_config():
    """Build the connection settings for ``mysql.connector.connect``.

    Values are read from the environment (populated from ``.env`` by
    :func:`dotenv.load_dotenv`), falling back to the defaults that match
    ``.env.example``. The port is returned as an ``int``.
    """
    return {
        "host": os.environ.get("DB_HOST", DEFAULTS["host"]),
        "port": int(os.environ.get("DB_PORT", DEFAULTS["port"])),
        "user": os.environ.get("DB_USER", DEFAULTS["user"]),
        "password": os.environ.get("DB_PASSWORD", DEFAULTS["password"]),
        "database": os.environ.get("DB_NAME", DEFAULTS["database"]),
    }


@contextmanager
def get_cursor():
    """Yield a cursor for a fresh connection, closing both afterwards.

    The connection and cursor are always released in the ``finally``
    block, even if the body raises. Queries in this application are
    read-only, so no commit is performed.
    """
    config = load_config()
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        yield cursor
    except mysql.connector.Error as exc:
        raise DatabaseError(
            "Could not connect to the database. Check that MySQL is "
            "running and your .env settings are correct. "
            "({0})".format(exc)
        ) from exc
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def run_query(sql, params=None):
    """Run a read-only query and return its columns and rows.

    :param sql: SQL statement with ``%s`` placeholders for any values.
    :param params: sequence of parameters bound to the placeholders.
    :returns: a ``(column_names, rows)`` tuple, where ``column_names``
        is a list of strings and ``rows`` is a list of tuples.
    :raises DatabaseError: if the query cannot be executed.
    """
    with get_cursor() as cursor:
        try:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            description = cursor.description or []
            column_names = [column[0] for column in description]
        except mysql.connector.Error as exc:
            raise DatabaseError(
                "The database query could not be completed. "
                "({0})".format(exc)
            ) from exc
    return column_names, rows
