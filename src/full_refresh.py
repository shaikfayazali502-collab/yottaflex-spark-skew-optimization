
import sqlite3

def full_refresh():

    connection = sqlite3.connect("yottaflex.db")
    cursor = connection.cursor()

    # Create source table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS source_orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            order_month TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Sample source data
    source_data = [
        (201, 2001, '2026-11-07', '2026-11', 2000, 'Completed', '2026-11-07T10:00:00'),
        (202, 2002, '2026-11-08', '2026-11', 3000, 'Pending', '2026-11-08T11:00:00'),
        (203, 2003, '2026-11-09', '2026-11', 4000, 'Completed', '2026-11-09T12:00:00')
    ]

    # Replace source records
    cursor.execute("DELETE FROM source_orders")

    cursor.executemany("""
        INSERT INTO source_orders VALUES (?, ?, ?, ?, ?, ?, ?)
    """, source_data)

    # Full refresh target
    cursor.execute("DELETE FROM orders")

    cursor.execute("""
        INSERT INTO orders
        SELECT * FROM source_orders
    """)

    connection.commit()

    print("Full refresh completed successfully!")

    cursor.execute("SELECT COUNT(*) FROM orders")

    print("Total target records:", cursor.fetchone()[0])

    connection.close()


if __name__ == "__main__":
    full_refresh()
