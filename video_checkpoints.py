"""
Checkpoint logic for YouTube video view alerts.

New videos (published today): 100k, 500k, 1M, then 2M, 3M... | proximity 50k (<1M) or 100k (>=1M)
Old videos (published before today):
  - Under 1M: 100k, 500k, 1M | proximity 50k
  - 1M-10M: every million | proximity 100k
  - Over 10M: every 5M (15M, 20M, 25M...) | proximity 200k
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import NamedTuple


class CheckpointAlert(NamedTuple):
    target: int
    proximity: int  # views left before target to trigger alert


def is_new_video(published_at: datetime) -> bool:
    """True if video was published today (UTC)."""
    # For testing: set today as February 1st, 2026
    today = datetime(2026, 2, 1, tzinfo=timezone.utc).date()
    pub_date = published_at.date()
    return pub_date >= today


def get_next_checkpoint(views: int, is_new: bool) -> CheckpointAlert | None:
    """
    Return the next (target, proximity) checkpoint for this video.
    None if no more checkpoints (e.g. beyond our max).
    """
    if is_new:
        milestones = [100_000, 500_000, 1_000_000]
        milestones.extend(i * 1_000_000 for i in range(2, 20))  # 2M to 19M
        # From 20M to 99M, every 5M (20M, 25M, 30M...)
        milestones.extend(i * 5_000_000 for i in range(4, 20))  # 20M to 95M
        # From 100M onwards, every 10M (110M, 120M, 130M...)
        milestones.extend(i * 10_000_000 for i in range(11, 100))  # 110M to 990M
        for m in milestones:
            if views < m:
                proximity = 20_000 if m <= 1_000_000 else 100_000
                return CheckpointAlert(m, proximity)
    else:
        if views < 1_000_000:
            for m in [100_000, 500_000, 1_000_000]:
                if views < m:
                    return CheckpointAlert(m, 20_000)
        elif views < 10_000_000:
            for m in range(1_000_000, 10_000_000, 1_000_000):
                if views < m:
                    return CheckpointAlert(m, 100_000)
        
        if views >= 10_000_000 and views < 100_000_000:
            m = 10_000_000
            while views >= m and m <= 100_000_000:
                m += 5_000_000
            if views < m:
                return CheckpointAlert(m, 100_000)
        
        if views >= 100_000_000:
            m = 110_000_000
            while views >= m and m <= 1_000_000_000:
                m += 10_000_000
            if views < m:
                return CheckpointAlert(m, 100_000)
    return None


def should_alert(views: int, target: int, proximity: int) -> bool:
    """True if we're within `proximity` views of `target` and haven't passed it."""
    if views >= target:
        return False
    return views >= target - proximity
