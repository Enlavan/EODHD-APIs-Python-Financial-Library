"""Illio beta bands.

Endpoint: ``GET /mp/illio/chapters/beta-bands/{id}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["BetaBandsAPI"]

_VALID_INDEX_IDS = {"SnP500", "DJI", "NDX"}


class BetaBandsAPI(BaseAPI):
    """Fetch beta bands data for an index."""

    def get(
        self,
        index_id: str,
    ) -> dict[str, Any]:
        """Return beta bands data.

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

        return self._get("mp/illio/chapters/beta-bands", index_id)
