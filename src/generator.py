
import sqlite3

def insert_sample_orders():

    connection = sqlite3.connect("yottaflex.db")

    cursor = connection.cursor()

    orders = [
        (101, 1001, "2026-11-01", "2026-11", 1500.00, "Completed", "2026-11-01T10:00:00"),
        (102, 1002, "2026-11-02", "2026-11", 2500.00, "Pending", "2026-11-02T11:00:00"),
        (103, 1003, "2026-11-03", "2026-11", 3500.00, "Completed", "2026-11-03T12:00:00"),
        (104, 1004, "2026-11-04", "2026-11", 1200.00, "Cancelled", "2026-11-04T13:00:00"),
        (105, 1005, "2026-11-05", "2026-11", 4500.00, "Completed", "2026-11-05T14:00:00")
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO orders
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, orders)

    connection.commit()

    connection.close()

    print("5 sample orders inserted successfully!")

if __name__ == "__main__":
    insert_sample_orders()
