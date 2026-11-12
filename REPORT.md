
# YottaFlex 72-Hour Challenge
## Spark Data Skew Diagnosis and Salting Optimization

### 1. Project Overview

This project demonstrates data skew in Apache Spark and implements salting as a mitigation technique for skewed-key aggregation.

### 2. Environment

- Language: Python
- Processing framework: Apache PySpark 4.3.0
- Java: OpenJDK 17
- Execution mode: Local Spark (local[*])
- Dataset size: 200,000 records
- Initial partitions: 8
- Shuffle partitions: 16
- Salt buckets: 16

### 3. Data Generation and Skew Diagnosis

A synthetic dataset of 200,000 records was generated.

- 180,000 records (90%) belong to HOT_CUSTOMER.
- Remaining 20,000 records belong to individual customer keys.
- Total distinct customer groups: 20,001.

This distribution demonstrates significant key skew.

### 4. Baseline Implementation

The baseline implementation groups records by customer_id and calculates:

- Total amount
- Total number of orders

A single-stage aggregation is used as the reference implementation.

### 5. Optimization: Salting

A deterministic salt value is calculated using xxhash64(order_id) and 16 salt buckets.

The aggregation is performed in two stages:

1. Group by customer_id and salt.
2. Aggregate the partial results by customer_id.

This distributes the hot-key aggregation across salted groups before combining the partial results.

### 6. Benchmark Observations

| Run | Baseline (seconds) | Salted (seconds) |
|---|---:|---:|
| 1 | 2.795 | 2.039 |
| 2 | 3.038 | 2.489 |

The salted implementation was faster in both observed local runs.

These are observational results from two runs, not a statistically conclusive benchmark. Execution time can vary with hardware, JVM warm-up, Spark scheduling, and system load.

### 7. Correctness Verification

Both implementations were compared using:

- Customer group keys
- Total aggregated amounts
- Total order counts

The verification passed in both observed Spark runs.

- Baseline groups: 20,001
- Optimized groups: 20,001
- Aggregation results: Matching

### 8. Automated Testing

Partition replacement tests were executed using pytest.

Result:
- 2 tests passed
- Execution time: 0.43 seconds

### 9. Design Decisions and Trade-offs

- Deterministic hashing provides reproducible salt assignment.
- Two-stage aggregation reduces concentration on the hot key.
- Additional shuffle and aggregation work is introduced by salting.
- A larger salt count is not automatically better.
- Salting may not improve small or evenly distributed workloads.

### 10. Limitations

- This experiment runs locally, not on a distributed Spark cluster.
- Only one synthetic skew distribution is tested.
- Benchmark observations are based on two runs.
- No production-scale cluster comparison has been performed.
- Hardware and system load may influence runtime.

### 11. Conclusion

The project successfully generates skewed data, diagnoses a hot key, implements salting, and verifies that optimized aggregation preserves the baseline results.

The observed local benchmark runs show lower execution times with salting, while further repeated and distributed testing is needed to establish consistent performance improvements.
