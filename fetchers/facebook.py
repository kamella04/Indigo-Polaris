"""Fetch Facebook Page follower count via Facebook Graph API."""

from __future__ import annotations

import config
import requests


def fetch_facebook_followers() -> int | None:
    """
    Fetch follower count for the configured Facebook Page.
    Requires FACEBOOK_ACCESS_TOKEN with pages_read_engagement permission.
    """
    if not config.FACEBOOK_ACCESS_TOKEN or not config.FACEBOOK_PAGE_ID:
        return None
    url = f"https://graph.facebook.com/v18.0/{config.FACEBOOK_PAGE_ID}"
    params = {
        "fields": "followers_count",
        "access_token": config.FACEBOOK_ACCESS_TOKEN,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return int(data.get("followers_count", 0))
    except Exception:
        return None
