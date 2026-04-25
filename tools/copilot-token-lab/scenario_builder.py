"""Create reusable token-efficiency benchmark fixtures for Copilot CLI."""

from __future__ import annotations

import argparse
import json
import shutil
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


def addon_policy_text(lines: int = 24) -> str:
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
        addon_policy_text(24),
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
    ]
    for domain in domains:
        base.extend(["", f"## {domain} policy"])
        for index in range(1, 61):
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
        addon_policy_text(24),
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
    write(
        workspace / "compressed-handoff.md",
        """
        # Compressed add-on routing handoff

        Frontend: show one compact add-on card and prevent duplicate notifications.
        Backend: calculate eligible add-ons, audit the decision, then emit one event.
        Operations: run the smoke test, check the dashboard, and roll back with the
        add-on routing feature flag.
        """,
    )
    write(
        workspace / "full-transcript.md",
        "\n\n".join(
            [
                large_doc("Turn history frontend", "Frontend decision history", 80),
                large_doc("Turn history backend", "Backend decision history", 80),
                large_doc("Turn history operations", "Operations decision history", 80),
                large_doc("Turn history unrelated billing", "Billing discussion", 80),
                large_doc("Turn history unrelated identity", "Identity discussion", 80),
            ]
        ),
    )
    return workspace


def build_mcp_configs(output: Path) -> tuple[Path, Path, Path]:
    """Create MCP workspaces and config files for wide versus discovery tests."""

    workspace = output / "mcp"
    workspace.mkdir(parents=True, exist_ok=True)
    write(workspace / "AGENTS.md", "Use MCP tools when the prompt asks for action metadata.\n")

    server = ROOT / "mcp_servers" / "token_lab_mcp.py"
    wide_config = output / "mcp-wide.json"
    discovery_config = output / "mcp-discovery.json"
    python = "python"

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
                "Read frontend.md, backend.md, and operations.md. Produce one combined "
                "implementation handoff with UI, API, operations, and validation notes. "
                "Do not edit files."
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
            text="Read only frontend.md and summarize UI requirements in three bullets.",
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
            text="Read only backend.md and summarize API requirements in three bullets.",
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
            text="Read only operations.md and summarize operational requirements in three bullets.",
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
                "Read every file in the context directory. Produce a combined handoff "
                "for only frontend, backend, and operations add-on routing concerns. "
                "Do not edit files."
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
            text="Read only context/frontend-deep.md and return three frontend handoff bullets.",
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
            text="Read only context/backend-deep.md and return three backend handoff bullets.",
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
            text="Read only context/operations-deep.md and return three operations handoff bullets.",
            workspace=large_context,
            models=["gpt-5.4-mini"],
            efforts=["low"],
        ),
        prompt(
            prompt_id="compression-full-history",
            name="No compression simulated long history",
            group="compression-simulation",
            variant="full-history",
            baseline=True,
            technique="uncompressed-history",
            text=(
                "Read full-transcript.md and return the final frontend, backend, "
                "operations, validation, and rollback decisions in five bullets. "
                "Do not edit files."
            ),
            workspace=large_context,
            models=common_models,
            efforts=common_effort,
        ),
        prompt(
            prompt_id="compression-summary",
            name="Compressed handoff summary",
            group="compression-simulation",
            variant="compressed-handoff",
            technique="compressed-context",
            text=(
                "Read compressed-handoff.md and return the final frontend, backend, "
                "operations, validation, and rollback decisions in five bullets. "
                "Do not edit files."
            ),
            workspace=large_context,
            models=common_models,
            efforts=common_effort,
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
            prompt_id="prompt-efficient",
            name="Efficient prompt",
            group="prompt-efficiency",
            variant="concise",
            technique="scoped-output-contract",
            text=(
                "Using README.md and ops/runbook.md only, return five bullets: flow, "
                "audit, notification rule, validation, rollback. Do not edit files."
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
