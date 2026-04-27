[Workshop index](README.md) | [Repository README](../../README.md)

---

# 3. Skills and MCP: local capabilities and connected tools

This chapter explains how Copilot gains capabilities in two different ways.

## 3.1 Concepts to explain first

Skills and MCP are both useful, but they solve different problems.

| Capability type | Best use |
| --- | --- |
| **Skills** | Easy-to-author, easy-to-share local capabilities, often stored in the repo and loaded on demand |
| **MCP** | Centrally managed, secure, enterprise-grade tools that connect to live systems or remote knowledge |

Good short explanation:

- skills excel when you want something lightweight, local, and easy to package with the repository
- MCP excels when you want live tools, external systems, or centrally managed enterprise integrations

## 3.2 See skills in action

Open:

- `.github\skills\simplecontext\SKILL.md`
- `.github\skills\json-to-xml-converter\SKILL.md`
- `examples\json\myjson.json`

### Try this: lightweight context skill

Ask:

```text
What is inventory number for BigDog?
```

### What to observe

- The model should recognize that the request matches the `simplecontext` skill.
- The detailed skill content is loaded only when needed.
- If your environment exposes tool traces or debug view, you can show the skill file being accessed.

### Try this: script-backed skill

Add `examples\json\myjson.json` to context and ask:

```text
Convert this to XML.
```

### What to observe

- This skill is a good example of a task that benefits from a deterministic script.
- Skills are not only extra text; they can also provide packaged workflows around scripts and resources.

## 3.3 Start with the MCP server that lives in this repo

Open:

- `.vscode\mcp.json`
- `mcp\README.md`
- `mcp\random_string_mcp\README.md`
- `mcp\random_string_mcp\src\main.py`

Start with the local server because it is transparent and easy to explain.

What to point out:

- `.vscode\mcp.json` registers `my-mcp-string-generator`
- it connects to `http://localhost:8000/sse`
- `mcp\random_string_mcp\src\main.py` is a tiny FastMCP server
- the server exposes two tools: `random_string` and `unique_string`
- this is a great teaching example because the audience can see both the tool registration and the implementation

### How this MCP server is built

`random_string_mcp` uses `FastMCP` and exposes Python functions as MCP tools with the `@mcp.tool()` decorator.

- `random_string(...)` generates a random suffix from the selected character classes
- `unique_string(...)` derives a predictable suffix from a seed using SHA-256, which is useful when you want stable names
- `mcp.run(transport="sse")` starts the server over Server-Sent Events, which is why the workspace configuration uses an HTTP URL

### How to start it

Open a terminal and run:

```pwsh
cd .\mcp\random_string_mcp\src
uv run main.py
```

The workspace MCP configuration points Copilot to `http://localhost:8000/sse`, so once the server is running the tool becomes available in chat.

### Try this

Use the earlier demo prompt:

```text
Generate names for 10 containers in format app1-xxxxxx where xxxxxx is random suffix consisting of lowercase letters and numbers.
```

Then show a second prompt that highlights deterministic behavior:

```text
Generate stable suffixes for dev, test, and prod using the unique string tool so that the same environment names always produce the same suffixes.
```

### What to observe

- this is a real MCP server that lives in the repository, not only a hosted enterprise integration
- the implementation is simple enough that students can understand how custom MCP tools are authored
- the random generator is useful for one-off names, while the unique generator is useful for repeatable naming patterns

## 3.4 Connect to broader MCP servers

After the local example, notice the configured servers such as:

- GitHub MCP
- Microsoft Docs MCP
- Kubernetes MCP
- Azure MCP Server

### Try this: official docs through MCP

Ask:

```text
Using the Microsoft Docs MCP server, find official guidance on custom agents in VS Code and summarize how handoffs work.
```

### Try this: repository knowledge through GitHub MCP

Ask:

```text
Using GitHub tools, list the workflows in this repository and summarize which ones are build, deploy, or security related.
```

### Optional follow-up prompts

If your environment supports these integrations, try:

```text
What plans we have for implementing PDF in our app? Check GitHub Issues.
```

```text
What versions my AKS clusters run?
```

```text
See my storage accounts, can I improve resiliency and data protection?
```

## 3.5 Why this chapter matters

The audience should now understand the difference between:

- local packaged capabilities
- repository-local MCP tools you can build yourself
- centrally connected tools

That distinction becomes important in the later chapters.

---


---

Previous: [Repository context](01-repository-context.md) | Next: [VS Code agents](03-vscode-agents.md)
