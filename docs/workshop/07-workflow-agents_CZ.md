[Workshop index](README_CZ.md) | [Repository README](../../README.md)

---

# 7. Přidejte workflow agenty do GitHub Actions

Tato kapitola rozšiřuje příběh z interaktivních agentů do repozitářové automatizace.

## 7.1 Koncepty, které vysvětlit jako první

Klasické GitHub Actions workflow jsou deterministické YAML pipeline. Jsou skvělé pro opakovatelné kroky, ale některé úkoly jsou judgement-driven a kontextově těžké (triage issue, shrnutí CI failu, governance follow-up po PR).

[GitHub Agentic Workflows](https://github.github.com/gh-aw/) (`gh-aw`) to řeší tím, že workflow píšete v **Markdownu místo YAML**. Agent běží v sandboxovaném GitHub Actions runneru.

- **Markdown source** — popisujete co chcete, ne detailní skript
- **Compiled lock file** — `gh aw compile` vytvoří standardní `.lock.yml`
- **Safe outputs** — write operace jdou přes explicitní allowlist
- **Read-only default** — zápisy vyžadují explicitní oprávnění
- **Additivní vůči CI/CD** — doplňují pipeline, nenahrazují build/test/release gates

## 7.2 Co dělají naše příklady

Otevřete:

- `.github\workflows\issue-triage.md`
- `examples\gh-aw\README.md`
- `examples\gh-aw\issue-triage.md`
- `examples\gh-aw\daily-maintainer-report.md`
- `examples\gh-aw\governance-after-pr.md`

### Issue triage

Nejkonkrétnější a nejméně rizikové demo workflow agenta. Spustitelný zdroj je v `.github\workflows\issue-triage.md`; vygenerovaný `.github\workflows\issue-triage.lock.yml` je commitnutý pro automatické spuštění. Workflow se spouští při otevření/znovuotevření issue, klasifikuje issue bez labelu a přidává krátký komentář s doporučením.

### Daily maintainer report

Workflow běží ve všední dny podle plánu. Agent analyzuje recent PR, failed runs, stale issues, dokumentační mezery a security follow-upy, pak vytvoří krátký issue report pro maintainery.

### Governance follow-up po pull requestu

Workflow reaguje na PR eventy. Agent shrne intent PR, zvýrazní unresolved review body, failing checks a security findings a doporučí další krok (coding agent, workflow agent nebo human review).

Tabulka maturity:

| Stage | Příklad | Safe outputs |
| --- | --- | --- |
| Start | Issue triage | přidání povolených labelů a jednoho komentáře |
| Scale | Daily maintainer report | vytvoření ohraničeného report issue |
| Govern | Governance after PR | vytvoření ohraničeného follow-up issue |

## 7.3 Vyzkoušejte

```text
Explain what this GitHub Agentic Workflow would do, what safe outputs it uses, and how it complements deterministic CI/CD instead of replacing it.
```

```text
Draft a variant of this workflow that creates a governance issue only when pull request checks fail or security findings appear.
```

## 7.4 Co pozorovat

- workflow agenti jsou přirozený další krok po coding agentech
- hodí se pro plánované i event-driven repo automatizace
- issue triage je nejrychlejší cesta k viditelnému užitku
- safe outputs dělají demo důvěryhodné
- lidské schválení a deterministické pipeline zůstávají důležité

---


---

Previous: [Governance, review, security, and hooks](06-governance-review-security-hooks_CZ.md) | Next: [Operations](08-operations_CZ.md)
