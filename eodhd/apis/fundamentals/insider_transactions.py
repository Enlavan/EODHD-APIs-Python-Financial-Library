"""Wrapper for the ``GET /insider-transactions`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["InsiderTransactionsAPI"]


class InsiderTransactionsAPI(BaseAPI):
    """Retrieve insider-transaction filings."""

    def get(
        self,
        *,
        date_from: str | None = None,
        date_to: str | None = None,
        code: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch insider transactions.

        Parameters
        ----------
        date_from:
            Start date in ``YYYY-MM-DD`` format.
        date_to:
            End date in ``YYYY-MM-DD`` format.
        code:
            Ticker code to filter by.
        limit:
            Maximum number of results.

        Returns
        -------
        list[dict[str, Any]]
            List of insider-transaction records.
        """
        params: dict[str, Any] = {}
        if date_from is not None:
            params["from"] = date_from
        if date_to is not None:
            params["to"] = date_to
        if code is not None:
            params["code"] = code
        if limit is not None:
            params["limit"] = limit
        return self._get("insider-transactions", params=params)
