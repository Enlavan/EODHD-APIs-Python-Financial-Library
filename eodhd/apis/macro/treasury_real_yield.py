"""Wrapper for the ``GET /ust/real-yield-rates`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["TreasuryRealYieldAPI"]


class TreasuryRealYieldAPI(BaseAPI):
    """Retrieve US Treasury real (inflation-adjusted) yield-curve rate data."""

    def get(self, *, year: int | None = None) -> dict[str, Any]:
        """Fetch Treasury real yield rates.

        Parameters
        ----------
        year:
            Filter by year (e.g. ``2024``).

        Returns
        -------
        dict[str, Any]
            Treasury real yield rate data.
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["filter[year]"] = year
        return self._get("ust/real-yield-rates", params=params)
