"""ESG companies list.

Endpoint: ``GET /mp/investverte/companies``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["CompaniesAPI"]


class CompaniesAPI(BaseAPI):
    """Fetch the list of companies with ESG data."""

    def get(self) -> list[dict[str, Any]]:
        """Return all companies with available ESG data."""
        return self._get("mp/investverte/companies")
