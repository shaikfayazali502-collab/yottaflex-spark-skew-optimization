import sqlite3
from src.partition_replacement import partition_replacement


def test_december_data_is_preserved():
    connection = sqlite3.connect("yottaflex.db")
    before = connection.execute(
        "SELECT * FROM orders WHERE order_month = '2026-12'"
    ).fetchall()
    connection.close()

    partition_replacement()

    connection = sqlite3.connect("yottaflex.db")
    after = connection.execute(
        "SELECT * FROM orders WHERE order_month = '2026-12'"
    ).fetchall()
    connection.close()

    assert before == after
    assert len(after) > 0


def test_november_partition_is_replaced():
    partition_replacement()

    connection = sqlite3.connect("yottaflex.db")
    count = connection.execute(
        "SELECT COUNT(*) FROM orders WHERE order_month = '2026-11'"
    ).fetchone()[0]
    connection.close()

    assert count == 2
