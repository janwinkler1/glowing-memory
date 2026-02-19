![CI](https://github.com/janwinkler1/digestif/actions/workflows/ci.yml/badge.svg)

# digestif

A gloriously over-engineered daily newsletter digest.

It fetches top stories from [Hacker News](https://news.ycombinator.com) and
[Lobste.rs](https://lobste.rs), scrapes the linked articles, runs them through a
free tier Mistral LLM to produce a short summary of the top stories, formats everything into an HTML
email and sends it via [Resend](https://resend.com).

Yes, this is massive overkill. This is why i added Github Actions for a simple CI and renovateBot to keep dependencies up to date.

## What it does

1. Fetches top stories from HN and Lobsters (async, naturally)
1. Scrapes and truncates the linked article text
1. Generates AI summaries via the Mistral API
1. Formats a styled HTML newsletter
1. Emails it to you

## Configuration

Set the following environment variables:

| Variable | Description |
|---|---|
| `MISTRAL_API_KEY` | Your Mistral API key |
| `RESEND_API_KEY` | Your Resend API key |
| `NL_RECIPIENT` | Recipient email address |
| `SELECTION_MODE` | `top` (default) or `random` |

## Build

```
docker compose build
docker compose up -d
docker compose exec app python /app/src/main.py
```

## Formatting and Linting

```
ruff format
ruff check --fix
```

## Tests

```
uv run pytest
```
