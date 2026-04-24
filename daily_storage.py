"""
Persistent daily YouTube view counts per video (JSON file on disk).
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime, timezone
from pathlib import Path

# Default: data/youtube_daily_history.json (next to this package)
_DATA_DIR = Path(__file__).resolve().parent / "data"
_DATA_FILE = _DATA_DIR / "youtube_daily_history.json"


def _ensure_parent() -> None:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_store(path: Path | None = None) -> dict:
    p = path or _DATA_FILE
    if not p.exists():
        return {"videos": {}}
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"videos": {}}


def save_store(data: dict, path: Path | None = None) -> None:
    p = path or _DATA_FILE
    _ensure_parent()
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # Avoid accidental credential leaks via file mode; keep readable
    if os.name != "nt":
        try:
            os.chmod(p, 0o600)
        except OSError:
            pass


def merge_today(
    video_id: str,
    title: str,
    views: int,
    on_date: date | None = None,
) -> None:
    """Update or set today's (or on_date) view count for one video."""
    d = on_date or datetime.now().date()
    key = d.isoformat()
    store = load_store()
    videos = store.setdefault("videos", {})
    entry = videos.setdefault(video_id, {"title": title, "by_date": {}})
    entry["title"] = title
    by_date = entry.setdefault("by_date", {})
    by_date[key] = views
    store["meta"] = {
        "last_run": datetime.now(timezone.utc).isoformat(),
    }
    save_store(store)


def merge_snapshot_from_api(rows: list[dict]) -> None:
    """rows: list of {video_id, title, views} from fetcher."""
    store = load_store()
    d = datetime.now().date().isoformat()
    videos = store.setdefault("videos", {})
    for r in rows:
        vid = r["video_id"]
        title = r["title"]
        views = r["views"]
        entry = videos.setdefault(vid, {"title": title, "by_date": {}})
        entry["title"] = title
        entry["by_date"][d] = views
    store["meta"] = {
        "last_run": datetime.now(timezone.utc).isoformat(),
    }
    save_store(store)
