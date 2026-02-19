"""Wrapper for the ``GET /calendar/earnings`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["EarningsAPI"]


class EarningsAPI(BaseAPI):
    """Retrieve earnings calendar data."""

    def get(
        self,
        *,
        from_date: str | None = None,
        to_date: str | None = None,
        symbols: str | None = None,
    ) -> dict[str, Any]:
        """Fetch upcoming and past earnings dates.

        Parameters
        ----------
        from_date:
            Start date in ``YYYY-MM-DD`` format.
        to_date:
            End date in ``YYYY-MM-DD`` format.
        symbols:
            Comma-separated ticker symbols to filter by.

        Returns
        -------
        dict[str, Any]
            Earnings calendar data.
        """
        params: dict[str, Any] = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if symbols is not None:
            params["symbols"] = symbols
        return self._get("calendar/earnings", params=params)
