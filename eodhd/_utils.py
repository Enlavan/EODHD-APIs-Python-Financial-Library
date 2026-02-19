"""Internal utility helpers."""

import re
from datetime import datetime, timedelta

_API_KEY_RE = re.compile(r"^[A-Za-z0-9.]{16,32}$")


def validate_api_key(api_key: str) -> None:
    """Raise ValueError if *api_key* is not a plausible EODHD token."""
    if api_key == "demo":
        return
    if not isinstance(api_key, str) or not _API_KEY_RE.match(api_key):
        raise ValueError("API key is invalid")


def str2datetime(dt_string: str) -> datetime:
    """Convert 'YYYY-MM-DD HH:MM:SS' to a datetime object."""
    prog = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
    if not prog.match(dt_string):
        raise ValueError("Incorrect datetime format: yyyy-mm-dd hh:mm:ss")
    return datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")


def str2epoch(dt_string: str) -> int:
    """Convert 'YYYY-MM-DD HH:MM:SS' to a UNIX epoch int."""
    return int(str2datetime(dt_string).timestamp())


def previous_day_last_second() -> str:
    """Return 'YYYY-MM-DD 23:59:59' for yesterday."""
    yesterday = datetime.today() - timedelta(days=1)
    return str(yesterday.date()) + " 23:59:59"


def previous_day_last_minute() -> str:
    """Return 'YYYY-MM-DD 23:59:00' for yesterday."""
    yesterday = datetime.today() - timedelta(days=1)
    return str(yesterday.date()) + " 23:59:00"
