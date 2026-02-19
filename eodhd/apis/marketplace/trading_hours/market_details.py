"""Trading-hours market details.

Endpoint: ``GET /mp/tradinghours/markets/details``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["MarketDetailsAPI"]


class MarketDetailsAPI(BaseAPI):
    """Fetch detailed information for a specific market."""

    def get(
        self,
        fin_id: str,
    ) -> dict[str, Any]:
        """Return detailed market information.

        Parameters
        ----------
        fin_id:
            The financial identifier of the market.
        """
        if not fin_id or not str(fin_id).strip():
            raise ValueError("fin_id is required")

        params: dict[str, Any] = {"fin_id": str(fin_id).strip()}

        return self._get("mp/tradinghours/markets/details", params=params)
