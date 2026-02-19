"""Wrapper for the ``GET /news-word-weights`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["NewsWordWeightsAPI"]


class NewsWordWeightsAPI(BaseAPI):
    """Retrieve word-weight analysis for news related to a ticker."""

    def get(
        self,
        s: str,
        *,
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Fetch news word weights.

        Parameters
        ----------
        s:
            Ticker symbol (e.g. ``"AAPL.US"``).
        date_from:
            Start date filter in ``YYYY-MM-DD`` format.
        date_to:
            End date filter in ``YYYY-MM-DD`` format.
        limit:
            Page limit for results.

        Returns
        -------
        dict[str, Any]
            Word-weight data for the requested ticker.
        """
        params: dict[str, Any] = {"s": s}
        if date_from is not None:
            params["filter[date_from]"] = date_from
        if date_to is not None:
            params["filter[date_to]"] = date_to
        if limit is not None:
            params["page[limit]"] = limit
        return self._get("news-word-weights", params=params)
