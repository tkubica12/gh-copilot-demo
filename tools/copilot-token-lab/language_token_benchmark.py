"""Compare tokenizer costs for equivalent prompts in different languages."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import tiktoken


DEFAULT_ENCODING = "o200k_base"


@dataclass(frozen=True)
class LanguageSample:
    """One text sample to count with a tokenizer."""

    group: str
    language: str
    text: str
    note: str
    baseline: bool = False


@dataclass(frozen=True)
class TokenRow:
    """Measured tokenizer result for one language sample."""

    group: str
    language: str
    text: str
    note: str
    characters: int
    utf8_bytes: int
    tokens: int
    ratio_to_english: float


SAMPLES = [
    LanguageSample("simple sentence", "English", "I met a huge dog", "baseline", True),
    LanguageSample("simple sentence", "Czech", "Potkal jsem obrovského psa", "Czech"),
    LanguageSample(
        "terse code task",
        "English",
        "Fix auth bug. Add test. Return diff only.",
        "baseline",
        True,
    ),
    LanguageSample(
        "terse code task",
        "Czech",
        "Oprav auth chybu. Přidej test. Vrať jen diff.",
        "Czech",
    ),
    LanguageSample(
        "structured API task",
        "English",
        "POST /api/users\nValidate: name req, email req+valid\n400 errors\n201 user",
        "baseline",
        True,
    ),
    LanguageSample(
        "structured API task",
        "Czech",
        "POST /api/users\nValiduj: name pov, email pov+platny\n400 chyby\n201 user",
        "Czech structured prompt",
    ),
    LanguageSample(
        "verbose API task",
        "English",
        "Create a POST /api/users endpoint that validates required name and email, "
        "returns 400 with errors on failure, and returns 201 with the created user.",
        "baseline",
        True,
    ),
    LanguageSample(
        "verbose API task",
        "Czech",
        "Vytvoř endpoint POST /api/users, který validuje povinné name a email, "
        "při chybě vrátí 400 s detaily a při úspěchu vrátí 201 s vytvořeným uživatelem.",
        "Czech prose",
    ),
    LanguageSample(
        "handoff style",
        "Normal",
        "After implementation, summarize what changed, why the approach was chosen, "
        "which files were edited, how validation was performed, and what risks remain.",
        "baseline",
        True,
    ),
    LanguageSample(
        "handoff style",
        "Caveman",
        "Impl done. Say: changed files, why, validation, risks. No intro. No recap. "
        "Five bullets max.",
        "human-readable terse output",
    ),
    LanguageSample(
        "handoff style",
        "Wenyan",
        "done -> files | why | checks | risks. no intro. <=5 bullets.",
        "machine-oriented handoff",
    ),
]


def count_tokens(text: str, encoding_name: str = DEFAULT_ENCODING) -> int:
    """Return tokenizer token count for text."""

    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def build_rows(encoding_name: str = DEFAULT_ENCODING) -> list[TokenRow]:
    """Build measured rows and ratios relative to each group's English baseline."""

    baseline_tokens: dict[str, int] = {}
    counted: list[tuple[LanguageSample, int]] = []
    for sample in SAMPLES:
        tokens = count_tokens(sample.text, encoding_name)
        counted.append((sample, tokens))
        if sample.baseline:
            baseline_tokens[sample.group] = tokens

    rows: list[TokenRow] = []
    for sample, tokens in counted:
        baseline = baseline_tokens[sample.group]
        rows.append(
            TokenRow(
                group=sample.group,
                language=sample.language,
                text=sample.text,
                note=sample.note,
                characters=len(sample.text),
                utf8_bytes=len(sample.text.encode("utf-8")),
                tokens=tokens,
                ratio_to_english=tokens / baseline,
            )
        )
    return rows


def write_markdown(rows: list[TokenRow], output: Path, encoding_name: str) -> None:
    """Write a Markdown report for tokenizer results."""

    lines = [
        "# Language tokenizer benchmark",
        "",
        f"Encoding: `{encoding_name}`. This is a tokenizer-only micro-benchmark, "
        "not Copilot OpenTelemetry. It demonstrates that fewer characters do not "
        "necessarily mean fewer tokens.",
        "",
        "| Group | Language | Text | Chars | UTF-8 bytes | Tokens | vs English | Note |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        text = row.text.replace("\n", "<br>")
        lines.append(
            "| {group} | {language} | `{text}` | {chars} | {bytes} | {tokens} | "
            "{ratio:.2f}x | {note} |".format(
                group=row.group,
                language=row.language,
                text=text,
                chars=row.characters,
                bytes=row.utf8_bytes,
                tokens=row.tokens,
                ratio=row.ratio_to_english,
                note=row.note,
            )
        )

    lines.extend(
        [
            "",
            "## Takeaways",
            "",
            "1. Prefer terse English for prompts and instructions unless the task "
            "specifically requires Czech.",
            "2. Czech is understandable to the model, but the benchmark should measure "
            "token cost instead of assuming character count predicts cost.",
            "3. Structured prompts often matter more than language choice.",
            "4. Caveman-style output can be useful when a human still reads the "
            "response; more extreme handoff styles are better reserved for agent-to-agent "
            "or durable context.",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """CLI entry point."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--encoding", default=DEFAULT_ENCODING)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports") / "language-token-benchmark.md",
    )
    args = parser.parse_args()

    rows = build_rows(args.encoding)
    write_markdown(rows, args.output, args.encoding)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
