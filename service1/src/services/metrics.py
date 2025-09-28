from __future__ import annotations

from datetime import datetime, timezone
import os


def build_status_record() -> str:
    uptime_seconds = _read_uptime_seconds()
    uptime_hours = uptime_seconds / 3600.0

    free_disk_mib = _read_free_disk_mib()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{timestamp}: uptime {uptime_hours:.2f} hours, free disk in root: {free_disk_mib} MBytes"


def _read_uptime_seconds() -> float:
    with open("/proc/uptime", "r", encoding="utf-8") as handle:
        first_field = handle.read().split()[0]
    return float(first_field)


def _read_free_disk_mib() -> int:
    stats = os.statvfs("/")
    free_bytes = stats.f_bavail * stats.f_frsize
    return int(free_bytes / (1024 * 1024))
