import os
import typer
import subprocess
import sys
import shutil
import yaml

def check_gh_installed():
    """Check if GitHub CLI is installed."""
    print(sys.platform)
    try:
        result = subprocess.run(["gh", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            typer.echo("GitHub CLI (gh) is not installed.")
            typer.echo("Do you want to install GitHub CLI? (y/n)")
            choice = input().strip().lower()
            if choice == 'y':
                if sys.platform == "darwin":
                    typer.echo("Installing GitHub CLI on macOS using Homebrew...")
                    subprocess.run(["brew", "install", "gh"], check=True)
                elif sys.platform == "linux":
                    typer.echo("Installing GitHub CLI on Linux using apt...")
                    subprocess.run(["sudo", "apt", "update"], check=True)
                    subprocess.run(["sudo", "apt", "install", "-y", "gh"], check=True)
                else:
                    typer.echo("Unsupported OS. Please install GitHub CLI manually.")
                    sys.exit(1)
            else:
                typer.echo("GitHub CLI (gh) is required. Exiting...")
                sys.exit(1)

            sys.exit(1)
    except FileNotFoundError:
        typer.echo("GitHub CLI (gh) is not installed.")
        sys.exit(1)

def check_repo():
    """Check if repository already exists."""
    result = subprocess.run("gh repo view Softala-MLOPS/ConfigRepoCLI", shell=True, capture_output=True)
    if result.returncode == 0:
        return True

def create_repo():
    result = subprocess.run("gh auth status", shell=True, capture_output=True, text=True)
    if "Logged in to github.com account" not in result.stdout:
        subprocess.run("gh auth login", shell=True)
    if not check_repo():
        subprocess.run('gh repo create Softala-MLOPS/ConfigRepoCLI --public --description "Upstream repository" --clone', shell=True)
        os.chdir("ConfigRepoCLI")
    else:
        typer.echo("Repository already exists.")

def create_repo_structure():
    current_dir = os.getcwd()
    if "ConfigRepoCLI" not in current_dir:
        result = subprocess.run(["ls", "ConfigRepoCLI"], capture_output=True, text=True)
        if result.returncode != 0:
            subprocess.run(["git", "clone", "git@github.com:Softala-MLOPS/ConfigRepoCLI.git"], check=True)
        try:
            os.chdir("ConfigRepoCLI")
        except FileNotFoundError:
            typer.echo("Repository not found. Exiting...")



    """Create the repository structure."""
    subprocess.run(f"mkdir -p .github/workflows", shell=True, capture_output=True)
    subprocess.run(f"touch .github/workflows/.gitkeep", shell=True, capture_output=True)
    subprocess.run(f"mkdir -p data", shell=True, capture_output=True)
    os.chdir("data")
    subprocess.run(f'echo "data" > Readme.md', shell=True, capture_output=True)
    os.chdir("../")
    subprocess.run(f"mkdir -p docs", shell=True, capture_output=True)
    os.chdir("docs")
    subprocess.run(f'echo "docs" > Readme.md', shell=True, capture_output=True)
    os.chdir("../")
    subprocess.run(f"mkdir -p models", shell=True, capture_output=True)
    os.chdir("models") 
    subprocess.run(f'echo "models" > Readme.md', shell=True, capture_output=True)
    os.chdir("../")
    subprocess.run(f"mkdir -p notebooks", shell=True, capture_output=True)
    subprocess.run(f"mkdir -p notebooks/components", shell=True, capture_output=True)
    os.chdir("notebooks")
    subprocess.run(f'echo "notebooks" > Readme.md', shell=True, capture_output=True)
    os.chdir("../")
    subprocess.run(f"mkdir -p src", shell=True, capture_output=True)
    os.chdir("src")
    subprocess.run(f'echo "src" > Readme.md', shell=True, capture_output=True)
    os.chdir("../")
    subprocess.run(f"mkdir -p tests", shell=True, capture_output=True)
    os.chdir("tests")
    subprocess.run(f'echo "tests" > Readme.md', shell=True, capture_output=True)
    os.chdir("../")
    subprocess.run(f'touch .gitignore', shell=True, capture_output=True)
    f = open(".gitignore", "a")
    f.write("config.yaml")
    f.close()
    subprocess.run(f'touch LICENSE', shell=True, capture_output=True)
    subprocess.run(f'touch README.md', shell=True, capture_output=True)
    subprocess.run(f'touch requirements.txt', shell=True, capture_output=True)

def set_config():
    """Create a config file for github secrets"""

    print("1 Create config file\n2 Already a config.yaml file in directory")
    choise = int(input())

    if choise == 1:
        """No config file"""
        print("Specify Kubeflow endpoint (if empty uses http://localhost:8080 by default)")
        kep = input().strip()
        if kep == "":
            kep = "http://localhost:8080"
        print("Specify Kubeflow username (if empty uses user@example.com by default)")
        kun = input().strip()
        if kun == "":
            kun = "user@example.com"
        print("Specify Kubeflow password (if empty uses 12341234 by default)")
        kpw = input().strip()
        if kpw == "":
            kpw = "12341234"
        print("Add remote cluster private key")
        remote_key = input().strip()
        print("Specify remote cluster IP")
        remote_ip = input().strip()
        print("Add remote cluster username")
        remote_username = input().strip()
        config = {
            'KUBEFLOW_ENDPOINT': kep,
            'KUBEFLOW_USERNAME': kun,
            'KUBEFLOW_PASSWORD': kpw,
            'REMOTE_CSC_CLUSTER_SSH_PRIVATE_KEY': remote_key,
            'REMOTE_CSC_CLUSTER_SSH_IP': remote_ip,
            'REMOTE_CSC_CLUSTER_SSH_USERNAME': remote_username
        }
        with open("config.yaml", 'w',) as f :
            yaml.dump(config, f, sort_keys=False)
            
    with open("config.yaml", "r") as yamlfile:
            data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            print("Read successful")
    print(data)

    for key, value in data.items():
        subprocess.run(f'gh secret set {key} --body {value} --org Softala-MLOPS', shell=True)


def push_repo():
    """Push the repository to GitHub."""
    subprocess.run([f"git", 'add', '.'])
    subprocess.run([f"git", 'commit', '-m', '"Initial commit"'])
    subprocess.run([f"git", 'push', 'origin', 'main'])

def create_branches():
    """Check if branches already exist."""
    result = subprocess.run(f'git branch -a', shell=True, capture_output=True, text=True)
    existing_branches = result.stdout.splitlines()

    branches_to_create = ["development", "staging", "production"]
    for branch in branches_to_create:
        if any(branch in line for line in existing_branches):
            print(f"Branch '{branch}' already exists.")
        else:
            subprocess.run(f'git checkout -b {branch}', shell=True)
            subprocess.run(f'git push --set-upstream origin {branch}', shell=True)
            print(f"Branch '{branch}' created successfully.")
            
    print("List of current branches:")
    subprocess.run(f'git branch -a', shell=True, capture_output=True)

def copy_files():
    """Copy branch specific files"""
    subprocess.run(f'git checkout development', shell=True)
    subprocess.run(f"cp ../oss-mlops-platform/tools/resources/workflows/start-local-run.yml .github/workflows", shell=True, capture_output=True)
    subprocess.run(f"cp ../oss-mlops-platform/tools/CLI-tool/Components/Dev/* notebooks/components", shell=True, capture_output=True)
    subprocess.run(f"cp ../oss-mlops-platform/tools/CLI-tool/Notebooks/Dev/demo-pipeline.ipynb notebooks", shell=True, capture_output=True)
    subprocess.run([f"git", 'add', '.'])
    subprocess.run([f"git", 'commit', '-m', '"Add branch specific files"'])
    subprocess.run(f'git push origin development', shell=True)

    subprocess.run(f'git checkout production', shell=True)
    subprocess.run(f"cp ../oss-mlops-platform/tools/resources/workflows/start-remote-run.yml .github/workflows", shell=True, capture_output=True)
    subprocess.run(f"cp ../oss-mlops-platform/tools/CLI-tool/Components/Prod/* notebooks/components", shell=True, capture_output=True)
    subprocess.run(f"cp ../oss-mlops-platform/tools/CLI-tool/Notebooks/Prod/demo-pipeline.ipynb notebooks", shell=True, capture_output=True)
    subprocess.run([f"git", 'add', '.'])
    subprocess.run([f"git", 'commit', '-m', '"Add branch specific files"'])
    subprocess.run(f'git push origin production', shell=True)


def main():

    print("Checking if GitHub CLI is installed...")
    check_gh_installed()


    print("Creating a new repository...")
    create_repo()
    
    """ print("Creating the repository structure...")
    create_repo_structure() """
    
    print("Setting up the configuration...")
    set_config()
    
    print("Pushing the repository to GitHub...")
    push_repo()

    print("Creating branches...")
    create_branches()

    print("Add branch specific files")
    copy_files()
    
    
if __name__ == "__main__":
    typer.run(main)
