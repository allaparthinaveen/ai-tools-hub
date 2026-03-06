# Bugfix Template

## Variables
- {{ERROR_LOG}}: The exact stack trace or error message.
- {{CODE}}: The problematic code section.
- {{CONTEXT}}: Steps to reproduce.

## Template
Analyze and fix the bug represented by the provided state.

Steps to Reproduce / Context:
{{CONTEXT}}

Error Trace:
{{ERROR_LOG}}

Suspect Code:
```
{{CODE}}
```

TASK:
1. Diagnose the issue following `prompts/workflows/bug-fixing/02-diagnose.md`.
2. Provide the corrected code.
3. Briefly explain the root cause.

## Usage
1. Replace variables with actual values
