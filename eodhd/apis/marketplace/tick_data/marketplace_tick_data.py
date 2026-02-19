"""Marketplace tick data.

Endpoint: ``GET /mp/unicornbay/tickdata/ticks``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["MarketplaceTickDataAPI"]


class MarketplaceTickDataAPI(BaseAPI):
    """Fetch marketplace tick data from Unicorn Bay."""

    def get(
        self,
        s: str,
        *,
        from_timestamp: int | None = None,
        to_timestamp: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Return tick data for a given ticker.

        Parameters
        ----------
        s:
            Ticker symbol.
        from_timestamp:
            Start of range as a UNIX timestamp (integer).
        to_timestamp:
            End of range as a UNIX timestamp (integer).
        limit:
            Maximum number of ticks to return (1--10000).
        """
        if not s or not str(s).strip():
            raise ValueError("s (ticker) is required")

        params: dict[str, Any] = {"s": str(s).strip()}

        if from_timestamp is not None:
            params["from"] = from_timestamp
        if to_timestamp is not None:
            params["to"] = to_timestamp
        if limit is not None:
            params["limit"] = limit

        return self._get("mp/unicornbay/tickdata/ticks", params=params)
