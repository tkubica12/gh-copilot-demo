"""Cross-platform runner for Copilot token-efficiency measurements."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import analyze_otel
import scenario_builder


ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "token-lab.toml"


@dataclass
class RunnerConfig:
    """Configuration loaded from token-lab.toml and command-line overrides."""

    backend: str
    copilot_command: str
    iterations: int
    execute: bool
    allow_all_tools: bool
    output_dir: Path
    workspace_dir: Path
    analysis_file: str
    pricing_file: Path | None
    models: list[str]
    efforts: list[str]


def load_config(path: Path) -> RunnerConfig:
    """Load runner settings from TOML."""

    data = tomllib.loads(path.read_text(encoding="utf-8"))
    backend = data.get("backend", {})
    run = data.get("run", {})
    report = data.get("report", {})
    output_dir = ROOT / run.get("output_dir", "suite-runs")
    workspace_dir = ROOT / run.get("workspace_dir", "suite-runs/scenario-workspaces")
    pricing_value = report.get("pricing_file")
    pricing_file = ROOT / pricing_value if pricing_value else None
    return RunnerConfig(
        backend=str(backend.get("name", "copilot-cli")),
        copilot_command=str(backend.get("copilot_command", "copilot")),
        iterations=int(run.get("iterations", 1)),
        execute=bool(run.get("execute", False)),
        allow_all_tools=bool(run.get("allow_all_tools", False)),
        output_dir=output_dir,
        workspace_dir=workspace_dir,
        analysis_file=str(run.get("analysis_file", "analysis.md")),
        pricing_file=pricing_file,
        models=[str(item) for item in run.get("models", ["auto"])],
        efforts=[str(item) for item in run.get("efforts", ["medium"])],
    )


def apply_overrides(config: RunnerConfig, args: argparse.Namespace) -> RunnerConfig:
    """Apply command-line overrides to loaded configuration."""

    output_dir_overridden = bool(getattr(args, "output_dir", None))
    workspace_dir_overridden = bool(getattr(args, "workspace_dir", None))
    if getattr(args, "output_dir", None):
        config.output_dir = Path(args.output_dir)
        if not config.output_dir.is_absolute():
            config.output_dir = ROOT / config.output_dir
    if getattr(args, "workspace_dir", None):
        config.workspace_dir = Path(args.workspace_dir)
        if not config.workspace_dir.is_absolute():
            config.workspace_dir = ROOT / config.workspace_dir
    elif output_dir_overridden and not workspace_dir_overridden:
        config.workspace_dir = config.output_dir / "scenario-workspaces"
    if getattr(args, "iterations", None) is not None:
        config.iterations = args.iterations
    if getattr(args, "execute", False):
        config.execute = True
    if getattr(args, "dry_run", False):
        config.execute = False
    if getattr(args, "allow_all_tools", False):
        config.allow_all_tools = True
    if getattr(args, "backend", None):
        config.backend = args.backend
    return config


def prompt_property(prompt: dict[str, Any], key: str, default: Any = None) -> Any:
    """Return a prompt property from the generated catalog."""

    return prompt[key] if key in prompt else default


def resolve_path(value: str, base: Path) -> Path:
    """Resolve a catalog path relative to the catalog location."""

    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def write_json(path: Path, value: Any) -> None:
    """Write JSON with stable formatting."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


def selected_prompts(catalog: dict[str, Any], prompt_ids: list[str]) -> list[dict[str, Any]]:
    """Filter prompt entries by id when requested."""

    prompts = list(catalog.get("prompts", []))
    if not prompt_ids:
        return prompts
    wanted = {item.lower() for item in prompt_ids}
    return [prompt for prompt in prompts if str(prompt.get("id", "")).lower() in wanted]


def build_arguments(
    prompt: dict[str, Any],
    model: str,
    effort: str,
    config: RunnerConfig,
    catalog_dir: Path,
) -> list[str]:
    """Build a Copilot CLI command for one prompt run."""

    args = [
        config.copilot_command,
        "-p",
        str(prompt["prompt"]),
        "--output-format",
        "json",
        "--stream",
        "off",
        "--mode",
        str(prompt.get("mode", "plan")),
        "--no-ask-user",
        "--log-level",
        "none",
    ]
    if model and model != "auto":
        args.extend(["--model", model])
    if effort:
        args.extend(["--reasoning-effort", effort])
    if config.allow_all_tools:
        args.append("--allow-all-tools")
    if prompt_property(prompt, "noCustomInstructions", False):
        args.append("--no-custom-instructions")
    if prompt_property(prompt, "disableBuiltinMcps", False):
        args.append("--disable-builtin-mcps")
    if "availableTools" in prompt:
        args.extend(["--available-tools", ",".join(prompt["availableTools"])])
    if "additionalMcpConfig" in prompt:
        mcp_config = resolve_path(str(prompt["additionalMcpConfig"]), catalog_dir)
        args.extend(["--additional-mcp-config", f"@{mcp_config}"])
    args.extend(str(item) for item in prompt.get("extraArgs", []))
    return args


def dry_run(run_dir: Path, stdout_path: Path, stderr_path: Path, otel_path: Path) -> int:
    """Create run files without invoking a model."""

    stdout_path.write_text("[DRY RUN] copilot command not executed\n", encoding="utf-8")
    stderr_path.write_text("", encoding="utf-8")
    otel_path.write_text("", encoding="utf-8")
    return 0


def run_copilot_cli(
    command: list[str],
    run_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    otel_path: Path,
    working_directory: Path | None,
) -> int:
    """Invoke Copilot CLI and write stdout, stderr, and OTel JSONL."""

    if not shutil.which(command[0]):
        raise FileNotFoundError(f"Copilot CLI command not found on PATH: {command[0]}")
    env = os.environ.copy()
    env["COPILOT_OTEL_FILE_EXPORTER_PATH"] = str(otel_path)
    env["COPILOT_OTEL_ENABLED"] = "true"
    env["OTEL_RESOURCE_ATTRIBUTES"] = "repo=gh-copilot-demo,experiment=copilot-token-lab"
    with stdout_path.open("w", encoding="utf-8") as stdout:
        with stderr_path.open("w", encoding="utf-8") as stderr:
            completed = subprocess.run(
                command,
                cwd=working_directory,
                env=env,
                stdout=stdout,
                stderr=stderr,
                check=False,
                text=True,
            )
    return int(completed.returncode)


def run_sdk_backend() -> None:
    """Document why a Copilot SDK backend is not implemented yet."""

    raise NotImplementedError(
        "The SDK backend is intentionally not implemented. The lab needs token "
        "telemetry, tool counts, and model metadata; Copilot CLI OpenTelemetry is "
        "the supported measured surface currently used by this repository. Add an "
        "SDK backend here when a stable Copilot SDK exposes equivalent telemetry."
    )


def run_catalog(
    catalog_path: Path,
    config: RunnerConfig,
    prompt_ids: list[str] | None = None,
) -> Path:
    """Run or dry-run all selected prompts from a generated catalog."""

    if config.backend == "sdk":
        run_sdk_backend()
    if config.backend != "copilot-cli":
        raise ValueError(f"Unsupported backend: {config.backend}")

    catalog_path = catalog_path.resolve()
    catalog_dir = catalog_path.parent
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    prompts = selected_prompts(catalog, prompt_ids or [])
    if not prompts:
        raise ValueError("No prompts selected.")

    run_root = config.output_dir / "runs"
    run_root.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for prompt in prompts:
        models = [str(item) for item in prompt.get("models", config.models)]
        efforts = [str(item) for item in prompt.get("efforts", config.efforts)]
        for model in models:
            for effort in efforts:
                for iteration in range(1, config.iterations + 1):
                    timestamp = time.strftime("%Y%m%d%H%M%S")
                    run_id = f"{prompt['id']}-{model}-{effort}-{iteration:03d}-{timestamp}"
                    run_dir = run_root / run_id
                    run_dir.mkdir(parents=True, exist_ok=True)
                    otel_path = run_dir / "copilot-otel.jsonl"
                    stdout_path = run_dir / "stdout.jsonl"
                    stderr_path = run_dir / "stderr.txt"
                    working_dir_value = prompt_property(prompt, "workingDirectory")
                    working_dir = (
                        resolve_path(str(working_dir_value), catalog_dir)
                        if working_dir_value
                        else None
                    )
                    command = build_arguments(prompt, model, effort, config, catalog_dir)
                    metadata = {
                        "runId": run_id,
                        "promptId": prompt["id"],
                        "promptName": prompt.get("name", ""),
                        "expectedTechnique": prompt.get("expectedTechnique", ""),
                        "comparisonGroup": prompt.get("comparisonGroup", ""),
                        "variant": prompt.get("variant", ""),
                        "baseline": bool(prompt.get("baseline", False)),
                        "backend": config.backend,
                        "model": model,
                        "effort": effort,
                        "mode": prompt.get("mode", "plan"),
                        "iteration": iteration,
                        "execute": config.execute,
                        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "otelPath": str(otel_path),
                        "stdoutPath": str(stdout_path),
                        "stderrPath": str(stderr_path),
                        "workingDirectory": str(working_dir) if working_dir else "",
                        "command": command,
                    }
                    write_json(run_dir / "metadata.json", metadata)
                    started = time.perf_counter()
                    if config.execute:
                        exit_code = run_copilot_cli(
                            command,
                            run_dir,
                            stdout_path,
                            stderr_path,
                            otel_path,
                            working_dir,
                        )
                    else:
                        exit_code = dry_run(run_dir, stdout_path, stderr_path, otel_path)
                    elapsed = round(time.perf_counter() - started, 3)
                    results.append(
                        {
                            "runId": run_id,
                            "promptId": prompt["id"],
                            "model": model,
                            "effort": effort,
                            "backend": config.backend,
                            "exitCode": exit_code,
                            "elapsedSeconds": elapsed,
                            "dryRun": not config.execute,
                        }
                    )

    write_json(config.output_dir / "run-summary.json", results)
    return run_root


def analyze_runs(runs_dir: Path, output: Path, pricing_file: Path | None = None) -> None:
    """Analyze run telemetry and write a Markdown report."""

    summaries = analyze_otel.summarize_runs(runs_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    analyze_otel.write_markdown(summaries, output, analyze_otel.load_pricing(pricing_file))
    print(f"Analyzed {len(summaries)} run(s). Wrote {output}")


def add_common_options(parser: argparse.ArgumentParser) -> None:
    """Add shared CLI options."""

    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--workspace-dir", type=Path)
    parser.add_argument("--iterations", type=int)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-all-tools", action="store_true")
    parser.add_argument("--backend", choices=["copilot-cli", "sdk"])


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    suite = subparsers.add_parser("suite", help="Generate fixtures, run, and analyze.")
    add_common_options(suite)
    suite.add_argument("--prompt-id", action="append", default=[])

    run = subparsers.add_parser("run", help="Run an existing generated catalog.")
    add_common_options(run)
    run.add_argument("--catalog", type=Path, required=True)
    run.add_argument("--prompt-id", action="append", default=[])

    analyze = subparsers.add_parser("analyze", help="Analyze existing run folders.")
    analyze.add_argument("--runs", type=Path, required=True)
    analyze.add_argument("--output", type=Path, required=True)
    analyze.add_argument("--pricing", type=Path)
    return parser


def main() -> int:
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args()
    if args.command == "analyze":
        analyze_runs(args.runs, args.output, args.pricing)
        return 0

    config = apply_overrides(load_config(args.config), args)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    if args.command == "suite":
        catalog_path = scenario_builder.build_catalog(config.workspace_dir)
    else:
        catalog_path = args.catalog
    runs_dir = run_catalog(catalog_path, config, args.prompt_id)
    analysis_path = config.output_dir / config.analysis_file
    analyze_runs(runs_dir, analysis_path, config.pricing_file)
    print(f"Scenario catalog: {catalog_path}")
    print(f"Analysis: {analysis_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
