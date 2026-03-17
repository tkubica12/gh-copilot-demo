# random_string_mcp

## How to start random_string_mcp

This MCP server is implemented in `src\main.py` with `FastMCP`.

It exposes two tools:

- `random_string(length, lower, upper, numeric, special)`
- `unique_string(seed_text, length, lower, upper, numeric, special)`

1. Open a terminal and navigate to the `random_string_mcp\src` directory:
   ```pwsh
   cd .\mcp\random_string_mcp\src
   ```
2. Start the MCP server using `uv`:
   ```pwsh
   uv run main.py
   ```

The server listens on `http://127.0.0.1:8000/sse`.

In this workspace, `.vscode\mcp.json` registers it as `my-mcp-string-generator`.

Good demo prompts:

```text
Generate names for 10 containers in format app1-xxxxxx where xxxxxx is random suffix consisting of lowercase letters and numbers.
```

```text
Generate stable suffixes for dev, test, and prod using the unique string tool so the same environment names always get the same suffixes.
```
