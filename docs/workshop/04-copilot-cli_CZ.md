[Workshop index](README_CZ.md) | [Repository README](../../README.md)

---

# 4. Pokračujte v exekuci v Copilot CLI

Tato kapitola přesouvá workflow z plánování v IDE do autonomní exekuce.

## 4.1 Koncepty, které vysvětlit jako první

Copilot CLI je důležitý, protože workflow dělá operacionálnějším:

- sessions jsou explicitní
- režimy jsou explicitní
- background práce je explicitní
- permissions jsou explicitní

Důležitá terminologie:

- **plan mode** slouží pro tvorbu a ladění plánu
- **autopilot** je autonomní režim exekuce
- **`/yolo`** je alias pro allow-all permissions
- **`/yolo` není samostatný režim**

## 4.2 Spusťte CLI

Otevřete terminál a spusťte:

```text
copilot
```

## 4.3 Nejprve použijte plan mode

Přepněte do plan mode (`Shift+Tab`) a zeptejte se:

```text
Create an implementation plan for modernizing the event-driven platform slice in this repository. Focus on examples/terraform, .github/workflows, hooks, and examples/gh-aw. Do not edit files yet.
```

### Co pozorovat

- Copilot CLI není jen execution surface; lze ho použít i pro plánování.

## 4.4 Pokračujte do exekuce

Po odsouhlasení plánu pokračujte:

```text
Now continue the agreed task. Keep changes focused on documentation and workshop assets first so the workflow remains easy to review.
```

Pokud je úkol dobře ohraničený a chcete diskutovat autonomii, vysvětlete, kdy je vhodný autopilot.

## 4.5 Vysvětlete session a task management

Copilot CLI sessions jsou lokálně v `~/.copilot/session-state/`. Můžete navázat na předchozí session, přejmenovat ji a spravovat background tasks.

Použijte a proberte:

```text
/tasks
/session
/resume
/rename
/compact
```

### Vyzkoušejte

Obnovte předchozí session přes picker:

```text
/resume
```

Picker seskupuje sessions podle branche a repozitáře. Vyberte session a pokračujte, pak ji přejmenujte:

```text
/rename Modernize event-driven slice
```

### Co pozorovat

- `/resume` funguje pro lokální CLI sessions i cloud coding agent sessions
- `/rename` usnadňuje orientaci při větším počtu sessions
- `/compact` komprimuje historii kvůli context-window tlaku nebo stale kontextu; není to univerzální tlačítko na úsporu nákladů

## 4.6 Review, diff a sdílení práce

Před otevřením pull requestu má CLI vestavěné nástroje na kontrolu změn a sdílení výsledků.

| Příkaz | Co dělá |
| --- | --- |
| `/diff` | Zobrazí změny se syntax-highlighted diffem; přepínání mezi session a branch diffy, line comments. |
| `/review` | Spustí code-review agenta nad staged/unstaged změnami. |
| `/share file [PATH]` | Export session konverzace do Markdown souboru. |
| `/share gist` | Export session jako privátní GitHub gist. |
| `/share html [PATH]` | Export session jako self-contained interaktivní HTML. |

### Vyzkoušejte

Po exekuci spusťte:

```text
/diff
```

Pak rychlé review:

```text
/review
```

A nakonec sdílení:

```text
/share gist
```

### Co pozorovat

- `/diff` a `/review` uzavírají mezeru mezi generováním kódu a PR
- `/share` dělá ze sessions first-class artefakt pro handoff nebo archivaci
- příkazy přirozeně navazují na kapitolu 6 (governance a PR review)

## 4.7 Research v CLI

Příkaz `/research` aktivuje specializovaného research agenta, který sbírá informace z codebase, GitHub repozitářů i webu. Výstupem je komplexní Markdown report s citacemi.

### Vyzkoušejte

```text
/research How is event-driven messaging implemented in this repository?
```

Po dokončení Copilot zobrazí summary a odkaz na plný report. `Ctrl+Y` otevře report v terminálovém editoru. Poté sdílejte:

```text
/share file research
```

### Co pozorovat

- research reporty se ukládají na disk jako trvalé artefakty
- agent hledá v lokálním repu, org repozitářích (pokud jste přihlášeni) i na webu
- formát reportu se přizpůsobuje typu dotazu
- research agent používá fixní model (nelze měnit `/model`)

## 4.8 Chronicle: session insights a sebe-zlepšení

`/chronicle` převádí historii CLI sessions na praktické insighty: standup reporty, personalizované tipy a návrhy custom instructions.

**Poznámka:** `/chronicle` je experimentální. Nejdříve povolte:

```text
/experimental on
```

| Subcommand | Co dělá |
| --- | --- |
| `/chronicle standup` | Shrnutí recent práce včetně branchí, PR odkazů a status checks |
| `/chronicle tips` | Personalizované tipy podle reálných usage patternů |
| `/chronicle improve` | Analýza friction patternů a generování custom instructions |
| `/chronicle reindex` | Rebuild session store ze souborů na disku |

### Vyzkoušejte

```text
/chronicle standup last 3 days
```

Pak:

```text
/chronicle tips
```

### Co pozorovat

- jde o feedback loop: Copilot využívá vaši historii, aby pomohl pracovat lépe
- `/chronicle improve` nachází opakované nepochopení záměru a navrhuje instrukce
- je to i token-efficiency smyčka: méně nedorozumění = méně oprav v dalších sessions
- data zůstávají lokálně v `~/.copilot/session-state/`

## 4.9 Vysvětlete paralelizaci

Pokud chcete ukázat fan-out práci, použijte `/fleet` pro jasně oddělitelné úkoly.

Příklad:

```text
Research this repository in parallel: one agent should inspect Terraform and deployment workflows, another should inspect hooks and workflow-agent examples, and another should summarize how the workshop story should flow for students.
```

## 4.10 Execution surfaces, Copilot Memory a third-party agenti

Copilot nabízí více způsobů, jak spouštět coding agenty. Je důležité rozumět celé krajině a zvolit správnou execution surface podle typu úkolu.

| Surface | Jak spustit | Nejlepší použití |
| --- | --- | --- |
| **Copilot CLI (local)** | `copilot` v terminálu | Interaktivní práce, plan mode, lokální iterace |
| **Copilot CLI task (background)** | Z VS Code nebo CLI | Dlouhé úlohy v lokálním worktree |
| **Cloud coding agent (PR-based)** | Přiřazení issue Copilotu nebo agents panel | Autonomní práce v GitHub cloudu |
| **Third-party agents (Claude, Codex)** | Agents tab, issues, PR comments (`@AGENT_NAME`) | Alternativní coding agenti s jinými silnými stránkami modelu |
| **GitHub.com web** | Agents panel na libovolné stránce | Rychlé úkoly, monitoring, review sessions |
| **GitHub Mobile** | Home view → agent sessions | Monitoring a vytváření tasků na cestách |

### Copilot Memory

Copilot si může vytvářet persistentní porozumění repozitáře ukládáním **memories** — úzce vymezených faktů odvozených během práce.

Klíčové body:

- memories jsou **repository-scoped**, ne user-scoped
- vznikají s **citacemi** a před použitím se validují proti aktuálnímu codebase
- **automaticky se mažou po 28 dnech**
- fungují napříč execution surfaces
- vlastníci repa je spravují v **Settings → Copilot → Memory**

### Third-party coding agenti

Vedle cloud coding agenta GitHubu jsou dostupní i **Anthropic Claude** a **OpenAI Codex** (public preview). Flow je stejný: zadat issue/prompt, agent vytvoří změny a PR, tým reviewuje a iteruje.

### Self-hosted runners pro cloud agenty

Cloud coding agenti a Copilot code review běží na GitHub Actions runnerech. Defaultně GitHub-hosted, ale organizace mohou použít **self-hosted runners** kvůli interním zdrojům, výkonu, síťové kontrole a compliance. Vyžaduje to **ARC** a **Ubuntu x64 Linux**.

## 4.11 Proč je tato kapitola důležitá

Tady workflow začíná připomínat skutečný engineering místo jedné konverzace. CLI není jen execution nástroj — pomáhá reviewovat změny, dělat research, učit se ze session historie a napojuje se na širší ekosystém surfaces, memory a third-party agentů.

---


---

Previous: [VS Code agents](03-vscode-agents_CZ.md) | Next: [Token efficiency](05-token-efficiency_CZ.md)
