"""ESG data for a specific country.

Endpoint: ``GET /mp/investverte/country/{code}``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ViewCountryAPI"]

_VALID_FREQUENCIES = {"FY", "Q1", "Q2", "Q3", "Q4"}


class ViewCountryAPI(BaseAPI):
    """Fetch ESG data for a specific country."""

    def get(
        self,
        code: str,
        *,
        year: int | None = None,
        frequency: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return ESG data for a country.

        Parameters
        ----------
        code:
            ISO alpha-2 country code (e.g. ``"US"``, ``"GB"``).
        year:
            Filter by year.
        frequency:
            Reporting frequency -- ``"FY"``, ``"Q1"``, ``"Q2"``,
            ``"Q3"``, or ``"Q4"``.
        """
        if not code or not str(code).strip():
            raise ValueError("code is required")

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

        return self._get("mp/investverte/country", str(code).strip(), params=params)
