"""Wrapper for the ``GET /ust/long-term-rates`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["TreasuryLongTermAPI"]


class TreasuryLongTermAPI(BaseAPI):
    """Retrieve US Treasury long-term rate data."""

    def get(self, *, year: int | None = None) -> dict[str, Any]:
        """Fetch Treasury long-term rates.

        Parameters
        ----------
        year:
            Filter by year (e.g. ``2024``).

        Returns
        -------
        dict[str, Any]
            Treasury long-term rate data.
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["filter[year]"] = year
        return self._get("ust/long-term-rates", params=params)
