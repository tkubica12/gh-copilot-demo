---
name: json-to-xml-converter
description: Convert JSON data to XML format with customizable root element and attribute handling
---

# JSON to XML Converter Skill

## Purpose

Convert JSON data structures into well-formed XML documents. Handles nested objects, arrays, and primitive types.

## Usage

### Command Line

```bash
# Basic conversion
python .github/skills/json-to-xml-converter/scripts/json2xml.py input.json output.xml

# Custom root element
python .github/skills/json-to-xml-converter/scripts/json2xml.py input.json output.xml --root "data"

# Pipe data
echo '{"name": "test"}' | python .github/skills/json-to-xml-converter/scripts/json2xml.py - -
```

### Parameters

- `input_file`: Path to JSON file or `-` for stdin
- `output_file`: Path to XML output file or `-` for stdout
- `--root`: Root element name (default: "root")

## Example

**Input JSON:**
```json
{"user": {"name": "Alice", "age": 30}, "items": [1, 2, 3]}
```

**Output XML:**
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

## Agent Integration

Use `run_in_terminal` to invoke the script:

```bash
python .github/skills/json-to-xml-converter/scripts/json2xml.py input.json output.xml --root "mydata"
```

**Important Notes:**
- No external dependencies (Python stdlib only)
- JSON keys with spaces are converted to underscores
- Arrays become `<item>` elements
- Handles invalid JSON with clear error messages
