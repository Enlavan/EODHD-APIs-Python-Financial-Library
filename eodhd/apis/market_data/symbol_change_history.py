"""Symbol change history.

Endpoint: ``GET /symbol-change-history``
Docs: https://eodhd.com/financial-apis/symbol-change-history
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["SymbolChangeHistoryAPI"]


class SymbolChangeHistoryAPI(BaseAPI):
    """Fetch the history of ticker symbol changes."""

    def get(
        self,
        *,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return symbol-change records.

        Parameters
        ----------
        from_date:
            Start date (``YYYY-MM-DD``).
        to_date:
            End date (``YYYY-MM-DD``).
        """
        params: dict[str, Any] = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return self._get("symbol-change-history", params=params)
