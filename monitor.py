"""
Indigo Polaris Metrics Monitor

Checks YouTube videos, subscribers, Instagram, Facebook, and Spotify followers periodically.
Sends email alerts when any metric gets close to its checkpoint.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import config
from email_sender import send_alert, send_video_alert
from followers_checkpoints import (
    get_next_follower_checkpoint,
    should_alert_followers,
)
from fetchers import (
    fetch_facebook_followers,
    #fetch_instagram_followers,
    fetch_youtube_subscribers,
    fetch_youtube_video_stats,
    fetch_spotify_followers,
)
from video_checkpoints import (
    get_next_checkpoint,
    is_new_video,
    should_alert,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

ALERTS_SENT_FILE = Path(__file__).parent / ".alerts_sent.json"


def load_sent_alerts() -> set[tuple]:
    """Load the set of alert keys we've already sent. Keys are tuples for JSON compat."""
    try:
        data = json.loads(ALERTS_SENT_FILE.read_text())
        return set(tuple(x) for x in data)
    except Exception:
        return set()


def save_sent_alert(alert_key: tuple) -> None:
    """Record that we sent an alert."""
    sent = load_sent_alerts()
    sent.add(alert_key)
    ALERTS_SENT_FILE.write_text(json.dumps([list(x) for x in sent], indent=2))


def run_check() -> None:
    """Fetch all metrics, check thresholds, and send alerts if needed."""
    logger.info(f"SMTP host: {config.SMTP_HOST}")
    logger.info(f"SMTP user configured: {'yes' if config.SMTP_USER else 'no'}")
    logger.info(f"ALERT_FROM_EMAIL configured: {'yes' if config.ALERT_FROM_EMAIL else 'no'}")
    sent_alerts = load_sent_alerts()

    # --- YouTube videos (per-video checkpoint logic) ---
    videos = getattr(config, "YOUTUBE_VIDEOS", None) or []
    if videos and config.YOUTUBE_API_KEY:
        for stats in fetch_youtube_video_stats():
            video_id = stats["video_id"]
            title = stats["title"]
            views = stats["views"]
            published_at = stats["published_at"]

            is_new = is_new_video(published_at)
            cp = get_next_checkpoint(views, is_new)
            if cp is None:
                continue

            target, proximity = cp.target, cp.proximity
            alert_key = ("video", video_id, target)
            if alert_key in sent_alerts:
                continue

            if should_alert(views, target, proximity):
                logger.info(
                    f"Video \"{title}\": {views:,} views, approaching {target:,} "
                    f"(within {proximity:,})"
                )
                if send_video_alert(title, video_id, views, target):
                    save_sent_alert(alert_key)
                    logger.info(f"Alert sent: \"{title}\" approaching {target:,} views")
                else:
                    logger.warning(f"Failed to send alert for \"{title}\"")

    # --- Follower metrics (YouTube, Instagram, Facebook, Spotify) ---
    # Checkpoints: under 1M = every 100k (5k left), over 1M = every 1M (15k left)
    fetchers = {
        "youtube_subscribers": fetch_youtube_subscribers,
        #"instagram_followers": fetch_instagram_followers,
        "facebook_followers": fetch_facebook_followers,
        "spotify_followers": fetch_spotify_followers,
    }

    for metric_key, fetch_fn in fetchers.items():
        current = fetch_fn()
        if current is None:
            continue

        cp = get_next_follower_checkpoint(current)
        if cp is None:
            continue

        target, proximity = cp.target, cp.proximity
        alert_key = (metric_key, target)
        if alert_key in sent_alerts:
            continue

        if should_alert_followers(current, target, proximity):
            logger.info(
                f"{metric_key}: {current:,}, approaching {target:,} "
                f"(within {proximity:,})"
            )
            if send_alert(metric_key, current, target):
                save_sent_alert(alert_key)
                logger.info(f"Alert sent: {metric_key} approaching {target:,}")
            else:
                logger.warning(f"Failed to send alert for {metric_key}")


def main() -> None:
    """Run checks on a schedule."""
    logger.info("Indigo Polaris Metrics Monitor started")
    logger.info(f"Check interval: {config.CHECK_INTERVAL_MINUTES} minutes")
    logger.info(f"Recipients: {config.ALERT_EMAILS}")
    logger.info(f"SMTP host: {config.SMTP_HOST}")
    logger.info(f"SMTP user configured: {'yes' if config.SMTP_USER else 'no'}")
    logger.info(f"ALERT_FROM_EMAIL configured: {'yes' if config.ALERT_FROM_EMAIL else 'no'}")
    logger.info(f"Tracking {len(getattr(config, 'YOUTUBE_VIDEOS', []) or [])} YouTube videos")

    while True:
        try:
            run_check()
        except Exception as e:
            logger.exception(f"Check failed: {e}")

        interval_seconds = config.CHECK_INTERVAL_MINUTES * 60
        logger.info(f"Next check in {config.CHECK_INTERVAL_MINUTES} minutes")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    main()
