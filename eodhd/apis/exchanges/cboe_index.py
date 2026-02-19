"""Wrapper for the ``GET /cboe/index`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["CboeIndexAPI"]


class CboeIndexAPI(BaseAPI):
    """Retrieve CBOE index data for a specific index, feed type, and date."""

    def get(
        self,
        index_code: str,
        feed_type: str,
        date: str,
        *,
        fmt: str | None = None,
    ) -> dict[str, Any]:
        """Fetch CBOE index data.

        Parameters
        ----------
        index_code:
            CBOE index code (e.g. ``"VIX"``).
        feed_type:
            Feed type identifier.
        date:
            Date in ``YYYY-MM-DD`` format.
        fmt:
            Response format override.

        Returns
        -------
        dict[str, Any]
            CBOE index data.
        """
        params: dict[str, Any] = {
            "filter[index_code]": index_code,
            "filter[feed_type]": feed_type,
            "filter[date]": date,
        }
        if fmt is not None:
            params["fmt"] = fmt
        return self._get("cboe/index", params=params)
