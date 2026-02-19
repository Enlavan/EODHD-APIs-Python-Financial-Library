"""Illio performance chapter.

Endpoint: ``GET /mp/illio/chapters/performance/{id}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["PerformanceAPI"]

_VALID_INDEX_IDS = {"SnP500", "DJI", "NDX"}


class PerformanceAPI(BaseAPI):
    """Fetch performance chapter data for an index."""

    def get(
        self,
        index_id: str,
    ) -> dict[str, Any]:
        """Return performance data.

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

        return self._get("mp/illio/chapters/performance", index_id)
