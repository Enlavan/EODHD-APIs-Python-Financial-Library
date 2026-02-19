"""Wrapper for the ``GET /bulk-fundamentals/{EXCHANGE}`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["BulkFundamentalsAPI"]


class BulkFundamentalsAPI(BaseAPI):
    """Retrieve bulk fundamental data for an entire exchange."""

    def get(
        self,
        exchange: str,
        *,
        symbols: str | None = None,
        offset: int | None = None,
        limit: int = 500,
        version: str | None = None,
    ) -> dict[str, Any]:
        """Fetch bulk fundamentals for *exchange*.

        Parameters
        ----------
        exchange:
            Exchange code (e.g. ``"US"``).
        symbols:
            Optional comma-separated list of ticker symbols to filter.
        offset:
            Pagination offset.
        limit:
            Maximum number of results (default ``500``).
        version:
            API version string (e.g. ``"1.2"``).

        Returns
        -------
        dict[str, Any]
            Bulk fundamental data for the requested exchange.
        """
        params: dict[str, Any] = {"limit": limit}
        if symbols is not None:
            params["symbols"] = symbols
        if offset is not None:
            params["offset"] = offset
        if version is not None:
            params["version"] = version
        return self._get("bulk-fundamentals", uri=exchange, params=params)
