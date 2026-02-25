"""Fetch Instagram follower count via Instagram Graph API (Meta)."""

from __future__ import annotations

import config
import requests


'''
def fetch_instagram_followers() -> int | None:
    """
    Fetch follower count for the configured Instagram Business/Creator account.
    Requires INSTAGRAM_ACCESS_TOKEN from Meta Developer App.
    """
    if not config.INSTAGRAM_ACCESS_TOKEN or not config.INSTAGRAM_USER_ID:
        return None
    url = f"https://graph.instagram.com/{config.INSTAGRAM_USER_ID}"
    params = {
        "fields": "followers_count",
        "access_token": config.INSTAGRAM_ACCESS_TOKEN,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return int(data.get("followers_count", 0))
    except Exception:
        return None
'''
