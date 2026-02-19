"""Wrapper for the ``GET /exchange-details/{CODE}`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ExchangeDetailsAPI"]


class ExchangeDetailsAPI(BaseAPI):
    """Retrieve detailed information about a specific exchange."""

    def get(
        self,
        code: str,
        *,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        """Fetch details for an exchange.

        Parameters
        ----------
        code:
            Exchange code (e.g. ``"US"``).
        from_date:
            Start date in ``YYYY-MM-DD`` format.
        to_date:
            End date in ``YYYY-MM-DD`` format.

        Returns
        -------
        dict[str, Any]
            Detailed exchange information.
        """
        params: dict[str, Any] = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        return self._get("exchange-details", uri=code, params=params)
