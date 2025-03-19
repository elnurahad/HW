import mysql.connector
from config import dbconfig, db_info  

table = input("Enter the name of the table: ")

if table not in db_info.keys():
    print("This table does not exist in the database.")
else:
    connection = mysql.connector.connect(**dbconfig)  
    cursor = connection.cursor()
    
    sql = f"SELECT * FROM {table}"  
    cursor.execute(sql)  
    result = cursor.fetchall()  
    
    print(*db_info[table], sep="\t\t")  
    for row in result:
        print(*row, sep="\t\t")  
    
    cursor.close()  
    connection.close()  