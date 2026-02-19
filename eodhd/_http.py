"""Central HTTP transport for all EODHD API calls.

Responsibilities:
  - holds ``requests.Session`` for connection pooling
  - automatic retry with exponential backoff
  - API-key injection (every request gets ``api_token``)
  - maps HTTP error codes to typed exceptions
  - Python ``logging`` instead of ``rich.Console``
  - never calls ``sys.exit()``
"""

import logging
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from eodhd.exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError as EODHDConnectionError,
    NotFoundError,
    RateLimitError,
    TimeoutError as EODHDTimeoutError,
)

logger = logging.getLogger("eodhd")

_DEFAULT_BASE_URL = "https://eodhd.com/api"


class HTTPClient:
    """Thin wrapper around ``requests.Session``.

    Parameters
    ----------
    api_key:
        EODHD API token (injected into every request as ``api_token``).
    base_url:
        Override the API root (useful for testing).
    timeout:
        Default request timeout in seconds.
    max_retries:
        Number of retries on transient failures (5xx, 429).
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

        self._session = requests.Session()
        retry = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    # --------------------------------------------------------------------- #
    # Public helpers
    # --------------------------------------------------------------------- #

    def get(
        self,
        endpoint: str,
        uri: str = "",
        *,
        params: dict[str, Any] | None = None,
        raw: bool = False,
    ) -> Any:
        """Perform a GET request.

        Parameters
        ----------
        endpoint:
            Path segment after ``/api/``, e.g. ``"eod"`` or ``"cboe/index"``.
        uri:
            Optional path suffix (typically a symbol), e.g. ``"AAPL.US"``.
        params:
            Extra query-string parameters (api_token and fmt are added
            automatically).
        raw:
            If *True* return the raw ``requests.Response`` (for binary
            payloads like logo images).
        """
        url = self._build_url(endpoint, uri)
        merged = self._merge_params(params)
        return self._request("GET", url, params=merged, raw=raw)

    def post(
        self,
        endpoint: str,
        uri: str = "",
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        """Perform a POST request (e.g. PRAAMS screener endpoints)."""
        url = self._build_url(endpoint, uri)
        merged = self._merge_params(params)
        return self._request("POST", url, params=merged, json_body=json_body)

    # --------------------------------------------------------------------- #
    # Internals
    # --------------------------------------------------------------------- #

    def _build_url(self, endpoint: str, uri: str) -> str:
        parts = [self._base_url, endpoint.strip("/")]
        if uri:
            parts.append(uri.strip("/"))
        return "/".join(parts)

    def _merge_params(self, extra: dict[str, Any] | None) -> dict[str, Any]:
        base: dict[str, Any] = {"api_token": self._api_key, "fmt": "json"}
        if extra:
            base.update(extra)
        return base

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        raw: bool = False,
    ) -> Any:
        try:
            resp = self._session.request(
                method,
                url,
                params=params,
                json=json_body,
                timeout=self._timeout,
            )
        except requests.ConnectionError as exc:
            raise EODHDConnectionError(str(exc)) from exc
        except requests.Timeout as exc:
            raise EODHDTimeoutError(str(exc)) from exc

        self._raise_for_status(resp)

        if raw:
            return resp

        return resp.json()

    @staticmethod
    def _raise_for_status(resp: requests.Response) -> None:
        if resp.status_code < 400:
            return

        # Try to extract a message from the JSON body
        message = ""
        body = ""
        try:
            data = resp.json()
            body = str(data)
            message = data.get("message", data.get("errors", ""))
            if isinstance(message, (dict, list)):
                message = str(message)
        except Exception:
            body = resp.text

        code = resp.status_code
        if code in (401, 403):
            raise AuthenticationError(code, message or "Authentication failed", body)
        if code == 404:
            raise NotFoundError(code, message or "Not found", body)
        if code == 429:
            retry_after = resp.headers.get("Retry-After")
            raise RateLimitError(
                code,
                message or "Rate limit exceeded",
                body,
                retry_after=float(retry_after) if retry_after else None,
            )
        raise APIError(code, message, body)
