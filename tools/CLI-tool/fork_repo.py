import os
import subprocess
import json

repo_name = "ConfigRepoCLI"

def get_repo_owner():

    result = subprocess.run(
        f"gh api -X GET search/repositories -f q='{repo_name} in:name' --jq '.items[] | {{name, owner: .owner.login}}'",
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error fetching repository information:", result.stderr)
        return None
    
    try:
        print(result.stdout)
        repo_info_list = [json.loads(line) for line in result.stdout.strip().split('\n')]
        repo_info = repo_info_list[0]
        print(repo_info)
        owner_name = repo_info['owner']
        print(owner_name)
        return owner_name
    except json.JSONDecodeError:
        print("Error decoding repository information")
        return None

def fork_repo(owner):
    # Run the gh command to fork the repo
    print("Enter unique name for your working repository")
    working_repo_name = input()
    subprocess.run(f'gh repo fork {owner}/{repo_name} --clone --fork-name "working-repo" --org {owner}', shell=True)


def main():

    print("Fetching repository information...")
    repo_owner = get_repo_owner()
    
    print("Forking the repository...")
    fork_repo(repo_owner)




if __name__ == "__main__":
    main()
