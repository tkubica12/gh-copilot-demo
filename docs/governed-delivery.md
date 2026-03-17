# Governed delivery

This chapter closes the workshop by showing how agentic delivery fits inside code review, security review, approval, and operational governance.

## Why it matters

- Agents augment the delivery system instead of bypassing it.
- Local agent work connects naturally to pull requests, checks, scans, and approvals.
- Workflow agents and Azure SRE Agent belong in the same enterprise-ready narrative.

## What to explore

1. A local or agent-produced change.
2. Pull request review and security review.
3. GitHub Agentic Workflows as a governed extension of CI/CD.
4. Azure SRE Agent as the same governed agentic pattern applied to operations.

## Code review and security review

This repository highlights:

- Copilot-assisted pull request review
- GitHub Advanced Security findings
- autofix as a governed remediation step
- auditability, evidence, and branch protection as the real enterprise differentiators

## Workflow agents

GitHub Agentic Workflows belong here because they extend agentic delivery into GitHub Actions without removing existing controls.

Key governance points:

- markdown-authored briefs make the agent's goal and guardrails inspectable
- workflow agents should work with existing build, scan, and deployment evidence
- approvals, permissions, runtime budgets, and escalation rules still matter

Governance checklist:

- keep approval flow explicit for review, merge, and deployment
- keep permissions minimal and prefer read-only access for analysis-first workflows
- keep audit evidence visible through workflow summaries, artifacts, and existing GitHub controls
- keep workflow agents additive to existing CI/CD, code quality, and security scanning

Useful repository assets:

- `.github\workflows\demo-agentic-pr-review.yml`
- `.github\workflows\demo-agentic-release-readiness.yml`

## Azure SRE Agent belongs in governed delivery

[Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/overview) belongs here because it extends the same control model into operations:

- diagnose production issues
- correlate telemetry and change history
- automate runbooks with human oversight
- reduce MTTR with explainable actions

That makes it a strong closing example: the agentic pattern scales from coding to review to operations, while governance remains visible.

## What to notice

- governed delivery is the difference between an interesting demo and an enterprise operating model
- workflow agents should complement CI/CD, not replace it
- Azure SRE Agent shows that the same approval, evidence, and oversight story applies beyond coding

## Supporting material

- [`enterprise_demo_flow.md`](enterprise_demo_flow.md)
- [`README.md`](../README.md)
