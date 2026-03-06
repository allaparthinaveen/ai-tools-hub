# API Specification

## Schema
```yaml
openapi: 3.0.0
info:
  title: [API Title]
  version: 1.0.0
paths:
  /[endpoint-path]:
    get:
      summary: [Summary]
      responses:
        '200':
          description: Successful response
```

## Usage in Prompts
Add this to any prompt: "Respond using ONLY the OpenAPI YAML schema from `templates/output-templates/api-spec.md`"
