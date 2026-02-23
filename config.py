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
# THRESHOLDS - Alert when metric gets within PROXIMITY_PERCENT of these values
# =============================================================================
THRESHOLDS = {
    "youtube_views": 1_000_000,       # e.g., 1M video views
    "youtube_subscribers": 100_000,    # e.g., 100K subscribers
    "instagram_followers": 50_000,     # e.g., 50K followers
    "facebook_followers": 25_000,      # e.g., 25K followers
    "spotify_listeners": 500_000,      # e.g., 500K monthly listeners
}

# How close (as percentage, 0-100) before sending alert. e.g., 10 = alert at 90% of threshold
PROXIMITY_PERCENT = 10

# =============================================================================
# PLATFORM IDs - Your channel/page/artist identifiers
# =============================================================================
YOUTUBE_CHANNEL_ID = ""           # e.g., "UCxxxxxxxxxxxxxxxxxxxxxxxxxx"
YOUTUBE_VIDEO_IDS = []            # List of video IDs to track, e.g., ["dQw4w9WgXcQ"]
INSTAGRAM_USER_ID = ""            # Instagram Business/Creator account ID (from Meta)
FACEBOOK_PAGE_ID = ""             # Facebook Page ID
SPOTIFY_ARTIST_ID = ""            # Spotify artist ID (from artist URL)

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
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

# =============================================================================
# SCHEDULE - How often to check (in minutes)
# =============================================================================
CHECK_INTERVAL_MINUTES = 60
