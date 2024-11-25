#!/bin/bash

# Navigate to the directory containing the script

# Install the requirements
pip install -r oss-mlops-platform/tools/CLI-tool/requirements.txt

read -p "Enter the organization name: " org_name

read -p "Enter the name of the config repo: " repo_name

echo "Which script(s) would you like to run?"
echo "1) setup_cli.py"
echo "2) fork_repo.py"
echo "3) Both"
read -p "Enter your choice (1/2/3): " choice

# Execute the selected script(s)
case $choice in
    1)
        python3 oss-mlops-platform/tools/CLI-tool/setup_cli.py "$repo_name" "$org_name"
        ;;
    2)
        python3 oss-mlops-platform/tools/CLI-tool/fork_repo.py "$repo_name" "$org_name"
        ;;
    3)
        python3 oss-mlops-platform/tools/CLI-tool/setup_cli.py "$repo_name" "$org_name"
        python3 oss-mlops-platform/tools/CLI-tool/fork_repo.py "$repo_name" "$org_name"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac