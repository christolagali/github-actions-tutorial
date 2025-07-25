#!/usr/bin/env python3
"""
SQLFluff Lint Runner
Runs SQLFluff linting on changed files with different configs based on file paths.
"""

import os
import subprocess
import sys
import json
from typing import List, Dict, Any

# Variables
REPEATABLE_MIGRATION_PATH = "airflow/dags/db/mwarehouse/migrations/repeatable"

DBT_MIGRATION_PATH = "airflow/dags/dbt"

REPEATABLE_CONFIG_PATH = "airflow/linters/config_files/repeatable/.sqlfluff"

OTHERS_CONFIG_PATH = "airflow/linters/config_files/others/.sqlfluff"

DBT_CONFIG_PATH = "airflow/linters/config_files/dbt/.sqlfluff"


def separate_files_by_path(changed_files: List[str]) -> tuple[List[str], List[str]]:
    """
    Separate files by path to determine which config to use.

    Args:
        changed_files: List of file paths

    Returns:
        tuple of (repeatable_files, other_files)
    """
    repeatable_files = []
    other_files = []

    # Iterate through changed files and categorize them
    for file in changed_files:
        if REPEATABLE_MIGRATION_PATH in file:
            repeatable_files.append(file)
        elif DBT_MIGRATION_PATH in file:
            # DBT files are handled separately, not in repeatable migrations
            continue
        else:
            other_files.append(file)

    return repeatable_files, other_files


def run_sqlfluff_json(
    files: List[str], config_path: str, file_type: str
) -> List[Dict[str, Any]]:
    """
    Run SQLFluff lint with JSON output.

    Args:
        files: List of file paths to lint
        config_path: Path to SQLFluff config file
        file_type: Description of file type for logging

    Returns:
        List of JSON results
    """
    if not files:
        return []

    print(f"Linting {file_type} files for JSON output: {' '.join(files)}")

    cmd = ["sqlfluff", "lint", "--config", config_path, "--format", "json"] + files

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            print(f"Error parsing JSON from {file_type} files: {result.stdout}")
            return []

    return []


def main():
    """Main function to generate JSON results."""
    # Get changed files from environment
    changed_files_str = os.environ.get("CHANGED_SQL_FILES", "")
    if not changed_files_str:
        print("No changed files found in environment")
        return

    changed_files = changed_files_str.split()

    # Separate files by path
    repeatable_files, other_files = separate_files_by_path(changed_files)

    # Initialize results
    combined_results = []
    repeatable_results = []
    other_results = []

    # Lint repeatable migration files with specific config
    if repeatable_files:
        repeatable_results = run_sqlfluff_json(
            repeatable_files, REPEATABLE_CONFIG_PATH, "repeatable migration"
        )

    # Lint other files with default config
    if other_files:
        other_results = run_sqlfluff_json(other_files, OTHERS_CONFIG_PATH, "other SQL")

    # Combine results
    combined_results = repeatable_results + other_results

    # Write combined results
    with open("sqlfluff-results.json", "w") as f:
        json.dump(combined_results, f, indent=2)

    print(
        f"Combined {len(repeatable_results)} repeatable results and {len(other_results)} other results"
    )

    # Set output for next step
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write("results-file=sqlfluff-results.json\n")


if __name__ == "__main__":
    main()
