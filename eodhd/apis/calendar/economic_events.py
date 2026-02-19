"""Wrapper for the ``GET /economic-events`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["EconomicEventsAPI"]


class EconomicEventsAPI(BaseAPI):
    """Retrieve economic events calendar data.

    Note: Although this module lives under the ``calendar`` sub-package
    the actual API path is ``/economic-events`` (not ``/calendar/...``).
    """

    def get(
        self,
        *,
        date_from: str | None = None,
        date_to: str | None = None,
        country: str | None = None,
        comparison: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch economic events.

        Parameters
        ----------
        date_from:
            Start date in ``YYYY-MM-DD`` format.
        date_to:
            End date in ``YYYY-MM-DD`` format.
        country:
            Two-letter country code (e.g. ``"US"``).
        comparison:
            Comparison filter value.
        offset:
            Pagination offset.
        limit:
            Maximum number of results.

        Returns
        -------
        list[dict[str, Any]]
            List of economic-event records.
        """
        params: dict[str, Any] = {}
        if date_from is not None:
            params["from"] = date_from
        if date_to is not None:
            params["to"] = date_to
        if country is not None:
            params["country"] = country
        if comparison is not None:
            params["comparison"] = comparison
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        return self._get("economic-events", params=params)
