"""End-of-day historical stock market data.

Endpoint: ``GET /eod/{SYMBOL}``
Docs: https://eodhd.com/financial-apis/api-for-historical-data-and-volumes
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["HistoricalEodAPI"]

_VALID_PERIODS = {"d", "w", "m"}
_VALID_ORDERS = {"a", "d"}


class HistoricalEodAPI(BaseAPI):
    """Fetch end-of-day OHLCV bars for a given symbol."""

    def get(
        self,
        symbol: str,
        *,
        period: str = "d",
        from_date: str | None = None,
        to_date: str | None = None,
        order: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return historical EOD prices.

        Parameters
        ----------
        symbol:
            Ticker with exchange suffix, e.g. ``"AAPL.US"``.
        period:
            Bar period -- ``"d"`` (daily), ``"w"`` (weekly), ``"m"`` (monthly).
        from_date:
            Start date in ``YYYY-MM-DD`` format.
        to_date:
            End date in ``YYYY-MM-DD`` format.
        order:
            Sort order -- ``"a"`` (ascending) or ``"d"`` (descending).
        """
        if not symbol or not str(symbol).strip():
            raise ValueError("symbol is required")

        period = str(period).lower()
        if period not in _VALID_PERIODS:
            raise ValueError(f"period must be one of {sorted(_VALID_PERIODS)}")

        if order is not None:
            order = str(order).lower()
            if order not in _VALID_ORDERS:
                raise ValueError(f"order must be one of {sorted(_VALID_ORDERS)}")

        params: dict[str, Any] = {"period": period}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if order is not None:
            params["order"] = order

        return self._get("eod", str(symbol).strip(), params=params)
