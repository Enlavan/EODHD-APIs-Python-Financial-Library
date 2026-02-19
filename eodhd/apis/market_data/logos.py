"""Company logo images.

Endpoint: ``GET /logo/{SYMBOL}``
Docs: https://eodhd.com/financial-apis/stock-logo-api
"""

from typing import Any

import requests

from eodhd.apis._base import BaseAPI

__all__ = ["LogosAPI"]


class LogosAPI(BaseAPI):
    """Fetch a company logo image."""

    def get(
        self,
        symbol: str,
    ) -> requests.Response:
        """Return the raw HTTP response containing logo image data.

        Parameters
        ----------
        symbol:
            Ticker with exchange suffix, e.g. ``"AAPL.US"``.

        Returns
        -------
        requests.Response
            The raw response whose ``.content`` attribute holds the binary
            image bytes.  Use ``.headers["Content-Type"]`` to determine the
            image format.
        """
        if not symbol or not str(symbol).strip():
            raise ValueError("symbol is required")

        return self._get("logo", str(symbol).strip(), raw=True)
