"""PRAAMS equity risk scoring (analysis).

Endpoints:
  - ``GET /mp/praams/analyse/equity/isin/{isin}``
  - ``GET /mp/praams/analyse/equity/ticker/{ticker}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["RiskScoringAPI"]


class RiskScoringAPI(BaseAPI):
    """Fetch equity risk scoring data via PRAAMS."""

    def get_by_isin(
        self,
        isin: str,
    ) -> dict[str, Any]:
        """Return risk scoring data by ISIN.

        Parameters
        ----------
        isin:
            International Securities Identification Number.
        """
        if not isin or not str(isin).strip():
            raise ValueError("isin is required")

        return self._get("mp/praams/analyse/equity/isin", str(isin).strip())

    def get_by_ticker(
        self,
        ticker: str,
    ) -> dict[str, Any]:
        """Return risk scoring data by ticker.

        Parameters
        ----------
        ticker:
            Ticker symbol.
        """
        if not ticker or not str(ticker).strip():
            raise ValueError("ticker is required")

        return self._get("mp/praams/analyse/equity/ticker", str(ticker).strip())
