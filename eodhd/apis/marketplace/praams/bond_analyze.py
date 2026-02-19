"""PRAAMS bond analysis.

Endpoint: ``GET /mp/praams/analyse/bond/{isin}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["BondAnalyzeAPI"]


class BondAnalyzeAPI(BaseAPI):
    """Fetch bond analysis data via PRAAMS."""

    def get(
        self,
        isin: str,
    ) -> dict[str, Any]:
        """Return bond analysis data.

        Parameters
        ----------
        isin:
            International Securities Identification Number of the bond.
        """
        if not isin or not str(isin).strip():
            raise ValueError("isin is required")

        return self._get("mp/praams/analyse/bond", str(isin).strip())
