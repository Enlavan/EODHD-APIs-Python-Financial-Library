"""Historical stock splits.

Endpoint: ``GET /splits/{SYMBOL}``
Docs: https://eodhd.com/financial-apis/api-splits-dividends
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["HistoricalSplitsAPI"]


class HistoricalSplitsAPI(BaseAPI):
    """Fetch historical split records for a ticker."""

    def get(
        self,
        ticker: str,
        *,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return historical split data.

        Parameters
        ----------
        ticker:
            Ticker with exchange suffix, e.g. ``"AAPL.US"``.
        date_from:
            Start date (``YYYY-MM-DD``).
        date_to:
            End date (``YYYY-MM-DD``).
        """
        if not ticker or not str(ticker).strip():
            raise ValueError("ticker is required")

        params: dict[str, Any] = {}
        if date_from is not None:
            params["from"] = date_from
        if date_to is not None:
            params["to"] = date_to

        return self._get("splits", str(ticker).strip(), params=params)
