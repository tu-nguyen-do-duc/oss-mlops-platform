import typer
import subprocess
import sys
import os
import yaml

# Define the Typer app
app = typer.Typer()

# Use Typer to define repo_name as an argument
@app.command()
def main(repo_name: str):
    """
    Main function to create a GitHub repository, set up structure, and configure secrets.
    """
    print(f"Working with repository: {repo_name}")

    print("Checking if GitHub CLI is installed...")
    check_gh_installed()

    print("Creating a new repository...")
    create_repo(repo_name)

    print("Pushing the repository to GitHub...")
    push_repo()

    print("Creating branches...")
    create_branches()

    print("Adding branch specific files...")
    copy_files()

    print("Setting up the configuration...")
    set_config()


def check_gh_installed():
    """Check if GitHub CLI is installed."""
    try:
        result = subprocess.run(["gh", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            typer.echo("GitHub CLI (gh) is not installed.")
            typer.echo("Do you want to install GitHub CLI? (y/n)")
            choice = input().strip().lower()
            if choice == 'y':
                if sys.platform == "darwin":
                    subprocess.run(["brew", "install", "gh"], check=True)
                elif sys.platform == "linux":
                    subprocess.run(["sudo", "apt", "install", "gh"], check=True)
                else:
                    typer.echo("Unsupported OS. Please install GitHub CLI manually.")
                    sys.exit(1)
            else:
                typer.echo("GitHub CLI (gh) is required. Exiting...")
                sys.exit(1)
    except FileNotFoundError:
        typer.echo("GitHub CLI (gh) is not installed.")
        sys.exit(1)


def check_repo(repo_name):
    """Check if repository already exists."""
    result = subprocess.run(f"gh repo view Softala-MLOPS/{repo_name}", shell=True, capture_output=True)
    return result.returncode == 0


def create_repo(repo_name):
    """Create a new GitHub repository."""
    result = subprocess.run("gh auth status", shell=True, capture_output=True, text=True)
    if "Logged in to github.com" not in result.stdout:
        subprocess.run("gh auth login", shell=True)

    if not check_repo(repo_name):
        subprocess.run(f'gh repo create Softala-MLOPS/{repo_name} --public --description "Upstream repository" --clone', shell=True)
        os.chdir(repo_name)
    else:
        typer.echo("Repository already exists.")

def push_repo():
    """Push the repository to GitHub."""
    # Check the current branch
    result = subprocess.run(["git", "branch"], capture_output=True, text=True, check=True)
    current_branch = None
    
    # Parse the branch list to get the current branch (the one with an asterisk)
    for line in result.stdout.splitlines():
        if line.startswith("*"):
            current_branch = line[2:].strip()  # Extract branch name

    if current_branch:
        print(f"Current branch is: {current_branch}")
    else:
        print("Error: Could not determine the current branch.")
        return

    # If the current branch is 'main', try to push it
    if current_branch == 'main':
        subprocess.run(["git", 'add', '.'], check=True)
        subprocess.run(["git", 'commit', '-m', '"Initial commit"'], check=True)
        subprocess.run(["git", 'push', 'origin', 'main'], check=True)
    elif current_branch == 'master':
        # If on master, push to 'master' instead of 'main'
        subprocess.run(["git", 'add', '.'], check=True)
        subprocess.run(["git", 'commit', '-m', '"Initial commit"'], check=True)
        subprocess.run(["git", 'push', 'origin', 'master'], check=True)
    else:
        print(f"Error: Branch '{current_branch}' is not 'main' or 'master'. Cannot push.")

def create_branches():
    """Create branches if they don't already exist."""
    result = subprocess.run("git branch -a", shell=True, capture_output=True, text=True)
    existing_branches = result.stdout.splitlines()

    branches_to_create = ["development", "staging", "production"]
    for branch in branches_to_create:
        if branch not in existing_branches:
            subprocess.run(f'git checkout -b {branch}', shell=True)
            subprocess.run(f'git push --set-upstream origin {branch}', shell=True)
            print(f"Branch '{branch}' created successfully.")


def copy_files():
    """Copy branch-specific files."""
    subprocess.run("git checkout development", shell=True)
    subprocess.run("cp -r ../oss-mlops-platform/tools/files/developement/* .", shell=True)
    subprocess.run("cp ../oss-mlops-platform/tools/resources/workflows/start-local-run.yml .github/workflows", shell=True)
    subprocess.run("git add .", shell=True)
    subprocess.run("git commit -m 'Add branch specific files'", shell=True)
    subprocess.run("git push origin development", shell=True)

    subprocess.run("git checkout production", shell=True)
    subprocess.run("cp -r ../oss-mlops-platform/tools/files/production/* .", shell=True)
    subprocess.run("cp ../oss-mlops-platform/tools/resources/workflows/start-remote-run.yml .github/workflows", shell=True)
    subprocess.run("git add .", shell=True)
    subprocess.run("git commit -m 'Add production files'", shell=True)
    subprocess.run("git push origin production", shell=True)

def set_config():
    """Create a config file for GitHub secrets"""
    print("1. Create config file\n2. Already a config.yaml file in directory")
    choice = int(input())

    if choice == 1:
        print("Specify Kubeflow endpoint (default: http://localhost:8080):")
        kep = input().strip()
        if not kep:
            kep = "http://localhost:8080"

        print("Specify Kubeflow username (default: user@example.com):")
        kun = input().strip()
        if not kun:
            kun = "user@example.com"

        print("Specify Kubeflow password (default: 12341234):")
        kpw = input().strip()
        if not kpw:
            kpw = "12341234"

        print("Add remote cluster private key:")
        remote_key = input().strip()
        print("Specify remote cluster IP:")
        remote_ip = input().strip()
        print("Add remote cluster username:")
        remote_username = input().strip()

        config = {
            'KUBEFLOW_ENDPOINT': kep,
            'KUBEFLOW_USERNAME': kun,
            'KUBEFLOW_PASSWORD': kpw,
            'REMOTE_CSC_CLUSTER_SSH_PRIVATE_KEY': remote_key,
            'REMOTE_CSC_CLUSTER_SSH_IP': remote_ip,
            'REMOTE_CSC_CLUSTER_SSH_USERNAME': remote_username
        }

        with open("config.yaml", 'w') as f:
            yaml.dump(config, f, sort_keys=False)

    # Read and set GitHub secrets from the config file
    with open("config.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        print("Config file read successfully.")
        print(data)

    for key, value in data.items():
        subprocess.run(f'gh secret set {key} --body {value} --org Softala-MLOPS', shell=True)


if __name__ == "__main__":
    app()