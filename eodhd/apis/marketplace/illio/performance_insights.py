"""Illio performance insights (categories).

Endpoint: ``GET /mp/illio/categories/performance/{id}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["PerformanceInsightsAPI"]

_VALID_INDEX_IDS = {"SnP500", "DJI", "NDX"}


class PerformanceInsightsAPI(BaseAPI):
    """Fetch performance insights by category for an index."""

    def get(
        self,
        index_id: str,
    ) -> dict[str, Any]:
        """Return performance insights data.

        Parameters
        ----------
        index_id:
            Index identifier -- ``"SnP500"``, ``"DJI"``, or ``"NDX"``.
        """
        if not index_id or not str(index_id).strip():
            raise ValueError("index_id is required")

        index_id = str(index_id).strip()
        if index_id not in _VALID_INDEX_IDS:
            raise ValueError(f"index_id must be one of {sorted(_VALID_INDEX_IDS)}")

        return self._get("mp/illio/categories/performance", index_id)
