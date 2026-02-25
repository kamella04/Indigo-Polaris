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
    "kamhoang04@gmail.com",  # Replace with email(s) that should receive alerts
]

# =============================================================================
# Follower metrics (YouTube, Instagram, Facebook, Spotify) use checkpoint rules:
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
    {"id": "RTBl0s8-y1o", "title": "OVER - KHOI VU (ft. khoivy) | Official Music Video"},
    {"id": "XgkBxgL9iFM", "title": "LIES - Khoi Vu ft. Radoux | Official Music Video"},
    {"id": "lzmz0aYW2Io", "title": "Bế Em Lên Cung Trăng"},
    {"id": "T5SpBJDIwjM", "title": "Hông về tình yêu (Not About Love) - Official Lyrics Video"},
    {"id": "Hg5H88WLvac", "title": "Fantasy"},
    {"id": "L5wqfBRT1OE", "title": "Vì đã lỡ lời - Official Lyrics Video"},
    {"id": "iIB0wWq0QTI", "title": "ECYA - Official Lyrics Video"},
    {"id": "aTCNqaWreu4", "title": "BMAGER - Official Lyrics Video"},
    {"id": "cdxYzYStkkg", "title": "chang.noi.duoc.gi"},
    {"id": "g5YCqQMfwNg", "title": "Tìm Tôi? - Official Lyric Video"},
    {"id": "6KCff8T5tR0", "title": "BERLIN - Official Lyrics Video"},
    {"id": "zDABZ5heLDQ", "title": "EM À - Official Remake"},
    {"id": "yNSK0QyBE_k", "title": "CHOCOLATE - Official Lyric Video"},
    {"id": "PprzEeogfQM", "title": "TANTHE - Official Lyric Video"},
    {"id": "21I0ijEEp_Y", "title": "CHUYẾN BAY - Official Lyric Video"},
    {"id": "P8dDhlax17A", "title": "TÌNH YÊU LÀ QUÃNG ĐƯỜNG TA ĐI - Official Lyric Video"},
    {"id": "YO6FSdStYUc", "title": "EM À - Official Lyric Video"},
    {"id": "_o2HdllsaxU", "title": "THE WAY I CALL YOU - Official Lyric Video"},
    {"id": "5NwoDz01mRU", "title": "LOVE PAIN - Official Lyric Video"},
    {"id": "yh2h_YwILII", "title": "CHÚ ĐẠI BI (VÔ LƯỢNG)"},
    {"id": "z2EYAGlwBB0", "title": "VÔ LƯỢNG (trích Chú Đại Bi)"},
    {"id": "HScTQOhUKDA", "title": "HỐI DUYÊN"},
    {"id": "lxzOIev1Pec", "title": "NHẤT THÂN"},
    {"id": "1pquvJRgIMY", "title": "ÁI NỘ"},
    {"id": "9gvKujFbHdc", "title": "GIẤC MƠ CÁNH DIỀU"},
    {"id": "FjhnvSWMoKM", "title": "BUỒN NHẸ NHÀNG THÔI"},
    {"id": "DmKifkrD9zk", "title": "TẾT ĐI EM ÊI"},
    {"id": "Ct8WoUjmdng", "title": "Unfollow"},
    {"id": "CNirp2pEodU", "title": "Thiêu Thân"},
    {"id": "XQkze4rQMsU", "title": "Sớm muộn thì"},
    {"id": "6mUZN9YArv8", "title": "Like A Horse"},
]

INSTAGRAM_USER_ID = "2041951224"
FACEBOOK_PAGE_ID = "100063766702292"
SPOTIFY_ARTIST_ID = "71Cy7nzbfpuGJAS5FGxm93"  # From artist URL, e.g. spotify.com/artist/xxxx -> xxxx

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
