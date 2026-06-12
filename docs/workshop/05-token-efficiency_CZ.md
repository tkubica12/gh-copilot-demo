[Workshop index](README_CZ.md) | [Repository README](../../README.md)

---

# 5. Šetřete tokeny pomocí context hygiene

Tato kapitola převádí tokenovou efektivitu na měřitelnou engineering praxi. Shrnuje doporučení z přednášky a odkazuje na opakovatelnou měřicí laboratoř v Copilot CLI.

Pro narativní verzi použijte doprovodný článek [Token saving in GitHub Copilot](https://tomaskubica.cz/en/2026/token-saving-cz/). Tato kapitola je záměrně zaměřená na workshop evidence, prompty a lab artefakty.

## Souhrn měřeného benchmarku

Výsledky pocházejí z reálného lokálního běhu opakovatelných scénářů v `..\..\tools\copilot-token-lab`. Berte je jako laboratorní důkaz a pravidelně je přeměřujte pro aktuální klient, model i stav repozitáře.

| Test | Baseline | Tokenově efektivní varianta | Výsledek raw tokeny | Výsledek output tokeny | Výsledek weighted units |
| --- | --- | --- | ---: | ---: | ---: |
| AGENTS.md vs skills | Velké škálované multi-domain `AGENTS.md` | Malé `AGENTS.md` + jeden relevantní skill | 54.3% méně | 96.4% více | 68.8% méně |
| Progressive MCP discovery | 100 verbose direct MCP tools | Search-then-fetch MCP tools | 33.6% méně | 144.8% více | 31.7% méně |
| Prompt efficiency | Verbose open-ended prompt | Scoped files + output contract | 70.3% méně | 88.6% méně | 73.3% méně |
| Compression simulation | Tříkolová kumulovaná session | Tři nové handoff sessions | 14.3% méně | 101.7% více | 10.5% méně |
| Caveman-style response | Detailní incident guide | Stručný output contract | 66.1% více | 89.4% méně | 41.4% méně |
| Multi-agent overhead case | Jeden malý prompt hlavního agenta | Tři mini-model shard calls | 231.9% více | 0.0% méně | 56.3% méně |
| Large-context sharding attempt | Jeden velký accumulated-context prompt | Tři focused mini-model shards | 211.0% více | 3.9% více | 53.8% méně |

Detaily: [suite example analysis](../../tools/copilot-token-lab/suite-example-analysis.md), [full Python run report](../../tools/copilot-token-lab/reports/python-suite-2026-04-26.md), [language tokenizer micro-benchmark](../../tools/copilot-token-lab/reports/language-token-benchmark.md), [rerun instructions](../../tools/copilot-token-lab/README.md), [scenario fixtures](../../tools/copilot-token-lab/scenario_builder.py).

S dodanou GPT-5.5 cenovou kartou stojí jeden output token stejně jako šest necachovaných input tokenů nebo šedesát cachovaných input tokenů. Proto mívají output constraints často nejvyšší ROI na token.

Typické agentic coding sessions bývají dominované input a cached input tokeny, ne finálním textem odpovědi. Použijte `/usage`, OpenTelemetry nebo lab reporty a ověřte si vlastní mix.

| Tvar session | Běžný token mix | Nákladová implikace |
| --- | --- | --- |
| One-shot automatizace/deployment | vysoký fresh input, malá cache, nějaký output | omezte soubory a logy před startem |
| Dlouhá multi-turn coding session | převážně cached input, střední fresh input, nízký output | pokračování může být levnější než restart podobné práce |
| High-reasoning průzkum | více output/reasoning tokenů | zvyšujte reasoning jen když to úloha vyžaduje |

## Kdy se vyplatí `/compact`

Nepoužívejte `/compact` jako rutinní tlačítko na úsporu během aktivní konverzace. Souhrn stojí output tokeny a další kola často znovu platí input za kontext, který by jinak byl levně cachovaný.

Kompakce dává smysl, když platí aspoň jedno:

1. Kontext je velký a zastaralý (staré logy, neúspěšné pokusy, nerelevantní exploration).
2. Budete kontext forkovat nebo opakovaně použijete.
3. Potřebujete durable stav (handoff/implementation poznámka v repu).
4. Klesá kvalita odpovědí kvůli šumu.

Pravidlo: pokud plánujete ještě jednu navazující otázku ve stejné koherentní session, obvykle držte cached thread. Pokud plánujete více fresh startů ze stejného destilovaného kontextu nebo je thread převážně šum, použijte compact/handoff.

```text
compact value ≈ reuse_count * removed stale context
                - summary output tokens
                - fresh input paid after losing cache-read history
```

Tokenová efektivita není o hladovění Copilota na kontextu. Jde o nejmenší high-signal pracovní sadu, která úlohu vyřeší správně.

### Koncepty vysvětlit jako první

Tokeny se spotřebovávají i mimo text, který píšete:

- always-on instrukce (`AGENTS.md`, repository instructions)
- vybrané soubory, editor kontext, obrázky, logy, tool výsledky
- historie chatu a souhrny mezi koly
- model output
- další model volání přes agenty, nástroje, retry a subagenty

Praktický cíl je **scoped sufficiency**: dost kontextu pro přesnost, ale ne víc.

### Tokenově efektivní patterny

| Drahý pattern | Efektivnější varianta |
| --- | --- |
| Vložit celé README, specs a logy | Nejdřív se zeptat, které soubory/výřezy jsou potřeba |
| Široký úkol bez orientace | Pojmenovat soubory, služby, data a oblasti „nečti“ |
| Všechna pravidla držet always-on | Stabilní pravidla do `AGENTS.md`, detailní workflow do promptů/skills |
| MCP fetch všeho | Nejdřív search/list, pak fetch jen vybraného výsledku |
| `/fleet` na každý problém | Subagenty jen když je práce skutečně paralelní |
| Screenshoty terminálu | Vkládat přesné textové výřezy, pokud nejde o vizuální layout |
| Věčně dlouhá stale session | Použít `/context`, `/compact`, `/research` nebo fresh start |
| Leštěná esej když stačí stručně | Caveman-style output contract |

### Formujte prompty pro tokenizéry

Méně znaků neznamená vždy méně tokenů. Viz tokenizer report `tools\copilot-token-lab\reports\language-token-benchmark.md`.

Používejte:

- odstavce nahraďte bullet/body key-value
- „Please create function...“ nahraďte signaturou + krátkým komentářem
- dlouhé vysvětlení patternu nahraďte „Like `getUserById`, but by email"
- opakované dlouhé termíny zkraťte rozumnými zkratkami

Bezpečnostní a compliance text nepřekomprimovávejte, jinak vzniká rework.

### Používejte trvalý kontext místo opakovaného vysvětlování

Tento repozitář už má znovupoužitelné kontextové artefakty:

- `AGENTS.md` pro stabilní engineering pravidla
- `PRD.md` pro product intent
- `specs\` pro architekturu, security, testování, deployment a runbooky
- `.github\prompts\` pro reusable workflow starts
- `.github\skills\` pro detailní lokální capability načítané jen při relevanci

`AGENTS.md` držte kompaktní, protože tvoří recurring context tax.

### Preferujte skills a MCP jako progressive reveal

Skills i MCP šetří tokeny, když se použijí správně:

- **Skills** načítají detailní instrukce a skripty až při matchi úlohy.
- **MCP** má přinášet cílená živá data místo vkládání velkých logů a dokumentů.

Doporučený MCP workflow:

1. Search/list kandidátních zdrojů.
2. Výběr relevantního zdroje.
3. Fetch jen potřebných detailů.
4. Shrnutí výsledku.

### Udržte Agent Mode ohraničený

Agent Mode je silný, ale drahý, protože každý krok může replayovat instrukce, schemas, historii i výsledky nástrojů.

| Cost driver | Efektivní kontrola |
| --- | --- |
| Vágní zadání | pojmenovat soubory, funkce, expected behavior a done criteria |
| Chybějící setup | deterministic setup (`copilot-setup-steps.yml`) |
| Příliš mnoho tool calls | explicitně říct minimalizaci a batch operace |
| Dlouhá interní smyčka | nastavit max-turn očekávání, při driftu rescope |
| Opakované nepochopení | `/chronicle improve` pro stručné custom instructions |

### Používejte agenty a subagenty ekonomicky

Subagenti jsou nástroj izolace kontextu, ne automatická úspora tokenů. Mohou šetřit, ale mohou i násobit náklady, pokud každý worker znovu načítá stejná data.

V tomto repu:

- `researcher` je read-only a vrací krátká high-signal shrnutí
- `implementer` dělá malé izolované změny po dokončení research
- `task` se hodí na testy/buildy (krátký output při success, detaily při failu)

Praktické patterny:

1. **Krátký handoff**: cíl, fakta, přesné soubory, constraints, acceptance criteria.
2. **Shard podle ownership**: každý worker jiný service/file family/question.
3. **Levnější modely cíleně**: extrakce/sumarizace na mini modely, těžké debugování na silnější model.
4. **High-density state**: handoff poznámky pro opakované použití.
5. **Compact pro reuse/kvalitu**: ne automaticky kvůli ceně.

Další čtení: [Anthropic multi-agent research](https://www.anthropic.com/engineering/built-multi-agent-research-system), [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [LangChain write/select/compress/isolate](https://blog.langchain.com/context-engineering-for-agents/), [Google ADK scoped multi-agent context](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/).

### Zvolte správný model

Defaultně použijte **Auto**, při potřebě přepínejte cíleně:

| Úloha | Modelová strategie |
| --- | --- |
| Formátování, extrakce, jednoduché docs | Auto nebo menší/rychlejší model |
| File discovery a orientace v repu | rychlý průzkum nebo read-only subagent |
| Test/build exekuce | deterministický shell nebo `task` agent |
| Architektura a těžký debugging | silnější model / vyšší reasoning effort |
| Multi-file implementace | silnější model + scoped files + plán |

Cena za token není vše. Silnější model může být levnější, pokud vyřeší úlohu v méně kolech.

### Text, screenshoty a logy

Pro textové problémy používejte text. Vkládejte přesné chyby, stack trace, JSON/YAML, shell output a kód. Screenshoty používejte tam, kde rozhoduje vizuální layout.

U logů začínejte:

1. jednovětým shrnutím problému
2. přesným příkazem nebo CI jobem
3. první + finální chybou a 20–50 okolními řádky
4. prostředím a recent změnou
5. celý log jen pokud je nutný

### Měřte místo odhadování

OpenTelemetry mění token hygiene z doporučení na měřitelné důkazy. Side-project `tools\copilot-token-lab` poskytuje opakovatelný Python harness s TOML konfigurací.

```shell
cd tools/copilot-token-lab
uv run python run_token_lab.py suite --execute --allow-all-tools --iterations 3 --output-dir suite-runs
uv run python run_token_lab.py analyze --runs suite-runs/runs --output suite-runs/analysis.md
```

Oddělený language/tokenizer report:

```shell
cd tools/copilot-token-lab
uv run python language_token_benchmark.py --output reports/language-token-benchmark.md
```

### Vyzkoušejte

Začněte file-discovery promptem:

```text
Find the smallest set of files I should give Copilot to understand the event-driven add-on flow. Do not summarize the whole repo; return only file paths and why each matters.
```

Pak omezte output:

```text
Using only those files, create a concise implementation plan. Keep the output under 20 lines and include validation steps.
```

Pak vytvořte reusable handoff:

```text
Compact this session into a handoff summary for implementation. Keep only decisions, relevant files, constraints, and validation steps.
```

### Co pozorovat

- menší kontext může dát lepší odpověď, pokud má vyšší signál
- skills a MCP jsou progressive-reveal nástroje, ne důvod k dumpování dat
- subagenti snižují clutter, ale paralelní agenti násobí práci
- Auto model selection je dobrý default, ale model má odpovídat složitosti úlohy
- OpenTelemetry zpřehledňuje tokeny, modely, nástroje i latenci
- admin budgets/model policies/content exclusion doplňují prompt hygiene, nenahrazují ji

---

Previous: [Copilot CLI](04-copilot-cli_CZ.md) | Next: [Governance, review, security, and hooks](06-governance-review-security-hooks_CZ.md)
