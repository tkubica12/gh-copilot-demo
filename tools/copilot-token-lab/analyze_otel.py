"""Analyze GitHub Copilot OpenTelemetry JSONL runs.

The parser is intentionally tolerant: Copilot CLI and VS Code OTel file
exporters can evolve, so the analyzer searches recursively for common GenAI
semantic-convention attributes instead of depending on one exact JSON shape.
"""

from __future__ import annotations

import argparse
import json
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


TOKEN_KEYS = {
    "gen_ai.usage.input_tokens": "input_tokens",
    "gen_ai.usage.output_tokens": "output_tokens",
    "gen_ai.usage.cache_read.input_tokens": "cache_read_input_tokens",
    "gen_ai.usage.cache_creation.input_tokens": "cache_creation_input_tokens",
}

MODEL_KEYS = ("gen_ai.response.model", "gen_ai.request.model")
BASELINE_HINTS = ("baseline", "large", "wide", "single", "verbose", "gpt-5.4")


@dataclass
class RunSummary:
    """Aggregated token and latency data for one run directory."""

    run_id: str
    prompt_id: str = ""
    technique: str = ""
    comparison_group: str = ""
    variant: str = ""
    baseline: bool = False
    requested_model: str = ""
    effort: str = ""
    resolved_models: set[str] = field(default_factory=set)
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    turn_count: int = 0
    tool_call_count: int = 0
    span_count: int = 0
    errors: int = 0
    duration_ms: float = 0.0

    @property
    def total_tokens(self) -> int:
        """Return all directly observed token counters."""

        return (
            self.input_tokens
            + self.output_tokens
            + self.cache_read_input_tokens
            + self.cache_creation_input_tokens
        )

    @property
    def variant_label(self) -> str:
        """Return the display label used for grouped comparisons."""

        if self.variant and self.variant != "selected-model":
            return self.variant
        return self.requested_model or "default"

    def model_label(self) -> str:
        """Return the model label for display and pricing lookup."""

        if len(self.resolved_models) == 1:
            return next(iter(self.resolved_models))
        return self.requested_model or "unknown"

    def estimated_cost_units(self, pricing: dict[str, dict[str, float]] | None) -> float | None:
        """Estimate relative cost units from token counters and model pricing."""

        if not pricing:
            return None
        model_pricing = pricing.get(self.model_label()) or pricing.get(self.requested_model)
        if not model_pricing:
            return None
        return (
            self.input_tokens * model_pricing.get("input", 0.0)
            + self.output_tokens * model_pricing.get("output", 0.0)
            + self.cache_read_input_tokens * model_pricing.get("cache_read", 0.0)
            + self.cache_creation_input_tokens * model_pricing.get("cache_creation", 0.0)
        ) / 1_000_000


def decode_otel_value(value: Any) -> Any:
    """Decode OpenTelemetry JSON value wrappers into native Python values."""

    if not isinstance(value, dict):
        return value
    for key in (
        "stringValue",
        "intValue",
        "doubleValue",
        "boolValue",
        "bytesValue",
    ):
        if key in value:
            raw = value[key]
            if key == "intValue":
                return int(raw)
            if key == "doubleValue":
                return float(raw)
            return raw
    if "arrayValue" in value:
        values = value["arrayValue"].get("values", [])
        return [decode_otel_value(item) for item in values]
    if "kvlistValue" in value:
        return attributes_to_dict(value["kvlistValue"].get("values", []))
    return value


def attributes_to_dict(attributes: Any) -> dict[str, Any]:
    """Normalize OTel attributes from list or dictionary form."""

    if isinstance(attributes, dict):
        return {str(key): decode_otel_value(value) for key, value in attributes.items()}
    if not isinstance(attributes, list):
        return {}

    result: dict[str, Any] = {}
    for item in attributes:
        if not isinstance(item, dict) or "key" not in item:
            continue
        result[str(item["key"])] = decode_otel_value(item.get("value"))
    return result


def walk_objects(value: Any) -> Iterable[dict[str, Any]]:
    """Yield every dictionary in a JSON-like object tree."""

    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_objects(child)


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    """Read newline-delimited JSON while ignoring blank lines."""

    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in {path}:{line_number}: {exc}") from exc
            if isinstance(parsed, dict):
                yield parsed


def duration_from_object(obj: dict[str, Any]) -> float:
    """Return span duration in milliseconds when timestamp fields are available."""

    start = obj.get("startTimeUnixNano") or obj.get("start_time_unix_nano")
    end = obj.get("endTimeUnixNano") or obj.get("end_time_unix_nano")
    if start is None or end is None:
        start = obj.get("startTime")
        end = obj.get("endTime")
        if isinstance(start, list) and isinstance(end, list) and len(start) == 2 and len(end) == 2:
            try:
                start_ns = int(start[0]) * 1_000_000_000 + int(start[1])
                end_ns = int(end[0]) * 1_000_000_000 + int(end[1])
                return max((end_ns - start_ns) / 1_000_000, 0.0)
            except (TypeError, ValueError):
                return 0.0
    if start is None or end is None:
        return 0.0
    try:
        return max((int(end) - int(start)) / 1_000_000, 0.0)
    except (TypeError, ValueError):
        return 0.0


def load_metadata(run_dir: Path) -> dict[str, Any]:
    """Load optional run metadata written by the token lab runner."""

    metadata_path = run_dir / "metadata.json"
    if not metadata_path.exists():
        return {}
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def summarize_run(run_dir: Path) -> RunSummary:
    """Summarize one run directory containing Copilot OTel JSONL."""

    metadata = load_metadata(run_dir)
    summary = RunSummary(
        run_id=metadata.get("runId", run_dir.name),
        prompt_id=metadata.get("promptId", ""),
        technique=metadata.get("expectedTechnique", ""),
        comparison_group=metadata.get("comparisonGroup", ""),
        variant=metadata.get("variant", ""),
        baseline=bool(metadata.get("baseline", False)),
        requested_model=metadata.get("model", ""),
        effort=metadata.get("effort", ""),
    )

    otel_value = metadata.get("otelPath")
    if otel_value:
        otel_path = Path(otel_value)
        if not otel_path.is_absolute():
            cwd_relative = Path.cwd() / otel_path
            run_relative = run_dir / otel_path
            if cwd_relative.exists():
                otel_path = cwd_relative
            elif run_relative.exists():
                otel_path = run_relative
            else:
                otel_path = run_dir / otel_path.name
    else:
        otel_path = run_dir / "copilot-otel.jsonl"

    seen_token_objects: set[int] = set()
    for record in read_jsonl(otel_path):
        for obj in walk_objects(record):
            attributes = attributes_to_dict(obj.get("attributes", {}))
            if attributes:
                is_span = (
                    obj.get("type") == "span"
                    or "spanId" in obj
                    or "span_id" in obj
                    or (
                        isinstance(obj.get("name"), str)
                        and (
                            obj["name"].startswith("chat")
                            or obj["name"].startswith("execute_tool")
                            or obj["name"] == "invoke_agent"
                        )
                    )
                )
                if is_span:
                    summary.span_count += 1
                    summary.duration_ms = max(summary.duration_ms, duration_from_object(obj))
                for source_key, target_field in TOKEN_KEYS.items():
                    value = attributes.get(source_key)
                    if isinstance(value, (int, float)):
                        object_key = id(obj) ^ hash(source_key)
                        if object_key not in seen_token_objects:
                            setattr(
                                summary,
                                target_field,
                                getattr(summary, target_field) + int(value),
                            )
                            seen_token_objects.add(object_key)
                for model_key in MODEL_KEYS:
                    value = attributes.get(model_key)
                    if value:
                        summary.resolved_models.add(str(value))
                if isinstance(attributes.get("github.copilot.turn_count"), (int, float)):
                    summary.turn_count = max(
                        summary.turn_count, int(attributes["github.copilot.turn_count"])
                    )
                tool_name = attributes.get("gen_ai.tool.name") or attributes.get(
                    "github.copilot.tool.name"
                )
                operation_name = attributes.get("gen_ai.operation.name", "")
                span_name = str(obj.get("name", ""))
                if tool_name and is_span and (
                    operation_name == "execute_tool" or span_name.startswith("execute_tool")
                ):
                    summary.tool_call_count += 1
                if attributes.get("error.type") or attributes.get("error.message"):
                    summary.errors += 1

            metric_name = obj.get("name")
            if metric_name == "gen_ai.client.token.usage":
                data_points = obj.get("dataPoints") or obj.get("data_points") or []
                for point in data_points:
                    point_attrs = attributes_to_dict(point.get("attributes", {}))
                    token_type = point_attrs.get("gen_ai.token.type") or point_attrs.get("type")
                    value = point.get("sum") or point.get("value") or point.get("asInt")
                    if not isinstance(value, (int, float)):
                        continue
                    if token_type == "input":
                        summary.input_tokens += int(value)
                    elif token_type == "output":
                        summary.output_tokens += int(value)

    return summary


def summarize_runs(runs_dir: Path) -> list[RunSummary]:
    """Summarize all child run directories."""

    return [
        summarize_run(path)
        for path in sorted(runs_dir.iterdir())
        if path.is_dir() and (path / "metadata.json").exists()
    ]


def load_pricing(path: Path | None) -> dict[str, dict[str, float]] | None:
    """Load optional relative model pricing from TOML."""

    if path is None:
        return None
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    models = data.get("models", {})
    return {
        str(model): {str(key): float(value) for key, value in values.items()}
        for model, values in models.items()
    }


def write_markdown(
    summaries: list[RunSummary],
    output: Path,
    pricing: dict[str, dict[str, float]] | None = None,
) -> None:
    """Write a Markdown comparison report."""

    lines = [
        "# Copilot token lab analysis",
        "",
        "| Run | Group | Variant | Prompt | Technique | Model | Effort | Input | "
        "Output | Cache read | Cache create | Total | Cost units | Turns | Tools | "
        "Duration ms | Errors |",
        "| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | "
        "---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in summaries:
        model = ", ".join(sorted(item.resolved_models)) or item.requested_model or "unknown"
        cost = item.estimated_cost_units(pricing)
        cost_text = "" if cost is None else f"{cost:.6f}"
        lines.append(
            (
                "| {run} | {group} | {variant} | {prompt} | {technique} | {model} | "
                "{effort} | {input} | {output} | {cache_read} | {cache_create} | "
                "{total} | {cost} | {turns} | {tools} | {duration:.1f} | {errors} |"
            ).format(
                run=item.run_id,
                group=item.comparison_group,
                variant=item.variant_label,
                prompt=item.prompt_id,
                technique=item.technique,
                model=model,
                effort=item.effort,
                input=item.input_tokens,
                output=item.output_tokens,
                cache_read=item.cache_read_input_tokens,
                cache_create=item.cache_creation_input_tokens,
                total=item.total_tokens,
                cost=cost_text,
                turns=item.turn_count,
                tools=item.tool_call_count,
                duration=item.duration_ms,
                errors=item.errors,
            )
        )

    grouped: dict[tuple[str, str], RunSummary] = {}
    for item in summaries:
        if not item.comparison_group:
            continue
        variant = item.variant_label
        key = (item.comparison_group, variant)
        if key not in grouped:
            grouped[key] = RunSummary(
                run_id="aggregate",
                prompt_id=variant,
                technique=item.technique,
                comparison_group=item.comparison_group,
                variant=variant,
                baseline=item.baseline,
                requested_model=item.requested_model,
                effort=item.effort,
            )
        aggregate = grouped[key]
        aggregate.resolved_models.update(item.resolved_models)
        aggregate.input_tokens += item.input_tokens
        aggregate.output_tokens += item.output_tokens
        aggregate.cache_read_input_tokens += item.cache_read_input_tokens
        aggregate.cache_creation_input_tokens += item.cache_creation_input_tokens
        aggregate.turn_count += item.turn_count
        aggregate.tool_call_count += item.tool_call_count
        aggregate.duration_ms += item.duration_ms
        aggregate.errors += item.errors

    if grouped:
        lines.extend(
            [
                "",
                "## Comparison groups",
                "",
                "| Group | Variant | Total observed tokens | Savings vs baseline | "
                "Output tokens | Output savings vs baseline | Cost units | "
                "Cost savings vs baseline | Turns | Tools | Duration ms | Errors |",
                "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        baseline_by_group: dict[str, int] = {}
        baseline_output_by_group: dict[str, int] = {}
        baseline_cost_by_group: dict[str, float | None] = {}
        for (group, variant), item in grouped.items():
            is_hint = any(hint in variant.lower() for hint in BASELINE_HINTS)
            if item.baseline or (group not in baseline_by_group and is_hint):
                baseline_by_group[group] = item.total_tokens
                baseline_output_by_group[group] = item.output_tokens
                baseline_cost_by_group[group] = item.estimated_cost_units(pricing)
        for (group, _variant), item in grouped.items():
            baseline_by_group.setdefault(group, item.total_tokens)
            baseline_output_by_group.setdefault(group, item.output_tokens)
            baseline_cost_by_group.setdefault(group, item.estimated_cost_units(pricing))
        for (group, variant), item in grouped.items():
            baseline = baseline_by_group[group]
            savings = 0.0
            if baseline > 0:
                savings = (baseline - item.total_tokens) / baseline * 100
            baseline_output = baseline_output_by_group[group]
            output_savings = 0.0
            if baseline_output > 0:
                output_savings = (baseline_output - item.output_tokens) / baseline_output * 100
            cost = item.estimated_cost_units(pricing)
            baseline_cost = baseline_cost_by_group[group]
            cost_savings = None
            if baseline_cost and cost is not None:
                cost_savings = (baseline_cost - cost) / baseline_cost * 100
            lines.append(
                "| {group} | {variant} | {total} | {savings:.1f}% | {output} | "
                "{output_savings:.1f}% | {cost} | {cost_savings} | {turns} | "
                "{tools} | {duration:.1f} | {errors} |".format(
                    group=group,
                    variant=variant,
                    total=item.total_tokens,
                    savings=savings,
                    output=item.output_tokens,
                    output_savings=output_savings,
                    cost="" if cost is None else f"{cost:.6f}",
                    cost_savings="" if cost_savings is None else f"{cost_savings:.1f}%",
                    turns=item.turn_count,
                    tools=item.tool_call_count,
                    duration=item.duration_ms,
                    errors=item.errors,
                )
            )

    lines.extend(
        [
            "",
            "## Interpretation checklist",
            "",
            "1. Compare total tokens only between runs with the same Copilot client "
            "version and repository state.",
            "2. Treat lower tokens as a win only when task quality remains acceptable.",
            "3. Inspect tool counts and errors before concluding a prompt is efficient.",
            "4. Cost units are relative estimates when model-pricing.toml is supplied.",
            "5. Keep content capture disabled unless the environment is trusted.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """CLI entry point."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--runs",
        type=Path,
        required=True,
        help="Directory containing run folders.",
    )
    parser.add_argument("--output", type=Path, required=True, help="Markdown report path.")
    parser.add_argument("--pricing", type=Path, help="Optional relative model pricing TOML.")
    args = parser.parse_args()

    summaries = summarize_runs(args.runs)
    write_markdown(summaries, args.output, load_pricing(args.pricing))
    print(f"Analyzed {len(summaries)} run(s). Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
