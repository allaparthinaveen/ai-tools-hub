# Code Review Template

## Variables
- {{CODE}}: The PR diff or code snippet to review.
- {{CONTEXT}}: Overall architecture or specific PR goals.

## Template
You are reviewing the following code snippet. 

Context: {{CONTEXT}}
Code to review:
```
{{CODE}}
```

TASK: Perform a thorough code review.

Constraints:
1. Check for immediate security vulnerabilities and off-by-one errors.
2. Check for readability and performance trade-offs.
3. Adhere to `prompts/tasks/debug/architecture-review.md`.

## Usage
1. Replace variables with actual PR diffs.
