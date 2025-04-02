import logging
import mysql.connector
from typing import Dict, List, Optional, Tuple, Union
from db_connection import get_connection
from SQL import (
    INSERT_USER_SQL,
    SELECT_USER_ID_SQL,
    SELECT_USER_INFO_SQL,
    UPDATE_USER_SQL,
    INSERT_QUERY_SQL,
    SELECT_USER_MOVIE_HISTORY_SQL,
    SELECT_USER_GENRE_HISTORY_SQL,
    SELECT_POPULAR_MOVIES_SQL,
    SELECT_POPULAR_GENRES_SQL,
    INSERT_RESPONSE_SQL,
)


def add_user_to_database(
    username: str,
    first_name: str,
    last_name: str
) -> None:
    conn = None
    try:
        conn = get_connection(db_name='elnur_ahadov_300924')
        cursor = conn.cursor()
        cursor.execute(INSERT_USER_SQL, (username, first_name, last_name))
        conn.commit()
    except mysql.connector.Error as err:
        logging.error(f"Error adding user: {err}")
        raise
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def user_exists_in_database(username: str) -> bool:
    conn = None
    try:
        conn = get_connection(db_name='elnur_ahadov_300924')
        cursor = conn.cursor()
        cursor.execute(SELECT_USER_ID_SQL, (username,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        logging.error(f"Error checking user: {err}")
        raise
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def fetch_user_info(username: str) -> Dict[str, Union[int, str]]:
    conn = None
    try:
        conn = get_connection(db_name='elnur_ahadov_300924')
        cursor = conn.cursor(dictionary=True)
        cursor.execute(SELECT_USER_INFO_SQL, (username,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        logging.error(f"Error fetching user info: {err}")
        raise
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def add_query_to_database(
    query: str,
    user_id: int,
    film_id: Optional[int] = None,
    genre_id: Optional[int] = None
) -> None:
    conn = None
    try:
        conn = get_connection(db_name='elnur_ahadov_300924')
        cursor = conn.cursor()
        cursor.execute(INSERT_QUERY_SQL, (query, user_id))
        query_id = cursor.lastrowid

        if film_id is not None:
            cursor.execute(INSERT_RESPONSE_SQL, (film_id, query_id, None))
        elif genre_id is not None:
            cursor.execute(INSERT_RESPONSE_SQL, (None, query_id, genre_id))

        conn.commit()
    except mysql.connector.Error as err:
        logging.error(f"Error adding query: {err}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def get_user_movie_history(
    username: str
) -> List[Dict[str, Union[str, int]]]:
    conn = None
    try:
        conn = get_connection(db_name='elnur_ahadov_300924')
        cursor = conn.cursor(dictionary=True)
        cursor.execute(SELECT_USER_MOVIE_HISTORY_SQL, (username,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        logging.error(f"Error fetching movie history: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def get_user_genre_history(username: str) -> List[Dict[str, str]]:
    conn = None
    try:
        conn = get_connection(db_name='elnur_ahadov_300924')
        cursor = conn.cursor(dictionary=True)
        cursor.execute(SELECT_USER_GENRE_HISTORY_SQL, (username,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        logging.error(f"Error fetching genre history: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def change_user_information(
    username: str,
    field: str,
    new_value: str
) -> None:
    conn = None
    try:
        conn = get_connection(db_name='elnur_ahadov_300924')
        cursor = conn.cursor()
        query = UPDATE_USER_SQL.format(field)
        cursor.execute(query, (new_value, username))
        conn.commit()
    except mysql.connector.Error as err:
        logging.error(f"Error updating user: {err}")
        raise
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def get_popular_movies() -> List[Tuple[str, int]]:
    conn = None
    try:
        conn = get_connection(db_name='elnur_ahadov_300924')
        cursor = conn.cursor()
        cursor.execute(SELECT_POPULAR_MOVIES_SQL)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        logging.error(f"Error fetching popular movies: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def get_popular_genres() -> List[Tuple[str, int]]:
    conn = None
    try:
        conn = get_connection(db_name='elnur_ahadov_300924')
        cursor = conn.cursor()
        cursor.execute(SELECT_POPULAR_GENRES_SQL)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        logging.error(f"Error fetching popular genres: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
