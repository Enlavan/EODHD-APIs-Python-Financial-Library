"""Wrapper for the ``GET /news`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["NewsAPI"]


class NewsAPI(BaseAPI):
    """Retrieve financial news articles."""

    def get(
        self,
        *,
        s: str | None = None,
        t: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch news articles.

        At least one of *s* or *t* must be provided.

        Parameters
        ----------
        s:
            Ticker symbol to filter news for (e.g. ``"AAPL.US"``).
        t:
            Tag or topic to filter news by.
        from_date:
            Start date in ``YYYY-MM-DD`` format.
        to_date:
            End date in ``YYYY-MM-DD`` format.
        limit:
            Maximum number of articles to return.
        offset:
            Pagination offset.

        Returns
        -------
        list[dict[str, Any]]
            List of news article objects.

        Raises
        ------
        ValueError
            If neither *s* nor *t* is provided.
        """
        if s is None and t is None:
            raise ValueError("At least one of 's' (ticker) or 't' (tag/topic) must be provided.")

        params: dict[str, Any] = {}
        if s is not None:
            params["s"] = s
        if t is not None:
            params["t"] = t
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._get("news", params=params)
