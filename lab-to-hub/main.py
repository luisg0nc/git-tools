#!/usr/bin/env python3
import argparse
import os
from git import Repo, GitCommandError

def migrate_repository(repo_name, gitlab_org, github_org):
    """
    Migrates a repository from GitLab to GitHub.
    Args:
        repo_name (str): The name of the repository to migrate.
        gitlab_org (str): The GitLab organization or user name.
        github_org (str): The GitHub organization or user name.
    Raises:
        GitCommandError: If there is an error during the Git operations.
    This function performs the following steps:
    1. Constructs the GitLab and GitHub repository URLs based on the provided organization/user names and repository name.
    2. Checks if the repository directory already exists locally.
        - If it exists, fetches updates from the GitLab remote.
        - If it does not exist, clones the repository from GitLab.
    3. Adds GitHub as a new remote to the local repository.
    4. Pushes the repository to GitHub with the mirror option to ensure all refs are copied.
    """
    gitlab_url = f"git@gitlab.com:{gitlab_org}/{repo_name}.git"
    github_url = f"git@github.com:{github_org}/{repo_name}.git"
    
    print(f"🚀 Migrating repository: {repo_name}")

    try:
        # Check if the repository directory already exists
        repo_dir = f"{repo_name}"
        if os.path.exists(repo_dir):
            print(f"📂 Directory {repo_dir} already exists. Fetching updates from GitLab.")
            repo = Repo(repo_dir)
            repo.remotes.origin.fetch()
        else:
            # Clone the repository from GitLab using SSH
            print(f"🔄 Cloning from: {gitlab_url}")
            repo = Repo.clone_from(gitlab_url, repo_dir, mirror=True)

        # Add GitHub as a new remote
        print(f"➕ Adding GitHub remote: {github_url}")
        repo.create_remote('github', github_url)
        
        # Push the repository to GitHub
        print(f"📤 Pushing to GitHub: {github_url}")
        repo.remotes.github.push(mirror=True)
    
    except GitCommandError as e:
        print(f"❌ Error: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Migration script for repositories.')
    parser.add_argument('repos_list', type=str, help='File containing list of repositories to create')
    parser.add_argument('gitlab_org', type=str, help='GitLab organization name')
    parser.add_argument('github_org', type=str, help='GitHub organization name')
    return parser.parse_args()

def main():
    args = parse_arguments()

    with open(args.repos_list, 'r') as file:
        repos = file.readlines()

    for repo in repos:
        migrate_repository(repo, args.gitlab_org, args.github_org)

if __name__ == '__main__':
    main()
