---
name: json-to-xml-converter
description: Convert JSON data to XML format with customizable root element and attribute handling
---

# JSON to XML Converter Skill

Use this skill when the repository itself should provide the conversion behavior and examples.

## When to use it

- transforming a local JSON sample into XML during a workshop,
- demonstrating that skills can bundle guidance plus runnable scripts,
- giving an agent a concrete, repo-scoped utility without calling an external system.

If the JSON comes from a live SaaS API or another remote system, use MCP to fetch the data first and then use this skill for the local conversion step.

## Quick usage

```bash
python .github/skills/json-to-xml-converter/scripts/json2xml.py input.json output.xml
python .github/skills/json-to-xml-converter/scripts/json2xml.py input.json output.xml --root data
echo '{"name": "test"}' | python .github/skills/json-to-xml-converter/scripts/json2xml.py - -
```

## Inputs

- `input_file`: path to a JSON file or `-` for stdin
- `output_file`: path to an XML file or `-` for stdout
- `--root`: optional root element name, default `root`

## Example

Input:

```json
{"user": {"name": "Alice", "age": 30}, "items": [1, 2, 3]}
```

Output:

```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <user>
    <name>Alice</name>
    <age>30</age>
  </user>
  <items>
    <item>1</item>
    <item>2</item>
    <item>3</item>
  </items>
</root>
```

## Notes for agents

- Prefer this skill over ad hoc conversion code when the task is local and repeatable.
- Mention that the script is standard-library only.
- Keep the boundary clear: this skill transforms data; it does not fetch live data on its own.
