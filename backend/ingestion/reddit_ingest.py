import os
from typing import Any

import praw
from dotenv import load_dotenv

load_dotenv()

SUBREDDITS = [
    "ChatGPT",
    "OpenAI",
    "LocalLLaMA",
    "artificial",
    "singularity",
]


def _reddit_client() -> praw.Reddit:
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "Missing Reddit credentials. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in backend/.env."
        )

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="ai-risk-intelligence-platform/0.1 by portfolio-demo",
    )


def fetch_reddit_posts(limit: int = 5) -> list[dict[str, Any]]:
    reddit = _reddit_client()
    posts: list[dict[str, Any]] = []

    for subreddit_name in SUBREDDITS:
        subreddit = reddit.subreddit(subreddit_name)

        for submission in subreddit.new(limit=limit):
            posts.append(
                {
                    "id": submission.id,
                    "subreddit": subreddit_name,
                    "title": submission.title,
                    "body": submission.selftext or "",
                    "url": f"https://www.reddit.com{submission.permalink}",
                    "score": submission.score,
                    "created_utc": submission.created_utc,
                }
            )

    return posts
