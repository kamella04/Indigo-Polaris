"""Fetch YouTube channel subscribers and video views via YouTube Data API v3."""

from __future__ import annotations

import config
import requests


def fetch_youtube_subscribers() -> int | None:
    """Fetch subscriber count for the configured YouTube channel."""
    if not config.YOUTUBE_API_KEY or not config.YOUTUBE_CHANNEL_ID:
        return None
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "statistics",
        "id": config.YOUTUBE_CHANNEL_ID,
        "key": config.YOUTUBE_API_KEY,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        if not items:
            return None
        return int(items[0]["statistics"]["subscriberCount"])
    except Exception:
        return None


def fetch_youtube_views() -> int | None:
    """
    Fetch total view count across configured videos, or channel view count
    if no video IDs are set.
    """
    if not config.YOUTUBE_API_KEY:
        return None

    # If specific videos are configured, sum their views
    if config.YOUTUBE_VIDEO_IDS:
        total = 0
        url = "https://www.googleapis.com/youtube/v3/videos"
        # API allows up to 50 IDs per request
        for i in range(0, len(config.YOUTUBE_VIDEO_IDS), 50):
            chunk = config.YOUTUBE_VIDEO_IDS[i : i + 50]
            params = {
                "part": "statistics",
                "id": ",".join(chunk),
                "key": config.YOUTUBE_API_KEY,
            }
            try:
                resp = requests.get(url, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                for item in data.get("items", []):
                    total += int(item["statistics"].get("viewCount", 0))
            except Exception:
                return None
        return total if total > 0 else None

    # Otherwise use channel total view count
    if not config.YOUTUBE_CHANNEL_ID:
        return None
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "statistics",
        "id": config.YOUTUBE_CHANNEL_ID,
        "key": config.YOUTUBE_API_KEY,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        if not items:
            return None
        return int(items[0]["statistics"].get("viewCount", 0))
    except Exception:
        return None
