[Workshop index](README.md) | [Repository README](..\..\README.md)

---

# 8. Operate with SRE agents

The workshop should end by showing that the lifecycle continues after merge and deployment.

## 8.1 If your environment supports it, try operational prompts

```text
What versions my AKS clusters run?
```

```text
See my storage accounts, can I improve resiliency and data protection?
```

```text
What namespaces I have in my Kubernetes cluster?
```

## 8.2 What to explain

- operations and SRE agents help after deployment
- they connect code changes, infrastructure, telemetry, and incidents
- they are a strong closing chapter because they complete the lifecycle story

If a dedicated Azure SRE Agent environment is available, this is the ideal final demo. If not, Azure or Kubernetes MCP prompts are still a strong close.

## 8.3 Observe Copilot with OpenTelemetry

Copilot Chat in VS Code and Copilot CLI can export **OpenTelemetry** traces, metrics, and events, giving you visibility into agent interactions, LLM calls, tool executions, and token usage. All signals follow the [OTel GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/).

### What gets collected

| Signal | Examples |
| --- | --- |
| **Traces** | Full span tree: agent orchestration → LLM calls → tool executions. Subagent invocations appear as child spans. |
| **Metrics** | LLM call duration, token usage (input/output), tool invocation count and latency, agent end-to-end duration, time to first token |
| **Events** | Session starts, per-tool invocations, per-turn LLM round-trips |

### How to enable

In VS Code, set `github.copilot.chat.otel.enabled` to `true` and configure the OTLP endpoint. In the CLI, set `COPILOT_OTEL_ENABLED=true` or `OTEL_EXPORTER_OTLP_ENDPOINT`.

Content capture (full prompts and responses) is **off by default** — enable with `captureContent` only in trusted environments.

### Try this

If you have a local observability stack, the fastest option is the **Aspire Dashboard**:

```text
docker run --rm -d -p 18888:18888 -p 4317:18889 --name aspire-dashboard mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

Then configure VS Code:

```json
{
  "github.copilot.chat.otel.enabled": true,
  "github.copilot.chat.otel.exporterType": "otlp-grpc",
  "github.copilot.chat.otel.otlpEndpoint": "http://localhost:4317"
}
```

Open `http://localhost:18888` → Traces to see agent interaction spans.

Other supported backends: Jaeger, Azure Application Insights, Langfuse, Grafana Tempo, Honeycomb, Datadog — any OTLP-compatible backend works.

### Why this matters for enterprise

- **compliance**: audit trail of what the agent did, which tools it called, and what context it used
- **cost management**: token usage metrics help teams understand and optimize AI spend
- **debugging**: trace trees show exactly where an agent interaction went wrong
- **performance**: latency metrics identify slow tool calls or model responses

---


---

Previous: [Workflow agents](07-workflow-agents.md) | Next: [Optional demos](09-optional-demos.md)
