from datetime import datetime, timezone, timedelta

async def get_top_stories_lobsters(session, last_hours=12, top_n=5):
    """
    Asynchronously fetches the top stories from Lobsters within the last specified hours.

    Parameters:
    session (aiohttp.ClientSession): The session used for HTTP requests.
    last_hours (int): Number of hours to look back for top stories. Defaults to 12.
    top_n (int): Number of top stories to return. Defaults to 5.

    Returns:
    list: A list of top stories from Lobsters.
    """
    async with session.get("https://lobste.rs/hottest.json") as response:
        stories = await response.json()

    current_time = datetime.now(timezone.utc)

    # Convert Lobsters' created_at to datetime and filter stories
    def filter_stories(story):
        story_time = datetime.fromisoformat(story['created_at'].rstrip('Z'))
        return current_time - story_time < timedelta(hours=last_hours)

    filtered_stories = filter(filter_stories, stories)

    # Sort and select top N stories based on score
    top_stories = sorted(filtered_stories, key=lambda x: x['score'], reverse=True)[:top_n]

    return top_stories

