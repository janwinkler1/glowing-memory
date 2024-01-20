import asyncio
from datetime import datetime

async def get_top_stories(session, last_hours=12, top_n=5):
    """
    Asynchronously fetches the top stories from Hacker News within the last specified hours.

    Parameters:
    session (aiohttp.ClientSession): The session used for HTTP requests.
    last_hours (int): Number of hours to look back for top stories. Defaults to 12.
    top_n (int): Number of top stories to return. Defaults to 5.

    Returns:
    list: A list of top stories from Hacker News.
    """
    # Fetching the top story IDs from Hacker News
    async with session.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    ) as response:
        story_ids = await response.json()

    # Define the current time for comparison
    current_time = datetime.utcnow()

    async def fetch_story(story_id):
        """
        Fetches and returns a story if it was posted within the last specified hours.

        Parameters:
        story_id (int): The Hacker News story ID.

        Returns:
        dict or None: The story data if it meets the time criteria, else None.
        """
        async with session.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        ) as story_response:
            story = await story_response.json()
            story_time = datetime.utcfromtimestamp(story.get("time", 0))
            time_diff = current_time - story_time
            # Check if story is within the specified time frame
            if time_diff.total_seconds() <= last_hours * 3600:
                return story

    # Create tasks to fetch stories
    tasks = [fetch_story(story_id) for story_id in story_ids[:1000]]
    all_stories = await asyncio.gather(*tasks)
    filtered_stories = [story for story in all_stories if story is not None]

    # Sort the stories by score and pick the top n stories
    top_stories = sorted(
        filtered_stories, key=lambda x: x.get("score", 0), reverse=True
    )[:top_n]
    return top_stories

def format_newsletter(stories):
    """
    Formats the given stories into a newsletter format.

    Parameters:
    stories (list): A list of Hacker News stories.

    Returns:
    str: A string formatted as a newsletter with the given stories.
    """
    newsletter_content = ""
    for story in stories:
        title = story.get("title", "No Title")
        url = story.get("url", "No URL")
        score = story.get("score", "No Score")
        newsletter_content += f"Title: {title}\nLink: {url}\nScore: {score}\n\n"
    return newsletter_content

