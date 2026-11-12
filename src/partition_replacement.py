
import sqlite3

def partition_replacement():

    connection = sqlite3.connect("yottaflex.db")
    cursor = connection.cursor()

    try:
        # New data for November partition
        november_data = [
            (301, 3001, '2026-11-11', '2026-11',
             2500, 'Completed', '2026-11-11T10:00:00'),

            (302, 3002, '2026-11-12', '2026-11',
             3500, 'Pending', '2026-11-12T11:00:00')
        ]

        # Add source data table if needed
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

        # Replace only November source records
        cursor.execute("""
            DELETE FROM source_orders
            WHERE order_month = '2026-11'
        """)

        cursor.executemany("""
            INSERT INTO source_orders
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, november_data)

        # Replace only November target partition
        cursor.execute("""
            DELETE FROM orders
            WHERE order_month = '2026-11'
        """)

        cursor.execute("""
            INSERT INTO orders
            SELECT * FROM source_orders
            WHERE order_month = '2026-11'
        """)

        connection.commit()

        print("Partition replacement completed successfully!")

        cursor.execute("""
            SELECT COUNT(*) FROM orders
            WHERE order_month = '2026-11'
        """)

        print("November records:", cursor.fetchone()[0])

        print("\nFINAL ORDER DETAILS")

        cursor.execute("""
            SELECT * FROM orders ORDER BY order_id
        """)

        for row in cursor.fetchall():
            print(row)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    partition_replacement()
