"""Unit tests for the cross-platform token lab runner."""

from __future__ import annotations

import json
import argparse
import tempfile
import unittest
from pathlib import Path

from module_loader import ROOT, load_module


run_token_lab = load_module("run_token_lab", "run_token_lab.py")


class RunnerTests(unittest.TestCase):
    """Tests for configuration and dry-run behavior."""

    def test_loads_toml_config(self) -> None:
        """The runner reads defaults from token-lab.toml."""

        config = run_token_lab.load_config(ROOT / "token-lab.toml")

        self.assertEqual(config.backend, "copilot-cli")
        self.assertEqual(config.iterations, 1)
        self.assertFalse(config.execute)
        self.assertEqual(config.pricing_file, ROOT / "model-pricing.toml")

    def test_output_override_moves_default_workspace_under_output(self) -> None:
        """Suite output overrides keep generated fixtures with the run output."""

        config = run_token_lab.load_config(ROOT / "token-lab.toml")
        args = argparse.Namespace(
            output_dir=Path("custom-output"),
            workspace_dir=None,
            iterations=None,
            execute=False,
            dry_run=False,
            allow_all_tools=False,
            backend=None,
        )

        updated = run_token_lab.apply_overrides(config, args)

        self.assertEqual(updated.workspace_dir, updated.output_dir / "scenario-workspaces")

    def test_dry_run_catalog_writes_metadata_and_analysis(self) -> None:
        """Dry runs create reproducible output without calling Copilot."""

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            catalog_path = root / "catalog.json"
            workspace = root / "workspace"
            workspace.mkdir()
            (workspace / "README.md").write_text("# Fixture\n", encoding="utf-8")
            catalog_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "prompts": [
                            {
                                "id": "dry-run-example",
                                "name": "Dry run example",
                                "mode": "plan",
                                "expectedTechnique": "dry-run",
                                "comparisonGroup": "dry-run",
                                "variant": "baseline",
                                "baseline": True,
                                "prompt": "Return ok. Do not edit files.",
                                "workingDirectory": str(workspace),
                                "models": ["gpt-5.5"],
                                "efforts": ["medium"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            config = run_token_lab.load_config(ROOT / "token-lab.toml")
            config.output_dir = root / "out"
            config.execute = False

            runs_dir = run_token_lab.run_catalog(catalog_path, config)
            analysis_path = config.output_dir / "analysis.md"
            run_token_lab.analyze_runs(runs_dir, analysis_path)

            metadata_files = list(runs_dir.glob("*/metadata.json"))
            self.assertEqual(len(metadata_files), 1)
            metadata = json.loads(metadata_files[0].read_text(encoding="utf-8"))
            self.assertEqual(metadata["backend"], "copilot-cli")
            self.assertFalse(metadata["execute"])
            self.assertTrue(analysis_path.exists())
