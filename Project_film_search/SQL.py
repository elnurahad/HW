from typing import Final

CREATE_DATABASE_SQL: Final[str] = """
CREATE DATABASE IF NOT EXISTS elnur_ahadov_300924;
"""

CREATE_USERS_TABLE_SQL: Final[str] = """
CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);"""

CREATE_QUERIES_TABLE_SQL: Final[str] = """
CREATE TABLE IF NOT EXISTS queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query VARCHAR(100) NOT NULL,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);"""

CREATE_RESPONSE_TABLE_SQL: Final[str] = """
CREATE TABLE IF NOT EXISTS response (
    id INT AUTO_INCREMENT PRIMARY KEY,
    film_id SMALLINT UNSIGNED,
    query_id INT NOT NULL,
    genre_id TINYINT UNSIGNED,
    FOREIGN KEY (query_id) REFERENCES queries(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES sakila.category(category_id)
);"""

CHECK_DATABASE_EXISTS_SQL = """
SELECT SCHEMA_NAME
FROM INFORMATION_SCHEMA.SCHEMATA
WHERE SCHEMA_NAME = %s;
"""

INSERT_USER_SQL: Final[str] = """
INSERT INTO Users (user_name, first_name,
last_name) VALUES (%s, %s, %s);
"""

INSERT_QUERY_SQL: Final[str] = """
INSERT INTO queries (query,
user_id) VALUES (%s, %s);
"""

INSERT_RESPONSE_SQL: Final[str] = """
INSERT INTO response (film_id, query_id,
genre_id) VALUES (%s, %s, %s);
"""

UPDATE_USER_SQL: Final[str] = """
UPDATE Users SET {} = %s WHERE user_name = %s;
"""

SELECT_USER_ID_SQL: Final[str] = """
SELECT id FROM Users WHERE user_name = %s;
"""

SELECT_USER_INFO_SQL: Final[str] = """
SELECT id, first_name, last_name FROM Users
WHERE user_name = %s;
"""

SELECT_TITLE_SQL: Final[str] = """
SELECT title FROM sakila.film WHERE film_id = %s;
"""

SELECT_USER_MOVIE_HISTORY_SQL: Final[str] = """
SELECT DISTINCT f.title, f.release_year
FROM elnur_ahadov_300924.queries q
JOIN elnur_ahadov_300924.response r ON q.id = r.query_id
JOIN sakila.film f ON r.film_id = f.film_id
WHERE q.user_id = (SELECT id FROM Users
WHERE user_name = %s)
ORDER BY q.id DESC;
"""

SELECT_USER_GENRE_HISTORY_SQL: Final[str] = """
SELECT DISTINCT c.name
FROM elnur_ahadov_300924.queries q
JOIN elnur_ahadov_300924.response r ON q.id = r.query_id
JOIN sakila.category c ON r.genre_id = c.category_id
WHERE q.user_id = (SELECT id FROM Users
WHERE user_name = %s)
ORDER BY q.id DESC;
"""

SELECT_MOVIES_BY_TITLE_SQL: Final[str] = """
SELECT f.film_id, f.title, f.release_year, c.name
FROM sakila.film f
JOIN sakila.film_category fc ON f.film_id = fc.film_id
JOIN sakila.category c ON fc.category_id = c.category_id
WHERE f.title LIKE %s;
"""

SELECT_MOVIES_BY_GENRE_SQL: Final[str] = """
SELECT f.film_id, f.title, f.release_year, c.name
FROM sakila.film f
JOIN sakila.film_category fc ON f.film_id = fc.film_id
JOIN sakila.category c ON fc.category_id = c.category_id
WHERE c.name LIKE %s;
"""

SELECT_MOVIES_BY_YEAR_SQL: Final[str] = """
SELECT f.film_id, f.title, f.release_year, c.name
FROM sakila.film f
JOIN sakila.film_category fc ON f.film_id = fc.film_id
JOIN sakila.category c ON fc.category_id = c.category_id
WHERE f.release_year = %s;
"""

SELECT_MOVIES_BY_ACTOR_SQL: Final[str] = """
SELECT f.film_id, f.title, f.release_year,
c.name, a.first_name, a.last_name
FROM sakila.film f
JOIN sakila.film_actor fa ON f.film_id = fa.film_id
JOIN sakila.actor a ON fa.actor_id = a.actor_id
JOIN sakila.film_category fc ON f.film_id = fc.film_id
JOIN sakila.category c ON fc.category_id = c.category_id
WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s;
"""

SELECT_POPULAR_MOVIES_SQL: Final[str] = """
SELECT f.title, COUNT(r.film_id) AS popularity
FROM sakila.film f
JOIN elnur_ahadov_300924.response r ON f.film_id = r.film_id
WHERE r.film_id IS NOT NULL
GROUP BY f.title
ORDER BY popularity DESC
LIMIT 10;
"""

SELECT_POPULAR_GENRES_SQL: Final[str] = """
SELECT c.name, COUNT(r.genre_id) AS popularity
FROM sakila.category c
JOIN elnur_ahadov_300924.response r ON c.category_id = r.genre_id
WHERE r.genre_id IS NOT NULL
GROUP BY c.name
ORDER BY popularity DESC
LIMIT 5;
"""

SELECT_GENRES_SQL: Final[str] = """
SELECT category_id FROM sakila.category WHERE name = %s;
"""

SELECT_MOVIES_FOR_SEARCH_ENGINE: Final[str] = """
SELECT film_id, title, description
FROM sakila.film;
"""
