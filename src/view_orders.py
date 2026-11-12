
import sqlite3

connection = sqlite3.connect("yottaflex.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM orders")

rows = cursor.fetchall()

print("ORDER DETAILS")

for row in rows:
    print(row)

connection.close()
