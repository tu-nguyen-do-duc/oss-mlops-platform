# CLI Tool for GitHub Repository Management
This CLI tool automates the creation, configuration, and management of GitHub configurator and working repositories for mlops usage. It includes two modules:

1. **Repository Setup Module:** Automates repository creation, branch setup, and configuration.
2. **Repository Forking Module:** Fetches repository details and forks them under a specified organization.

## Current limitation with environmental secrets in GitHub

Environmental secrets are set up currently as GitHub organization level secrets. This means that you may need separate GitHub organizations for difference ML setups.

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

### 1. GitHub CLI (gh):

Ensure that GitHub CLI is installed and authenticated.
Install using:
- macOS: brew install gh
- Linux:
  (type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
	&& wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y

### 2. Python:

Python 3.8 or higher.

-----

## Usage

Note: You may want to create a Python virtual environment and activate it.

After cloning the repository, step out of the `oss-mlops-project` folder with cd `../` and then run:

```
oss-mlops-platform/tools/CLI-tool/setupCLITool.sh
```

### Configuration File

The setup script asks you about configuring GitHub secrets using a config.yaml file. You can choose from options:

1. Create a new configuration file interactively.
2. Copy an existing configuration file from a specified path.

Example config.yaml:
```
KUBEFLOW_ENDPOINT: "http://localhost:8080"
KUBEFLOW_USERNAME: "user@example.com"
KUBEFLOW_PASSWORD: "12341234"
REMOTE_CSC_CLUSTER_SSH_PRIVATE_KEY: "Your_Key"
REMOTE_CSC_CLUSTER_SSH_IP: "192.168.1.1"
REMOTE_CSC_CLUSTER_SSH_USERNAME: "user"
```

### Post setup script set up on GitHub's site

After the repositories are made you may need to enable the GitHub Actions for the working repository.
This can be done from the GitHub site by navigating to the working repository and it's Actions tab and clicking the big green button.

Secondly you want to add the self-hosted GitHub Actions runner to the repository (it can also be added to whole organization) from Settings > Actions > Runner > New self-hosted runner. (More details can be found in 'starting a local run.md' step 4)
