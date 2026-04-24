"""
Run the monitor check ONCE and exit.

Used for cloud schedulers (GitHub Actions / cron jobs).
"""

from __future__ import annotations

from monitor import run_check


def main() -> int:
    run_check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

