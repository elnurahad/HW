import mysql.connector
import logging
from typing import Dict, Any, Optional
from config import dbconfig_edit, dbconfig_read

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='database_connection.log'
)


def get_connection(
    db_name: Optional[str] = None,
    readonly: bool = False
) -> mysql.connector.connection.MySQLConnection:
    config: Dict[str, Any] = dbconfig_read if readonly else dbconfig_edit
    conn_params: Dict[str, Any] = config.copy()

    if db_name:
        conn_params['database'] = db_name

    try:
        connection: mysql.connector.connection.MySQLConnection = (
            mysql.connector.connect(**conn_params)
        )
        logging.info(
            f"Connected to database: {conn_params.get('database')}"
        )
        return connection
    except mysql.connector.Error as err:
        logging.error(
            f"Connection failed to {conn_params.get('database')}: {err}"
        )
        raise
