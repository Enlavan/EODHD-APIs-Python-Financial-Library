"""Shared enums and type aliases for the eodhd package."""

from enum import Enum
from typing import Any

JSONDict = dict[str, Any]
JSONList = list[dict[str, Any]]


class Interval(Enum):
    """Supported price bar intervals."""

    MINUTE = "1m"
    FIVEMINUTES = "5m"
    HOUR = "1h"
    ONEDAY = "d"
    WEEK = "w"
    MONTH = "m"


class Order(Enum):
    """Sort order for date-based results."""

    ASC = "a"
    DESC = "d"
