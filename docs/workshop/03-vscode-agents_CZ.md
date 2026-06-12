[Workshop index](README_CZ.md) | [Repository README](../../README.md)

---

# 3. Plánujte a specializujte práci ve VS Code

V této kapitole se hlavní workflow stává více agentic.

## 3.1 Koncepty, které vysvětlit jako první

Tato kapitola zavádí čtyři související myšlenky:

| Koncept | Nejlepší použití |
| --- | --- |
| **Prompt file** | Konzistentní start workflow |
| **Custom agent** | Udržení aktivní specializované role |
| **Handoff** | Přesun konverzace mezi specialisty při zachování kontextu |
| **Subagent** | Delegace užší, cílené práce bez zahlcení hlavní konverzace |

Klíčový cíl učení:

> prompt file umí zahájit workflow, custom agent nese roli, handoff přepíná role a subagent scope ještě více zužuje.

## 3.2 Otevřít nejdřív

Otevřete:

- `.github\prompts\workshopPlan.prompt.md`
- `.github\agents\planner.agent.md`
- `.github\agents\integration-specialist.agent.md`
- `.github\agents\deployment-specialist.agent.md`
- `.github\agents\researcher.agent.md`
- `.github\agents\implementer.agent.md`

## 3.3 Spusťte workflow z prompt souboru

Použijte:

```text
/workshopPlan Create a step-by-step plan for modernizing the event-driven platform slice in this repository. Focus on examples/terraform, .github/workflows, hooks, and workflow automation. Do not edit files yet.
```

### Co pozorovat

- Workflow odstartoval prompt soubor.
- Prompt zároveň routoval konverzaci do `planner` custom agenta.

## 3.4 Pokračujte handoffem na specialisty

Použijte handoff pro pokračování do `integration-specialist`.

Pokud chcete direct prompt:

```text
Use the integration-specialist agent to identify which repo files define the current Service Bus, container app, and worker flow, summarize the change surface, and propose the smallest safe implementation slice.
```

Pak pokračujte do `deployment-specialist`:

```text
Use the deployment-specialist agent to review Terraform, GitHub Actions, hooks, and workflow-agent assets that should change together for this scenario.
```

### Co pozorovat

- Každý agent má jinou roli a důraz.
- Handoffy udržují workflow strukturované místo míchání všeho do jedné konverzace.

## 3.5 Vytvořte custom agenta živě

Po ukázce předpřipravených agentů vytvořte nového přirozeným jazykem, aby bylo vidět, že custom agenti nejsou jen ručně psané soubory.

Použijte:

```text
/create-agent This agent is specialized for business analytics, interactively gathers requirements, asks clarifying questions and outputs PRDs
```

Pokud Copilot položí doplňující otázky, odpovězte tak, aby scope byl o něco širší než čisté dashboardy:

```text
Analytics plus broader product PRDs. Keep it lightweight and business-facing, but proactive about KPIs and reporting requirements.
```

### Co pozorovat

- `/create-agent` převádí plain-language specializaci do znovupoužitelného `.agent.md`.
- Copilot nepotřebuje perfektní specifikaci na začátku; umí draftovat, hledat nejasnosti a iterovat.
- Je to silná ukázka převodu opakovaného stylu práce do trvalého specialisty.
- Výsledný artefakt je pořád jen soubor, takže jde reviewovat, verzovat a zlepšovat.

## 3.6 Vysvětlete subagenty

Teď ukažte:

- `.github\agents\researcher.agent.md`
- `.github\agents\implementer.agent.md`

Vysvětlete:

- hlavní specialista drží broad úkol
- subagent řeší užší část s menším kontextem
- tím se snižuje context clutter a orchestrace je jednodušší

Není nutné vždy vynucovat viditelné spuštění subagenta. Stačí vysvětlit pattern a ukázat, jak je definovaný v repozitáři.

## 3.7 Proč je tato kapitola důležitá

Tady studenti obvykle uvidí skutečný rozdíl mezi:

- plain chat prompting
- reusable workflow design
- multi-agent engineering

---


---

Previous: [Skills and MCP](02-skills-and-mcp_CZ.md) | Next: [Copilot CLI](04-copilot-cli_CZ.md)
