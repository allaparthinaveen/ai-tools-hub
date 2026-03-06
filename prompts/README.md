# Prompts Library

Welcome to the **Prompts Library** for the AI Tools Hub. 

This repository of prompts is designed to be highly modular, reusable, and structured for various AI tools, agents, and applications. The files within this directory provide battle-tested templates that guide Large Language Models (LLMs) to perform specific roles, execute complex workflows, or format data correctly.

---

## 🎯 Purpose and Philosophy

The primary goals of this library are:
1. **Reusability:** Write once, use everywhere. The prompts are generalized enough to be embedded in python scripts, MCP servers, or pasted directly into a chat interface.
2. **Modularity:** Separate the **System Instructions** (the *how*) from the **Task Constraints** (the *what*) and the **Domain Knowledge** (the *context*).
3. **Quality Control:** Establish a high bar for prompt engineering. Every prompt should define clear roles, instructions, expected formats, and usage examples.

---

## 📂 Directory Architecture

The prompts are organized categorically. You can combine a *Role*, a *Pattern*, and a *Task* to create a highly sophisticated system message. 

```text
prompts/
├─ README.md                # This documentation
├─ system/                  # Core behavioral instructions and guardrails
├─ roles/                   # Persona definitions (e.g., "You are a Senior Security Engineer")
├─ tasks/                   # Action-oriented directives (e.g., debugging, refactoring, code-generation)
├─ patterns/                # Reasoning structures (e.g., Chain-of-Thought, Tree-of-Thought)
├─ workflows/               # Step-by-step instructions for multi-stage processes
├─ domains/                 # Context and terminology for specific fields (e.g., Crypto, DevOps)
├─ formats/                 # Output templates ensuring structured responses (e.g., JSON, YAML, ADRs)
├─ meta/                    # Prompts that evaluate, check, or generate other prompts
└─ playground/              # Experimental scratchpad for work-in-progress prompts
```

### 1. `system/` (Global Behavior)
System prompts define the overarching constraints and behavior of the agent. Use these to establish the AI's baseline personality, safety guardrails, and formatting rules. 
- *Example:* `system/coding-assistant.md` defines a strict, no-hallucination assistant dedicated to clean code.

### 2. `roles/` (Personas)
Role prompts instruct the AI to adopt a specific perspective, vocabulary, and expertise.
- *Example:* `roles/senior-software-engineer.md` will focus on scalability and maintainability, whereas `roles/product-manager.md` will heavily index on user value and requirements.

### 3. `tasks/` (Directives)
Task prompts are action-oriented. They tell the model what specific job needs to be done.
- *Example:* `tasks/refactor/clean-code.md` or `tasks/debug/architecture-review.md`.

### 4. `patterns/` (Cognitive Structures)
Pattern prompts explicitly instruct the model *how* to think through a problem before answering. 
- *Example:* `patterns/chain-of-thought.md` forces the model to emit a `<thought_process>` block before producing its final answer, improving logical accuracy.

### 5. `workflows/` (Multi-Step Execution)
Workflow prompts break down massive complex tasks into smaller, sequential steps that can be run consecutively by the same agent or pipelined between multiple agents.
- *Example:* `workflows/feature-development/` outlines a 4-step pipeline from requirements gathering to code review.

### 6. `domains/` (Industry Context)
Domain prompts provide specialized terminology and industry standards. They ensure the AI speaks the right jargon and understands the environment.
- *Example:* `domains/trading/risk-analysis.md` provides definitions for maximum drawdown and Sharpe ratio constraints.

### 7. `formats/` (Output Data Structures)
Format prompts strictly enforce how the AI's output is shaped. They are crucial for programmatic environments where the output must be parsed (e.g., by a rigid schema).
- *Example:* `formats/response-styles/json-output.md` ensures the AI returns *only* valid JSON without conversational wrapper text.

### 8. `meta/` (Evaluations)
Meta prompts act as validators. They take in *other* prompts or *AI outputs* to score, analyze, or ensure safety compliance.
- *Example:* `meta/hallucination-checker.md` verifies claims against source contexts.

---

## 🛠️ How to Use These Prompts

Each `.md` file in this directory follows a strict layout designed for easy copy-pasting or dynamic inclusion in code:

### The Anatomy of a Prompt File
Every prompt file includes:
1. **Purpose:** A short description of what the prompt achieves.
2. **Instructions (for the user):** How you should deploy this prompt (e.g., "Use this as the primary system message").
3. **System Prompt (for the AI):** The actual, raw prompt text intended for the LLM. 
4. **Usage Examples:** Concrete examples demonstrating how to use the prompt with variables.

### Variables and Placeholders
Many prompts use explicit injection markers like `<<<CONTEXT>>>`, `<<<CODE_SNIPPET>>>`, or `<<<TARGET_JSON_SCHEMA>>>`. 
Before submitting the prompt to the AI, **you must replace these placeholders** with your actual runtime data.

#### Example Combination
If you are building an automated code reviewer, you might construct your final prompt by concatenating:
1. `system/style-guide.md`
2. `roles/senior-software-engineer.md`
3. `tasks/debug/code-debugging.md`
4. `formats/response-styles/json-output.md`

## 🤝 Contributing

We welcome additions to the Prompts Library! 

When submitting a Pull Request, please ensure your prompt:
*   Follows the identical structure of existing prompts (Purpose, Instructions, System Prompt, Examples).
*   Avoids embedding specific personal context; keep it generalized.
*   Clearly marks replacement variables with `<<<VARIABLE_NAME>>>`.
*   Includes a small, reproducible example.
