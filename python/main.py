import asyncio
import os
from dotenv import load_dotenv
import aiohttp
import random
from aggregate_article_texts import aggregate_article_texts
from generate_exec_summary_gpt_turbo import generate_executive_summary_gpt_turbo
from get_top_stories_hn import get_top_stories_hn
from get_top_stories_lobsters import get_top_stories_lobsters
from format_newsletter import format_newsletter_generic, create_html_newsletter
from send_email_via_gmx import send_email_via_gmx


load_dotenv()

async def main():
    selection_mode = os.environ.get("SELECTION_MODE", "top")

    async with aiohttp.ClientSession() as session:
        hn_stories = await get_top_stories_hn(session)
        lobsters_stories = await get_top_stories_lobsters(session)

    # Depending on the selection_mode, select stories
    if selection_mode == "random":
        selected_hn_stories = random.sample(hn_stories, min(len(hn_stories), 5))
        selected_lobsters_stories = random.sample(lobsters_stories, min(len(lobsters_stories), 5))
    elif selection_mode == "top":
        selected_hn_stories = hn_stories[:1]
        selected_lobsters_stories = lobsters_stories[:1]

    aggregated_hn = aggregate_article_texts(selected_hn_stories)
    aggregated_lobsters = aggregate_article_texts(selected_lobsters_stories)
    summary_hn = generate_executive_summary_gpt_turbo(aggregated_hn)
    summary_lobsters = generate_executive_summary_gpt_turbo(aggregated_lobsters)

    newsletter_html = create_html_newsletter(summary_hn, summary_lobsters, hn_stories, lobsters_stories)
    send_email_via_gmx("Daily Digest with Summary", newsletter_html, os.environ.get("NL_RECIPIENT"), html=True)

if __name__ == "__main__":
    asyncio.run(main())

