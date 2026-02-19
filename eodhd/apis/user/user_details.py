"""Retrieve authenticated user information.

Endpoint: ``GET /internal-user``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["UserDetailsAPI"]


class UserDetailsAPI(BaseAPI):
    """Fetch details for the currently authenticated user."""

    def get(self) -> dict[str, Any]:
        """Return a dict with the current user's account information."""
        return self._get("internal-user")
