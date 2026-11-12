# YottaFlex - Spark Data Skew Optimization Lab

## Project Overview
This project demonstrates data skew in Apache Spark and applies salting to reduce the impact of skewed keys during aggregation.

## Problem
A highly skewed dataset contains 200,000 records. 90% of records belong to one hot customer key, which can create an uneven workload across partitions.

## Solution
The project:
1. Generates reproducible skewed data.
2. Diagnoses data skew.
3. Runs a baseline aggregation.
4. Applies a salting-based two-stage aggregation.
5. Compares execution times.
6. Verifies that both aggregation results are correct.

## Technologies
- Python
- Apache PySpark
- SQLite
- Pytest

## Run the Project

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt