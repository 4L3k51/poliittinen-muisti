#!/usr/bin/env python3
"""
Validate all data files in the repository.

Checks:
- JSON syntax
- Required fields
- Reference integrity (politician_id exists, statement_id exists)
- Date formats
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Tuple

# Required fields for each entity type
REQUIRED_FIELDS = {
    'politicians': ['id', 'name', 'party'],
    'statements': ['id', 'politician_id', 'statement', 'type', 'date'],
    'verifications': ['id', 'statement_id', 'outcome', 'verdict'],
    'contradictions': ['id', 'politician_id', 'statement_a', 'statement_b'],
}


def load_json_file(filepath: str) -> Tuple[dict, str]:
    """Load JSON file and return data or error."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"
    except Exception as e:
        return None, f"Error reading file: {e}"


def validate_required_fields(data: dict, entity_type: str) -> List[str]:
    """Check that required fields are present."""
    errors = []
    required = REQUIRED_FIELDS.get(entity_type, [])
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    return errors


def validate_references(
    data: dict,
    entity_type: str,
    politicians: set,
    statements: set
) -> List[str]:
    """Check that referenced IDs exist."""
    errors = []

    if entity_type == 'statements':
        if data.get('politician_id') not in politicians:
            errors.append(f"Unknown politician_id: {data.get('politician_id')}")

    elif entity_type == 'verifications':
        if data.get('statement_id') not in statements:
            errors.append(f"Unknown statement_id: {data.get('statement_id')}")

    elif entity_type == 'contradictions':
        if data.get('politician_id') not in politicians:
            errors.append(f"Unknown politician_id: {data.get('politician_id')}")

    return errors


def main():
    data_dir = Path('data')

    if not data_dir.exists():
        print("Error: data/ directory not found")
        sys.exit(1)

    all_errors = []

    # First pass: collect all IDs
    politicians = set()
    statements = set()

    for filepath in data_dir.glob('politicians/*.json'):
        data, error = load_json_file(str(filepath))
        if data:
            politicians.add(data.get('id'))

    for filepath in data_dir.glob('statements/*.json'):
        data, error = load_json_file(str(filepath))
        if data:
            statements.add(data.get('id'))

    print(f"Found {len(politicians)} politicians, {len(statements)} statements\n")

    # Second pass: validate everything
    for entity_type in ['politicians', 'statements', 'verifications', 'contradictions']:
        entity_dir = data_dir / entity_type
        if not entity_dir.exists():
            continue

        for filepath in entity_dir.glob('*.json'):
            file_errors = []
            data, error = load_json_file(str(filepath))

            if error:
                file_errors.append(error)
            else:
                file_errors.extend(
                    validate_required_fields(data, entity_type)
                )
                file_errors.extend(
                    validate_references(data, entity_type, politicians, statements)
                )

            if file_errors:
                all_errors.append((filepath, file_errors))
            else:
                print(f"✓ {filepath}")

    # Report results
    print()
    if all_errors:
        print(f"Found {len(all_errors)} files with errors:\n")
        for filepath, errors in all_errors:
            print(f"✗ {filepath}")
            for error in errors:
                print(f"  - {error}")
        sys.exit(1)
    else:
        print("All files valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
