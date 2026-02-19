"""Wrapper for the ``GET /ust/bill-rates`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["TreasuryBillRatesAPI"]


class TreasuryBillRatesAPI(BaseAPI):
    """Retrieve US Treasury bill rate data."""

    def get(
        self,
        *,
        year: int | None = None,
        page_limit: int | None = None,
        page_offset: int | None = None,
    ) -> dict[str, Any]:
        """Fetch Treasury bill rates.

        Parameters
        ----------
        year:
            Filter by year (e.g. ``2024``).
        page_limit:
            Number of results per page.
        page_offset:
            Page offset for pagination.

        Returns
        -------
        dict[str, Any]
            Treasury bill rate data.
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["filter[year]"] = year
        if page_limit is not None:
            params["page[limit]"] = page_limit
        if page_offset is not None:
            params["page[offset]"] = page_offset
        return self._get("ust/bill-rates", params=params)
