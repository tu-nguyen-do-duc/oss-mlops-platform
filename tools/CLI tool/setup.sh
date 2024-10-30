#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Install the requirements
pip install -r requirements.txt

python3 setup_cli.py

python3 fork_repo.py