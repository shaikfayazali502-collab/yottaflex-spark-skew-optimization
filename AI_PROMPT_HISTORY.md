# AI Prompt History

## Project: YottaFlex Spark Data Skew Optimization

AI assistance was used during project development for learning, debugging, implementation guidance, and documentation.

### Development Assistance

1. Understanding the YottaFlex 72-hour challenge requirements.
2. Understanding Spark data skew and hot-key distribution.
3. Generating synthetic skewed datasets.
4. Implementing baseline Spark aggregation.
5. Implementing two-stage salting optimization.
6. Comparing baseline and optimized execution times.
7. Verifying aggregation correctness.
8. Debugging Python imports and pytest errors.
9. Preparing GitHub and project documentation.

### Example Prompts

- Explain Spark data skew in simple terms.
- Generate a reproducible skewed dataset using PySpark.
- Implement baseline aggregation by customer ID.
- Explain salting and how it reduces data skew.
- Compare baseline and salted aggregation results.
- Help debug pytest import errors.
- Prepare project setup and execution instructions.

### AI Usage Disclosure

AI assistance was used as a development aid. Code was executed locally, and reported test and benchmark results were obtained from actual execution.

This document summarizes AI assistance and is not a verbatim transcript of all prompts.## AI Tool Disclosure
ChatGPT was the only AI tool used during this project. No other AI tools such as Gemini, Claude, or GitHub Copilot were used.
## Reconstructed Prompt and Task History
The following is a reconstructed summary of the requests made during development, not a verbatim transcript of every chat message.
1. Understand the YottaFlex 72-hour project requirements and submission guidelines.
2. Help build a reproducible Spark workload with a highly skewed key distribution.
3. Generate synthetic order data and identify the hot key.
4. Implement baseline aggregation and diagnose the data-skew bottleneck.
5. Implement salting as a skew mitigation technique.
6. Compare baseline and optimized execution times.
7. Validate that both approaches produce matching results.
8. Debug Python, PySpark, and pytest errors step by step.
9. Implement and verify partition replacement tests.
10. Prepare the README, technical report, and GitHub repository.
11. Fix test imports so tests work from a clean environment.
12. Review the submission requirements and prepare the final project documentation.
## How ChatGPT Was Used
ChatGPT assisted with understanding requirements, implementation guidance, debugging, test corrections, and documentation.
## My Review and Validation
I ran the Spark workload locally, checked the skew distribution, compared execution timings, verified matching aggregation results, ran pytest successfully, and pushed the project to my public GitHub repository.
The recorded test result was 2 passed. Performance measurements are local observations and are not a guarantee of improvement on every Spark cluster.
