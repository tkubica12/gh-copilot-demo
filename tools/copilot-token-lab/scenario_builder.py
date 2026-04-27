"""Create reusable token-efficiency benchmark fixtures."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent


def write(path: Path, content: str) -> None:
    """Write text content and create parent directories."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def build_common_workspace(path: Path) -> None:
    """Create the shared files used by most benchmark scenarios."""

    write(
        path / "README.md",
        """
        # Token lab fixture

        The Trip Add-on Router receives trip events, chooses eligible add-ons,
        records an audit decision, and sends one customer notification.
        """,
    )
    write(
        path / "src" / "addon_router.py",
        """
        RULES = {
            "ski": ["boot-rental", "lift-pass"],
            "beach": ["sunshade", "snorkel"],
            "city": ["museum-pass", "metro-card"],
        }


        def eligible_addons(trip_type: str) -> list[str]:
            return RULES.get(trip_type, [])
        """,
    )
    write(
        path / "src" / "audit_policy.py",
        """
        def audit_message(trip_id: str, addons: list[str]) -> str:
            return f"{trip_id}: offered {', '.join(addons)}"
        """,
    )
    write(
        path / "ops" / "runbook.md",
        """
        # Add-on routing runbook

        Validate a change by running unit tests, checking one synthetic ski trip,
        and confirming exactly one customer notification is emitted.
        """,
    )


def addon_policy_text(lines: int = 48) -> str:
    """Return the relevant add-on policy that can live in AGENTS.md or a skill."""

    base = [
        "# Add-on routing policy",
        "",
        "When evaluating add-on routing, preserve auditability, idempotency, "
        "and one customer notification per trip event.",
        "",
    ]
    for index in range(1, lines + 1):
        base.append(
            f"- Add-on rule {index:03d}: before changing add-on routing, restate "
            "the input event, eligible add-ons, audit implication, validation "
            "command, rollback note, ownership boundary, and customer impact."
        )
    return "\n".join(base)


def big_agents_text() -> str:
    """Return intentionally verbose always-on instructions spanning many domains."""

    base = [
        "# Token Lab Instructions",
        "",
        "Always answer as a concise senior engineer.",
        "",
        addon_policy_text(),
    ]
    domains = [
        "billing",
        "identity",
        "frontend",
        "telemetry",
        "data-retention",
        "mobile",
        "compliance",
        "incident-response",
        "partner-api",
        "data-science",
        "localization",
        "procurement",
        "accessibility",
        "support",
        "legal",
        "finance",
    ]
    for domain in domains:
        base.extend(["", f"## {domain} policy"])
        for index in range(1, 121):
            base.append(
                f"- {domain} detail {index:03d}: preserve ownership, validation, "
                "observability, rollback, release notes, escalation, and audit "
                "language for this unrelated domain."
            )
    return "\n".join(base)


def build_agents_variants(output: Path) -> tuple[Path, Path]:
    """Create big-AGENTS and small-AGENTS-plus-skill workspaces."""

    big = output / "agents-big"
    small = output / "agents-small-skills"
    for workspace in (big, small):
        if workspace.exists():
            shutil.rmtree(workspace)
        build_common_workspace(workspace)

    write(big / "AGENTS.md", big_agents_text())
    write(
        small / "AGENTS.md",
        """
        # Token Lab Instructions

        Keep answers concise. For add-on routing details, use the local
        `addon-routing` skill only when the task needs the full procedure.
        """,
    )
    write(
        small / ".github" / "skills" / "addon-routing" / "SKILL.md",
        addon_policy_text(),
    )
    unrelated_skills = {
        "billing-policy": "Billing adjustments",
        "identity-policy": "Identity lifecycle",
        "telemetry-policy": "Telemetry conventions",
        "support-policy": "Support escalation",
        "legal-policy": "Legal review",
    }
    for skill_name, subject in unrelated_skills.items():
        write(
            small / ".github" / "skills" / skill_name / "SKILL.md",
            large_doc(f"{subject} skill", subject, sections=80),
        )
    return big, small


def build_workflow_workspace(output: Path) -> Path:
    """Create files for single-agent versus decomposed workflow comparisons."""

    workspace = output / "workflow"
    if workspace.exists():
        shutil.rmtree(workspace)
    build_common_workspace(workspace)
    write(
        workspace / "frontend.md",
        """
        The UI should show a compact add-on card with title, price, and one
        dismiss action. It must not show duplicate notifications.
        """,
    )
    write(
        workspace / "backend.md",
        """
        The API should expose eligible add-ons by trip type and record the audit
        decision before sending the notification event.
        """,
    )
    write(
        workspace / "operations.md",
        """
        Operations require one smoke test, one dashboard check, and rollback by
        disabling the add-on routing feature flag.
        """,
    )
    write(workspace / "AGENTS.md", "Answer in at most six bullets.\n")
    return workspace


def large_doc(title: str, subject: str, sections: int = 120) -> str:
    """Return a large deterministic document for context-heavy scenarios."""

    lines = [f"# {title}", ""]
    for index in range(1, sections + 1):
        lines.append(
            f"Section {index:03d}: {subject} requires explicit ownership, audit "
            "trail preservation, validation evidence, rollback readiness, telemetry "
            "review, customer impact notes, and concise handoff language."
        )
    return "\n".join(lines)


def compressed_handoff_text() -> str:
    """Return the compact handoff used for compression comparisons."""

    return """
    # Compressed add-on routing handoff

    Frontend: show one compact add-on card and prevent duplicate notifications.
    Backend: calculate eligible add-ons, audit the decision, then emit one event.
    Operations: run the smoke test, check the dashboard, and roll back with the
    add-on routing feature flag.
    """


def full_transcript_text() -> str:
    """Return verbose synthetic turn history for compression comparisons."""

    return "\n\n".join(
        [
            large_doc("Turn history frontend", "Frontend decision history", 27),
            large_doc("Turn history backend", "Backend decision history", 27),
            large_doc("Turn history operations", "Operations decision history", 27),
            large_doc("Turn history unrelated billing", "Billing discussion", 27),
            large_doc("Turn history unrelated identity", "Identity discussion", 27),
        ]
    )


def compression_turn_context(subject: str) -> str:
    """Return one large context block for multi-turn compression scenarios."""

    return large_doc(f"{subject} turn context", subject, 80)


def build_large_context_workspace(output: Path) -> Path:
    """Create a workspace where decomposed shards can avoid large irrelevant context."""

    workspace = output / "large-context"
    if workspace.exists():
        shutil.rmtree(workspace)
    build_common_workspace(workspace)
    write(workspace / "AGENTS.md", "Use only the files requested by the prompt.\n")
    subjects = {
        "frontend-deep.md": "Frontend add-on cards",
        "backend-deep.md": "Backend add-on eligibility",
        "operations-deep.md": "Operational validation",
        "billing-deep.md": "Billing adjustments",
        "identity-deep.md": "Identity lifecycle",
        "mobile-deep.md": "Mobile notification behavior",
        "security-deep.md": "Security review",
        "analytics-deep.md": "Analytics instrumentation",
    }
    for filename, subject in subjects.items():
        write(workspace / "context" / filename, large_doc(subject, subject))
    write(workspace / "compressed-handoff.md", compressed_handoff_text())
    write(workspace / "full-transcript.md", full_transcript_text())
    return workspace


def build_mcp_configs(output: Path) -> tuple[Path, Path, Path]:
    """Create MCP workspaces and config files for wide versus discovery tests."""

    workspace = output / "mcp"
    workspace.mkdir(parents=True, exist_ok=True)
    write(workspace / "AGENTS.md", "Use MCP tools when the prompt asks for action metadata.\n")

    server = ROOT / "mcp_servers" / "token_lab_mcp.py"
    wide_config = output / "mcp-wide.json"
    discovery_config = output / "mcp-discovery.json"
    python = sys.executable

    wide_config.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "token-lab-wide": {
                        "command": python,
                        "args": [str(server), "wide"],
                    }
                }
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    discovery_config.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "token-lab-discovery": {
                        "command": python,
                        "args": [str(server), "discovery"],
                    }
                }
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return workspace, wide_config, discovery_config


def prompt(
    *,
    prompt_id: str,
    name: str,
    group: str,
    variant: str,
    technique: str,
    text: str,
    workspace: Path,
    models: list[str],
    efforts: list[str],
    baseline: bool = False,
    **extra: object,
) -> dict[str, object]:
    """Build one prompt catalog entry."""

    result: dict[str, object] = {
        "id": prompt_id,
        "name": name,
        "mode": "plan",
        "comparisonGroup": group,
        "variant": variant,
        "baseline": baseline,
        "expectedTechnique": technique,
        "prompt": text,
        "workingDirectory": str(workspace),
        "models": models,
        "efforts": efforts,
        "disableBuiltinMcps": True,
    }
    result.update(extra)
    return result


def build_catalog(output: Path) -> Path:
    """Build all scenario fixtures and return the generated prompt catalog path."""

    output = output.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    big_agents, small_agents = build_agents_variants(output)
    workflow = build_workflow_workspace(output)
    large_context = build_large_context_workspace(output)
    mcp_workspace, wide_mcp, discovery_mcp = build_mcp_configs(output)
    common_models = ["gpt-5.5"]
    common_effort = ["medium"]

    prompts = [
        prompt(
            prompt_id="agents-big",
            name="Large always-on AGENTS.md",
            group="agents-context",
            variant="large-agents",
            baseline=True,
            technique="large-always-on-instructions",
            text=(
                "Explain the add-on routing change-control procedure in five bullets. "
                "Use repository instructions. Do not edit files."
            ),
            workspace=big_agents,
            models=common_models,
            efforts=common_effort,
        ),
        prompt(
            prompt_id="agents-small-skill",
            name="Small AGENTS.md with skill on demand",
            group="agents-context",
            variant="small-agents-skill",
            technique="small-instructions-dynamic-skill",
            text=(
                "Explain the add-on routing change-control procedure in five bullets. "
                "Use the addon-routing skill only if needed. Do not edit files."
            ),
            workspace=small_agents,
            models=common_models,
            efforts=common_effort,
        ),
        prompt(
            prompt_id="mcp-wide-tools",
            name="MCP server exposing 100 direct actions",
            group="mcp-discovery",
            variant="wide-100-tools",
            baseline=True,
            technique="wide-tool-surface",
            text=(
                "Use MCP tools to find metadata for action TARGET-SUNSET. Return only "
                "the action id, owner, and payload. Do not edit files."
            ),
            workspace=mcp_workspace,
            models=common_models,
            efforts=common_effort,
            additionalMcpConfig=str(wide_mcp),
            disableBuiltinMcps=True,
        ),
        prompt(
            prompt_id="mcp-progressive-discovery",
            name="MCP search then targeted fetch",
            group="mcp-discovery",
            variant="search-then-fetch",
            technique="progressive-mcp-discovery",
            text=(
                "Use MCP tools to search for action TARGET-SUNSET, then fetch only that "
                "action. Return only the action id, owner, and payload. Do not edit files."
            ),
            workspace=mcp_workspace,
            models=common_models,
            efforts=common_effort,
            additionalMcpConfig=str(discovery_mcp),
            disableBuiltinMcps=True,
        ),
        prompt(
            prompt_id="workflow-single-agent",
            name="One broad main-agent prompt",
            group="workflow-overhead",
            variant="single-main-agent",
            baseline=True,
            technique="single-broad-context",
            text=(
                "Do not use tools. Use these excerpts only. frontend.md: The UI should "
                "show a compact add-on card with title, price, and one dismiss action. "
                "It must not show duplicate notifications. backend.md: The API should "
                "expose eligible add-ons by trip type and record the audit decision "
                "before sending the notification event. operations.md: Operations "
                "require one smoke test, one dashboard check, and rollback by disabling "
                "the add-on routing feature flag. Produce one combined implementation "
                "handoff with UI, API, operations, and validation notes."
            ),
            workspace=workflow,
            models=common_models,
            efforts=common_effort,
        ),
        prompt(
            prompt_id="workflow-shard-frontend",
            name="Low-context frontend shard",
            group="workflow-overhead",
            variant="orchestrated-mini-shards",
            technique="external-low-context-subtask",
            text=(
                "Do not use tools. Excerpt: The UI should show a compact add-on card "
                "with title, price, and one dismiss action. It must not show duplicate "
                "notifications. Summarize UI requirements in three bullets."
            ),
            workspace=workflow,
            models=["gpt-5.4-mini"],
            efforts=["low"],
        ),
        prompt(
            prompt_id="workflow-shard-backend",
            name="Low-context backend shard",
            group="workflow-overhead",
            variant="orchestrated-mini-shards",
            technique="external-low-context-subtask",
            text=(
                "Do not use tools. Excerpt: The API should expose eligible add-ons by "
                "trip type and record the audit decision before sending the notification "
                "event. Summarize API requirements in three bullets."
            ),
            workspace=workflow,
            models=["gpt-5.4-mini"],
            efforts=["low"],
        ),
        prompt(
            prompt_id="workflow-shard-ops",
            name="Low-context operations shard",
            group="workflow-overhead",
            variant="orchestrated-mini-shards",
            technique="external-low-context-subtask",
            text=(
                "Do not use tools. Excerpt: Operations require one smoke test, one "
                "dashboard check, and rollback by disabling the add-on routing feature "
                "flag. Summarize operational requirements in three bullets."
            ),
            workspace=workflow,
            models=["gpt-5.4-mini"],
            efforts=["low"],
        ),
        prompt(
            prompt_id="workflow-large-single",
            name="Large accumulated context single agent",
            group="workflow-large-shards",
            variant="single-large-context",
            baseline=True,
            technique="large-accumulated-context",
            text=(
                f"Read every file in {large_context / 'context'}. Produce a combined "
                "handoff for only frontend, backend, and operations add-on routing "
                "concerns. Do not edit files."
            ),
            workspace=large_context,
            models=common_models,
            efforts=common_effort,
        ),
        prompt(
            prompt_id="workflow-large-shard-frontend",
            name="Focused frontend shard",
            group="workflow-large-shards",
            variant="focused-mini-shards",
            technique="compressed-subtask-context",
            text=(
                f"Read only {large_context / 'context' / 'frontend-deep.md'} and "
                "return three frontend handoff bullets."
            ),
            workspace=large_context,
            models=["gpt-5.4-mini"],
            efforts=["low"],
        ),
        prompt(
            prompt_id="workflow-large-shard-backend",
            name="Focused backend shard",
            group="workflow-large-shards",
            variant="focused-mini-shards",
            technique="compressed-subtask-context",
            text=(
                f"Read only {large_context / 'context' / 'backend-deep.md'} and "
                "return three backend handoff bullets."
            ),
            workspace=large_context,
            models=["gpt-5.4-mini"],
            efforts=["low"],
        ),
        prompt(
            prompt_id="workflow-large-shard-ops",
            name="Focused operations shard",
            group="workflow-large-shards",
            variant="focused-mini-shards",
            technique="compressed-subtask-context",
            text=(
                f"Read only {large_context / 'context' / 'operations-deep.md'} and return three operations "
                "handoff bullets."
            ),
            workspace=large_context,
            models=["gpt-5.4-mini"],
            efforts=["low"],
        ),
        prompt(
            prompt_id="compression-full-history",
            name="Three resumed turns without compaction",
            group="compression-simulation",
            variant="full-history",
            baseline=True,
            technique="uncompressed-history",
            text="Multi-turn accumulated context scenario.",
            workspace=large_context,
            models=common_models,
            efforts=common_effort,
            sessionStrategy="resume",
            turns=[
                {
                    "prompt": (
                        "Turn 1 of 3. Do not use tools. Load this frontend context "
                        "into the working conversation and reply with three retained "
                        "frontend decisions.\n\n"
                        f"{compression_turn_context('Frontend add-on routing decisions')}"
                    )
                },
                {
                    "prompt": (
                        "Turn 2 of 3. Do not use tools. Keep prior frontend decisions, "
                        "load this backend context, and reply with three retained "
                        "backend decisions.\n\n"
                        f"{compression_turn_context('Backend add-on routing decisions')}"
                    )
                },
                {
                    "prompt": (
                        "Turn 3 of 3. Do not use tools. Keep prior frontend and backend "
                        "decisions, load this operations context, and return final "
                        "frontend, backend, operations, validation, and rollback "
                        "decisions in five bullets.\n\n"
                        f"{compression_turn_context('Operations add-on routing decisions')}"
                    )
                },
            ],
        ),
        prompt(
            prompt_id="compression-summary",
            name="Fresh turns with compact handoff",
            group="compression-simulation",
            variant="compressed-handoff",
            technique="compressed-context",
            text="Multi-turn compact handoff scenario.",
            workspace=large_context,
            models=common_models,
            efforts=common_effort,
            sessionStrategy="fresh-handoff",
            turns=[
                {
                    "prompt": (
                        "Turn 1 of 3. Do not use tools. Load this frontend context and "
                        "return only a compact handoff with durable decisions, open "
                        "risks, and validation notes.\n\n"
                        f"{compression_turn_context('Frontend add-on routing decisions')}"
                    ),
                    "captureHandoff": True,
                    "dryRunHandoff": "Frontend compact handoff.",
                },
                {
                    "prompt": (
                        "Turn 2 of 3. Do not use tools. Previous compact handoff:\n"
                        "{previous_handoff}\n\nLoad this backend context and return "
                        "only an updated compact handoff with durable decisions, open "
                        "risks, and validation notes.\n\n"
                        f"{compression_turn_context('Backend add-on routing decisions')}"
                    ),
                    "captureHandoff": True,
                    "dryRunHandoff": "Frontend and backend compact handoff.",
                },
                {
                    "prompt": (
                        "Turn 3 of 3. Do not use tools. Previous compact handoff:\n"
                        "{previous_handoff}\n\nLoad this operations context and return "
                        "final frontend, backend, operations, validation, and rollback "
                        "decisions in five bullets.\n\n"
                        f"{compression_turn_context('Operations add-on routing decisions')}"
                    )
                },
            ],
        ),
        prompt(
            prompt_id="prompt-verbose",
            name="Verbose prompt",
            group="prompt-efficiency",
            variant="verbose",
            baseline=True,
            technique="over-specified-prompt",
            text=(
                "I need you to carefully think through the add-on router. Please read "
                "all available local documents, consider UI, API, operational, "
                "validation, rollback, audit, and customer-notification concerns, "
                "then provide a thoughtful answer with background, assumptions, "
                "recommendations, validation, risks, and next steps. Do not edit files."
            ),
            workspace=workflow,
            models=common_models,
            efforts=common_effort,
        ),
        prompt(
            prompt_id="response-normal",
            name="Normal explanatory response",
            group="response-style",
            variant="normal",
            baseline=True,
            technique="normal-response-style",
            text=(
                "Do not use tools. Write a detailed add-on router incident guide for "
                "engineers and operators. Include these sections with rich explanations: "
                "overview, symptoms, immediate triage, likely root causes, diagnostics, "
                "mitigation, rollback, validation, customer communication, follow-up "
                "actions, and prevention. Use paragraphs plus examples and a final "
                "checklist. Do not edit files."
            ),
            workspace=workflow,
            models=common_models,
            efforts=common_effort,
        ),
        prompt(
            prompt_id="response-caveman",
            name="Caveman-inspired terse response",
            group="response-style",
            variant="caveman-terse",
            technique="terse-output-contract",
            text=(
                "Do not use tools. Terse like caveman. Technical substance exact. No "
                "pleasantries, hedging, or background unless required. Fragments OK. "
                "Create the same add-on router incident guide in max eight bullets: "
                "symptoms, triage, causes, diagnostics, mitigation, rollback, "
                "validation, follow-up. Do not edit files."
            ),
            workspace=workflow,
            models=common_models,
            efforts=common_effort,
        ),
        prompt(
            prompt_id="prompt-efficient",
            name="Efficient prompt",
            group="prompt-efficiency",
            variant="concise",
            technique="scoped-output-contract",
            text=(
                f"Using {workflow / 'README.md'} and {workflow / 'ops' / 'runbook.md'} "
                "only, return five bullets: flow, audit, notification rule, "
                "validation, rollback. Do not edit files."
            ),
            workspace=workflow,
            models=common_models,
            efforts=common_effort,
        ),
    ]

    catalog = {
        "version": 2,
        "description": "Generated token-efficiency benchmark scenarios.",
        "prompts": prompts,
    }
    catalog_path = output / "generated-prompts.json"
    catalog_path.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    return catalog_path


def main() -> int:
    """CLI entry point."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(build_catalog(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
