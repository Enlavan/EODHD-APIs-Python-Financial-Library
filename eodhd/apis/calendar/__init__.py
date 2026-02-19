"""Calendar-related API wrappers."""

from eodhd.apis.calendar.earnings import EarningsAPI
from eodhd.apis.calendar.trends import TrendsAPI
from eodhd.apis.calendar.dividends import DividendsAPI
from eodhd.apis.calendar.splits import SplitsAPI
from eodhd.apis.calendar.ipos import IposAPI
from eodhd.apis.calendar.economic_events import EconomicEventsAPI

__all__ = [
    "EarningsAPI",
    "TrendsAPI",
    "DividendsAPI",
    "SplitsAPI",
    "IposAPI",
    "EconomicEventsAPI",
]
