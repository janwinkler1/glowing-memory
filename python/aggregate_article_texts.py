from newspaper import Article

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
        try:
            article_obj = Article(article['url'])
            article_obj.download()
            article_obj.parse()
            # Limit the text of each article to `text_limit` characters to keep it concise
            aggregated_texts.append(article_obj.text[:text_limit])
        except Exception as e:
            print(f"Error fetching article from {article['url']}: {e}")
            # Optionally, handle specific exceptions (e.g., download or parse failures)

    # Join all texts into a single string for summarization
    return " ".join(aggregated_texts)
