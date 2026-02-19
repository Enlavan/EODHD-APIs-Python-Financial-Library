"""Trading-hours market status.

Endpoint: ``GET /mp/tradinghours/markets/status``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["MarketStatusAPI"]


class MarketStatusAPI(BaseAPI):
    """Fetch the current status of a specific market."""

    def get(
        self,
        fin_id: str,
    ) -> dict[str, Any]:
        """Return the current market status.

        Parameters
        ----------
        fin_id:
            The financial identifier of the market.
        """
        if not fin_id or not str(fin_id).strip():
            raise ValueError("fin_id is required")

        params: dict[str, Any] = {"fin_id": str(fin_id).strip()}

        return self._get("mp/tradinghours/markets/status", params=params)
