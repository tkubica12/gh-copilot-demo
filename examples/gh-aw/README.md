# GitHub Agentic Workflows examples

This folder contains **source markdown examples** for [GitHub Agentic Workflows](https://github.github.com/gh-aw/).

## Why this is in the workshop

GitHub Agentic Workflows (`gh-aw`) are a strong bridge between:

- interactive coding agents
- pull request review and governance
- repository automation in GitHub Actions

For this workshop, they help tell the story that agentic delivery does not stop when an interactive coding session ends.

## Key ideas to explain

- workflow source is written in **Markdown**
- execution happens through a compiled GitHub Actions **`.lock.yml`** workflow
- deterministic CI/CD stays in place
- agentic workflows are **additive**
- write actions should be done through **safe outputs**

## Suggested presenter flow

1. show coding agents and PR review
2. show issue triage as the lowest-risk write workflow: labels plus a recommendation comment
3. show security findings and governance expectations
4. show a `gh-aw` workflow that summarizes repository state or PR follow-up
5. emphasize human review and guardrails

## Example files

- `daily-maintainer-report.md`
- `governance-after-pr.md`
- `issue-triage.md`

## Practical note

Most examples are intentionally stored outside `.github/workflows/` so they remain demo artifacts rather than active workflows in this repository. The issue triage source also lives in `.github\workflows\issue-triage.md` with its compiled `.lock.yml` because it is the low-risk workflow intended for the live workshop.

If you want to use the other examples for real:

1. copy the markdown file into `.github\workflows\`
2. compile it with the `gh aw` CLI into a `.lock.yml`
3. review both files before enabling the workflow

## Useful starting points

```powershell
gh extension install github/gh-aw
gh aw compile .github/workflows/my-workflow.md
```

For real usage, always review permissions, safe outputs, and security guidance carefully.

## Demo-ready issue triage pattern

The `issue-triage.md` example mirrors GitHub's current Agentic Workflows guidance: start with small, reviewable writes before enabling agents to create code changes. The workflow can add only allowed labels and one explanatory comment. That makes it a strong first live demo because the audience can immediately see classification, feasibility assessment, and recommended next action without risking repository state.
