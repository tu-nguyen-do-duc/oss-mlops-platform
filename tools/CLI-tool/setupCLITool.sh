#!/bin/bash

# Navigate to the directory containing the script

# Install the requirements
pip install -r oss-mlops-platform/tools/CLI-tool/requirements.txt

read -p "Enter the repository name you want to create: " repo_name

python3 oss-mlops-platform/tools/CLI-tool/setup_cli.py "$repo_name"

python3 oss-mlops-platform/tools/CLI-tool/fork_repo.py "$repo_name"