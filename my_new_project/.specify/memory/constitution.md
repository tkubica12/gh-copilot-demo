<!--
Sync Impact Report:
Version change: none → 1.0.0
Added principles:
- I. Clarity-First Communication
- II. Simplicity-First Design
- III. Speed-First Development
Added sections:
- Development Standards
- Quality Gates
Templates requiring updates:
✅ plan-template.md - Constitution Check section aligns with new principles
✅ spec-template.md - User story prioritization aligns with speed-first principle
✅ tasks-template.md - Task organization reflects clarity and simplicity principles
Follow-up TODOs: None - all placeholders filled
-->

# My New Project Constitution

## Core Principles

### I. Clarity-First Communication
Every feature, API, and process MUST prioritize understanding over cleverness. Code must be self-documenting through clear naming, structure, and minimal abstraction layers. Documentation must answer "why" not just "what". Error messages must provide actionable guidance. No feature ships without clear user scenarios and acceptance criteria.

**Rationale**: Unclear systems create maintenance debt, slow onboarding, and increase bug rates. Clarity accelerates every subsequent development activity.

### II. Simplicity-First Design
Choose the simplest solution that meets requirements. Avoid premature optimization, unnecessary abstractions, and over-engineering. When complexity is unavoidable, isolate it behind simple interfaces. Default to proven patterns over novel approaches. Every added dependency must justify its complexity cost.

**Rationale**: Simple systems are faster to build, easier to debug, and more reliable. Complexity should be earned through proven necessity, not assumed.

### III. Speed-First Development
Prioritize rapid iteration and quick feedback loops. Features must be independently testable and deployable. Use test-driven development to catch issues early. Implement highest-priority user stories first to validate assumptions quickly. Automate repetitive tasks to maintain development velocity.

**Rationale**: Fast feedback reveals problems sooner when they're cheaper to fix. Independent feature delivery reduces risk and enables continuous value delivery.

## Development Standards

### Code Quality Requirements
- All code must pass automated linting and formatting checks
- Functions and classes must have single responsibilities
- Dependencies must be explicitly declared and version-pinned
- Configuration must be externalized from code
- Secrets must never be committed to version control

### Documentation Standards
- Every public API must have usage examples
- Every feature must have user scenarios with acceptance criteria
- Every complex algorithm must explain its approach and trade-offs
- Every configuration option must document its purpose and impact

## Quality Gates

### Pre-Implementation Gates
- Feature specifications must include prioritized user stories
- Each user story must be independently testable
- Technical approach must justify complexity over simpler alternatives
- All dependencies must be approved and documented

### Pre-Deployment Gates
- All tests must pass (unit, integration, contract)
- Code coverage must meet project standards (minimum 80% for new code)
- Security scans must pass with no high-severity issues
- Performance requirements must be verified
- Documentation must be complete and current

## Governance

This constitution supersedes all other development practices and guidelines. All code reviews, architectural decisions, and feature planning must verify compliance with these principles. When principles conflict, prioritize in order: Clarity, Simplicity, Speed.

**Amendment Process**: Changes require documented justification, team approval, and migration plan for existing code. Breaking changes require major version increment.

**Compliance Review**: Monthly reviews ensure adherence. Violations must be justified or remediated within one sprint.

**Version**: 1.0.0 | **Ratified**: 2025-11-07 | **Last Amended**: 2025-11-07
