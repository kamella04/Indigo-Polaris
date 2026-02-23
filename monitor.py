"""
Indigo Polaris Metrics Monitor

Checks YouTube, Instagram, Facebook, and Spotify metrics periodically.
Sends email alerts when any metric gets close to its configured threshold.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import config
from email_sender import send_alert
from fetchers import (
    fetch_facebook_followers,
    fetch_instagram_followers,
    fetch_spotify_listeners,
    fetch_youtube_subscribers,
    fetch_youtube_views,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Track which alerts we've already sent to avoid spamming
ALERTS_SENT_FILE = Path(__file__).parent / ".alerts_sent.json"


def load_sent_alerts() -> set[str]:
    """Load the set of (metric_key, threshold) alerts we've already sent."""
    try:
        data = json.loads(ALERTS_SENT_FILE.read_text())
        return set(tuple(x) for x in data)
    except Exception:
        return set()


def save_sent_alert(metric_key: str, threshold: int) -> None:
    """Record that we sent an alert for this metric/threshold."""
    sent = load_sent_alerts()
    sent.add((metric_key, threshold))
    ALERTS_SENT_FILE.write_text(
        json.dumps([list(x) for x in sent], indent=2)
    )


def is_near_threshold(current: int | None, threshold: int) -> bool:
    """True if current is within PROXIMITY_PERCENT of threshold."""
    if current is None or threshold <= 0:
        return False
    pct = config.PROXIMITY_PERCENT / 100
    # Alert when current >= threshold * (1 - proximity)
    return current >= threshold * (1 - pct)


def run_check() -> None:
    """Fetch all metrics, check thresholds, and send alerts if needed."""
    fetchers = {
        "youtube_views": fetch_youtube_views,
        "youtube_subscribers": fetch_youtube_subscribers,
        "instagram_followers": fetch_instagram_followers,
        "facebook_followers": fetch_facebook_followers,
        "spotify_listeners": fetch_spotify_listeners,
    }

    sent_alerts = load_sent_alerts()

    for metric_key, fetch_fn in fetchers.items():
        threshold = config.THRESHOLDS.get(metric_key)
        if threshold is None:
            continue

        current = fetch_fn()
        if current is not None:
            logger.info(f"{metric_key}: {current:,} (threshold: {threshold:,})")

        if is_near_threshold(current, threshold):
            alert_key = (metric_key, threshold)
            if alert_key in sent_alerts:
                logger.debug(f"Alert already sent for {metric_key}, skipping")
                continue

            if send_alert(metric_key, current or 0, threshold):
                logger.info(f"Alert sent: {metric_key} approaching {threshold:,}")
                save_sent_alert(metric_key, threshold)
            else:
                logger.warning(f"Failed to send alert for {metric_key}")


def main() -> None:
    """Run checks on a schedule."""
    logger.info("Indigo Polaris Metrics Monitor started")
    logger.info(f"Check interval: {config.CHECK_INTERVAL_MINUTES} minutes")
    logger.info(f"Recipients: {config.ALERT_EMAILS}")

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
