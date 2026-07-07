"""
Database connection module for the University Management System.

This module provides a robust database connection handler with transaction
support and query execution capabilities.
"""

import logging
from contextlib import contextmanager
from typing import Dict, List, Optional, Tuple, Union

import psycopg2
from psycopg2.extras import execute_batch

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Handles all database operations with transaction support.

    This class provides a clean interface for database operations including
    connection management, query execution, and transaction handling.

    Attributes:
        config: Database configuration dictionary
        conn: Active database connection
        logger: Logger instance for this class

    Example:
        >>> config = {
        ...     'host': 'localhost',
        ...     'port': 5432,
        ...     'database': 'university_db',
        ...     'user': 'postgres',
        ...     'password': 'secret'
        ... }
        >>> db = DatabaseConnection(config)
        >>> db.connect()
        True
    """

    def __init__(self, config: Dict[str, Union[str, int]]) -> None:
        """
        Initialize the database connection manager.

        Args:
            config: Dictionary containing database connection parameters
        """
        self.config = config
        self.conn = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """
        Establish a connection to the database.

        Returns:
            bool: True if connection successful, False otherwise

        Example:
            >>> db.connect()
            True
        """
        try:
            self.conn = psycopg2.connect(**self.config)
            self.logger.info("Database connection established successfully")
            return True
        except psycopg2.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            return False

    def disconnect(self) -> None:
        """Close the database connection and clean up resources."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.logger.info("Database connection closed")

    @contextmanager
    def transaction(self):
        """
        Context manager for handling database transactions.

        This ensures proper commit/rollback behavior for database operations.

        Yields:
            cursor: Database cursor for executing queries

        Raises:
            RuntimeError: If no active database connection exists
            Exception: If an error occurs during the transaction

        Example:
            >>> with db.transaction() as cursor:
            ...     cursor.execute("INSERT INTO students VALUES (%s, %s)", (1, 'John'))
        """
        if not self.conn:
            raise RuntimeError("No active database connection")

        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
            self.logger.debug("Transaction committed successfully")
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Transaction failed, rolled back: {e}")
            raise
        finally:
            cursor.close()

    def execute_query(
        self, query: str, params: Optional[Tuple] = None, fetch: bool = True
    ) -> Union[List[Tuple], bool]:
        """
        Execute a SQL query with parameters.

        Args:
            query: SQL query string with placeholders
            params: Tuple of parameters for the query
            fetch: Whether to fetch and return results

        Returns:
            List of tuples if fetch=True, otherwise True

        Raises:
            RuntimeError: If no active database connection exists

        Example:
            >>> results = db.execute_query(
            ...     "SELECT * FROM students WHERE year = %s",
            ...     (4,)
            ... )
            >>> print(results)
            [(1, 'John Doe', 4), (2, 'Jane Smith', 4)]
        """
        if not self.conn:
            raise RuntimeError("No active database connection")

        with self.transaction() as cursor:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            return True

    def execute_batch(
        self, query: str, params_list: List[Tuple], page_size: int = 1000
    ) -> bool:
        """
        Execute a batch query with multiple parameter sets.

        This is more efficient for inserting/updating many records.

        Args:
            query: SQL query string with placeholders
            params_list: List of parameter tuples
            page_size: Number of records per batch

        Returns:
            bool: True if successful

        Example:
            >>> students = [(1, 'John'), (2, 'Jane'), (3, 'Bob')]
            >>> db.execute_batch(
            ...     "INSERT INTO students (id, name) VALUES (%s, %s)",
            ...     students
            ... )
            True
        """
        if not self.conn:
            raise RuntimeError("No active database connection")

        with self.transaction() as cursor:
            execute_batch(cursor, query, params_list, page_size)
            return True

    def __enter__(self):
        """
        Enter context manager for 'with' statement.

        Returns:
            DatabaseConnection: Self instance
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager and clean up.

        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        """
        self.disconnect()


def create_connection_string(config: Dict[str, Union[str, int]]) -> str:
    """
    Create a database connection string from configuration.

    Args:
        config: Dictionary with database connection parameters

    Returns:
        str: Formatted connection string

    Example:
        >>> config = {'host': 'localhost', 'port': 5432, 'database': 'db'}
        >>> create_connection_string(config)
        'host=localhost port=5432 dbname=db'
    """
    return (
        f"host={config.get('host', 'localhost')} "
        f"port={config.get('port', 5432)} "
        f"dbname={config.get('database', 'university_db')} "
        f"user={config.get('user', 'postgres')} "
        f"password={config.get('password', '')}"
    )
