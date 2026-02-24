"""
Checkpoint logic for follower/subscriber alerts (YouTube, Instagram, Facebook).

Under 1M: milestones every 100k (100k, 200k, 300k... 1M), notify when 5k left.
Over 1M: milestones every 1M (1M, 2M, 3M...), notify when 15k left.
"""

from __future__ import annotations

from typing import NamedTuple


class FollowerCheckpoint(NamedTuple):
    target: int
    proximity: int


def get_next_follower_checkpoint(count: int) -> FollowerCheckpoint | None:
    """
    Return the next (target, proximity) checkpoint for followers/subscribers.
    Under 1M: 100k, 200k... 1M with 5k proximity.
    Over 1M: 1M, 2M, 3M... with 15k proximity.
    """
    if count < 1_000_000:
        for m in range(100_000, 1_100_000, 100_000):
            if count < m:
                return FollowerCheckpoint(m, 5_000)
    else:
        m = 1_000_000
        while count >= m and m <= 50_000_000:
            m += 1_000_000
        if count < m:
            return FollowerCheckpoint(m, 15_000)
    return None


def should_alert_followers(count: int, target: int, proximity: int) -> bool:
    """True if within `proximity` of `target` and haven't passed it."""
    if count >= target:
        return False
    return count >= target - proximity
