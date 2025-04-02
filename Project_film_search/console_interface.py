from typing import List, Tuple
import mysql.connector
from mysql.connector.connection import MySQLConnection
from db_connection import get_connection
from db_operations import (
    add_user_to_database,
    user_exists_in_database,
    fetch_user_info,
    add_query_to_database,
    get_popular_movies,
    change_user_information,
    get_popular_genres,
    get_user_movie_history,
    get_user_genre_history
)
from SQL import (
    SELECT_MOVIES_BY_TITLE_SQL,
    SELECT_MOVIES_BY_GENRE_SQL,
    SELECT_MOVIES_BY_YEAR_SQL,
    SELECT_MOVIES_BY_ACTOR_SQL,
    SELECT_MOVIES_FOR_SEARCH_ENGINE,
    SELECT_GENRES_SQL,
    SELECT_TITLE_SQL
)

from search_engine import find_documents, STOP_WORDS


def get_movies_by_title(conn: MySQLConnection, title: str) -> List[Tuple]:
    cursor = conn.cursor()
    cursor.execute(SELECT_MOVIES_BY_TITLE_SQL, (f'%{title}%',))
    results = cursor.fetchall()
    cursor.close()
    return results


def get_movies_by_genre(conn: MySQLConnection, genre: str) -> List[Tuple]:
    cursor = conn.cursor()
    cursor.execute(SELECT_MOVIES_BY_GENRE_SQL, (f'%{genre}%',))
    results = cursor.fetchall()
    cursor.close()
    return results


def get_movies_by_year(conn: MySQLConnection, year: int) -> List[Tuple]:
    cursor = conn.cursor()
    cursor.execute(SELECT_MOVIES_BY_YEAR_SQL, (year,))
    results = cursor.fetchall()
    cursor.close()
    return results


def get_movies_by_actor(conn: MySQLConnection, actor: str) -> List[Tuple]:
    cursor = conn.cursor()
    cursor.execute(SELECT_MOVIES_BY_ACTOR_SQL, (f'%{actor}%',))
    results = cursor.fetchall()
    cursor.close()
    return results


def get_movies_for_search_engine(conn: MySQLConnection) -> List[Tuple]:
    cursor = conn.cursor()
    cursor.execute(SELECT_MOVIES_FOR_SEARCH_ENGINE)
    results = cursor.fetchall()
    cursor.close()
    return results


def show_search_results(results: List[Tuple], result_type: str) -> None:
    if not results:
        print("\n❌ No results found")
        return

    if result_type == "title":
        print("\n🎬 Found movies:")
        for film_id, title, year, genre in results:
            print(f"  - {title} ({year}) | 💽 {genre}")
    elif result_type == "genre":
        print("\n💽 Movies in this genre:")
        for film_id, title, year, genre in results:
            print(f"  - {title} ({year})")
    elif result_type == "year":
        print("\n📅 Movies in this year:")
        for film_id, title, year, genre in results:
            print(f"  - {title} ({year})")
    elif result_type == "actor":
        print("\n🌟 Movies with this actor:")
        for film_id, title, year, genre, first, last in results:
            print(f"  - {title} ({year}) | 👤 {first} {last}")


def main() -> None:
    username = input("👤 Enter username: ")

    if user_exists_in_database(username):
        user = fetch_user_info(username)
        print(f"🖐 Welcome back, {user['first_name']} {user['last_name']}!")
        user_id = user['id']
    else:
        first_name = input("📝 First name: ")
        last_name = input("📝 Last name: ")
        add_user_to_database(username, first_name, last_name)
        user_id = fetch_user_info(username)['id']
        print("✅ Registration completed")

    conn = get_connection(db_name="sakila")
    all_movies = [(row[0], set(row[2].lower().split()))
                  for row in get_movies_for_search_engine(conn)]
    conn.close()

    while True:
        print("\n1️⃣ - Search by title")
        print("2️⃣ - Search by genre")
        print("3️⃣ - Search by year")
        print("4️⃣ - Search by actor")
        print("5️⃣ - Search by description")
        print("6️⃣ - View statistics")
        print("7️⃣ - Update profile")
        print("8️⃣ - Exit")

        choice = input("👉 Select: ")
        conn = get_connection(db_name="sakila")

        try:
            if choice == "1":
                title = input("\n🔍 Movie title: ")
                results = get_movies_by_title(conn, title)
                show_search_results(results, "title")
                if results:
                    add_query_to_database(
                        title, user_id, film_id=results[0][0])

            elif choice == "2":
                genre = input("\n💽 Genre: ")
                results = get_movies_by_genre(conn, genre)
                show_search_results(results, "genre")
                if results:
                    cursor = conn.cursor()
                    cursor.execute(SELECT_GENRES_SQL, (results[0][3],))
                    genre_id_result = cursor.fetchone()
                    if genre_id_result:
                        add_query_to_database(
                            genre, user_id, genre_id=genre_id_result[0])

            elif choice == "3":
                try:
                    year = int(input("\n📅 Year: "))
                    results = get_movies_by_year(conn, year)
                    show_search_results(results, "year")
                    if results:
                        add_query_to_database(str(year), user_id)
                except ValueError:
                    print("\n⚠️ Please enter a valid year")

            elif choice == "4":
                actor = input("\n🌟 Actor name: ")
                results = get_movies_by_actor(conn, actor)
                show_search_results(results, "actor")
                if results:
                    add_query_to_database(actor, user_id)

            elif choice == "5":
                desc = input("\n📝 Description keywords: ")
                search_results = find_documents(all_movies, STOP_WORDS, desc)

                if search_results:
                    print("\n📝 Top 10 matching movies by relevance:")
                    max_relevance = (
                        search_results[0][1] if search_results else 1
                    )

                    for i, (film_id, relevance) in enumerate(
                            search_results[:10], 1):
                        percentage = int(
                            (relevance / max_relevance) * 100
                        ) if max_relevance > 0 else 0
                        cursor = conn.cursor()
                        cursor.execute(SELECT_TITLE_SQL, (film_id,))
                        title = cursor.fetchone()[0]
                        cursor.close()
                        print(
                            f"  {i}. {title} - Relevance Score: {percentage}%")

                    if search_results:
                        add_query_to_database(
                            desc, user_id, film_id=search_results[0][0])
                else:
                    print("\n❌ No results found")

            elif choice == "6":
                print("\n📊 Statistics Menu:")
                print("1. 🔥 Top 10 Movies")
                print("2. 🏆 Top 5 Genres")
                print("3. 📜 My Search History")
                stat_choice = input("👉 Select: ")

                if stat_choice == "1":
                    print("\n🔥 Top 10 Movies:")
                    for i, (title, count) in enumerate(
                            get_popular_movies(), 1):
                        print(f"  {i}. {title}: {count} searches")

                elif stat_choice == "2":
                    print("\n🏆 Top 5 Genres:")
                    for i, (genre, count) in enumerate(
                            get_popular_genres(), 1):
                        print(f"  {i}. {genre}: {count} searches")

                elif stat_choice == "3":
                    print("\n📜 Your Search History:")

                    movie_history = get_user_movie_history(username)
                    if movie_history:
                        print("\n🎬 Movies you searched for:")
                        for movie in movie_history:
                            print(
                                f"  - {movie['title']} ({movie.get(
                                        'release_year', 'N/A')})")

                    genre_history = get_user_genre_history(username)
                    if genre_history:
                        print("\n💽 Genres you searched for:")
                        for genre in genre_history:
                            print(f"  - {genre['name']}")

                    if not movie_history and not genre_history:
                        print("\n📭 No history found")

            elif choice == "7":
                print("\n⚙️ Update profile:")
                print("1. First name")
                print("2. Last name")
                print("3. Username")
                option = input("👉 Field to update: ")
                new_value = input("✏️ New value: ")
                fields = {
                    '1': 'first_name',
                    '2': 'last_name',
                    '3': 'user_name'}
                if option in fields:
                    change_user_information(
                        username, fields[option], new_value)
                    print("\n✅ Profile updated")
                else:
                    print("\n⚠️ Invalid option")

            elif choice == "8":
                print("\n👋 Goodbye!")
                break

        except mysql.connector.Error as err:
            print(f"\n❌ Database error: {err}")
        finally:
            conn.close()


if __name__ == "__main__":
    main()
