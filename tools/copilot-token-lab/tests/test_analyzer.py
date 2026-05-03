"""Unit tests for the OTel analyzer."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from module_loader import ROOT, load_module


analyze_otel = load_module("analyze_otel", "analyze_otel.py")


class AnalyzeOtelTests(unittest.TestCase):
    """Tests for sample telemetry aggregation."""

    def test_sample_runs_show_scoped_prompt_uses_fewer_tokens(self) -> None:
        """Sample telemetry compares broad and scoped prompt styles."""

        runs = analyze_otel.summarize_runs(ROOT / "tests" / "sample-runs")
        by_prompt = {run.prompt_id: run for run in runs}

        self.assertEqual(by_prompt["broad-repo-summary"].total_tokens, 10800)
        self.assertEqual(by_prompt["scoped-file-discovery"].total_tokens, 1540)
        self.assertLess(
            by_prompt["scoped-file-discovery"].total_tokens,
            by_prompt["broad-repo-summary"].total_tokens,
        )
        self.assertEqual(by_prompt["broad-repo-summary"].tool_call_count, 2)
        self.assertEqual(by_prompt["scoped-file-discovery"].tool_call_count, 1)

    def test_markdown_report_contains_expected_columns(self) -> None:
        """Markdown output is stable enough for workshop sharing."""

        runs = analyze_otel.summarize_runs(ROOT / "tests" / "sample-runs")
        output = ROOT / "tests" / "sample-analysis.md"

        analyze_otel.write_markdown(runs, output)

        text = output.read_text(encoding="utf-8")
        self.assertIn("| Run | Group | Variant | Prompt | Technique | Model |", text)
        self.assertIn("baseline-broad-context", text)
        self.assertIn("scoped-context-first", text)

    def test_markdown_report_can_include_weighted_cost_units(self) -> None:
        """Pricing TOML adds weighted columns without changing token parsing."""

        runs = analyze_otel.summarize_runs(ROOT / "tests" / "sample-runs")
        pricing = analyze_otel.load_pricing(ROOT / "model-pricing.toml")
        output = ROOT / "tests" / "sample-analysis.md"

        analyze_otel.write_markdown(runs, output, pricing)

        text = output.read_text(encoding="utf-8")
        self.assertIn("Weighted units", text)
        self.assertIn("Estimated cost", text)
        self.assertIn("99250", text)
        self.assertIn("0.099250", text)

    def test_multiturn_otel_paths_sum_all_turn_tokens(self) -> None:
        """Multi-turn runs sum each OTel file without dropping later turns."""

        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir) / "multi-turn"
            run_dir.mkdir()
            metadata = {
                "runId": "multi-turn",
                "promptId": "multi-turn",
                "model": "gpt-5.5",
                "otelPaths": [
                    str(run_dir / "copilot-otel-turn-01.jsonl"),
                    str(run_dir / "copilot-otel-turn-02.jsonl"),
                ],
            }
            (run_dir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
            for index, input_tokens in enumerate((100, 200), start=1):
                record = {
                    "resourceSpans": [
                        {
                            "scopeSpans": [
                                {
                                    "spans": [
                                        {
                                            "name": "chat",
                                            "attributes": [
                                                {
                                                    "key": "gen_ai.response.model",
                                                    "value": {"stringValue": "gpt-5.5"},
                                                },
                                                {
                                                    "key": "gen_ai.usage.input_tokens",
                                                    "value": {"intValue": str(input_tokens)},
                                                },
                                                {
                                                    "key": "gen_ai.usage.output_tokens",
                                                    "value": {"intValue": str(index)},
                                                },
                                                {
                                                    "key": "gen_ai.usage.cache_read.input_tokens",
                                                    "value": {"intValue": str(index * 10)},
                                                },
                                            ],
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
                (run_dir / f"copilot-otel-turn-{index:02d}.jsonl").write_text(
                    json.dumps(record) + "\n",
                    encoding="utf-8",
                )

            summary = analyze_otel.summarize_run(run_dir)

            self.assertEqual(summary.input_tokens, 300)
            self.assertEqual(summary.output_tokens, 3)
            self.assertEqual(summary.cache_read_input_tokens, 30)

    def test_grouped_report_includes_output_savings(self) -> None:
        """Grouped comparisons show output savings separately from total savings."""

        runs = [
            analyze_otel.RunSummary(
                run_id="normal",
                prompt_id="response-normal",
                comparison_group="response-style",
                variant="normal",
                baseline=True,
                requested_model="gpt-5.5",
                input_tokens=1000,
                output_tokens=1000,
            ),
            analyze_otel.RunSummary(
                run_id="terse",
                prompt_id="response-caveman",
                comparison_group="response-style",
                variant="caveman-terse",
                requested_model="gpt-5.5",
                input_tokens=1000,
                output_tokens=250,
            ),
        ]
        output = ROOT / "tests" / "sample-analysis.md"

        analyze_otel.write_markdown(runs, output)

        text = output.read_text(encoding="utf-8")
        self.assertIn("Output savings vs baseline", text)
        self.assertIn("| response-style | caveman-terse |  |  | 1250 | 37.5% |", text)
        self.assertIn("| 1000 | 250 | 75.0% |", text)
