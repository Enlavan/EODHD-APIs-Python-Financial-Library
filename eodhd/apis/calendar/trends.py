"""Wrapper for the ``GET /calendar/trends`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["TrendsAPI"]


class TrendsAPI(BaseAPI):
    """Retrieve earnings trends data."""

    def get(self, symbols: str) -> dict[str, Any]:
        """Fetch earnings trends for given symbols.

        Parameters
        ----------
        symbols:
            Comma-separated ticker symbols (e.g. ``"AAPL.US,MSFT.US"``).

        Returns
        -------
        dict[str, Any]
            Trends data for the requested symbols.
        """
        params: dict[str, Any] = {"symbols": symbols}
        return self._get("calendar/trends", params=params)
