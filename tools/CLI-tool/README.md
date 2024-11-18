# CLI Tool for GitHub Repository Management
This CLI tool automates the creation, configuration, and management of GitHub configurator and working repositories for mlops usage. It includes two modules:

1. **Repository Setup Module:** Automates repository creation, branch setup, and configuration.
2. **Repository Forking Module:** Fetches repository details and forks them under a specified organization.


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
- Linux: sudo apt install gh
### 2. Python:

Python 3.8 or higher.

## Usage
Create a virtual env and acitavate it

cd ../ out of the oss-mlops-project folder then run

```
oss-mlops-platform/tools/CLI-tool/setupCLITool.sh
```
## Configuration File

The setup_repo.py script allows you to configure GitHub secrets using a config.yaml file. You can:

1. Create a new configuration file interactively.
2. Copy an existing configuration file from a specified path.
Example config.yaml:
```
KUBEFLOW_ENDPOINT: "http://localhost:8080"
KUBEFLOW_USERNAME: "user@example.com"
KUBEFLOW_PASSWORD: "12341234"
REMOTE_CSC_CLUSTER_SSH_PRIVATE_KEY: "path/to/private/key"
REMOTE_CSC_CLUSTER_SSH_IP: "192.168.1.1"
REMOTE_CSC_CLUSTER_SSH_USERNAME: "user"
```
