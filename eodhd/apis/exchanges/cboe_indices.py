"""Wrapper for the ``GET /cboe/indices`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["CboeIndicesAPI"]


class CboeIndicesAPI(BaseAPI):
    """Retrieve the list of available CBOE indices."""

    def get(self, *, fmt: str | None = None) -> dict[str, Any]:
        """Fetch CBOE indices listing.

        Parameters
        ----------
        fmt:
            Response format override.

        Returns
        -------
        dict[str, Any]
            CBOE indices data.
        """
        params: dict[str, Any] = {}
        if fmt is not None:
            params["fmt"] = fmt
        return self._get("cboe/indices", params=params)
