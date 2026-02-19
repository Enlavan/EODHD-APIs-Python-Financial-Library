"""Intraday historical data.

Endpoint: ``GET /intraday/{SYMBOL}``
Docs: https://eodhd.com/financial-apis/intraday-historical-data-api
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["IntradayAPI"]

_VALID_INTERVALS = {"5m", "1h", "1m"}


class IntradayAPI(BaseAPI):
    """Fetch intraday OHLCV bars for a given symbol."""

    def get(
        self,
        symbol: str,
        *,
        interval: str = "5m",
        from_unix_time: int | str | None = None,
        to_unix_time: int | str | None = None,
    ) -> list[dict[str, Any]]:
        """Return intraday bars.

        Parameters
        ----------
        symbol:
            Ticker with exchange suffix, e.g. ``"AAPL.US"``.
        interval:
            Bar interval -- ``"1m"``, ``"5m"``, or ``"1h"``.
        from_unix_time:
            Start of range as a UNIX timestamp.
        to_unix_time:
            End of range as a UNIX timestamp.
        """
        if not symbol or not str(symbol).strip():
            raise ValueError("symbol is required")

        interval = str(interval).lower()
        if interval not in _VALID_INTERVALS:
            raise ValueError(f"interval must be one of {sorted(_VALID_INTERVALS)}")

        params: dict[str, Any] = {"interval": interval}
        if from_unix_time is not None:
            params["from"] = str(from_unix_time)
        if to_unix_time is not None:
            params["to"] = str(to_unix_time)

        return self._get("intraday", str(symbol).strip(), params=params)
