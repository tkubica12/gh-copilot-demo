# Enterprise demo flow (CZ)

>> SLIDE: Přehled platformy GitHub Enterprise a GitHub Copilot

## 1. Začněte rychlými ukázkami, ale stručně

- Next-edit suggestion a autocomplete ve VS Code
- Rychlý prompt na porozumění codebase v kontextu tohoto repozitáře
- Volitelně krátká zmínka o volbě modelu, ale nenechte ji převzít hlavní část session

Cíl: vytvořit základní orientaci a rychle přejít k hlavnímu příběhu.

## 2. Vysvětlete vrstvy customizace před agentic částí

- `AGENTS.md` jako always-on kontrakt repozitáře
- Prompt soubory jako znovupoužitelné jednorázové workflow
- Custom agenti jako trvalé specializované persony
- Hooks jako deterministické policy a audit guardrails
- Skills jako balené lokální schopnosti
- MCP jako most k externím systémům a živým nástrojům

Tato část dává publiku slovník pro zbytek demo flow.

## 3. Přejděte do custom agentů ve VS Code

- Ukažte `planner` agenta a vytvořte plán pro hlavní scénář
- Přes handoff přejděte do `integration-specialist`
- Poté handoff do `deployment-specialist`
- Použijte `/create-agent` pro business-analytics agenta, který sbírá požadavky a vytváří PRD
- Vysvětlete, že `researcher` a `implementer` existují jako fokusované helper subagenty

Klíčové sdělení:

- prompt soubory spouští práci konzistentně
- custom agenti drží aktivní roli/personu
- custom agenty lze vytvářet live přirozeným jazykem a iterativně ladit
- subagenti zužují scope a omezují context clutter

## 4. Pokračujte v Copilot CLI

- Předejte práci z VS Code do Copilot CLI
- Ukažte izolaci workspace vs worktree
- Nejdříve plan mode, autopilot až u dobře ohraničeného úkolu
- Vysvětlete `/yolo` přesně jako allow-all permissions alias, ne jako samostatný režim
- Ukažte `/tasks`, `/resume` a `/session`
- Podle potřeby ukažte `/fleet` pro paralelní nezávislé tasky
- Zařaďte kapitolu tokenové efektivity (`docs\workshop\05-token-efficiency.md`): scoped context, `/context`, `/compact`, Auto model selection, rozumné používání subagentů a měření pomocí OpenTelemetry

Je to silná část live dema, protože propojuje plánování v IDE s autonomní background exekucí.

## 5. Přesuňte se od coding agentů ke governed delivery

- Vytvořte nebo popište PR flow
- Použijte Copilot code review
- Ukažte, jak po implementaci navazují security findings, code scanning nebo autofix
- Hook toggle zapínejte jen těsně před deterministic policy demo a pak jej opět vypněte
- Zdůrazněte, že finální rozhodování zůstává na lidech

## 6. Přidejte GitHub Agentic Workflows (`gh-aw`)

- Představte `gh-aw` jako doplňkovou automatizaci uvnitř GitHub Actions
- Vysvětlete markdown workflow source + kompilovaný `.lock.yml`
- Vysvětlete safe outputs, sandboxing a security-first design
- Použijte ukázkové workflow z `examples\gh-aw`
- Workflow agenty umístěte jako další vrstvu po interaktivních coding agentech:
  - sumarizace health stavu repozitáře
  - triage PR follow-upů
  - vytváření governance issue pro maintainery

Klíčové sdělení:

- deterministické CI/CD je stále páteř
- workflow agenti ho rozšiřují o Continuous AI

## 7. Zakončete SRE a operations

- Po merge a deploymentu příběh nekončí
- Ukažte přínos Azure SRE Agent nebo podobných operational agentů
- Propojte deployment změny, telemetry, incidenty a remediation

To je nejlepší závěr, protože pokrývá celý software lifecycle, ne jen generování kódu.

## 8. Volitelná rozšíření při dostatku času

- generování dokumentace
- KQL a SQL prompting
- vision a image-to-code
- web search a cílený fetch
- MCP deep dives
- Spark

Používejte je jen když je publikum explicitně chce nebo když potřebujete záložní větev dema.
