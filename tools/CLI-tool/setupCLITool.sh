#!/bin/bash

# Navigate to the directory containing the script

# Install the requirements
pip install -r oss-mlops-platform/tools/CLI-tool/requirements.txt



python3 oss-mlops-platform/tools/CLI-tool/setup_cli.py

python3 oss-mlops-platform/tools/CLI-tool/fork_repo.py