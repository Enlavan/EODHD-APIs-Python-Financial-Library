"""Wrapper for the ``GET /calendar/dividends`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["DividendsAPI"]


class DividendsAPI(BaseAPI):
    """Retrieve dividend calendar data."""

    def get(
        self,
        *,
        symbol: str | None = None,
        date_eq: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        page_limit: int | None = None,
        page_offset: int | None = None,
    ) -> dict[str, Any]:
        """Fetch dividend calendar entries.

        At least one of *symbol* or *date_eq* must be provided.

        Parameters
        ----------
        symbol:
            Ticker symbol (e.g. ``"AAPL.US"``).
        date_eq:
            Exact date filter in ``YYYY-MM-DD`` format.
        date_from:
            Start date in ``YYYY-MM-DD`` format.
        date_to:
            End date in ``YYYY-MM-DD`` format.
        page_limit:
            Number of results per page.
        page_offset:
            Page offset for pagination.

        Returns
        -------
        dict[str, Any]
            Dividend calendar data.

        Raises
        ------
        ValueError
            If neither *symbol* nor *date_eq* is provided.
        """
        if symbol is None and date_eq is None:
            raise ValueError("At least one of 'symbol' or 'date_eq' must be provided.")

        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if date_eq is not None:
            params["date_eq"] = date_eq
        if date_from is not None:
            params["from"] = date_from
        if date_to is not None:
            params["to"] = date_to
        if page_limit is not None:
            params["page[limit]"] = page_limit
        if page_offset is not None:
            params["page[offset]"] = page_offset
        return self._get("calendar/dividends", params=params)
