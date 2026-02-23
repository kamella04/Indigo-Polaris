"""Send alert emails when metrics approach thresholds."""

from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


# Friendly names for metrics in emails
METRIC_NAMES = {
    "youtube_views": "YouTube video views",
    "youtube_subscribers": "YouTube subscribers",
    "instagram_followers": "Instagram followers",
    "facebook_followers": "Facebook followers",
    "spotify_listeners": "Spotify monthly listeners",
}


def send_alert(metric_key: str, current_value: int, threshold: int) -> bool:
    """
    Send an email alert that a metric is approaching its threshold.
    Returns True if sent successfully.
    """
    if not config.SMTP_USER or not config.SMTP_PASSWORD or not config.ALERT_EMAILS:
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
    except Exception:
        return False
