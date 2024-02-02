import asyncio
import os
from dotenv import load_dotenv
import aiohttp
import random
# Import new functionality
from aggregate_article_texts import aggregate_article_texts
from generate_exec_summary_gpt_turbo import generate_executive_summary_gpt_turbo
from get_top_stories_hn import get_top_stories_hn
from get_top_stories_lobsters import get_top_stories_lobsters
from get_github_repo_stats import get_github_repo_stats
# Assuming you've refactored format_newsletter to be more generic
from format_newsletter import format_newsletter_generic, create_html_newsletter
from send_email_via_gmx import send_email_via_gmx
from write_to_db import write_to_db


load_dotenv()

async def main():
    selection_mode = os.environ.get("SELECTION_MODE", "top")
    # Initialize aiohttp session for all HTTP requests
    
    # List of GitHub repositories to fetch statistics for
    repos = [
        "tensorflow/tensorflow",
        "pytorch/pytorch",
        "openai/openai-python",
        "Dataherald/dataherald",
        "langchain-ai/langchain",
    ]
    # Database connection parameters retrieved from environment variables
    db_params = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST"),
        "port": os.environ.get("DB_PORT"),
    }
    async with aiohttp.ClientSession() as session:
        # Fetch GitHub stats, Hacker News, and Lobsters stories
        github_stats = await get_github_repo_stats(repos)
        hn_stories = await get_top_stories_hn(session)
        lobsters_stories = await get_top_stories_lobsters(session)
        
        # Combine and format stories from both sources
        #combined_stories = hn_stories + lobsters_stories  # Assuming you adjust your data structure accordingly
        #newsletter = format_newsletter_generic(combined_stories)
    

    # Depending on the selection_mode, select stories
    if selection_mode == "random":
        selected_hn_stories = random.sample(hn_stories, min(len(hn_stories), 5))
        selected_lobsters_stories = random.sample(lobsters_stories, min(len(lobsters_stories), 5))
    elif selection_mode == "top":
        selected_hn_stories = hn_stories[:1]  # Assuming stories are already sorted
        selected_lobsters_stories = lobsters_stories[:1]    
    # Aggregate texts and generate summary (optional)
    aggregated_hn = aggregate_article_texts(selected_hn_stories)
    aggregated_lobsters = aggregate_article_texts(selected_lobsters_stories)
    summary_hn = generate_executive_summary_gpt_turbo(aggregated_hn)
    summary_lobsters = generate_executive_summary_gpt_turbo(aggregated_lobsters)


    newsletter_html = create_html_newsletter(summary_hn, summary_lobsters, hn_stories, lobsters_stories)
    # Include summary in the newsletter (optional)
    #newsletter += "\nExecutive Summary:\n" + summary
        
    # Database and Email operations remain similar
    write_to_db(github_stats, db_params)
    send_email_via_gmx("Daily Digest with Summary", newsletter_html, os.environ.get("NL_RECIPIENT"),html=True)

if __name__ == "__main__":
    asyncio.run(main())

