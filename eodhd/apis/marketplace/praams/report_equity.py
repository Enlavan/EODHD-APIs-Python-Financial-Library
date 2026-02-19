"""PRAAMS equity report (PDF).

Endpoints:
  - ``GET /mp/praams/reports/equity/isin/{isin}``
  - ``GET /mp/praams/reports/equity/ticker/{ticker}``
"""

from typing import Any

import requests

from eodhd.apis._base import BaseAPI

__all__ = ["ReportEquityAPI"]


class ReportEquityAPI(BaseAPI):
    """Fetch an equity report PDF via PRAAMS."""

    def get_by_isin(
        self,
        isin: str,
        email: str,
        *,
        is_full: bool | None = None,
    ) -> requests.Response:
        """Return the raw response containing an equity report PDF by ISIN.

        Parameters
        ----------
        isin:
            International Securities Identification Number.
        email:
            Email address for the report.
        is_full:
            If ``True``, generate a full report.
        """
        if not isin or not str(isin).strip():
            raise ValueError("isin is required")
        if not email or not str(email).strip():
            raise ValueError("email is required")

        params: dict[str, Any] = {"email": str(email).strip()}

        if is_full is not None:
            params["isFull"] = is_full

        return self._get(
            "mp/praams/reports/equity/isin", str(isin).strip(), params=params, raw=True
        )

    def get_by_ticker(
        self,
        ticker: str,
        email: str,
        *,
        is_full: bool | None = None,
    ) -> requests.Response:
        """Return the raw response containing an equity report PDF by ticker.

        Parameters
        ----------
        ticker:
            Ticker symbol.
        email:
            Email address for the report.
        is_full:
            If ``True``, generate a full report.
        """
        if not ticker or not str(ticker).strip():
            raise ValueError("ticker is required")
        if not email or not str(email).strip():
            raise ValueError("email is required")

        params: dict[str, Any] = {"email": str(email).strip()}

        if is_full is not None:
            params["isFull"] = is_full

        return self._get(
            "mp/praams/reports/equity/ticker",
            str(ticker).strip(),
            params=params,
            raw=True,
        )
