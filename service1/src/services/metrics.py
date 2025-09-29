from __future__ import annotations

from datetime import datetime, timezone
import os
import time

_START_TIME_MONOTONIC = time.monotonic()


def build_status_record() -> str:
    uptime_hours = _read_uptime_hours()
    free_disk_mib = _read_free_disk_mib()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        f"{timestamp}: uptime {uptime_hours:.2f} hours, "
        f"free disk in root: {free_disk_mib} MBytes"
    )


def _read_uptime_hours() -> float:
    elapsed_seconds = time.monotonic() - _START_TIME_MONOTONIC
    return elapsed_seconds / 3600.0


def _read_free_disk_mib() -> int:
    stats = os.statvfs("/")
    free_bytes = stats.f_bavail * stats.f_frsize
    return int(free_bytes / (1024 * 1024))
