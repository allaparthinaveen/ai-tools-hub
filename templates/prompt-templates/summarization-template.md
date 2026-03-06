# Summarization Template

## Variables
- {{CONTEXT}}: The raw, long-form text or transcript to be summarized.
- {{SUMMARY_LENGTH}}: desired length (e.g., '1 paragraph', '3 bullet points').
- {{AUDIENCE}}: who the summary is for (e.g., 'executives', 'engineers').

## Template
Please summarize the following context for {{AUDIENCE}}.

TEXT TO SUMMARIZE:
{{CONTEXT}}

Constraints:
1. The length must be exactly: {{SUMMARY_LENGTH}}
2. Capture the core themes without losing critical nuances.
3. Use principles from `prompts/tasks/research/summarize-sources.md`.

## Usage
1. Replace variables with actual values
