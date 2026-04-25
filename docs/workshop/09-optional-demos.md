[Workshop index](README.md) | [Repository README](..\..\README.md)

---

# 9. Optional demos

Not every audience wants the same depth. The chapters above are the main story. The items below are excellent optional branches when you want to go deeper or adapt to a different audience.

## 9.1 Foundations and quick wins

### Inline suggestions

Open `src\services\toy\main.py` and type `# Configure Prometheus` — wait for suggestions. Use TAB to accept, ESC to reject, or CTRL+arrow to accept partially.

Then around line 25 change `logger` to `logging` and wait for Copilot to predict the next edit.

### Chat and codebase understanding

Ask Copilot to search and understand your code:

```text
Where in my code am I processing messages from Service Bus queues and what is the code doing?
```

Experiment with different model selections to compare quality and speed.

### Documentation generation

This is still an excellent demo for many developers because it solves a common day-to-day task quickly.

Add all Terraform files from `examples\terraform` to context and try this sequence:

```text
Create basic Markdown documentation for this Terraform project, explain how to deploy it, and summarize the purpose of each file.
```

```text
Create list of cloud resources used in this project.
```

```text
Create chapter listing environment variables used with each container app and put it into nice table.
```

## 9.2 Structured prompting

### KQL

Attach [query_data.csv](..\..\examples\kql\query_data.csv) and ask:

```text
Give me microsoft Kusto Query (KQL) to display percentage of processor time grouped by instance and process id which is part of properties. Name of table is AppPerformanceCounters. Attached are example data.
```

### SQL

Attach [users_denormalized.json](..\..\examples\sql\users_denormalized.json) and ask:

```text
Generate CREATE commands for normalized users, addresses and orders using Microsoft SQL.
```

Then follow up:

```text
Based on data structure, create 10 lines of sample data and make sure it makes sense and foreign keys are respected.
```

```text
Give me SQL statement to list userId, name, number of orders and number of addresses for each user.
```

### Vision

Attach [classes.png](..\..\examples\vision\classes.png), create `classes.py` and ask:

```text
Generate code for classes in Python according to attached schema.
```

Then in Edit mode follow with:

```text
Create markdown documentation for classes.py and include mermaid diagram.
```

## 9.3 Web and browser demos

### Browser elements

Open Simple Browser (command palette CTRL+ALT+P and search for it), enter some URL. Click on **Add element to chat** and ask `What is this element doing?`

### Web search and fetch

Useful for demonstrating the difference between model-only answers, server-side web grounding, MCP-backed research, and targeted fetch of known documentation.

Try without tools first:

```text
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version? Do NOT use any tools.
```

Then with tools enabled:

```text
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version?
```

And with explicit fetch of known documentation:

```text
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version?
#fetch
https://github.com/microsoft/agent-framework/releases
https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
```

## 9.4 Additional MCP integrations

The main flow already covers the in-repo `random_string_mcp` server and GitHub MCP. If the audience wants more, try:

- Kubernetes MCP
- Azure MCP
- Database MCP
- Playwright MCP

## 9.5 Model selection and BYOM/BYOK

### Model selection basics

Copilot CLI supports model switching during a session with `/model`. Show the model picker and explain the trade-offs:

- **Larger models** (Claude Opus, GPT-5.3-Codex): better for complex, multi-file tasks
- **Faster models** (Claude Haiku, GPT-5 mini, GPT-4.1): better for quick tasks, included at no premium request cost
- **Reasoning models**: toggle reasoning visibility with `Ctrl+T`, configure reasoning effort

### Bring your own model provider

Copilot CLI supports connecting your own model provider or running fully local models. Configure via environment variables before launching the CLI:

- **Remote providers**: Azure OpenAI, Anthropic, OpenAI, or any OpenAI-compatible endpoint
- **Local models**: Ollama, vLLM, Foundry Local
- **Offline mode**: set `COPILOT_OFFLINE=true` to prevent all communication with GitHub servers — fully air-gapped development
- **GitHub auth becomes optional**: when using your own provider, you can start the CLI without GitHub authentication. Sign in to GitHub to also get `/delegate`, GitHub Code Search, and the GitHub MCP server.

Sub-agents (explore, task, code-review) automatically inherit your provider configuration.

### Try this

If you have Ollama running locally:

```text
COPILOT_PROVIDER_BASE_URL=http://localhost:11434 copilot
```

Or show the help for provider setup:

```text
copilot help providers
```

### Enterprise BYOK

For organization-managed Copilot, enterprise BYOK allows admins to connect API keys from supported providers (Anthropic, Microsoft Foundry, OpenAI, xAI). Once connected, all models tied to that key are available in Copilot Chat across GitHub.com and supported IDEs. Usage through BYOK is billed directly by the provider and does not count against Copilot request quotas.

## 9.6 LSP in the CLI

LSP (Language Server Protocol) gives Copilot CLI IDE-like intelligence: go-to-definition, hover information, and diagnostics. This helps the agent navigate your codebase with the same precision as a full IDE.

### Configuration

Configure LSP servers via:

- **Global**: `~/.copilot/lsp-config.json`
- **Repository**: `.github/lsp.json`

Plugins can also contribute LSP servers automatically.

### Managing LSP

```text
/lsp show     # see configured servers
/lsp test     # verify a server works
/lsp reload   # reload configuration
/lsp help     # full documentation
```

### What to explain

- without LSP, the CLI relies on grep and pattern matching for code navigation
- with LSP, it understands types, references, and definitions — making refactoring and cross-module work significantly more accurate
- this is particularly valuable for statically typed languages with complex type hierarchies

## 9.7 Self-hosted runners deep-dive

For enterprise audiences who want more detail on running cloud agents on their own infrastructure:

- cloud coding agents and Copilot code review can run on **self-hosted runners** using ARC (Actions Runner Controller)
- only **Ubuntu x64 Linux** runners are supported
- organization admins can **set a default runner type** and **lock the setting** to prevent individual repos from overriding it
- firewall rules must allow connections to `api.githubcopilot.com`, `uploads.github.com`, and `user-images.githubusercontent.com`
- configuration is done via `copilot-setup-steps.yml` in the repository or organization-level settings

Use cases:

- **internal network access**: agent can reach internal package registries, databases, or APIs
- **performance**: use larger runners for faster builds and tests
- **compliance**: keep agent execution within your own infrastructure
- **cost control**: use reserved compute instead of pay-per-minute GitHub-hosted runners

## 9.8 Future-looking closing topics

- GitHub Spark

---

Previous: [Operations](08-operations.md)
