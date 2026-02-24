"""Fetch YouTube channel subscribers and video views via YouTube Data API v3."""

from __future__ import annotations

from datetime import datetime
from typing import TypedDict

import config
import requests


class VideoStats(TypedDict):
    video_id: str
    title: str
    views: int
    published_at: datetime


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


def fetch_youtube_video_stats() -> list[VideoStats]:
    """
    Fetch view count and publish date for each configured video.
    Returns list of {video_id, title, views, published_at}.
    """
    videos = getattr(config, "YOUTUBE_VIDEOS", None) or []
    if not config.YOUTUBE_API_KEY or not videos:
        return []

    video_ids = [v["id"] for v in videos]
    title_by_id = {v["id"]: v.get("title", "Unknown") for v in videos}
    result: list[VideoStats] = []

    url = "https://www.googleapis.com/youtube/v3/videos"
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i : i + 50]
        params = {
            "part": "statistics,snippet",
            "id": ",".join(chunk),
            "key": config.YOUTUBE_API_KEY,
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("items", []):
                vid = item["id"]
                stats = item.get("statistics", {})
                snippet = item.get("snippet", {})
                published_str = snippet.get("publishedAt", "")
                try:
                    published_at = datetime.fromisoformat(
                        published_str.replace("Z", "+00:00")
                    )
                except Exception:
                    published_at = datetime.min
                result.append(
                    {
                        "video_id": vid,
                        "title": title_by_id.get(vid, snippet.get("title", "Unknown")),
                        "views": int(stats.get("viewCount", 0)),
                        "published_at": published_at,
                    }
                )
        except Exception:
            pass
    return result


def fetch_youtube_views() -> int | None:
    """
    Fetch total view count across configured videos.
    Kept for backward compatibility; prefer fetch_youtube_video_stats for per-video tracking.
    """
    stats = fetch_youtube_video_stats()
    if not stats:
        return None
    return sum(s["views"] for s in stats)
