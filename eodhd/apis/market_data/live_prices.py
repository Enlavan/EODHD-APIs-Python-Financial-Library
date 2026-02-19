"""Live (delayed) stock prices.

Endpoint: ``GET /real-time/{SYMBOL}``
Docs: https://eodhd.com/financial-apis/live-realtime-stocks-api
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["LivePricesAPI"]


class LivePricesAPI(BaseAPI):
    """Fetch live / delayed price snapshots."""

    def get(
        self,
        ticker: str,
        *,
        s: str | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Return a live price snapshot.

        Parameters
        ----------
        ticker:
            Primary ticker with exchange suffix, e.g. ``"AAPL.US"``.
        s:
            Optional comma-separated additional tickers to fetch in one call,
            e.g. ``"MSFT.US,TSLA.US"``.
        """
        if not ticker or not str(ticker).strip():
            raise ValueError("ticker is required")

        params: dict[str, Any] = {}
        if s is not None:
            params["s"] = str(s)

        return self._get("real-time", str(ticker).strip(), params=params)
