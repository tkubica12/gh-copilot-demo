[Workshop index](README_CZ.md) | [Repository README](../../README.md)

---

# 2. Skills a MCP: lokální schopnosti a propojené nástroje

Tato kapitola vysvětluje, jak Copilot získává schopnosti dvěma různými cestami.

## 2.1 Koncepty, které vysvětlit jako první

Skills i MCP jsou užitečné, ale řeší odlišné problémy.

| Typ schopnosti | Nejlepší použití |
| --- | --- |
| **Skills** | Snadno vytvářené a sdílené lokální schopnosti, často uložené v repozitáři a načítané na vyžádání |
| **MCP** | Centrálně spravované, bezpečné, enterprise-grade nástroje propojené na živé systémy nebo vzdálené znalosti |

Krátké vysvětlení:

- skills vynikají, když chcete něco lehkého, lokálního a snadno balitelného s repozitářem
- MCP vyniká, když potřebujete live nástroje, externí systémy nebo centrálně spravované enterprise integrace

Pro hlubší diskusi o centrální správě skills místo kopírování složek po repozitářích odkažte na článek [Agent skills and central management](https://tomaskubica.cz/en/2026/agent-skills-centralni-sprava/). Tuto kapitolu držte praktickou a zaměřenou na lokální ukázky v repu.

## 2.2 Ukažte skills v praxi

Otevřete:

- `.github\skills\simplecontext\SKILL.md`
- `.github\skills\json-to-xml-converter\SKILL.md`
- `examples\json\myjson.json`

### Vyzkoušejte: lightweight context skill

Zeptejte se:

```text
What is inventory number for BigDog?
```

### Co pozorovat

- Model má rozpoznat, že dotaz odpovídá skillu `simplecontext`.
- Detailní obsah skillu se načte až v případě potřeby.
- Pokud prostředí ukazuje tool traces/debug view, ukažte přístup ke skill souboru.

### Vyzkoušejte: script-backed skill

Přidejte `examples\json\myjson.json` do kontextu a zeptejte se:

```text
Convert this to XML.
```

### Co pozorovat

- Tento skill dobře ukazuje úlohu, kde se hodí deterministický skript.
- Skills nejsou jen extra text; mohou balit workflow kolem skriptů a resources.

## 2.3 Začněte MCP serverem, který žije v tomto repu

Otevřete:

- `.vscode\mcp.json`
- `mcp\README.md`
- `mcp\random_string_mcp\README.md`
- `mcp\random_string_mcp\src\main.py`

Začněte lokálním serverem, protože je transparentní a snadno vysvětlitelný.

Co zdůraznit:

- `.vscode\mcp.json` registruje `my-mcp-string-generator`
- připojuje se na `http://localhost:8000/sse`
- `mcp\random_string_mcp\src\main.py` je malý FastMCP server
- server vystavuje dva nástroje: `random_string` a `unique_string`
- je to výborný teaching příklad, protože je vidět registrace i implementace

### Jak je tento MCP server postaven

`random_string_mcp` používá `FastMCP` a přes dekorátor `@mcp.tool()` vystavuje Python funkce jako MCP nástroje.

- `random_string(...)` generuje náhodný suffix z vybraných znakových tříd
- `unique_string(...)` odvozuje predikovatelný suffix ze seedu přes SHA-256, což se hodí pro stabilní názvy
- `mcp.run(transport="sse")` spouští server přes Server-Sent Events, proto konfigurace používá HTTP URL

### Jak to spustit

Otevřete terminál a spusťte:

```pwsh
cd .\mcp\random_string_mcp\src
uv run main.py
```

Workspace MCP konfigurace směřuje Copilot na `http://localhost:8000/sse`, takže po spuštění je nástroj dostupný v chatu.

### Vyzkoušejte

Použijte dřívější demo prompt:

```text
Generate names for 10 containers in format app1-xxxxxx where xxxxxx is random suffix consisting of lowercase letters and numbers.
```

Pak ukažte druhý prompt zdůrazňující determinismus:

```text
Generate stable suffixes for dev, test, and prod using the unique string tool so that the same environment names always produce the same suffixes.
```

### Co pozorovat

- jde o skutečný MCP server v repozitáři, ne jen hostovanou enterprise integraci
- implementace je dost jednoduchá, aby studenti viděli, jak se custom MCP nástroje vytváří
- random generátor se hodí na jednorázové názvy, unique generátor na opakovatelné naming patterns

## 2.4 Připojte širší MCP servery

Po lokální ukázce upozorněte na nakonfigurované servery jako:

- GitHub MCP
- Microsoft Docs MCP
- Kubernetes MCP
- Azure MCP Server

### Vyzkoušejte: oficiální dokumentace přes MCP

Zeptejte se:

```text
Using the Microsoft Docs MCP server, find official guidance on custom agents in VS Code and summarize how handoffs work.
```

### Vyzkoušejte: znalost repozitáře přes GitHub MCP

Zeptejte se:

```text
Using GitHub tools, list the workflows in this repository and summarize which ones are build, deploy, or security related.
```

### Volitelné follow-up prompty

Pokud prostředí podporuje tyto integrace, zkuste:

```text
What plans we have for implementing PDF in our app? Check GitHub Issues.
```

```text
What versions my AKS clusters run?
```

```text
See my storage accounts, can I improve resiliency and data protection?
```

## 2.5 Proč je tato kapitola důležitá

Publikum má nyní chápat rozdíl mezi:

- lokálními balenými schopnostmi
- repo-lokálními MCP nástroji, které si můžete postavit sami
- centrálně připojenými nástroji

Toto rozlišení je důležité pro další kapitoly.

---


---

Previous: [Repository context](01-repository-context_CZ.md) | Next: [VS Code agents](03-vscode-agents_CZ.md)
