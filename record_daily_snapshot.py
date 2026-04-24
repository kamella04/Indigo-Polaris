"""
Run once per day (e.g. end of day) to save YouTube view counts for all
videos listed in config.YOUTUBE_VIDEOS. Used by the stats website.

  python record_daily_snapshot.py
"""

from __future__ import annotations

import sys

import config
from daily_storage import merge_snapshot_from_api
from fetchers.youtube import fetch_youtube_video_stats


def main() -> int:
    if not config.YOUTUBE_API_KEY or not (getattr(config, "YOUTUBE_VIDEOS", None) or []):
        print("YOUTUBE_API_KEY and YOUTUBE_VIDEOS must be set in config / .env", file=sys.stderr)
        return 1
    rows = fetch_youtube_video_stats()
    if not rows:
        print("No video stats returned (check API key and video IDs).", file=sys.stderr)
        return 1
    out = [
        {
            "video_id": s["video_id"],
            "title": s["title"],
            "views": s["views"],
        }
        for s in rows
    ]
    merge_snapshot_from_api(out)
    print(f"Saved daily snapshot for {len(out)} video(s) for today.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
