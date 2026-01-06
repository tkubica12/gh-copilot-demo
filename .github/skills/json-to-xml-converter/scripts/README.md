# JSON to XML Converter

A simple Python-based skill for converting JSON data to XML format.

## Quick Start

### Using the Script Directly

```bash
# Convert a JSON file to XML
python scripts/json2xml.py input.json output.xml

# Use custom root element
python scripts/json2xml.py input.json output.xml --root "mydata"

# Pipe data
echo '{"name": "test", "value": 123}' | python scripts/json2xml.py - -
```

### Using with uv (Optional)

```bash
# Create virtual environment and install (if needed)
uv sync

# Run tests
uv run pytest
```

## Features

- ✓ No external dependencies (uses Python stdlib only)
- ✓ Handles nested JSON objects
- ✓ Supports arrays and primitive types
- ✓ Pretty-printed XML output
- ✓ Customizable root element
- ✓ CLI and Python API

## Examples

See [SKILL.md](SKILL.md) for detailed usage examples and documentation.

## Testing

Create a sample JSON file:

```bash
echo '{"user": {"name": "Alice", "age": 30}, "items": [1, 2, 3]}' > sample.json
python scripts/json2xml.py sample.json output.xml
cat output.xml
```

Expected output:
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

## License

Part of the gh-copilot-demo project.
