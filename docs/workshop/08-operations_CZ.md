[Workshop index](README_CZ.md) | [Repository README](../../README.md)

---

# 8. Operujte pomocí SRE agentů

Workshop by měl skončit ukázkou, že lifecycle pokračuje i po merge a deploymentu.

## 8.1 Pokud to prostředí podporuje, zkuste operational prompty

```text
What versions my AKS clusters run?
```

```text
See my storage accounts, can I improve resiliency and data protection?
```

```text
What namespaces I have in my Kubernetes cluster?
```

## 8.2 Co vysvětlit

- operations a SRE agenti pomáhají po deploymentu
- propojují změny v kódu, infrastrukturu, telemetry i incidenty
- je to silná závěrečná kapitola, protože dokončuje lifecycle příběh

Pokud je dostupné prostředí Azure SRE Agent, je to ideální finální demo. Pokud ne, dobře poslouží Azure/Kubernetes MCP prompty.

## 8.3 Pozorujte Copilot s OpenTelemetry

Copilot Chat ve VS Code i Copilot CLI umí exportovat **OpenTelemetry** traces, metrics a events, takže máte viditelnost do agent interactions, LLM volání, tool executions a token usage. Signály odpovídají [OTel GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/).

### Co se sbírá

| Signál | Příklady |
| --- | --- |
| **Traces** | Celý span strom: orchestrace → LLM volání → nástroje; subagenti jako child spany |
| **Metrics** | Délka LLM volání, token usage, počty/latence nástrojů, end-to-end agent duration, time to first token |
| **Events** | Start sessions, invokace nástrojů, LLM round-tripy po tazích |

### Jak zapnout

Ve VS Code nastavte `github.copilot.chat.otel.enabled=true` a OTLP endpoint. V CLI nastavte `COPILOT_OTEL_ENABLED=true` nebo `OTEL_EXPORTER_OTLP_ENDPOINT`.

Content capture je defaultně vypnutý — zapínejte jej jen v trusted prostředí.

### Vyzkoušejte

Nejrychleji lokálně přes Aspire Dashboard:

```text
docker run --rm -d -p 18888:18888 -p 4317:18889 --name aspire-dashboard mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

Poté VS Code konfigurace:

```json
{
  "github.copilot.chat.otel.enabled": true,
  "github.copilot.chat.otel.exporterType": "otlp-grpc",
  "github.copilot.chat.otel.otlpEndpoint": "http://localhost:4317"
}
```

Otevřete `http://localhost:18888` → Traces.

Podporované jsou i další backendy: Jaeger, Azure Application Insights, Langfuse, Grafana Tempo, Honeycomb, Datadog a další OTLP kompatibilní řešení.

### Proč je to důležité pro enterprise

- **compliance**: audit trail akcí agenta, volaných nástrojů a použitého kontextu
- **cost management**: metriky tokenů pomáhají optimalizovat AI spend
- **debugging**: trace stromy ukazují, kde se interakce pokazila
- **performance**: latence odhaluje pomalá volání nástrojů/modelů

---


---

Previous: [Workflow agents](07-workflow-agents_CZ.md) | Next: [Optional demos](09-optional-demos_CZ.md)
