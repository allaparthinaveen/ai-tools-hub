# Prompts Architecture Guide

## The Philosophy of Modular Prompting
Instead of writing one massive "do everything" prompt (which often leads to hallucination and dropped instructions), this repository breaks prompts into composable blocks.

### The 8 Modularity Pillars
1. **System:** The baseline physical laws of the AI (e.g., "Never output Markdown if JSON is requested").
2. **Roles:** The behavioral persona (e.g., "Senior Security Engineer").
3. **Tasks:** The actual job to be done (e.g., "Review Code").
4. **Patterns:** The cognitive approach (e.g., "Chain of Thought").
5. **Workflows:** Sequential task chaining.
6. **Domains:** Industry-specific knowledge (e.g., "Quantitative Trading").
7. **Formats:** Output constraints (e.g., "JSON Schema").
8. **Meta:** Evaluators and meta-analyzers.

## Use Cases
### 1. Generating a Pull Request Reviewer
Combine:
`system/coding-assistant.md` + `roles/senior-software-engineer.md` + `tasks/debug/architecture-review.md` + `output-templates/markdown-report.md`

### 2. Creating a Strict JSON Data Extractor
Combine:
`system/general.md` + `tasks/research/summarize-sources.md` + `formats/response-styles/json-output.md`
