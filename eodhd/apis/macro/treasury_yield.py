"""Wrapper for the ``GET /ust/yield-rates`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["TreasuryYieldAPI"]


class TreasuryYieldAPI(BaseAPI):
    """Retrieve US Treasury yield-curve rate data."""

    def get(self, *, year: int | None = None) -> dict[str, Any]:
        """Fetch Treasury yield rates.

        Parameters
        ----------
        year:
            Filter by year (e.g. ``2024``).

        Returns
        -------
        dict[str, Any]
            Treasury yield rate data.
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["filter[year]"] = year
        return self._get("ust/yield-rates", params=params)
