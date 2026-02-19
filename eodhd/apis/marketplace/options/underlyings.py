"""Marketplace options underlying symbols.

Endpoint: ``GET /mp/unicornbay/options/underlying-symbols``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["UnderlyingsAPI"]


class UnderlyingsAPI(BaseAPI):
    """Fetch available underlying symbols for options."""

    def get(
        self,
        *,
        page_offset: int = 0,
        page_limit: int = 1000,
        fmt: str = "json",
    ) -> dict[str, Any]:
        """Return underlying symbols for options.

        Parameters
        ----------
        page_offset:
            Pagination offset (default ``0``).
        page_limit:
            Pagination limit (default ``1000``).
        fmt:
            Response format (default ``"json"``).
        """
        params: dict[str, Any] = {
            "page[offset]": page_offset,
            "page[limit]": page_limit,
            "fmt": fmt,
        }

        return self._get("mp/unicornbay/options/underlying-symbols", params=params)
