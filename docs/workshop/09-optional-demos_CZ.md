[Workshop index](README_CZ.md) | [Repository README](../../README.md)

---

# 9. Volitelné demo ukázky

Ne každé publikum chce stejnou hloubku. Kapitoly výše jsou hlavní příběh. Následující body jsou vhodné volitelné větve pro hlubší průchod nebo jiné publikum.

## 9.1 Základy a rychlé výhry

### Inline suggestions

Otevřete `src\services\toy\main.py` a napište `# Configure Prometheus` — počkejte na návrhy. TAB přijme, ESC odmítne, CTRL+šipka přijme částečně.

Pak kolem řádku 25 změňte `logger` na `logging` a sledujte predikci další editace.

### Chat a porozumění codebase

```text
Where in my code am I processing messages from Service Bus queues and what is the code doing?
```

Experimentujte s volbou modelu pro porovnání kvality a rychlosti.

### Generování dokumentace

Přidejte všechny Terraform soubory z `examples\terraform` do kontextu:

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

Přiložte [query_data.csv](../../examples/kql/query_data.csv) a zeptejte se:

```text
Give me microsoft Kusto Query (KQL) to display percentage of processor time grouped by instance and process id which is part of properties. Name of table is AppPerformanceCounters. Attached are example data.
```

### SQL

Přiložte [users_denormalized.json](../../examples/sql/users_denormalized.json) a zeptejte se:

```text
Generate CREATE commands for normalized users, addresses and orders using Microsoft SQL.
```

Pak:

```text
Based on data structure, create 10 lines of sample data and make sure it makes sense and foreign keys are respected.
```

```text
Give me SQL statement to list userId, name, number of orders and number of addresses for each user.
```

### Vision

Přiložte [classes.png](../../examples/vision/classes.png), vytvořte `classes.py` a zeptejte se:

```text
Generate code for classes in Python according to attached schema.
```

Poté v Edit mode:

```text
Create markdown documentation for classes.py and include mermaid diagram.
```

## 9.3 Web a browser demo

### Browser elements

Otevřete Simple Browser (CTRL+ALT+P), zadejte URL, klikněte na **Add element to chat** a zeptejte se `What is this element doing?`

### Web search a fetch

```text
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version? Do NOT use any tools.
```

Pak s nástroji:

```text
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version?
```

A s explicitním fetch:

```text
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version?
#fetch
https://github.com/microsoft/agent-framework/releases
https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
```

## 9.4 Další MCP integrace

- Kubernetes MCP
- Azure MCP
- Database MCP
- Playwright MCP

## 9.5 Model selection a BYOM/BYOK

### Základy model selection

Copilot CLI podporuje přepínání modelu během session přes `/model`.

- **Larger models** (Claude Opus, GPT-5.3-Codex): lepší pro složité multi-file úlohy
- **Faster models** (Claude Haiku, GPT-5 mini, GPT-4.1): lepší pro rychlé úkoly
- **Reasoning models**: viditelnost reasoning přes `Ctrl+T`, konfigurace reasoning effort

### Bring your own model provider

Copilot CLI umí připojit vlastní provider nebo lokální modely přes env proměnné.

- **Remote providers**: Azure OpenAI, Anthropic, OpenAI, OpenAI-compatible endpoint
- **Local models**: Ollama, vLLM, Foundry Local
- **Offline mode**: `COPILOT_OFFLINE=true`
- **GitHub auth je volitelná** při vlastním provideru (pro `/delegate` a GitHub nástroje je stále užitečná)

### Vyzkoušejte

```text
COPILOT_PROVIDER_BASE_URL=http://localhost:11434 copilot
```

Nebo:

```text
copilot help providers
```

### Enterprise BYOK

Enterprise BYOK umožňuje adminům připojit klíče providerů (Anthropic, Microsoft Foundry, OpenAI, xAI). Použití přes BYOK se účtuje přímo u providera a nepočítá se do Copilot request quotas.

## 9.6 LSP v CLI

LSP dává Copilot CLI IDE-like inteligenci: go-to-definition, hover info, diagnostiku.

### Konfigurace

- **Global**: `~/.copilot/lsp-config.json`
- **Repository**: `.github/lsp.json`

### Správa LSP

```text
/lsp show
/lsp test
/lsp reload
/lsp help
```

### Co vysvětlit

- bez LSP CLI spoléhá více na grep/pattern matching
- s LSP rozumí typům, referencím a definicím přesněji

## 9.7 Self-hosted runners deep-dive

- cloud coding agenti a Copilot code review mohou běžet na self-hosted runnerech přes ARC
- podporované jsou pouze **Ubuntu x64 Linux** runnery
- admin může nastavit default runner type a locknout politiku
- firewall musí pustit `api.githubcopilot.com`, `uploads.github.com`, `user-images.githubusercontent.com`
- konfigurace přes `copilot-setup-steps.yml` nebo org nastavení

Use cases:

- interní síťový přístup
- výkon
- compliance
- cost control

## 9.8 Závěrečná témata do budoucna

- GitHub Spark

---

Previous: [Operations](08-operations_CZ.md)
