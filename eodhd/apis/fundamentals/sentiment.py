"""Wrapper for the ``GET /sentiments`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["SentimentAPI"]


class SentimentAPI(BaseAPI):
    """Retrieve sentiment scores for ticker symbols."""

    def get(
        self,
        s: str,
        *,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        """Fetch sentiment data.

        Parameters
        ----------
        s:
            Comma-separated ticker symbols (e.g. ``"AAPL.US,MSFT.US"``).
        from_date:
            Start date in ``YYYY-MM-DD`` format.
        to_date:
            End date in ``YYYY-MM-DD`` format.

        Returns
        -------
        dict[str, Any]
            Sentiment data keyed by ticker symbol.
        """
        params: dict[str, Any] = {"s": s}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        return self._get("sentiments", params=params)
