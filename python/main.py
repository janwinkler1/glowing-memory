import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from github_stats import get_github_repo_stats
from hacker_news import get_top_stories, format_newsletter
from email_sender import send_email_via_gmx
from write_db import write_to_db

# Load environment variables from .env file
load_dotenv()


async def main():
    """
    Main asynchronous function to handle data aggregation and notification.

    Fetches GitHub repository statistics, writes them to a database,
    retrieves top stories from Hacker News, formats these stories into a newsletter,
    and sends the newsletter via email.
    """
    # List of GitHub repositories to fetch statistics for
    repos = [
        "tensorflow/tensorflow",
        "pytorch/pytorch",
        "openai/openai-python",
        "Dataherald/dataherald",
        "langchain-ai/langchain",
    ]

    # Fetch GitHub statistics asynchronously
    github_stats = await get_github_repo_stats(repos)

    # Database connection parameters retrieved from environment variables
    db_params = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST"),
        "port": os.environ.get("DB_PORT"),
    }

    # Write GitHub statistics to the database
    write_to_db(github_stats, db_params)

    # Create an aiohttp session to fetch top stories from Hacker News
    async with aiohttp.ClientSession() as session:
        top_stories = await get_top_stories(session)

    # Format the top stories into a newsletter format
    newsletter = format_newsletter(top_stories)

    # Send the formatted newsletter via email
    send_email_via_gmx(
        "Daily Hacker News Digest", newsletter, os.environ.get("NL_RECEPIENT")
    )


if __name__ == "__main__":
    # Run the main function in an asyncio event loop
    asyncio.run(main())
