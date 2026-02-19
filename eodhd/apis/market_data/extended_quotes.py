"""US extended (delayed, exchange-compliant) quotes.

Endpoint: ``GET /us-quote-delayed``
Docs: https://eodhd.com/financial-apis/live-realtime-stocks-api
"""

from typing import Any, Sequence

from eodhd.apis._base import BaseAPI

__all__ = ["ExtendedQuotesAPI"]


class ExtendedQuotesAPI(BaseAPI):
    """Fetch delayed extended quotes for US symbols."""

    def get(
        self,
        symbols: str | Sequence[str],
        *,
        page_limit: int | None = None,
        page_offset: int | None = None,
        fmt: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return extended quote data for one or more US tickers.

        Parameters
        ----------
        symbols:
            One or more tickers. Accepts a comma-separated string
            (``"AAPL.US,TSLA.US"``), or any iterable of strings.
        page_limit:
            Number of symbols per page (max 100).
        page_offset:
            Pagination offset (>= 0).
        fmt:
            Response format -- ``"json"`` (default) or ``"csv"``.
        """
        # Normalize symbols to a comma-separated string
        if isinstance(symbols, (list, tuple, set)):
            parts = [str(s).strip() for s in symbols if s is not None and str(s).strip()]
            if not parts:
                raise ValueError("symbols is required (one or more tickers)")
            symbols_str = ",".join(parts)
        else:
            symbols_str = str(symbols).strip()
            if not symbols_str:
                raise ValueError("symbols is required (one or more tickers)")

        if page_limit is not None:
            page_limit = int(page_limit)
            if page_limit < 1 or page_limit > 100:
                raise ValueError("page_limit must be in range 1..100")

        if page_offset is not None:
            page_offset = int(page_offset)
            if page_offset < 0:
                raise ValueError("page_offset must be >= 0")

        if fmt is not None:
            fmt = str(fmt).lower()
            if fmt not in ("json", "csv"):
                raise ValueError("fmt must be 'json' or 'csv'")

        params: dict[str, Any] = {"s": symbols_str}
        if page_limit is not None:
            params["page[limit]"] = page_limit
        if page_offset is not None:
            params["page[offset]"] = page_offset
        if fmt is not None:
            params["fmt"] = fmt

        return self._get("us-quote-delayed", params=params)
