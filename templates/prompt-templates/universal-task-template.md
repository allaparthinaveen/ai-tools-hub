# Universal Task Template

## Variables
- {{ROLE}}: The persona the AI should adopt.
- {{CONTEXT}}: Background information relevant to the task.
- {{OBJECTIVE}}: What exactly needs to be achieved.
- {{CONSTRAINTS}}: Rules the AI cannot break.
- {{OUTPUT_FORMAT}}: The specific format (e.g., Markdown table, JSON) required.

## Template
You are {{ROLE}}.
{{CONTEXT}}

TASK: {{OBJECTIVE}}

Constraints:
{{CONSTRAINTS}}

Please format your response strictly as:
{{OUTPUT_FORMAT}}

## Usage
1. Replace variables with actual values
2. Paste into AI system message or user turn
Note: Works exceptionally well when combined with `prompts/patterns/step-by-step.md`.
