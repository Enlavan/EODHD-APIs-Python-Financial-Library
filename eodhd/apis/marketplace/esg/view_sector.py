"""ESG data for a specific sector.

Endpoint: ``GET /mp/investverte/sector/{sector}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ViewSectorAPI"]


class ViewSectorAPI(BaseAPI):
    """Fetch ESG data for a specific sector."""

    def get(
        self,
        sector: str,
        *,
        year: int | None = None,
    ) -> dict[str, Any]:
        """Return ESG data for a sector.

        Parameters
        ----------
        sector:
            Sector name.
        year:
            Filter by year.
        """
        if not sector or not str(sector).strip():
            raise ValueError("sector is required")

        params: dict[str, Any] = {}

        if year is not None:
            params["year"] = year

        return self._get("mp/investverte/sector", str(sector).strip(), params=params)
