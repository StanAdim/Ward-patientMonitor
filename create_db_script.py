import mysql.connector

new_db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = ""
)

my_cursor = new_db.cursor()

#my_cursor.execute("CREATE DATABASE ward_patient")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)