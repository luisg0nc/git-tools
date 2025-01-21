# GitLab to GitHub Migration Script

## Description

This script migrates repositories from a GitLab organization to a GitHub organization. It performs the following steps for each repository:
1. Constructs the GitLab and GitHub repository URLs based on the provided organization/user names and repository name.
2. Checks if the repository directory already exists locally.
    - If it exists, fetches updates from the GitLab remote.
    - If it does not exist, clones the repository from GitLab.
3. Adds GitHub as a new remote to the local repository.
4. Pushes the repository to GitHub with the mirror option to ensure all refs are copied.

## Prerequisites

- Python 3.x
- `GitPython` library

## Installation

1. Clone this repository to your local machine.
2. Install the required Python library:

```sh
pip install gitpython
```

## Usage

1. Create a text file containing the list of repositories to migrate, one repository name per line.
2. Run the script with the following command:


```sh
python lab-to-hub.py <repos_list_file> <gitlab_org> <github_org>
```

 - `<repos_list_file>`: Path to the file containing the list of repositories to migrate.
 - `<gitlab_org>`: The GitLab organization or user name.
 - `<github_org>`: The GitHub organization or user name.

### Example

 ```sh
 python lab-to-hub.py repos.txt my-gitlab-org my-github-org
 ```


## Script Details

### `migrate_repository(repo_name, gitlab_org, github_org)`

Migrates a repository from GitLab to GitHub.

**Args:**
- `repo_name` (str): The name of the repository to migrate.
- `gitlab_org` (str): The GitLab organization or user name.
- `github_org` (str): The GitHub organization or user name.

**Raises:**
- `GitCommandError`: If there is an error during the Git operations.

### `parse_arguments()`

Parses command-line arguments.

**Returns:**
- Parsed arguments.

### `main()`

Main function that reads the list of repositories and calls `migrate_repository` for each repository.

## Error Handling

If there is an error during the Git operations, the script will print an error message and continue with the next repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Luis Goncalves

## Date

2025-01-21
