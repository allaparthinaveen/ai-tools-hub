# Q&A Template

## Variables
- {{USER_QUERY}}: The explicit question asked by the user.
- {{SOURCES}}: Verified information or documentation to base the answer on.

## Template
Context material:
<<<
{{SOURCES}}
>>>

TASK: Answer the following user query based ONLY on the context material above.

Query: {{USER_QUERY}}

Constraints:
- Do not hallucinate. 
- If the answer is not contained entirely within the context, state "INSUFFICIENT INPUT".
- Apply principles from `prompts/patterns/retrieval-augmented.md`.

## Usage
1. Replace variables with actual values
2. Ideal for RAG (Retrieval-Augmented Generation) pipelines.
