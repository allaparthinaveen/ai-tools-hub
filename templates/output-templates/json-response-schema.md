# JSON Response Schema

## Schema
```json
{
  "status": "string (success|error)",
  "data": {
    "type": "object",
    "description": "The requested output or generated content"
  },
  "metadata": {
    "type": "object",
    "description": "Any logs or token usage stats"
  }
}
```

## Usage in Prompts
Add this to any prompt: "Respond using ONLY the schema from `templates/output-templates/json-response-schema.md`"
