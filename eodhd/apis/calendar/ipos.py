"""Wrapper for the ``GET /calendar/ipos`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["IposAPI"]


class IposAPI(BaseAPI):
    """Retrieve IPO calendar data."""

    def get(
        self,
        *,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        """Fetch IPO calendar entries.

        Parameters
        ----------
        from_date:
            Start date in ``YYYY-MM-DD`` format.
        to_date:
            End date in ``YYYY-MM-DD`` format.

        Returns
        -------
        dict[str, Any]
            IPO calendar data.
        """
        params: dict[str, Any] = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        return self._get("calendar/ipos", params=params)
