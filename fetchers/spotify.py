"""
Fetch Spotify artist metrics via Spotify Web API.
Note: The public API provides follower count. Monthly listeners would require
Spotify for Artists / Spotify Analytics API (different auth). Using followers
as the closest available metric.
"""

from __future__ import annotations

import base64

import config
import requests


def _get_spotify_token() -> str | None:
    """Get Spotify API access token using client credentials flow."""
    if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
        return None
    url = "https://accounts.spotify.com/api/token"
    auth = base64.b64encode(
        f"{config.SPOTIFY_CLIENT_ID}:{config.SPOTIFY_CLIENT_SECRET}".encode()
    ).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    try:
        resp = requests.post(url, headers=headers, data=data, timeout=10)
        resp.raise_for_status()
        return resp.json()["access_token"]
    except Exception:
        return None


def fetch_spotify_followers() -> int | None:
    """
    Fetch follower count for the configured Spotify artist.
    Requires SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.
    """
    if not config.SPOTIFY_ARTIST_ID:
        return None
    token = _get_spotify_token()
    if not token:
        return None
    url = f"https://api.spotify.com/v1/artists/{config.SPOTIFY_ARTIST_ID}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return int(data.get("followers", {}).get("total", 0))
    except Exception:
        return None
