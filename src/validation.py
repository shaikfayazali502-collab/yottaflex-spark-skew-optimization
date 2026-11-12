
def validate_orders(records):

    valid_records = []
    rejected_records = []

    seen_ids = set()

    for record in records:

        order_id, customer_id, amount, status = record

        reason = None

        if order_id is None:
            reason = "Missing order ID"

        elif customer_id is None:
            reason = "Missing customer ID"

        elif order_id in seen_ids:
            reason = "Duplicate order ID"

        elif amount is None or amount < 0:
            reason = "Invalid order amount"

        elif status not in ["Completed", "Pending", "Cancelled"]:
            reason = "Invalid order status"

        if reason:
            rejected_records.append((record, reason))
        else:
            valid_records.append(record)
            seen_ids.add(order_id)

    print("VALIDATION REPORT")
    print("-----------------")

    print("Total records:", len(records))
    print("Valid records:", len(valid_records))
    print("Rejected records:", len(rejected_records))

    print("\nVALID RECORDS")

    for record in valid_records:
        print(record)

    print("\nREJECTED RECORDS")

    for record in rejected_records:
        print(record)

    return valid_records, rejected_records


if __name__ == "__main__":

    sample_records = [
        (501, 5001, 2000, "Completed"),
        (502, 5002, 3000, "Pending"),
        (503, 5003, -500, "Completed"),
        (504, None, 1500, "Pending"),
        (501, 5005, 2500, "Completed"),
        (505, 5006, 1000, "Unknown")
    ]

    validate_orders(sample_records)
