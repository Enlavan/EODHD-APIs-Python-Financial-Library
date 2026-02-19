"""Wrapper for the ``GET /mp/unicornbay/spglobal/comp/{SYMBOL}`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["IndexComponentsAPI"]


class IndexComponentsAPI(BaseAPI):
    """Retrieve components (constituents) of a market index."""

    def get(
        self,
        symbol: str,
        *,
        historical: int | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        """Fetch index components for *symbol*.

        Parameters
        ----------
        symbol:
            Index symbol (e.g. ``"GSPC.INDX"``).
        historical:
            Set to ``1`` to include historical components.
        from_date:
            Start date in ``YYYY-MM-DD`` format (used with *historical*).
        to_date:
            End date in ``YYYY-MM-DD`` format (used with *historical*).

        Returns
        -------
        dict[str, Any]
            Index component data.
        """
        params: dict[str, Any] = {}
        if historical is not None:
            params["historical"] = historical
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        return self._get("mp/unicornbay/spglobal/comp", uri=symbol, params=params)
