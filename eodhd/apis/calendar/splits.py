"""Wrapper for the ``GET /calendar/splits`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["SplitsAPI"]


class SplitsAPI(BaseAPI):
    """Retrieve stock-split calendar data."""

    def get(
        self,
        *,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        """Fetch stock-split calendar entries.

        Parameters
        ----------
        from_date:
            Start date in ``YYYY-MM-DD`` format.
        to_date:
            End date in ``YYYY-MM-DD`` format.

        Returns
        -------
        dict[str, Any]
            Stock-split calendar data.
        """
        params: dict[str, Any] = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        return self._get("calendar/splits", params=params)
