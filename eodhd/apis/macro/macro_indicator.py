"""Wrapper for the ``GET /macro-indicator/{COUNTRY}`` endpoint."""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["MacroIndicatorAPI"]


class MacroIndicatorAPI(BaseAPI):
    """Retrieve macroeconomic indicator data for a country."""

    def get(
        self,
        country: str,
        *,
        indicator: str = "gdp_current_usd",
    ) -> list[dict[str, Any]]:
        """Fetch macro-indicator time series.

        Parameters
        ----------
        country:
            Three-letter country code (e.g. ``"USA"``).
        indicator:
            Indicator key (default ``"gdp_current_usd"``).

        Returns
        -------
        list[dict[str, Any]]
            List of data points for the requested indicator.
        """
        params: dict[str, Any] = {"indicator": indicator}
        return self._get("macro-indicator", uri=country, params=params)
