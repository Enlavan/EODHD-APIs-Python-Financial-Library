"""PRAAMS bank balance sheet data.

Endpoints:
  - ``GET /mp/praams/bank/balance_sheet/isin/{isin}``
  - ``GET /mp/praams/bank/balance_sheet/ticker/{ticker}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["BankBalanceSheetAPI"]


class BankBalanceSheetAPI(BaseAPI):
    """Fetch bank balance sheet data via PRAAMS."""

    def get_by_isin(
        self,
        isin: str,
    ) -> list[dict[str, Any]]:
        """Return balance sheet data by ISIN.

        Parameters
        ----------
        isin:
            International Securities Identification Number.
        """
        if not isin or not str(isin).strip():
            raise ValueError("isin is required")

        return self._get("mp/praams/bank/balance_sheet/isin", str(isin).strip())

    def get_by_ticker(
        self,
        ticker: str,
    ) -> list[dict[str, Any]]:
        """Return balance sheet data by ticker.

        Parameters
        ----------
        ticker:
            Ticker symbol.
        """
        if not ticker or not str(ticker).strip():
            raise ValueError("ticker is required")

        return self._get("mp/praams/bank/balance_sheet/ticker", str(ticker).strip())
