# Agent Configurations (`agent-config/*.yaml`)

Agent configurations are YAML files that define the absolute perimeter of an AI assistant. They combine the LLM model parameters with the physical System Prompts from our library.

## What is an Agent Config?
An Agent Config defines:
- The Provider (OpenAI, Anthropic, etc.)
- The Model (GPT-4o, Claude 3.5 Sonnet)
- The Temperature (Creativity vs Determinism)
- The **System Prompt Template** (which `.md` files to inject)
- The Tools available (e.g., `execute_code`, `search_web`)
- The Memory constraints (Max tokens)

## Detailed Use Cases

### `coding-agent.yaml`
- **What it is:** A deterministic Claude 3.5 Sonnet agent configured specifically to write, review, and execute Python code without conversational filler.
- **Use Case:** Headless auto-completion, generating unit tests in CI/CD pipelines, or autonomous bug fixing.

### `research-agent.yaml`
- **What it is:** A GPT-4o agent with slightly higher temperature (0.3) allowing it to synthesize broader topics, equipped with web-search capabilities.
- **Use Case:** Deep-diving into new frameworks, summarizing vast swaths of documentation, or comparing abstract architectural choices.

### `trading-agent.yaml`
- **What it is:** A near-zero temperature agent (using reasoning models) primed with strict domain knowledge regarding financial risk.
- **Use Case:** Analyzing algorithmic trade algorithms, calculating Sharpe ratios, or building backtesting infrastructure.

### `reviewer-agent.yaml`
- **What it is:** A risk and safety analyzer that refuses to generate code but EXCELS at finding security flaws.
- **Use Case:** Automated PR reviews before a human ever looks at the code.
