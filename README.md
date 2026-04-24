# Indigo Polaris Metrics Monitor

An automated monitor that tracks YouTube views/subscribers, Instagram followers, Facebook followers, and Spotify followers. When any metric gets close to its checkpoint, it sends an email alert to the listed recipients.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure `config.py`

- **ALERT_EMAILS** – List of email addresses to receive alerts
- **YOUTUBE_CHANNEL_ID** – Your channel
- **YOUTUBE_VIDEOS** – List of `{"id": "video_id", "title": "Video Title"}` to track
- **INSTAGRAM_USER_ID**, **FACEBOOK_PAGE_ID** – Platform IDs

### 3. Set environment variables

Copy `.env.example` to `.env` and fill in:

- **SMTP_*** – Email settings (use an [App Password](https://support.google.com/accounts/answer/185833) for Gmail)
- **YOUTUBE_API_KEY** – [Google Cloud Console](https://console.cloud.google.com/) → YouTube Data API v3
- **INSTAGRAM_ACCESS_TOKEN** – [Meta for Developers](https://developers.facebook.com/)
- **FACEBOOK_ACCESS_TOKEN** – Same Meta developer setup
- **SPOTIFY_CLIENT_ID** / **SPOTIFY_CLIENT_SECRET** – [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

### 4. Spotify: redirect URI (dashboard only)

This project uses the **Client Credentials** flow for Spotify, so you do not log in in a browser and you do not need a real redirect URL. If the Spotify app form requires **Redirect URIs**, add a placeholder, for example:

- `http://127.0.0.1:8888/callback`

### 5. Run the email monitor

```bash
cd path/to/Indigo-Polaris
python monitor.py
```

It checks metrics every `CHECK_INTERVAL_MINUTES` (default: 60). Alerts are sent only once per metric/threshold to avoid spam.

### 6. Daily YouTube view history + website

1. Once per day (e.g. end of day), record view counts. This appends a row per video for **today** in `data/youtube_daily_history.json`:

   ```bash
   python record_daily_snapshot.py
   ```

2. View the table (current views, growth vs previous day and vs 7 days ago):

   ```bash
   python webapp.py
   ```

   Open **http://127.0.0.1:5000** in your browser.

3. On Windows, use **Task Scheduler** to run `record_daily_snapshot.py` at a time you consider “end of day” (e.g. 23:55) so each calendar day has one snapshot.

Remove `data/youtube_daily_history.json` from `.gitignore` if you want to commit that file (it is ignored by default).

## Follower Checkpoint Rules (YouTube, Instagram, Facebook, Spotify)

- **Under 1M:** milestones every 100k (100k, 200k... 1M), notify when **5k** left
- **Over 1M:** milestones every 1M (1M, 2M, 3M...), notify when **15k** left

## YouTube Video Checkpoint Rules

View alerts use different rules based on publish date:

**New videos (published today):**
- Checkpoints: 100k → 500k → 1M → 2M → 3M → …
- Alert when within **50k views** of checkpoint (for under 1M) or **100k views** (for 1M+)

**Older videos (published before today):**
- **Under 1M views:** 100k, 500k, 1M — alert when **50k** views left
- **1M–10M views:** every million — alert when **100k** views left
- **Over 10M views:** 15M, 20M, 25M… (every 5M) — alert when **200k** views left

## API Notes

- **YouTube** – Enable YouTube Data API v3 in Google Cloud and create an API key.
- **Instagram** – Requires an Instagram Business or Creator account linked to a Meta App.
- **Facebook** – Requires a Page access token with `pages_read_engagement`.
- **Spotify** – Artist follower count via Web API (Client ID + Secret). Works for any public artist.

## Example alert

> These YouTube subscribers are coming closer to 100,000.  
> Current value: 92,500  
> Target threshold: 100,000  
> Progress: 92.5%
