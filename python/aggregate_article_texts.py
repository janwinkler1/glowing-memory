import logging
from newspaper import Article

logger = logging.getLogger("newsletter.aggregate")

def aggregate_article_texts(articles, text_limit=4000):
    """
    Fetches and aggregates text from a list of article URLs.

    Parameters:
    articles (list): A list of dictionaries, each containing the 'url' of an article.
    text_limit (int): Maximum number of characters to include from each article.

    Returns:
    str: Aggregated text from all articles, up to `text_limit` characters each.
    """
    aggregated_texts = []

    for article in articles:
        url = article.get('url', 'unknown')
        try:
            logger.info("Downloading article: %s", url)
            article_obj = Article(url)
            article_obj.download()
            article_obj.parse()
            text_len = len(article_obj.text)
            aggregated_texts.append(article_obj.text[:text_limit])
            logger.info("Parsed article (%d chars, limited to %d): %s", text_len, text_limit, url)
        except Exception as e:
            logger.error("Error fetching article from %s: %s", url, e)

    logger.info("Aggregated %d articles", len(aggregated_texts))
    return " ".join(aggregated_texts)
