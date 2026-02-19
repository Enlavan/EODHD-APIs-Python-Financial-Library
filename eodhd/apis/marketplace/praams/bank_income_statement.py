"""PRAAMS bank income statement data.

Endpoints:
  - ``GET /mp/praams/bank/income_statement/isin/{isin}``
  - ``GET /mp/praams/bank/income_statement/ticker/{ticker}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["BankIncomeStatementAPI"]


class BankIncomeStatementAPI(BaseAPI):
    """Fetch bank income statement data via PRAAMS."""

    def get_by_isin(
        self,
        isin: str,
    ) -> list[dict[str, Any]]:
        """Return income statement data by ISIN.

        Parameters
        ----------
        isin:
            International Securities Identification Number.
        """
        if not isin or not str(isin).strip():
            raise ValueError("isin is required")

        return self._get("mp/praams/bank/income_statement/isin", str(isin).strip())

    def get_by_ticker(
        self,
        ticker: str,
    ) -> list[dict[str, Any]]:
        """Return income statement data by ticker.

        Parameters
        ----------
        ticker:
            Ticker symbol.
        """
        if not ticker or not str(ticker).strip():
            raise ValueError("ticker is required")

        return self._get("mp/praams/bank/income_statement/ticker", str(ticker).strip())
