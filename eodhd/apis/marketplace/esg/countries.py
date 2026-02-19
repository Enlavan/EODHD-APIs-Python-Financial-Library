"""ESG countries list.

Endpoint: ``GET /mp/investverte/countries``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["CountriesAPI"]


class CountriesAPI(BaseAPI):
    """Fetch the list of countries with ESG data."""

    def get(self) -> list[dict[str, Any]]:
        """Return all countries with available ESG data."""
        return self._get("mp/investverte/countries")
