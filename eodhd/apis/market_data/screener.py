"""Stock market screener.

Endpoint: ``GET /screener``
Docs: https://eodhd.com/financial-apis/stock-market-screener-api
"""

import json
from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ScreenerAPI"]


class ScreenerAPI(BaseAPI):
    """Screen stocks by fundamental and technical criteria."""

    def get(
        self,
        *,
        sort: str | None = None,
        filters: list[list[Any]] | str | None = None,
        limit: int | None = None,
        signals: str | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return screener results.

        Parameters
        ----------
        sort:
            Field to sort by, e.g. ``"market_capitalization.desc"``.
        filters:
            Filter criteria.  Accepts a list of lists (will be JSON-encoded)
            or a pre-encoded JSON string.  Example::

                [["market_capitalization", ">", 1000000000],
                 ["exchange", "=", "us"]]

        limit:
            Maximum number of results to return.
        signals:
            Signal filter, e.g. ``"bookvalue_neg"``.
        offset:
            Pagination offset.
        """
        params: dict[str, Any] = {}

        if sort is not None:
            params["sort"] = str(sort)
        if filters is not None:
            if isinstance(filters, list):
                params["filters"] = json.dumps(filters)
            else:
                params["filters"] = str(filters)
        if limit is not None:
            params["limit"] = int(limit)
        if signals is not None:
            params["signals"] = str(signals)
        if offset is not None:
            params["offset"] = int(offset)

        return self._get("screener", params=params)
