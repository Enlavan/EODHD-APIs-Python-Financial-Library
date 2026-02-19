"""PRAAMS bond screener.

Endpoint: ``POST /mp/praams/explore/bond``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ScreenerBondAPI"]


class ScreenerBondAPI(BaseAPI):
    """Screen bonds using PRAAMS filters."""

    def search(
        self,
        *,
        skip: int | None = None,
        take: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return bond screener results.

        Parameters
        ----------
        skip:
            Number of results to skip (pagination offset).
        take:
            Number of results to return (pagination limit).
        filters:
            Filter criteria as a dict. Supported keys include
            ``mainRatioMin``, ``mainRatioMax``, ``regions``,
            ``countries``, ``sectors``, ``industries``, etc.
        """
        params: dict[str, Any] = {}

        if skip is not None:
            params["skip"] = skip
        if take is not None:
            params["take"] = take

        json_body: dict[str, Any] | None = filters if filters else None

        return self._post("mp/praams/explore/bond", params=params, json_body=json_body)
