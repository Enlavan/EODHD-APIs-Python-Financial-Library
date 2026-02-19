"""Base class for all new-style API modules.

Every API class receives an ``HTTPClient`` at construction time and
delegates HTTP calls through it.  Individual API methods never see the
raw API key.
"""
from typing import Any

from eodhd._http import HTTPClient


class BaseAPI:
    """Thin base shared by every endpoint wrapper."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    # Convenience shortcuts so subclasses stay concise.

    def _get(
        self,
        endpoint: str,
        uri: str = "",
        *,
        params: dict[str, Any] | None = None,
        raw: bool = False,
    ) -> Any:
        return self._http.get(endpoint, uri, params=params, raw=raw)

    def _post(
        self,
        endpoint: str,
        uri: str = "",
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        return self._http.post(endpoint, uri, params=params, json_body=json_body)
