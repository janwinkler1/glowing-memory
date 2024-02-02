import aiohttp
import asyncio
from datetime import datetime
import os

# Retrieve the GitHub Personal Access Token from environment variables
github_token = os.environ.get("GITHUB_TOKEN")


async def get_github_repo_stat(session, repo):
    """
    Asynchronously fetches statistics for a single GitHub repository.

    Parameters:
    session (aiohttp.ClientSession): The HTTP client session for making requests.
    repo (str): The full name of the repository (e.g., 'username/reponame').

    Returns:
    dict: A dictionary containing various statistics about the repository.
    """
    # Header for GitHub API, including the authorization token
    headers = {"Authorization": f"token {github_token}"}
    github_api_url = f"https://api.github.com/repos/{repo}"

    # Asynchronous HTTP GET request to fetch repository data
    async with session.get(github_api_url, headers=headers) as response:
        data = await response.json()
        stars = data.get("stargazers_count", 0)
        forks = data.get("forks_count", 0)
        created_at = data.get("created_at")
        last_updated = data.get("updated_at")

        # Formatting datetime for PostgreSQL compatibility
        created_at = (
            datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").isoformat()
            if created_at
            else None
        )
        last_updated = (
            datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%SZ").isoformat()
            if last_updated
            else None
        )

        # Fetch the latest release information for the repository
        async with session.get(github_api_url + "/releases/latest") as release_response:
            release_data = await release_response.json()
            release = release_data.get("tag_name", "No release data")
            release_date = release_data.get("published_at")

        release_date = (
            datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%SZ").isoformat()
            if release_date
            else None
        )

        # Record the time of the request
        request_time = datetime.now().isoformat()

        # Return a dictionary of repository statistics and metadata
        return {
            "repository": repo,
            "stars": stars,
            "forks": forks,
            "release": release,
            "release_date": release_date,
            "created_at": created_at,
            "last_updated": last_updated,
            "request_time": request_time,
        }


async def get_github_repo_stats(repo_list):
    """
    Asynchronously fetches statistics for a list of GitHub repositories.

    Parameters:
    repo_list (list): A list of repository names to fetch statistics for.

    Returns:
    list: A list of dictionaries containing statistics for each repository.
    """
    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Create a list of asynchronous tasks for each repository
        tasks = [get_github_repo_stat(session, repo) for repo in repo_list]
        # Gather and return the results of all tasks
        return await asyncio.gather(*tasks)
