# Output Templates (`output-templates/*.md`)

Output Templates are the "contract" between the LLM and the downstream application. They enforce rigid structural JSON or Markdown.

## Why use Output Templates?
If you are building an API that wraps an LLM, you cannot afford the LLM to reply with "Sure! Here is your JSON:". Output templates contain instructions that forbid conversational text and force exact schema adherence.

## The Schemas

### `json-response-schema.md`
- **Forces:** `{"status": "...", "data": {}, "metadata": {}}`
- **Use Case:** When the LLM's response needs to be immediately `JSON.parse()` mapped to an object by your frontend or backend logic.

### `markdown-report.md`
- **Forces:** Exact header hierarchy (Title -> Exec Summary -> Findings -> Next Steps).
- **Use Case:** Synthesizing research into a format immediately publishable to a Notion page or internal wiki.

### `api-spec.md`
- **Forces:** Valid OpenAPI 3.0 YAML.
- **Use Case:** Auto-generating Swagger documentation from backend code.
