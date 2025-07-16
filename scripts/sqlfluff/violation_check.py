#!/usr/bin/env python3
"""
Violation Checker
Checks if SQLFluff found any violations and exits accordingly.
"""

import json
import sys
from typing import List, Dict, Any


def format_sqlfluff_results(results: List[Dict[str, Any]]) -> str:
    """
    Format SQLFluff JSON results into human-readable string.
    
    Args:
        results: List of SQLFluff JSON results
        
    Returns:
        Human-readable formatted string
    """
    if not results:
        return "✓ No SQLFluff violations found."

    output_lines = []

    for result in results:
        filepath = result.get('filepath', 'Unknown file')
        violations = result.get('violations', [])

        output_lines.append(f"✗ {filepath}: {len(violations)} violation(s)")

        for i, violation in enumerate(violations, 1):
            # Extract only the specified keys
            start_line_no = violation.get('start_line_no', 'N/A')
            start_line_pos = violation.get('start_line_pos', 'N/A')
            code = violation.get('code', 'N/A')
            description = violation.get('description', 'N/A')
            start_file_pos = violation.get('start_file_pos', 'N/A')
            end_line_no = violation.get('end_line_no', 'N/A')
            end_file_pos = violation.get('end_file_pos', 'N/A')

            output_lines.append(f"  {i}. [{code}] {description}")
            output_lines.append(f"     Line {start_line_no}:{start_line_pos} (pos {start_file_pos}) -> Line {end_line_no} (pos {end_file_pos})")
            output_lines.append("")  # Empty line for readability

    return "\n".join(output_lines)

def main():
    """Main function to check for violations."""
    try:
        # Read SQLFluff results
        with open('sqlfluff-results.json', 'r') as f:
            results = json.load(f)
        
        violation_count = len(results)

        formatted_results = format_sqlfluff_results(results)

        print(formatted_results)

        if violation_count > 0:
            sys.exit(1)
            
    except FileNotFoundError:
        print("SQLFluff results file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error parsing SQLFluff results")
        sys.exit(1)
    except Exception as error:
        print(f"Error checking violations: {error}")
        sys.exit(1)


if __name__ == '__main__':
    main()
