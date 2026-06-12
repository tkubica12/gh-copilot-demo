[Workshop index](README_CZ.md) | [Repository README](../../README.md)

---

# 1. Jak formovat chování Copilota kontextem repozitáře

Tato kapitola vysvětluje, jak je Copilot veden **ještě předtím**, než začne dělat změny.

## 1.1 Koncepty, které vysvětlit jako první

Tato kapitola je o trvalém kontextu, zatím ještě ne o specializaci.

| Koncept | Nejlepší použití |
| --- | --- |
| **AGENTS.md** | Always-on pravidla repozitáře a engineering preference |
| **PRD a specs** | Product intent, architektura, kontrakty, testování, security a hranice služeb |
| **Constitution a spec-kit** | Opakovatelný způsob, jak bootstrapovat a evolvovat spec-driven delivery |
| **Copilot Spaces** | Sdílený plánovací kontext napříč repozitáři, dokumenty a týmy |

Nejsnazší vysvětlení vztahů:

- `AGENTS.md` učí Copilot, jak tento repozitář funguje
- `PRD.md` a `specs\` vysvětlují, co má systém dělat
- constitution a šablony udržují konzistentní specifikace napříč projekty
- Copilot Spaces pomáhají, když je plánovací kontext širší než jeden repozitář

Prompt soubory, custom agenti, handoffy a hooks jsou stále důležité, ale učí se lépe až poté, co publikum vidí, jak kontext dává samotný repozitář.

## 1.2 AGENTS.md do hloubky

Otevřete `AGENTS.md` a projděte ho. Je to nejdůležitější soubor pro formování chování Copilota.

VS Code s GitHub Copilot plně podporuje standard [AGENTS.md](https://agents.md/). `AGENTS.md` lze umístit i do podsložek pro monorepo situace, kde různé služby mají různá pravidla.

**Poznámka**: Kromě repository custom instructions můžete nastavovat i [personal custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions) pro osobní preference a [organization custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-organization-instructions) pro týmové standardy.

### Tipy, co dát do AGENTS.md

- **Coding style** — Terraform struktura, struktura kódu, použití Pydantic apod.
- **Frameworks a nástroje** — použijte FastAPI, uv jako package manager, v Terraformu provider azurerm, místo Kustomize Helm charty apod.
- **Procesy a doporučení** — vždy kontrolovat návrh řešení, vést implementation log, evidovat common errors
- **Testy a ad-hoc artefakty** — preferovat standardní testování, ad-hoc věci prefixovat a následně mazat
- **Běžná prostředí a konfigurace** — používat `.env`, rozhodnout direct env vs config class apod.
- **Dokumentační strategie** — používat docstrings, nekomentovat inline obvious věci
- **Nástroje** — preferovat nástroje před ručním CLI/script postupem, složitější situace řešit ad-hoc test skriptem

### Vyzkoušejte: vygenerujte AGENTS.md ze sdílené šablony

`AGENTS.md` můžete stavět ze šablony, sdílených standardů a projektových vstupů:

```text
I want you to generate file AGENTS.md in root folder or completely replace existing one.
- Use this template: #fetch https://raw.githubusercontent.com/tkubica12/gh-copilot-constitution/refs/heads/main/templates/AGENTS.md
- In this project we will use Terraform, extract key insights from https://raw.githubusercontent.com/tkubica12/gh-copilot-constitution/refs/heads/main/standards/TERRAFORM.md
- In this project we will use Python, extract key insights from https://raw.githubusercontent.com/tkubica12/gh-copilot-constitution/refs/heads/main/standards/PYTHON.md
- This project is specifically designed for learning therefore we strive for simplicity.
  - Make sure you do not do complicated and premature abstractions
  - It is OK to start with basic security so users learn fast, but make sure to document next steps for production use cases
  - It is OK to run with simple deployment setup without HA
```

## 1.3 Otevřít nejdřív

Otevřete:

- `AGENTS.md`
- `PRD.md`
- `specs\platform\ARCHITECTURE.md`
- `specs\trip\ARCHITECTURE.md`
- `specs\trip\TESTING.md`

Co zdůraznit:

- `AGENTS.md` dává sdílené výchozí chování pro Copilot a agenty
- `PRD.md` zachycuje produktové cíle, scope a success criteria
- `specs\platform\` drží cross-cutting architektonické guidance
- `specs\trip\` a další service složky ukazují service-level kontrakty a očekávání delivery

Tohle je první důležité sdělení workshopu: kvalitní agentic práce začíná explicitním kontextem, ne jen chytrým implementačním promptem.

## 1.4 Vyzkoušejte

Začněte bezpečnou read-only otázkou:

```text
/discuss Based on AGENTS.md, PRD.md, and the specs folders, summarize the architecture of this repository, the most important engineering rules, and what constraints a new service should follow. Do not modify files.
```

Pak se zeptejte:

```text
Which files in specs\platform and specs\trip should I read before changing event-driven messaging, deployment, or testing behavior in this repository?
```

## 1.5 Co pozorovat

- Odpověď by měla reflektovat pravidla z `AGENTS.md`.
- Copilot má brát PRD a specs jako first-class kontext, ne jako šum.
- Tato kapitola má působit jako architektonické ukotvení, ne jako execution.

## 1.6 Doplňte spec-driven design do příběhu

Repozitář už ukazuje výstupy spec-driven práce přes `PRD.md` a `specs\`. Užitečné je také ukázat, jak tento styl bootstrapovat nebo evolvovat pomocí constitution a spec tooling.

Klíčové reference:

- sdílený constitution přístup v [gh-copilot-constitution](https://github.com/tkubica12/gh-copilot-constitution)
- `specs\platform\` pro projektová rozhodnutí
- `specs\<service>\` pro service-specific architekturu, security, testování, deployment a runbooky

Pokud chcete ukázat spec-kit od nuly, použijte kompaktní flow:

```text
uvx --from git+https://github.com/github/spec-kit.git specify init my_new_project
code my_new_project
/speckit.constitution Create principles focused on clarity, simplicity, speed of development
/speckit.specify Build application that allows people to share ideas using sticky notes with persistent layout and export options
/speckit.plan Frontend is Vite with minimal libraries. Backend is Python and stores sticky note content and spatial layout.
/speckit.tasks
```

Hodnota není jen nástroj. Je to disciplína: sepsat intent, constraints, kontrakty a architekturu předtím, než požádáte agenty o implementaci.

## 1.7 Doplňte Copilot Spaces do kontextového příběhu

Copilot Spaces sem přirozeně zapadnou, protože rozšiřují plánovací kontext mimo jeden repozitář.

Otevřete:

- `.vscode\mcp.json`

Co zdůraznit:

- GitHub MCP server v tomto workspace zpřístupňuje `copilot_spaces` toolset přes headers
- Spaces se hodí pro multi-repo plánování, PRD shaping, architektonické diskuse a přípravu issue/projektů
- je to silný most mezi high-level plánováním a implementačními kapitolami dál

Vyzkoušejte:

```text
What are common errors when automating email processing? #list_copilot_spaces #get_copilot_space
```

## 1.8 Proč je tato kapitola důležitá

Publikum by mělo odejít s jedním jasným mentálním modelem:

> Copilot funguje lépe, když jsou instrukce repozitáře, produktový záměr, specifikace a sdílený plánovací kontext definované předem.

---


---

Previous: [Repository README](../../README.md) | Next: [Skills and MCP](02-skills-and-mcp_CZ.md)
