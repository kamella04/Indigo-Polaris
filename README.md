# Indigo Polaris Metrics Monitor

An automated monitor that tracks YouTube views/subscribers, Instagram followers, Facebook followers, and Spotify metrics. When any metric gets close to its configured threshold, it sends an email alert to the listed recipients.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure `config.py`

- **ALERT_EMAILS** – List of email addresses to receive alerts
- **THRESHOLDS** – Target values for each metric (alert when within `PROXIMITY_PERCENT`)
- **PROXIMITY_PERCENT** – How close to the threshold before alerting (e.g., 10 = alert at 90% of target)
- **YOUTUBE_CHANNEL_ID**, **YOUTUBE_VIDEO_IDS** – Your channel and videos to track
- **INSTAGRAM_USER_ID**, **FACEBOOK_PAGE_ID**, **SPOTIFY_ARTIST_ID** – Platform IDs

### 3. Set environment variables

Copy `.env.example` to `.env` and fill in:

- **SMTP_*** – Email settings (use an [App Password](https://support.google.com/accounts/answer/185833) for Gmail)
- **YOUTUBE_API_KEY** – [Google Cloud Console](https://console.cloud.google.com/) → YouTube Data API v3
- **INSTAGRAM_ACCESS_TOKEN** – [Meta for Developers](https://developers.facebook.com/)
- **FACEBOOK_ACCESS_TOKEN** – Same Meta developer setup
- **SPOTIFY_CLIENT_ID** / **SPOTIFY_CLIENT_SECRET** – [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

### 4. Run the monitor

```bash
python monitor.py
```

It checks metrics every `CHECK_INTERVAL_MINUTES` (default: 60). Alerts are sent only once per metric/threshold to avoid spam.

## API Notes

- **YouTube** – Enable YouTube Data API v3 in Google Cloud and create an API key.
- **Instagram** – Requires an Instagram Business or Creator account linked to a Meta App.
- **Facebook** – Requires a Page access token with `pages_read_engagement`.
- **Spotify** – The public API provides artist follower count. Monthly listeners would require Spotify for Artists or other tools.

## Example alert

> These YouTube subscribers are coming closer to 100,000.  
> Current value: 92,500  
> Target threshold: 100,000  
> Progress: 92.5%
