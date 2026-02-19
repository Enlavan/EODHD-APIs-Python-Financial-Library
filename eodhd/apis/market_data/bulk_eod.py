"""Bulk end-of-day data (last trading day).

Endpoint: ``GET /eod-bulk-last-day/{EXCHANGE}``
Docs: https://eodhd.com/financial-apis/bulk-api-eod-splits-dividends
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["BulkEodAPI"]


class BulkEodAPI(BaseAPI):
    """Fetch bulk EOD, splits, or dividends data for an exchange."""

    def get(
        self,
        country: str = "US",
        *,
        type: str | None = None,
        date: str | None = None,
        symbols: str | None = None,
        filter: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return bulk end-of-day data for the last trading day.

        Parameters
        ----------
        country:
            Exchange code used as the URI path segment (default ``"US"``).
        type:
            Data type -- ``"splits"``, ``"dividends"``, or omit for EOD prices.
        date:
            Specific trading date (``YYYY-MM-DD``).
        symbols:
            Comma-separated list of tickers to filter.
        filter:
            Fields to include in the response, e.g.
            ``"extended"`` or ``"last_close_price"``.
        """
        params: dict[str, Any] = {}
        if type is not None:
            params["type"] = str(type)
        if date is not None:
            params["date"] = str(date)
        if symbols is not None:
            params["symbols"] = str(symbols)
        if filter is not None:
            params["filter"] = str(filter)

        return self._get("eod-bulk-last-day", str(country).strip(), params=params)
