import os
import subprocess
import json
import sys

import json
import subprocess
import typer

# Define the Typer app
app = typer.Typer()


# Use Typer to define repo_name as an argument
@app.command()
def main(repo_name: str, org_name: str):
    """
    Main function to fetch repo details and fork it.
    """
    fork_repo(repo_name, org_name)


def get_working_repo_name(config_repo_name: str):
    if config_repo_name.startswith("Config-"):
        as_split = config_repo_name.split("-")
        as_split[0] = "Working"
        default_working_repo_name = "-".join(as_split)
        return typer.prompt(
            "Enter unique name for your working repository:",
            type=str,
            default=default_working_repo_name,
        )
    return typer.prompt("Enter unique name for your working repository:", type=str)


def fork_repo(repo_name: str, org_name):
    """Fork the repository using GitHub CLI."""
    default_working_repo_name = "TODO-This-Should-Not-Depend-On-Config-Repo-Name-At-All"
    # Hack to see if this conforms to our default naming conv! Evil...
    if repo_name.startswith("Config-"):
        as_split = repo_name.split("-")
        as_split[0] = "Working"
        default_working_repo_name = "-".join(as_split)

    working_repo_name = typer.prompt(
        "Enter unique name for your working repository:",
        type=str,
        default=default_working_repo_name,
    )
    version = subprocess.run(["gh", "--version"], capture_output=True, text=True)

    if "2.4.0" in version.stdout:
        subprocess.run(
            f"gh repo fork {org_name}/{repo_name} --clone --remote-name {working_repo_name} --org {org_name}",
            shell=True,
        )
    else:
        subprocess.run(
            f'gh repo fork {org_name}/{repo_name} --clone --fork-name "{working_repo_name}" --org {org_name}',
            shell=True,
        )
        os.chdir(working_repo_name)
        subprocess.run(["git", "checkout", "-b", "staging", "origin/staging"])
        subprocess.run(["git", "checkout", "-b", "production", "origin/production"])
        subprocess.run(["git", "checkout", "development"])
        os.chdir("../")

        # This option was for the older versions of GH in order to clone the forked repo

    # if sys.platform == "darwin":
    #     subprocess.run(f'gh repo fork {owner}/{repo_name} --clone --fork-name "{working_repo_name}" --org {owner}', shell=True)
    # elif sys.platform == "linux":
    #     subprocess.run(f'gh repo fork {owner}/{repo_name} --clone --remote-name {working_repo_name} --org {owner}', shell=True)


if __name__ == "__main__":
    app()
