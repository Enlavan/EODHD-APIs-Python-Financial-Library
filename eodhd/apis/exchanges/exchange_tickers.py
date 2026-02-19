"""Wrapper for the ``GET /exchange-symbol-list/{CODE}`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ExchangeTickersAPI"]


class ExchangeTickersAPI(BaseAPI):
    """Retrieve ticker symbols listed on an exchange."""

    def get(
        self,
        code: str,
        *,
        delisted: int = 0,
    ) -> list[dict[str, Any]]:
        """Fetch tickers for an exchange.

        Parameters
        ----------
        code:
            Exchange code (e.g. ``"US"``).
        delisted:
            Set to ``1`` to include delisted tickers (default ``0``).

        Returns
        -------
        list[dict[str, Any]]
            List of ticker symbol objects.
        """
        params: dict[str, Any] = {"delisted": delisted}
        return self._get("exchange-symbol-list", uri=code, params=params)
