"""Trading-hours market lookup.

Endpoint: ``GET /mp/tradinghours/markets/lookup``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["LookupAPI"]


class LookupAPI(BaseAPI):
    """Search for trading-hours markets."""

    def get(
        self,
        *,
        q: str | None = None,
        group: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return markets matching the search criteria.

        Parameters
        ----------
        q:
            Search term.
        group:
            Filter group.
        """
        params: dict[str, Any] = {}

        if q is not None:
            params["q"] = q
        if group is not None:
            params["group"] = group

        return self._get("mp/tradinghours/markets/lookup", params=params)
