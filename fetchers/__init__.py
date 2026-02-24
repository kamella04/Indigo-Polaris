"""Platform metric fetchers."""

from .youtube import (
    fetch_youtube_subscribers,
    fetch_youtube_video_stats,
    fetch_youtube_views,
)
from .instagram import fetch_instagram_followers
from .facebook import fetch_facebook_followers

__all__ = [
    "fetch_youtube_subscribers",
    "fetch_youtube_video_stats",
    "fetch_youtube_views",
    "fetch_instagram_followers",
    "fetch_facebook_followers",
]
