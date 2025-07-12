#!/usr/bin/env python3
"""
SQLFluff Lint Runner
Runs SQLFluff linting on changed files with different configs based on file paths.
"""

import os
import subprocess
import sys
from typing import List, Tuple


def separate_files_by_path(changed_files: List[str]) -> Tuple[List[str], List[str]]:
    """
    Separate files by path to determine which config to use.
    
    Args:
        changed_files: List of file paths
        
    Returns:
        Tuple of (repeatable_files, other_files)
    """
    repeatable_files = []
    other_files = []
    
    for file in changed_files:
        if "scripts/sqlfluff/sql_scripts/repeatable" in file:
            repeatable_files.append(file)
        else:
            other_files.append(file)
    
    return repeatable_files, other_files


def run_sqlfluff_lint(files: List[str], config_path: str, file_type: str) -> bool:
    """
    Run SQLFluff lint on a list of files with specified config.
    
    Args:
        files: List of file paths to lint
        config_path: Path to SQLFluff config file
        file_type: Description of file type for logging
        
    Returns:
        True if linting passed, False if failed
    """
    if not files:
        return True
    
    print(f"Linting {file_type} files: {' '.join(files)}")
    
    cmd = [
        'sqlfluff', 'lint',
        '--config', config_path,
        '--format', 'github-annotation',
        '--annotation-level', 'failure'
    ] + files
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print output
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode == 0


def main():
    """Main function to run SQLFluff linting."""
    # Get changed files from environment
    changed_files_str = os.environ.get('CHANGED_FILES', '')
    if not changed_files_str:
        print("No changed files found in environment")
        return
    
    changed_files = changed_files_str.split()
    print(f"Changed SQL files: {' '.join(changed_files)}")
    
    # Separate files by path
    repeatable_files, other_files = separate_files_by_path(changed_files)
    
    # Track if any linting fails
    lint_passed = True
    
    # Lint repeatable migration files with specific config
    if repeatable_files:
        success = run_sqlfluff_lint(
            repeatable_files, 
            'scripts/sqlfluff/sql_scripts/repeatable/.sqlfluff',
            'repeatable migration'
        )
        if not success:
            lint_passed = False
    
    # Lint other files with default config
    if other_files:
        success = run_sqlfluff_lint(
            other_files,
            'scripts/sqlfluff/sql_scripts/versioned/.sqlfluff',
            'other SQL'
        )
        if not success:
            lint_passed = False
    
    # Exit with error if any linting failed
    if not lint_passed:
        print("SQLFluff linting failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
