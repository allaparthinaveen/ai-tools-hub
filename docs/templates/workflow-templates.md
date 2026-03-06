# Workflow Templates (`workflow-templates/*.yaml`)

Workflows are multi-step orchestration pipelines. They define how the output of Step A becomes the input of Step B.

## What is a Workflow Template?
A workflow defines an entire lifecycle of a complex task that is too large for a single LLM call. It breaks the job down into discrete prompts executed consecutively.

## Detailed Pipelines

### `feature-development.yaml`
1. Takes a raw idea (`User Input`)
2. Converts it to formal requirements (Step 1)
3. Converts requirements to technical architecture (Step 2)
4. Converts architecture into implementation code (Step 3)
- **Use Case:** End-to-end building of a new microservice.

### `bug-fixing.yaml`
1. Takes an error log
2. Forces the AI to perform a Root Cause Analysis (Step 1)
3. Passes the RCA alongside the broken code to implement a fix (Step 2)
- **Use Case:** Automated CI/CD failure resolution.

### `research-pipeline.yaml`
1. Scopes the user's vague query
2. Collects sources based on the precise scope
3. Synthesizes a massive report.
- **Use Case:** Preparing a comparative analysis on PostgreSQL vs MongoDB for a specific workload.
