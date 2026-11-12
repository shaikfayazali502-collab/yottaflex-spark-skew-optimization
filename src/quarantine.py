
import csv
from validation import validate_orders

sample_records = [
    (501, 5001, 2000, "Completed"),
    (502, 5002, 3000, "Pending"),
    (503, 5003, -500, "Completed"),
    (504, None, 1500, "Pending"),
    (501, 5005, 2500, "Completed"),
    (505, 5006, 1000, "Unknown")
]

# Validate records
valid_records, rejected_records = validate_orders(sample_records)

# Save rejected records
with open("rejected_records.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "order_id",
        "customer_id",
        "amount",
        "status",
        "rejection_reason"
    ])

    for record, reason in rejected_records:
        writer.writerow([*record, reason])

print("\nQuarantine completed successfully!")
print("Rejected records saved:", len(rejected_records))
print("File: rejected_records.csv")
