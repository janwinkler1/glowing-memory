# digestif

A gloriously over-engineered daily newsletter digest.

It fetches top stories from [Hacker News](https://news.ycombinator.com) and
[Lobste.rs](https://lobste.rs), scrapes the linked articles, runs them through a
free tier Mistral LLM to produce a short summary of the top stories, formats everything into an HTML
email and sends it via [Resend](https://resend.com).

Yes, this is massive overkill.

## What it does

1. Fetches top stories from HN and Lobsters (async, naturally)
2. Scrapes and truncates the linked article text
3. Generates AI summaries via the Mistral API
4. Formats a styled HTML newsletter
5. Emails it to you

## Configuration

Set the following environment variables:

| Variable | Description |
|---|---|
| `MISTRAL_API_KEY` | Your Mistral API key |
| `RESEND_API_KEY` | Your Resend API key |
| `NL_RECIPIENT` | Recipient email address |
| `SELECTION_MODE` | `top` (default) or `random` |

## Running

```bash
uv run src/main.py
```

A GitHub Actions workflow is included to run this on a schedule. Also, I use renovate to keep dependencies up-to-date.
