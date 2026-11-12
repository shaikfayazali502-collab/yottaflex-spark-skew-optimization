
import sqlite3

connection = sqlite3.connect("yottaflex.db")
cursor = connection.cursor()

# 1. INSERT a new order
cursor.execute("""
INSERT INTO orders VALUES
(106, 1006, '2026-11-06', '2026-11',
 5500.00, 'Pending', '2026-11-06T10:00:00')
""")

print("New order inserted!")

# 2. UPDATE an existing order
cursor.execute("""
UPDATE orders
SET status = 'Completed'
WHERE order_id = 102
""")

print("Order updated!")

# 3. DELETE an order
cursor.execute("""
DELETE FROM orders
WHERE order_id = 104
""")

print("Order deleted!")

connection.commit()

# Display final records
cursor.execute("SELECT * FROM orders")

for row in cursor.fetchall():
    print(row)

connection.close()
