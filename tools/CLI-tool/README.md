# CLI Tool for GitHub Repository Management
This CLI tool automates the creation, configuration and management of GitHub configurator and working repositories for MLOPS usage. It includes two modules:

1. **Repository Setup Module:** Automates repository creation, branch setup, and configuration.
2. **Repository Forking Module:** Fetches repository details and forks them under a specified organization.

## Current limitation with the tool

- Tooling works in Unix commandline environments meaning MacOS or Linux (WSL for Windows)
- GitHub authentication via Token and the HTTPS option instead of SSH for the `gh`
	- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic
	- https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git?platform=linux
- For the tool to be able to fork and rename the working repo correctly a sufficently new `gh` version needed (see Prequisities below)
- Environmental secrets are set up currently as GitHub organization level secrets. This means that you may need separate GitHub organizations for difference ML setups.
- Python virtual environments may interfere with GitHub actions runner. (No defined solution for this at the moment)
- Multiple steps required interacting with GitHub site:
    - Setting up the organizations
    - Turning on the GitHub actions for the working repo (Actions tab > Big green button after reading the warnings)
    - Setting up the self-hosted runner
    - Setting up the SSH secret for remote cluster access

## Features

### Repository Setup Module

- Create a new GitHub repository in a specified organization.
- Clone the repository and initialize it with predefined branches: development, staging, and production.
- Copy branch-specific files for different environments.
- Set up GitHub secrets using a configuration file (config.yaml).
- Set the development branch as the default branch.

### Repository Forking Module

- Fetch repository details.
- Fork an existing repository under a specified organization with a unique name.

## Prerequisites

### 1. GitHub CLI (tested with versions 2.62.0 and 2.45.0):

Ensure that GitHub CLI is installed and authenticated.
Install using:
- macOS:
```
  brew install gh
 ```
- **! FOLLOWING STEP IS ONLY NEEDED IF YOU ARE USING AN OLDER VERSION OF LINUX WHERE ONLY OLD VERSIONS OF GH ARE AVAILABLE BY DEFAULT !**
- Ubuntu 24.xx can install gh 2.45.0 which is new enough
- Linux:
	- source: https://github.com/cli/cli/blob/trunk/docs/install_linux.md 	
```
  (type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
	&& wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y
```

### 2. Python:

Python 3.10 or higher.

Note: It is recommended to install a newer Linux than try to force install a newer Python version which isn't supported natively on older Linux.

-----

## Usage

Note: You may want to create a Python virtual environment and activate it. This will help with the package installation warnings.

https://python.land/virtual-environments/virtualenv

After cloning the repository, step out of the `oss-mlops-project` folder with cd `../` and then run:

```
oss-mlops-platform/tools/CLI-tool/create_gitrepo_devops_for_ml_work.sh
```

### Configuration File

The setup script asks you about configuring GitHub secrets using a config.yaml file. You can choose from options:

1. Create a new configuration file interactively.
2. Copy existing config.yaml from 'oss-mlops-platform/tools/CLI-tool/config.yaml'

Example config.yaml:
```
KUBEFLOW_ENDPOINT: "http://localhost:8080"
KUBEFLOW_USERNAME: "user@example.com"
KUBEFLOW_PASSWORD: "12341234"
REMOTE_CLUSTER_SSH_PRIVATE_KEY_PATH: "your/ssh/key/file/path"
REMOTE_CLUSTER_SSH_IP: "192.168.1.1"
REMOTE_CLUSTER_SSH_USERNAME: "user"
```

The scripts sets the secrets on the org level. You can set repo level secrets that take precident over org level ones if needed.
If a non-exact path for the SSH key file is passed, the script will search for the file containing the SSH key across the entire user home directory. This can be very slow on a populated drive (e.g. running the install script on bare metal Linux or MacOS).

### Post setup script set up on GitHub's site

After the repositories are made you may need to enable the GitHub Actions for the working repository.
This can be done from the GitHub site by navigating to the working repository and it's Actions tab and clicking the big green button.

Secondly you want to add the self-hosted GitHub Actions runner to the repository (it can also be added to whole organization) from Settings > Actions > Runner > New self-hosted runner. (More details can be found in 'starting a local run.md' step 4)
