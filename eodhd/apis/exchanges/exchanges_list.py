"""Wrapper for the ``GET /exchanges-list`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ExchangesListAPI"]


class ExchangesListAPI(BaseAPI):
    """Retrieve the list of available exchanges."""

    def get(self) -> list[dict[str, Any]]:
        """Fetch all supported exchanges.

        Returns
        -------
        list[dict[str, Any]]
            List of exchange objects.
        """
        return self._get("exchanges-list")
