"""ESG data for a specific company.

Endpoint: ``GET /mp/investverte/esg/{symbol}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ViewCompanyAPI"]

_VALID_FREQUENCIES = {"FY", "Q1", "Q2", "Q3", "Q4"}


class ViewCompanyAPI(BaseAPI):
    """Fetch ESG data for a specific company."""

    def get(
        self,
        symbol: str,
        *,
        year: int | None = None,
        frequency: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return ESG data for a company.

        Parameters
        ----------
        symbol:
            Company ticker symbol.
        year:
            Filter by year.
        frequency:
            Reporting frequency -- ``"FY"``, ``"Q1"``, ``"Q2"``,
            ``"Q3"``, or ``"Q4"``.
        """
        if not symbol or not str(symbol).strip():
            raise ValueError("symbol is required")

        params: dict[str, Any] = {}

        if year is not None:
            params["year"] = year
        if frequency is not None:
            frequency = str(frequency).upper()
            if frequency not in _VALID_FREQUENCIES:
                raise ValueError(
                    f"frequency must be one of {sorted(_VALID_FREQUENCIES)}"
                )
            params["frequency"] = frequency

        return self._get("mp/investverte/esg", str(symbol).strip(), params=params)
