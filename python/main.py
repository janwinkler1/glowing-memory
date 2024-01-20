import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from github_stats import get_github_repo_stats
from hacker_news import get_top_stories, format_newsletter
from email_sender import send_email_via_gmx
from write_db import write_to_db

load_dotenv()


async def main():
    # List of GitHub repositories
    repos = ['tensorflow/tensorflow', 'pytorch/pytorch', 'openai/openai-python', 'Dataherald/dataherald', 'langchain-ai/langchain']
    
    # Fetch GitHub statistics
    github_stats = await get_github_repo_stats(repos)
    
    # Database connection parameters
    db_params = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),  # Replace with your username
        'password': os.environ.get('DB_PASSWORD'),  # Replace with your password
        'host': os.environ.get('DB_HOST'),  # Replace with your database host
        'port': os.environ.get('DB_PORT')  # Replace with your database port
    }

    # Write GitHub statistics to the database
    write_to_db(github_stats, db_params)

    # Rest of your existing code for fetching top stories and sending email
    async with aiohttp.ClientSession() as session:
        top_stories = await get_top_stories(session)
    
    newsletter = format_newsletter(top_stories)
    send_email_via_gmx("Daily Hacker News Digest", newsletter, os.environ.get('NL_RECEPIENT'))

if __name__ == "__main__":
    asyncio.run(main())
