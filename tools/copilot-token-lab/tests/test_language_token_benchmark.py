"""Unit tests for the language tokenizer benchmark."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from module_loader import load_module


language_token_benchmark = load_module(
    "language_token_benchmark", "language_token_benchmark.py"
)


class LanguageTokenBenchmarkTests(unittest.TestCase):
    """Tests for tokenizer-only language benchmark output."""

    def test_build_rows_includes_expected_groups_and_ratios(self) -> None:
        """Rows include language and technical prompt groups with English baselines."""

        rows = language_token_benchmark.build_rows()
        by_key = {(row.group, row.language): row for row in rows}

        self.assertIn(("simple sentence", "English"), by_key)
        self.assertIn(("simple sentence", "Czech"), by_key)
        self.assertIn(("structured API task", "English"), by_key)
        self.assertIn(("handoff style", "Normal"), by_key)
        self.assertIn(("handoff style", "Caveman"), by_key)
        self.assertIn(("handoff style", "Wenyan"), by_key)
        self.assertEqual(by_key[("simple sentence", "English")].ratio_to_english, 1.0)
        self.assertGreater(by_key[("simple sentence", "Czech")].tokens, 0)
        self.assertLess(
            by_key[("handoff style", "Caveman")].tokens,
            by_key[("handoff style", "Normal")].tokens,
        )
        self.assertLess(
            by_key[("handoff style", "Wenyan")].tokens,
            by_key[("handoff style", "Caveman")].tokens,
        )

    def test_markdown_report_is_written(self) -> None:
        """Markdown output is suitable for linking from the token lab docs."""

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "language.md"
            rows = language_token_benchmark.build_rows()

            language_token_benchmark.write_markdown(
                rows, output, language_token_benchmark.DEFAULT_ENCODING
            )

            text = output.read_text(encoding="utf-8")
            self.assertIn("# Language tokenizer benchmark", text)
            self.assertIn("vs English", text)
            self.assertIn("Czech", text)
            self.assertIn("Caveman", text)
            self.assertIn("Wenyan", text)
