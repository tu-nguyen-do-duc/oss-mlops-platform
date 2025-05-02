#!/bin/bash
set -e

# Navigate to the directory containing the script:
# ${BASH_SOURCE[0]} - resolve full file path of script
# "$(dirname "${BASH_SOURCE[0]}")" - extract directory portion from full file path of script
cli_tool_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install the requirements
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r "${cli_tool_dir}/requirements.txt"

# Check if script is run outside of git repository
if ! python3 "${cli_tool_dir}/check_git_repo.py"; then
    echo "The script must be run from outside any git repository to create working and configuration repositories correctly."
    exit 1
fi

read -p "Enter the organization name: " org_name

if [[ -z "$org_name" ]]; then
    echo "Cannot continue without organization name!"
    exit 1
fi

read -p "Enter the name of the config repo (default: Config-%username-%Y-%m-%d-%tag): " repo_name

if [[ -z "$repo_name" ]]; then
    git_username=$(git config --global user.name | sed 's/ /-/g; s/[\d128-\d255]//g')
    repo_tag=$(openssl rand -hex 4)
    repo_name="Config-${git_username}-$(date +'%Y-%m-%d')-${repo_tag}"

    echo "No repository name specified, using generated repository name $repo_name"
fi

while true; do
    echo "Select an option:"
    echo "Which script(s) would you like to run?"
    echo "1) Configure Github (GH) for the tool (configure_gh.py)"
    echo "2) Create configuration repo for one or more ML project working repos (create_config_repo.py)"
    echo "3) Create one ML project working repo based on a configuration repo (create_working_repo.py)"
    echo "4) Both (step 3 is based on config repo created in step 2) 🟢 RECOMMENDED 🟢"
    echo "5) Exit"
    read -p "Enter your choice: " choice

    case $choice in
        1)
            python3 "${cli_tool_dir}/configure_gh.py"
            ;;
        2)
            python3 "${cli_tool_dir}/configure_gh.py"
            python3 "${cli_tool_dir}/create_config_repo.py" "$repo_name" "$org_name"                             
            ;;
        3)
            python3 "${cli_tool_dir}/configure_gh.py"
            python3 "${cli_tool_dir}/create_working_repo.py" "$repo_name" "$org_name"
            exit 0
            ;;
        4)
            python3 "${cli_tool_dir}/configure_gh.py"
            python3 "${cli_tool_dir}/create_config_repo.py" "$repo_name" "$org_name"
            python3 "${cli_tool_dir}/create_working_repo.py" "$repo_name" "$org_name"
            exit 0
            ;;
        5)
            echo "Exiting. Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done
