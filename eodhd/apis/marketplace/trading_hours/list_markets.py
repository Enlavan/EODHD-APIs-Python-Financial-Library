"""List trading-hours markets.

Endpoint: ``GET /mp/tradinghours/markets``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ListMarketsAPI"]

_VALID_GROUPS = {"core", "extended", "all", "allowed"}


class ListMarketsAPI(BaseAPI):
    """Fetch the list of available trading-hours markets."""

    def get(
        self,
        *,
        group: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return a list of markets.

        Parameters
        ----------
        group:
            Filter group -- ``"core"``, ``"extended"``, ``"all"``,
            or ``"allowed"``.
        """
        params: dict[str, Any] = {}

        if group is not None:
            group = str(group).lower()
            if group not in _VALID_GROUPS:
                raise ValueError(f"group must be one of {sorted(_VALID_GROUPS)}")
            params["group"] = group

        return self._get("mp/tradinghours/markets", params=params)
