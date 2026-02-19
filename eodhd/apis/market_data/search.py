"""Symbol search.

Endpoint: ``GET /search/{QUERY}``
Docs: https://eodhd.com/financial-apis/search-api-for-stocks-etfs-mutual-funds-and-indices
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["SearchAPI"]

_VALID_TYPES = {"all", "stock", "etf", "fund", "bond", "index", "crypto"}


class SearchAPI(BaseAPI):
    """Search for tickers by name or code."""

    def get(
        self,
        query_string: str,
        *,
        limit: int | None = None,
        bonds_only: int | None = None,
        exchange: str | None = None,
        type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return matching symbols.

        Parameters
        ----------
        query_string:
            Free-text search query, e.g. ``"Apple"`` or ``"AAPL"``.
        limit:
            Maximum number of results (default 15, max 500).
        bonds_only:
            Set to ``1`` to search bonds only.
        exchange:
            Limit results to a specific exchange code.
        type:
            Asset type filter -- ``"all"``, ``"stock"``, ``"etf"``,
            ``"fund"``, ``"bond"``, ``"index"``, or ``"crypto"``.
        """
        if not query_string or not str(query_string).strip():
            raise ValueError("query_string is required")

        if limit is not None:
            limit = int(limit)
            if limit < 1 or limit > 500:
                raise ValueError("limit must be in range 1..500")

        if bonds_only is not None and int(bonds_only) not in (0, 1):
            raise ValueError("bonds_only must be 0 or 1")

        if type is not None:
            type = str(type).lower()
            if type not in _VALID_TYPES:
                raise ValueError(f"type must be one of {sorted(_VALID_TYPES)}")

        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if bonds_only is not None:
            params["bonds_only"] = int(bonds_only)
        if exchange is not None:
            params["exchange"] = str(exchange)
        if type is not None:
            params["type"] = type

        return self._get("search", str(query_string).strip(), params=params)
