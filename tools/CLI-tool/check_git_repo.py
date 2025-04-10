import sys
import git

try:
    git.Repo('.', search_parent_directories=True)
    print("Error: git repository exists in this directory.")
    sys.exit(1)
except git.exc.InvalidGitRepositoryError:
    sys.exit(0)
