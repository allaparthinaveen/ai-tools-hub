# Prompt Templates (`prompt-templates/*.md`)

Prompt Templates are parameterized Markdown files that act as the interface between the User/Application and the LLM. 

## Parameterization Syntax
Every template uses `{{VARIABLE_NAME}}`. Before sending the payload to the LLM API, your application logic must `replace("{{VARIABLE}}", target)`.

## Detailed Templates

### `universal-task-template.md`
- **What it is:** The bedrock template. It forces every request into a Role, Context, Objective, Constraints, and Output Format model.
- **Why use it:** It guarantees the LLM receives perfectly structured data rather than stream-of-consciousness user input.

### `qa-template.md`
- **What it is:** A strict Retrieval-Augmented Generation (RAG) wrapper.
- **Why use it:** It explicitly forbids the LLM from using its pre-trained knowledge, forcing it to look *only* at the explicitly provided `{{SOURCES}}`.

### `code-generation-template.md` & `code-review-template.md`
- **What they are:** specialized wrappers for dealing with source code.
- **Why use them:** They explicitly instruct the AI on whether it needs to *produce* valid runnable code or *evaluate* existing code for vulnerabilities.

### `bugfix-template.md`
- **What it is:** A template that accepts a stack trace (`{{ERROR_LOG}}`), the broken `{{CODE}}`, and the steps to reproduce it.
