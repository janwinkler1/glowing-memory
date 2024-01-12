import aiohttp
import asyncio
from datetime import datetime
import os

# Your Personal Access Token
github_token = os.get.environ('GITHUB_TOKEN')  # Replace with your actual token

async def get_github_repo_stat(session, repo):
    headers = {'Authorization': f'token {github_token}'}
    github_api_url = f'https://api.github.com/repos/{repo}'
    async with session.get(github_api_url, headers=headers) as response:
        data = await response.json()
        stars = data.get('stargazers_count', 0)
        forks = data.get('forks_count', 0)
        created_at = data.get('created_at')
        last_updated = data.get('updated_at')

        # Formatting datetime for PostgreSQL
        created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ').isoformat() if created_at else None
        last_updated = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ').isoformat() if last_updated else None

        # Fetch latest release info
        async with session.get(github_api_url + '/releases/latest') as release_response:
            release_data = await release_response.json()
            release = release_data.get('tag_name', 'No release data')
            release_date = release_data.get('published_at')

        release_date = datetime.strptime(release_date, '%Y-%m-%dT%H:%M:%SZ').isoformat() if release_date else None

        # Record the request time
        request_time = datetime.now().isoformat()

        return {
            'repository': repo,
            'stars': stars,
            'forks': forks,
            'release': release,
            'release_date': release_date,
            'created_at': created_at, 
            'last_updated': last_updated, 
            'request_time': request_time
        }

async def get_github_repo_stats(repo_list):
    async with aiohttp.ClientSession() as session:
        tasks = [get_github_repo_stat(session, repo) for repo in repo_list]
        return await asyncio.gather(*tasks)
