"""ESG sectors list.

Endpoint: ``GET /mp/investverte/sectors``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["SectorsAPI"]


class SectorsAPI(BaseAPI):
    """Fetch the list of sectors with ESG data."""

    def get(self) -> list[dict[str, Any]]:
        """Return all sectors with available ESG data."""
        return self._get("mp/investverte/sectors")
