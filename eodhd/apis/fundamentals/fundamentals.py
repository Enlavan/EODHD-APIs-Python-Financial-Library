"""Wrapper for the ``GET /fundamentals/{SYMBOL}`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["FundamentalsAPI"]


class FundamentalsAPI(BaseAPI):
    """Retrieve fundamental data for a given ticker symbol."""

    def get(self, ticker: str) -> dict[str, Any]:
        """Fetch fundamentals for *ticker*.

        Parameters
        ----------
        ticker:
            Ticker symbol including exchange suffix (e.g. ``"AAPL.US"``).

        Returns
        -------
        dict[str, Any]
            Fundamental data for the requested symbol.
        """
        return self._get("fundamentals", uri=ticker)
