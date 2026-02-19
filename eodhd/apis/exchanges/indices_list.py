"""Wrapper for the ``GET /mp/unicornbay/spglobal/list`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["IndicesListAPI"]


class IndicesListAPI(BaseAPI):
    """Retrieve the list of available market indices."""

    def get(self) -> list[dict[str, Any]]:
        """Fetch all available indices.

        Returns
        -------
        list[dict[str, Any]]
            List of index objects.
        """
        return self._get("mp/unicornbay/spglobal/list")
