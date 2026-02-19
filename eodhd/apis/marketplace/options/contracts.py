"""Marketplace options contracts data.

Endpoint: ``GET /mp/unicornbay/options/contracts``
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["ContractsAPI"]


class ContractsAPI(BaseAPI):
    """Fetch options contract data from the Unicorn Bay marketplace."""

    def get(
        self,
        *,
        underlying_symbol: str | None = None,
        contract: str | None = None,
        exp_date_eq: str | None = None,
        exp_date_from: str | None = None,
        exp_date_to: str | None = None,
        tradetime_eq: str | None = None,
        tradetime_from: str | None = None,
        tradetime_to: str | None = None,
        type: str | None = None,
        strike_eq: str | float | None = None,
        strike_from: str | float | None = None,
        strike_to: str | float | None = None,
        sort: str | None = None,
        page_offset: int = 0,
        page_limit: int = 1000,
        fields: str | list[str] | None = None,
        fmt: str = "json",
    ) -> dict[str, Any]:
        """Return options contract data.

        Parameters
        ----------
        underlying_symbol:
            Filter by underlying symbol.
        contract:
            Filter by contract identifier.
        exp_date_eq:
            Filter by exact expiration date.
        exp_date_from:
            Filter by expiration date range start.
        exp_date_to:
            Filter by expiration date range end.
        tradetime_eq:
            Filter by exact trade time.
        tradetime_from:
            Filter by trade time range start.
        tradetime_to:
            Filter by trade time range end.
        type:
            Filter by option type -- ``"put"`` or ``"call"``.
        strike_eq:
            Filter by exact strike price.
        strike_from:
            Filter by strike price range start.
        strike_to:
            Filter by strike price range end.
        sort:
            Sort field.
        page_offset:
            Pagination offset (default ``0``).
        page_limit:
            Pagination limit (default ``1000``).
        fields:
            Specific fields to return. Can be a string or list of strings.
        fmt:
            Response format (default ``"json"``).
        """
        params: dict[str, Any] = {
            "page[offset]": page_offset,
            "page[limit]": page_limit,
            "fmt": fmt,
        }

        if underlying_symbol is not None:
            params["filter[underlying_symbol]"] = underlying_symbol
        if contract is not None:
            params["filter[contract]"] = contract
        if exp_date_eq is not None:
            params["filter[exp_date_eq]"] = exp_date_eq
        if exp_date_from is not None:
            params["filter[exp_date_from]"] = exp_date_from
        if exp_date_to is not None:
            params["filter[exp_date_to]"] = exp_date_to
        if tradetime_eq is not None:
            params["filter[tradetime_eq]"] = tradetime_eq
        if tradetime_from is not None:
            params["filter[tradetime_from]"] = tradetime_from
        if tradetime_to is not None:
            params["filter[tradetime_to]"] = tradetime_to
        if type is not None:
            params["filter[type]"] = type
        if strike_eq is not None:
            params["filter[strike_eq]"] = strike_eq
        if strike_from is not None:
            params["filter[strike_from]"] = strike_from
        if strike_to is not None:
            params["filter[strike_to]"] = strike_to
        if sort is not None:
            params["sort"] = sort
        if fields is not None:
            if isinstance(fields, list):
                params["fields[options-contracts]"] = ",".join(fields)
            else:
                params["fields[options-contracts]"] = fields

        return self._get("mp/unicornbay/options/contracts", params=params)
