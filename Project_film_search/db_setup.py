import mysql.connector
import logging
from typing import Optional, Tuple, Any
from db_connection import get_connection
from SQL import (
    CREATE_DATABASE_SQL,
    CREATE_USERS_TABLE_SQL,
    CREATE_QUERIES_TABLE_SQL,
    CREATE_RESPONSE_TABLE_SQL,
    CHECK_DATABASE_EXISTS_SQL
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='database_setup.log'
)


def database_is_exists(db_name: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(CHECK_DATABASE_EXISTS_SQL, (db_name,))
        result: Optional[Tuple[Any, ...]] = cursor.fetchone()
        cursor.close()
        conn.close()
        logging.info(f"Checked if database exists: {db_name}")
        return result is not None
    except mysql.connector.Error as err:
        logging.error(f"Error checking database existence: {err}")
        return False


def create_struct_database() -> None:
    conn: Optional[mysql.connector.connection.MySQLConnection] = None
    cursor: Optional[mysql.connector.cursor.MySQLCursor] = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(CREATE_DATABASE_SQL)
        cursor.execute("USE elnur_ahadov_300924")
        cursor.execute(CREATE_USERS_TABLE_SQL)
        cursor.execute(CREATE_QUERIES_TABLE_SQL)
        cursor.execute(CREATE_RESPONSE_TABLE_SQL)
        logging.info("Database and tables created successfully")
    except mysql.connector.Error as err:
        logging.error(f"MySQL error: {err}")
    finally:
        if conn and conn.is_connected():
            if cursor:
                cursor.close()
            conn.close()
