
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, concat, lit, pmod, xxhash64,
    sum as spark_sum, count
)

# Configuration
NUM_ROWS = 200000
NUM_PARTITIONS = 8
SALT_BUCKETS = 16

def main():

    spark = (
        SparkSession.builder
        .appName("YottaFlex-Spark-Skew-Lab")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "16")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    print("\n===== YOTTAFLEX SPARK SKEW LAB =====")

    # 1. Generate skewed source data
    print("\n1. Generating skewed data...")

    source = (
        spark.range(0, NUM_ROWS, 1, NUM_PARTITIONS)
        .withColumnRenamed("id", "order_id")
        .withColumn(
            "customer_id",
            when(
                col("order_id") % 100 < 90,
                lit("HOT_CUSTOMER")
            ).otherwise(
                concat(lit("CUSTOMER_"), col("order_id").cast("string"))
            )
        )
        .withColumn(
            "amount",
            ((col("order_id") % 1000) + 1).cast("double")
        )
        .cache()
    )

    source.count()

    print("Total records:", source.count())

    # 2. Diagnose data skew
    print("\n2. DATA SKEW DIAGNOSIS")

    source.groupBy("customer_id") \
        .count() \
        .orderBy(col("count").desc()) \
        .show(5, truncate=False)

    # 3. Baseline aggregation
    print("\n3. Running baseline aggregation...")

    start = time.perf_counter()

    baseline = (
        source.groupBy("customer_id")
        .agg(
            spark_sum("amount").alias("total_amount"),
            count("*").alias("total_orders")
        )
        .cache()
    )

    baseline_rows = baseline.collect()
    baseline_time = time.perf_counter() - start

    print("Baseline runtime:", round(baseline_time, 3), "seconds")

    # 4. Apply salting mitigation
    print("\n4. Applying salting mitigation...")

    salted_source = source.withColumn(
        "salt",
        pmod(xxhash64("order_id"), lit(SALT_BUCKETS))
    )

    start = time.perf_counter()

    partial = (
        salted_source.groupBy("customer_id", "salt")
        .agg(
            spark_sum("amount").alias("partial_amount"),
            count("*").alias("partial_orders")
        )
    )

    optimized = (
        partial.groupBy("customer_id")
        .agg(
            spark_sum("partial_amount").alias("total_amount"),
            spark_sum("partial_orders").alias("total_orders")
        )
        .cache()
    )

    optimized_rows = optimized.collect()
    optimized_time = time.perf_counter() - start

    print("Optimized runtime:", round(optimized_time, 3), "seconds")

    # 5. Verify correctness
    print("\n5. CORRECTNESS VERIFICATION")

    baseline_result = {
        row["customer_id"]: (
            row["total_amount"],
            row["total_orders"]
        )
        for row in baseline_rows
    }

    optimized_result = {
        row["customer_id"]: (
            row["total_amount"],
            row["total_orders"]
        )
        for row in optimized_rows
    }

    assert baseline_result.keys() == optimized_result.keys()

    for key in baseline_result:
        old_amount, old_count = baseline_result[key]
        new_amount, new_count = optimized_result[key]

        assert abs(old_amount - new_amount) < 0.001, (
            f"Amount mismatch for {key}"
        )
        assert old_count == new_count, (
            f"Count mismatch for {key}"
        )

    print("PASS: Both results match!")
    print("Baseline groups:", len(baseline_result))
    print("Optimized groups:", len(optimized_result))

    # 6. Performance comparison
    print("\n6. PERFORMANCE COMPARISON")

    print("Baseline:", round(baseline_time, 3), "seconds")
    print("Optimized:", round(optimized_time, 3), "seconds")

    if optimized_time < baseline_time:
        print("Salting was faster in this run.")
    else:
        print("Salting was not faster in this run.")
        print("Additional shuffle overhead may affect small workloads.")

    # 7. Cleanup
    baseline.unpersist()
    optimized.unpersist()
    source.unpersist()
    spark.stop()

    print("\n===== SPARK SKEW LAB COMPLETED =====")


if __name__ == "__main__":
    main()
