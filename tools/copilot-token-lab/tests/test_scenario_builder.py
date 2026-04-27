"""Unit tests for generated benchmark scenarios."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from module_loader import load_module


scenario_builder = load_module("scenario_builder", "scenario_builder.py")


class ScenarioBuilderTests(unittest.TestCase):
    """Tests for scenario catalog generation."""

    def test_scenario_builder_creates_required_comparisons(self) -> None:
        """Generated catalog covers the benchmark families used in the lecture."""

        with tempfile.TemporaryDirectory() as temp_dir:
            catalog_path = scenario_builder.build_catalog(Path(temp_dir))

            catalog = catalog_path.read_text(encoding="utf-8")
            self.assertIn("agents-context", catalog)
            self.assertIn("mcp-discovery", catalog)
            self.assertIn("workflow-overhead", catalog)
            self.assertIn("workflow-large-shards", catalog)
            self.assertIn("compression-simulation", catalog)
            self.assertIn("prompt-efficiency", catalog)
            self.assertIn("response-style", catalog)
