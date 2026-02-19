"""EODHD — Official Python library for the EODHD Financial API.

Quick start::

    from eodhd import APIClient

    client = APIClient("YOUR_API_KEY")

    # New namespaced style
    data = client.market_data.historical_eod.get("AAPL.US")

    # Old flat style (still works)
    data = client.get_eod_historical_stock_market_data(symbol="AAPL.US")
"""
from eodhd.__version__ import __version__

# Primary public API
from eodhd.client import APIClient
from eodhd.scanner import ScannerClient
from eodhd.graphs import EODHDGraphs
from eodhd.websocket_client import WebSocketClient

# Exceptions
from eodhd.exceptions import (
    EODHDError,
    APIError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ConnectionError,
    TimeoutError,
)

# Types
from eodhd._types import Interval, Order

# Backward compat: ``import eodhd.APIs`` still works via the old package
# The old APIs/ directory is kept as-is; the shim module provides
# deprecation-warned access.
from eodhd import APIs  # noqa: F401

__all__ = [
    "__version__",
    "APIClient",
    "ScannerClient",
    "EODHDGraphs",
    "WebSocketClient",
    "EODHDError",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
    "ConnectionError",
    "TimeoutError",
    "Interval",
    "Order",
]
