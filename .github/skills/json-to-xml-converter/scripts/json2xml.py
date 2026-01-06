#!/usr/bin/env python3
"""
JSON to XML Converter

Converts JSON data structures to well-formed XML documents.
Handles nested objects, arrays, and primitive types.
"""

import json
import sys
import argparse
import xml.etree.ElementTree as ET
from typing import Any, Optional
from pathlib import Path


def sanitize_tag_name(name: str) -> str:
    """
    Sanitize a string to be a valid XML tag name.
    
    Args:
        name: The string to sanitize
        
    Returns:
        A valid XML tag name
    """
    # Replace spaces and invalid characters with underscores
    sanitized = name.replace(' ', '_')
    sanitized = ''.join(c if c.isalnum() or c in ('_', '-', '.') else '_' for c in sanitized)
    
    # Ensure it doesn't start with a digit
    if sanitized and sanitized[0].isdigit():
        sanitized = '_' + sanitized
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = 'item'
    
    return sanitized


def dict_to_xml(data: Any, parent: Optional[ET.Element] = None, tag_name: str = 'item') -> ET.Element:
    """
    Convert a dictionary or other data structure to XML elements.
    
    Args:
        data: The data to convert (dict, list, or primitive)
        parent: The parent XML element (None for root)
        tag_name: The tag name to use for this element
        
    Returns:
        An XML Element
    """
    if parent is None:
        element = ET.Element(sanitize_tag_name(tag_name))
    else:
        element = ET.SubElement(parent, sanitize_tag_name(tag_name))
    
    if isinstance(data, dict):
        # Handle dictionary - create child elements for each key
        for key, value in data.items():
            dict_to_xml(value, element, key)
    elif isinstance(data, list):
        # Handle list - create 'item' elements for each entry
        for item in data:
            dict_to_xml(item, element, 'item')
    elif data is None:
        # Handle null values
        element.text = ''
    else:
        # Handle primitive types (str, int, float, bool)
        element.text = str(data)
    
    return element


def convert_json_to_xml(json_str: str, root_name: str = 'root') -> str:
    """
    Convert a JSON string to an XML string.
    
    Args:
        json_str: The JSON string to convert
        root_name: The name of the root XML element
        
    Returns:
        A formatted XML string
        
    Raises:
        json.JSONDecodeError: If the JSON is invalid
    """
    data = json.loads(json_str)
    root = dict_to_xml(data, tag_name=root_name)
    
    # Pretty print the XML
    indent_xml(root)
    
    # Convert to string with XML declaration
    xml_str = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
    
    return xml_str


def indent_xml(elem: ET.Element, level: int = 0) -> None:
    """
    Add indentation to XML elements for pretty printing.
    
    Args:
        elem: The XML element to indent
        level: The current indentation level
    """
    indent = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent


def json_file_to_xml_file(input_path: str, output_path: str, root_name: str = 'root') -> None:
    """
    Convert a JSON file to an XML file.
    
    Args:
        input_path: Path to input JSON file (or '-' for stdin)
        output_path: Path to output XML file (or '-' for stdout)
        root_name: The name of the root XML element
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        json.JSONDecodeError: If the JSON is invalid
    """
    # Read input
    if input_path == '-':
        json_str = sys.stdin.read()
    else:
        with open(input_path, 'r', encoding='utf-8') as f:
            json_str = f.read()
    
    # Convert
    xml_str = convert_json_to_xml(json_str, root_name)
    
    # Write output
    if output_path == '-':
        sys.stdout.write(xml_str)
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)


def main() -> int:
    """
    Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description='Convert JSON files to XML format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.json output.xml
  %(prog)s input.json output.xml --root data
  echo '{"name": "test"}' | %(prog)s - -
  %(prog)s - - < input.json > output.xml
        """
    )
    
    parser.add_argument(
        'input',
        help='Input JSON file (use "-" for stdin)'
    )
    parser.add_argument(
        'output',
        help='Output XML file (use "-" for stdout)'
    )
    parser.add_argument(
        '--root',
        default='root',
        help='Name of the root XML element (default: root)'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        json_file_to_xml_file(args.input, args.output, args.root)
        
        # Print success message if not using stdout
        if args.output != '-':
            print(f"✓ Successfully converted {args.input} to {args.output}", file=sys.stderr)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: Input file not found: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
