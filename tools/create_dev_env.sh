#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the Python files
python3 "$SCRIPT_DIR/setup_cli.py"
python3 "$SCRIPT_DIR/fork_repo.py"