#!/usr/bin/env python3
"""
Violation Checker
Checks if SQLFluff found any violations and exits accordingly.
"""

import json
import sys


def main():
    """Main function to check for violations."""
    try:
        # Read SQLFluff results
        with open('sqlfluff-results.json', 'r') as f:
            results = json.load(f)
        
        violation_count = len(results)
        
        if violation_count > 0:
            print(f"SQLFluff found {violation_count} violation(s)")
            print(results)
            sys.exit(1)
        else:
            print("No violations found")
            
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
