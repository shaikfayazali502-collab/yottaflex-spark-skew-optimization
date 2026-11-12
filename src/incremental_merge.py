
import sqlite3

def incremental_merge():

    connection = sqlite3.connect("yottaflex.db")
    cursor = connection.cursor()

    try:
        # New and changed source records
        changes = [
            (202, 2002, '2026-11-08', '2026-11',
             3000, 'Completed', '2026-11-10T10:00:00'),

            (204, 2004, '2026-11-10', '2026-11',
             6000, 'Pending', '2026-11-10T11:00:00')
        ]

        # Update source table with incoming records
        cursor.executemany("""
            INSERT INTO source_orders
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(order_id) DO UPDATE SET
                customer_id = excluded.customer_id,
                order_date = excluded.order_date,
                order_month = excluded.order_month,
                amount = excluded.amount,
                status = excluded.status,
                updated_at = excluded.updated_at
        """, changes)

        # Merge source changes into target
        cursor.executemany("""
            INSERT INTO orders
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(order_id) DO UPDATE SET
                customer_id = excluded.customer_id,
                order_date = excluded.order_date,
                order_month = excluded.order_month,
                amount = excluded.amount,
                status = excluded.status,
                updated_at = excluded.updated_at
        """, changes)

        connection.commit()

        print("Incremental merge completed successfully!")
        print("Incoming records processed:", len(changes))

        cursor.execute("SELECT COUNT(*) FROM orders")
        print("Total target records:", cursor.fetchone()[0])

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
    incremental_merge()
