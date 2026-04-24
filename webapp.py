"""
Local website: daily YouTube views per video and day-over-day growth.

  pip install -r requirements.txt
  python webapp.py
  Open http://127.0.0.1:5000
"""

from __future__ import annotations

import os
from datetime import date, timedelta

from flask import Flask, render_template

import daily_storage

app = Flask(__name__)


def _rows_for_table_from_store(store: dict) -> list[dict]:
    videos: dict = store.get("videos", {})
    rows: list[dict] = []
    for video_id, entry in videos.items():
        by_date: dict = entry.get("by_date") or {}
        if not by_date:
            continue
        dates_sorted = sorted(by_date.keys())
        latest = dates_sorted[-1]
        views_now = by_date[latest]
        growth_1d = None
        if len(dates_sorted) >= 2:
            prev = dates_sorted[-2]
            growth_1d = views_now - by_date[prev]
        # growth vs 7 days ago (same calendar comparison)
        growth_7d = None
        try:
            latest_d = date.fromisoformat(latest)
            target = (latest_d - timedelta(days=7)).isoformat()
            if target in by_date:
                growth_7d = views_now - by_date[target]
        except Exception:
            pass
        rows.append(
            {
                "video_id": video_id,
                "title": entry.get("title", "—"),
                "latest_date": latest,
                "views": views_now,
                "growth_1d": growth_1d,
                "growth_7d": growth_7d,
            }
        )
    rows.sort(key=lambda r: r["views"], reverse=True)
    return rows


@app.route("/")
def index():
    store = daily_storage.load_store()
    rows = _rows_for_table_from_store(store)
    meta = store.get("meta", {})
    return render_template(
        "index.html",
        rows=rows,
        last_run=meta.get("last_run"),
    )


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
