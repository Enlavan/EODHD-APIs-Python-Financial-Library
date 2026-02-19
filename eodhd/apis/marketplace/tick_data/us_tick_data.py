"""US tick-level trade data.

Endpoint: ``GET /mp/us-tick-data``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["USTickDataAPI"]


class USTickDataAPI(BaseAPI):
    """Fetch US tick-level trade data."""

    def get(
        self,
        symbol: str,
        *,
        from_timestamp: int | str | None = None,
        to_timestamp: int | str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Return tick data for a US symbol.

        Parameters
        ----------
        symbol:
            Ticker symbol (e.g. ``"AAPL"``).
        from_timestamp:
            Start of range as a UNIX timestamp.
        to_timestamp:
            End of range as a UNIX timestamp.
        limit:
            Maximum number of ticks to return.
        """
        if not symbol or not str(symbol).strip():
            raise ValueError("symbol is required")

        params: dict[str, Any] = {"s": str(symbol).strip()}

        if from_timestamp is not None:
            params["from"] = from_timestamp
        if to_timestamp is not None:
            params["to"] = to_timestamp
        if limit is not None:
            params["limit"] = limit

        return self._get("mp/us-tick-data", params=params)
