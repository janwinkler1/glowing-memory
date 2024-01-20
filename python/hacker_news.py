import aiohttp
import asyncio
from datetime import datetime

async def get_top_stories(session, last_hours=12, top_n=5):
    async with session.get('https://hacker-news.firebaseio.com/v0/topstories.json') as response:
        story_ids = await response.json()

    current_time = datetime.utcnow()
    stories = []

    async def fetch_story(story_id):
        async with session.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json') as story_response:
            story = await story_response.json()
            story_time = datetime.utcfromtimestamp(story.get('time', 0))
            time_diff = current_time - story_time
            if time_diff.total_seconds() <= last_hours * 3600:
                return story

    tasks = [fetch_story(story_id) for story_id in story_ids[:1000]]
    all_stories = await asyncio.gather(*tasks)
    filtered_stories = [story for story in all_stories if story is not None]

    # Sort and pick top n stories
    top_stories = sorted(filtered_stories, key=lambda x: x.get('score', 0), reverse=True)[:top_n]
    return top_stories

def format_newsletter(stories):
    newsletter_content = ""
    for story in stories:
        title = story.get('title', 'No Title')
        url = story.get('url', 'No URL')
        score = story.get('score', 'No Score')
        newsletter_content += f"Title: {title}\nLink: {url}\nScore: {score}\n\n"
    return newsletter_content

