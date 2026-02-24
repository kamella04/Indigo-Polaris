"""
Configuration for the Indigo Polaris metrics monitor.
Edit thresholds and recipient emails here.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# RECIPIENT EMAILS - Who receives the alerts
# =============================================================================
ALERT_EMAILS = [
    "recipient1@example.com",
    "recipient2@example.com",
]

# =============================================================================
# Follower metrics (YouTube, Instagram, Facebook) use checkpoint rules:
# Under 1M: every 100k, notify when 5k left. Over 1M: every 1M, notify when 15k left.
# =============================================================================

# =============================================================================
# PLATFORM IDs - Your channel/page/artist identifiers
# =============================================================================
YOUTUBE_CHANNEL_ID = "UCWBhkwRP-zQy194ZhzlMTTA"

# YouTube videos to track for view milestones. Format: {"id": "video_id", "title": "Video Title"}
YOUTUBE_VIDEOS = [
    {"id": "nM5KfGltl8g", "title": "Đi về thôi"},
    {"id": "cxa58jMyGxI", "title": "Sairoi"},
    {"id": "_kqhp2PwXQM", "title": "You know"},
    {"id": "X-atPgZWZHo", "title": "Lonely in Dalat"},
]
INSTAGRAM_USER_ID = "2041951224"
FACEBOOK_PAGE_ID = "100063766702292"

# =============================================================================
# EMAIL (SMTP) SETTINGS - For sending alerts
# =============================================================================
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")      # Your email
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # App password, not regular password
ALERT_FROM_EMAIL = os.getenv("ALERT_FROM_EMAIL", SMTP_USER)

# =============================================================================
# API KEYS - Load from environment variables (never commit real keys!)
# =============================================================================
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN", "")

# =============================================================================
# SCHEDULE - How often to check (in minutes)
# =============================================================================
CHECK_INTERVAL_MINUTES = 60
