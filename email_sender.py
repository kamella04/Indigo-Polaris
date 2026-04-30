"""Send alert emails when metrics approach thresholds."""

from __future__ import annotations

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

logger = logging.getLogger(__name__)

# Friendly names for metrics in emails
METRIC_NAMES = {
    "youtube_subscribers": "YouTube subscribers",
    #"instagram_followers": "Instagram followers",
    "facebook_followers": "Facebook followers",
    "spotify_followers": "Spotify followers",
}


def send_video_alert(
    video_title: str, video_id: str, current_views: int, target_views: int
) -> bool:
    """
    Send an email alert that a YouTube video is approaching a view milestone.
    Returns True if sent successfully.
    """
    if not config.SMTP_USER or not config.SMTP_PASSWORD or not config.ALERT_EMAILS:
        logger.warning(
            "Email alert skipped because SMTP config is incomplete: user=%s password=%s recipients=%s",
            bool(config.SMTP_USER),
            bool(config.SMTP_PASSWORD),
            bool(config.ALERT_EMAILS),
        )
        return False

    subject = f"Indigo Polaris: \"{video_title}\" approaching {target_views:,} views!"
    body = (
        f"Hello,\n\n"
        f"This is an automated alert from the Indigo Polaris metrics monitor.\n\n"
        f"These YouTube video views are coming closer to {target_views:,}.\n\n"
        f"Video: {video_title}\n"
        f"Link: https://youtu.be/{video_id}\n"
        f"Current views: {current_views:,}\n"
        f"Target: {target_views:,}\n"
        f"Progress: {(current_views / target_views * 100):.1f}%\n\n"
        f"Keep up the great work!\n"
    )

    msg = MIMEMultipart()
    msg["From"] = config.ALERT_FROM_EMAIL
    msg["To"] = ", ".join(config.ALERT_EMAILS)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.sendmail(
                config.ALERT_FROM_EMAIL,
                config.ALERT_EMAILS,
                msg.as_string(),
            )
        return True
    except Exception as exc:
        logger.exception("Failed to send video alert email")
        return False


def send_alert(metric_key: str, current_value: int, threshold: int) -> bool:
    """
    Send an email alert that a metric is approaching its threshold.
    Returns True if sent successfully.
    """
    if not config.SMTP_USER or not config.SMTP_PASSWORD or not config.ALERT_EMAILS:
        logger.warning(
            "Email alert skipped because SMTP config is incomplete: user=%s password=%s recipients=%s",
            bool(config.SMTP_USER),
            bool(config.SMTP_PASSWORD),
            bool(config.ALERT_EMAILS),
        )
        return False

    metric_name = METRIC_NAMES.get(metric_key, metric_key)
    subject = f"Indigo Polaris: {metric_name} approaching {threshold:,}!"

    body = (
        f"Hello,\n\n"
        f"This is an automated alert from the Indigo Polaris metrics monitor.\n\n"
        f"These {metric_name} are coming closer to {threshold:,}.\n\n"
        f"Current value: {current_value:,}\n"
        f"Target threshold: {threshold:,}\n"
        f"Progress: {(current_value / threshold * 100):.1f}%\n\n"
        f"Keep up the great work!\n"
    )

    msg = MIMEMultipart()
    msg["From"] = config.ALERT_FROM_EMAIL
    msg["To"] = ", ".join(config.ALERT_EMAILS)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.sendmail(
                config.ALERT_FROM_EMAIL,
                config.ALERT_EMAILS,
                msg.as_string(),
            )
        return True
    except Exception as exc:
        logger.exception("Failed to send metric alert email")
        return False
