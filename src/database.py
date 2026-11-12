
import sqlite3

def create_database():

    connection = sqlite3.connect("yottaflex.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            order_month TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()

    print("Database created successfully!")

if __name__ == "__main__":
    create_database()
