"""PRAAMS bond report (PDF).

Endpoint: ``GET /mp/praams/reports/bond/{isin}``
"""

from typing import Any

import requests

from eodhd.apis._base import BaseAPI

__all__ = ["ReportBondAPI"]


class ReportBondAPI(BaseAPI):
    """Fetch a bond report PDF via PRAAMS."""

    def get(
        self,
        isin: str,
        email: str,
        *,
        is_full: bool | None = None,
    ) -> requests.Response:
        """Return the raw response containing a bond report PDF.

        Parameters
        ----------
        isin:
            International Securities Identification Number of the bond.
        email:
            Email address for the report.
        is_full:
            If ``True``, generate a full report.
        """
        if not isin or not str(isin).strip():
            raise ValueError("isin is required")
        if not email or not str(email).strip():
            raise ValueError("email is required")

        params: dict[str, Any] = {"email": str(email).strip()}

        if is_full is not None:
            params["isFull"] = is_full

        return self._get(
            "mp/praams/reports/bond", str(isin).strip(), params=params, raw=True
        )
