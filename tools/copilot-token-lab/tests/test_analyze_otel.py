"""Unit tests for the Copilot token lab analyzer."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analyze_otel.py"
spec = importlib.util.spec_from_file_location("analyze_otel", MODULE_PATH)
assert spec and spec.loader
analyze_otel = importlib.util.module_from_spec(spec)
sys.modules["analyze_otel"] = analyze_otel
spec.loader.exec_module(analyze_otel)

SCENARIO_PATH = ROOT / "scenario_builder.py"
scenario_spec = importlib.util.spec_from_file_location("scenario_builder", SCENARIO_PATH)
assert scenario_spec and scenario_spec.loader
scenario_builder = importlib.util.module_from_spec(scenario_spec)
sys.modules["scenario_builder"] = scenario_builder
scenario_spec.loader.exec_module(scenario_builder)


class AnalyzeOtelTests(unittest.TestCase):
    """Tests for sample telemetry aggregation."""

    def test_sample_runs_show_scoped_prompt_uses_fewer_tokens(self) -> None:
        """Sample telemetry proves the analyzer can compare broad and scoped runs."""

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

    def test_scenario_builder_creates_required_comparisons(self) -> None:
        """Generated scenario catalog covers the requested benchmark families."""

        with tempfile.TemporaryDirectory() as temp_dir:
            catalog_path = scenario_builder.build_catalog(Path(temp_dir))

            catalog = catalog_path.read_text(encoding="utf-8")
            self.assertIn("agents-context", catalog)
            self.assertIn("mcp-discovery", catalog)
            self.assertIn("workflow-overhead", catalog)
            self.assertIn("workflow-large-shards", catalog)
            self.assertIn("compression-simulation", catalog)
            self.assertIn("prompt-efficiency", catalog)
