#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Luis Goncalves
Description: This script creates GitHub repositories in a specified organization.
             It handles existing repositories and rate limiting.
Date: 2025-01-21
"""

import requests
import sys
import argparse
import time

def create_github_repo(repo_name, owner, token, private):
    """
    Create a GitHub repository in the specified organization.

    Args:
        repo_name (str): The name of the repository to create.
        owner (str): The name of the organization that will own the repository.
        token (str): The GitHub personal access token for authentication.
        private (bool): Whether the repository should be private.

    Returns:
        None

    Raises:
        Exception: If the repository creation fails for reasons other than rate limiting or existing repository.

    This function attempts to create a new repository in the specified GitHub organization using the provided
    personal access token for authentication. If the repository already exists, it calls the `handle_existing_repo`
    function to handle the existing repository. If the rate limit is exceeded, it waits until the rate limit resets
    before retrying. If the repository creation fails for other reasons, it prints an error message and exits.
    """
    url = f'https://api.github.com/orgs/{owner}/repos'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': repo_name,
        'private': private
    }
    while True:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f'✅ Successfully created repository {repo_name} in organization {owner}')
            break
        elif response.status_code == 422 and 'already exists' in response.json().get('errors', [{}])[0].get('message', ''):
            handle_existing_repo(repo_name, owner, headers, private)
            break
        elif response.status_code == 403 and 'secondary rate limit' in response.json().get('message', ''):
            reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
            wait_time = max(0, reset_time - time.time())
            wait_time_minutes = wait_time / 60
            print(f'⌛ Rate limit exceeded. Retrying after {wait_time_minutes:.2f} minutes...')
            time.sleep(wait_time)
        else:
            print(f'❌ Failed to create repository {repo_name} in organization {owner}: {response.json()}')
            break

def handle_existing_repo(repo_name, owner, headers, private):
    """
    Handle an existing repository in a GitHub organization.

    This function checks if a repository already exists in the specified GitHub organization.
    If the repository exists and is public, it can optionally change the repository to private.

    Args:
        repo_name (str): The name of the repository.
        owner (str): The owner (organization) of the repository.
        headers (dict): The headers to include in the GitHub API requests, typically including authorization.
        private (bool): A flag indicating whether the repository should be private.

    Prints:
        A message indicating the status of the repository and any changes made.
    """
    print(f'⚠️ Repository {repo_name} already exists in organization {owner}')
    repo_url = f'https://api.github.com/repos/{owner}/{repo_name}'
    repo_response = requests.get(repo_url, headers=headers)
    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        if private and (not repo_data.get('private', True)):
            print(f'🔄 Repository {repo_name} is public. Changing to private...')
            update_data = {'private': True}
            update_response = requests.patch(repo_url, headers=headers, json=update_data)
            if update_response.status_code == 200:
                print(f'📝 Successfully changed repository {repo_name} to private')
            else:
                print(f'❌ Failed to change repository {repo_name} to private: {update_response.json()}')

def main():
    parser = argparse.ArgumentParser(description='Create and verify GitHub repositories.')
    parser.add_argument('repos_list', type=str, help='File containing list of repositories to create')
    parser.add_argument('github_owner', type=str, help='GitHub organization owner')
    parser.add_argument('github_token', type=str, help='GitHub token')
    parser.add_argument('private', type=bool, help='Private repository flag')
    args = parser.parse_args()

    with open(args.repos_list, 'r') as file:
        repos = file.readlines()

    for repo in repos:
        repo_name = repo.strip()
        if repo_name:
            create_github_repo(repo_name, args.github_owner, args.github_token, args.private)

if __name__ == '__main__':
    main()
