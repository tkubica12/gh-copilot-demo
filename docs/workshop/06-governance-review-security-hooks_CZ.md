[Workshop index](README_CZ.md) | [Repository README](../../README.md)

---

# 6. Governujte delivery pomocí review, security a hooks

Tato kapitola ukazuje, že engineering nekončí vygenerováním kódu.

Governance a token efficiency se překrývají, ale nejsou to stejné control planes. Budgety, user-level AI-credit limity, model availability a content exclusion jsou administrativní kontroly. Prompt compression, scoped instructions a MCP hygiene snižují spotřebu na úkol, ale nenahrazují budget/model policy.

## 6.1 Otevřete pull request a použijte Copilot review v GitHubu

Nejlepší je ukázat code review přímo v GitHub portálu.

Doporučený flow:

1. Vytvořte branch s malou, ale reálnou workshop změnou.
2. Otevřete pull request.
3. Ukažte PR summary a kartu **Files changed**.
4. Spusťte Copilot review nebo PR review experience.
5. Požádejte Copilot o correctness risks, missing validation a follow-up checks.

Ukázkové prompty:

```text
Review the proposed changes. Focus on correctness, risk, and what still needs validation.
```

```text
What are the highest-risk parts of this change if it were opened as a pull request?
```

### Co pozorovat

- GitHub je přirozené místo pro review jako součást spolupráce
- PR review spojuje Copilot, lidi, CI výsledky a branch policy
- je to ideální most mezi coding agenty a governance
- propojte s kapitolou CLI: `/review` před commitem, PR review před mergem

## 6.2 Ukažte security review v GitHub portálu

Vysvětlete navazující surfaces:

- karta **Security**
- code scanning alerts
- dependency findings
- autofix a remediation
- workflow checks v `.github\workflows`

Otevřete:

- `.github\workflows\devskim.yml`
- `.github\workflows\ossar.yml`
- `.github\workflows\tfsec.yml`
- `.github\workflows\sonarcloud.yml`

Co vysvětlit:

- repo už obsahuje security-oriented workflow pro PR
- `devskim`, `ossar`, `tfsec` nahrávají SARIF výsledky do GitHub security surfaces
- security review je silnější, když je vidět vazba mezi PR checks, findings a remediation

## 6.3 Vysvětlete hooks

Hooks přidávají **deterministickou skriptovanou policy** kolem Copilot agenta. Zatímco prompty a custom agenti ovlivňují chování pravděpodobnostně, hooks spouštějí skutečné skripty v konkrétních lifecycle událostech a umí vynucovat hard rules.

Copilot čte hook konfiguraci z `.github\hooks\copilot-policy.json`. V tomto repu je výchozí `.github\hooks\copilot-policy.json.disabled`, aby byly hooks defaultně neaktivní.

Definované hooky:

| Hook event | Co dělá v našem příkladu |
| --- | --- |
| **sessionStart** | Spustí se při startu agent session a zobrazí policy banner |
| **userPromptSubmitted** | Spustí se po každém promptu a zapisuje audit log |
| **preToolUse** | Běží před nástrojem; kontroluje a blokuje nebezpečné příkazy |

Otevřete:

- `.github\hooks\copilot-policy.json.disabled`
- `.github\hooks\scripts\session-banner.ps1`
- `.github\hooks\scripts\log-prompt.ps1`
- `.github\hooks\scripts\pre-tool-policy.ps1`

Aktivace:

```powershell
Rename-Item .\.github\hooks\copilot-policy.json.disabled copilot-policy.json
```

Deaktivace po demo části:

```powershell
Rename-Item .\.github\hooks\copilot-policy.json copilot-policy.json.disabled
```

### Co pozorovat

- hooks nejsou AI, jsou deterministické skripty
- v tomto repu se registrují až po explicitním vytvoření runtime policy souboru
- `preToolUse` může blokovat nebezpečné akce bez ohledu na model

## 6.4 Critic agent (Rubber Duck)

Critic agent (Rubber Duck) je experimentální funkce, kde druhé LLM z jiné modelové rodiny kontroluje plán i implementaci primárního agenta ještě předtím, než výstup uvidíte vy.

Když orchestrace běží na Claude, Rubber Duck běží na GPT-5.4 (a naopak). Odlišné modelové biasy pomáhají odhalit chyby, které primární model opakovaně přehlíží.

**Poznámka:** vyžaduje `/experimental on` v CLI a je aktuálně dostupné pro modely Claude.

## 6.5 Proč je tato kapitola důležitá

Studenti mají vidět, že AI engineering není jen generování, ale také:

- kontrola
- governance
- validace

---


---

Previous: [Token efficiency](05-token-efficiency_CZ.md) | Next: [Workflow agents](07-workflow-agents_CZ.md)
