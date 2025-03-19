# В базе данных ich_edit три таблицы. Users с полями (id, name, age), Products с полями (pid,
# prod, quantity) и Sales с полями (sid, id, pid).
# Программа должна вывести все имена из таблицы users, дать пользователю выбрать
# одно из них и вывести все покупки этого пользователя.

import mysql.connector
from config import dbconfig, db_info  

def main():
    with mysql.connector.connect(**dbconfig) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT name FROM users")
            result = cursor.fetchall()
            names = [res[0] for res in result]

            print("Available users:", ", ".join(names))
            selected_name = input("Choose one of the users: ")

            if selected_name not in names:
                print("This user does not exist.")
                return

            sql = """
                SELECT users.name, users.age, product.prod 
                FROM users 
                JOIN sales ON users.id = sales.id 
                JOIN product ON product.pid = sales.pid 
                WHERE users.name = %s
            """
            cursor.execute(sql, (selected_name,))
            purchases = cursor.fetchall()

            if not purchases:
                print(f"The user {selected_name} has no purchases.")
            else:
                print("NAME\t\tAGE\t\tPRODUCT")
                for row in purchases:
                    print(*row, sep="\t\t")

if __name__ == "__main__":
    main()