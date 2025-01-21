# GitHub Mass Repository Creation

## Description

This script creates GitHub repositories in a specified organization. It handles existing repositories and rate limiting.

## Prerequisites

- Python 3.x
- `requests` library

## Installation

1. Clone this repository to your local machine.
2. Install the required Python library:

    ```sh
    pip install requests
    ```

## Usage

Run the script with the following command:

```sh
python create_repos.py <repo_name> <owner> <token> <private>
```

- `<repo_name>`: The name of the repository to create.
- `<owner>`: The name of the organization that will own the repository.
- `<token>`: The GitHub personal access token for authentication.
- `<private>`: Whether the repository should be private (True/False).

### Example

```sh
python create_repos.py my-repo my-org my-token True
```

## Script Details

### `create_github_repo(repo_name, owner, token, private)`

Creates a GitHub repository in the specified organization.

**Args:**
- `repo_name` (str): The name of the repository to create.
- `owner` (str): The name of the organization that will own the repository.
- `token` (str): The GitHub personal access token for authentication.
- `private` (bool): Whether the repository should be private.

**Returns:**
- None

**Raises:**
- `Exception`: If the repository creation fails for reasons other than rate limiting or existing repository.

This function attempts to create a new repository in the specified GitHub organization using the provided personal access token for authentication. If the repository already exists, it calls the `handle_existing_repo` function to handle the existing repository. If the rate limit is exceeded, it waits until the rate limit resets before retrying. If the repository creation fails for other reasons, it prints an error message and exits.

## Error Handling

If there is an error during the repository creation, the script will print an error message and exit.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Luis Goncalves

## Date

2025-01-21
