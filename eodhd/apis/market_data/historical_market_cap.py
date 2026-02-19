"""Historical market capitalization.

Endpoint: ``GET /historical-market-cap/{TICKER}``
Docs: https://eodhd.com/financial-apis/historical-market-capitalization-api
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["HistoricalMarketCapAPI"]


class HistoricalMarketCapAPI(BaseAPI):
    """Fetch historical market capitalization for a ticker."""

    def get(
        self,
        ticker: str,
        *,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return historical market-cap data.

        Parameters
        ----------
        ticker:
            Ticker with exchange suffix, e.g. ``"AAPL.US"``.
        from_date:
            Start date (``YYYY-MM-DD``).
        to_date:
            End date (``YYYY-MM-DD``).
        """
        if not ticker or not str(ticker).strip():
            raise ValueError("ticker is required")

        params: dict[str, Any] = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return self._get("historical-market-cap", str(ticker).strip(), params=params)
