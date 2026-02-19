"""EODHD exception hierarchy.

All exceptions inherit from EODHDError so callers can catch a single
base class when they want a broad catch-all.
"""


class EODHDError(Exception):
    """Base exception for all EODHD library errors."""


class APIError(EODHDError):
    """The EODHD API returned a non-2xx status code."""

    def __init__(
        self,
        status_code: int,
        message: str = "",
        response_body: str = "",
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        super().__init__(f"({status_code}) {message}")


class AuthenticationError(APIError):
    """401 / 403 — invalid or missing API key."""


class RateLimitError(APIError):
    """429 — too many requests."""

    def __init__(
        self,
        status_code: int = 429,
        message: str = "Rate limit exceeded",
        response_body: str = "",
        retry_after: float | None = None,
    ) -> None:
        super().__init__(status_code, message, response_body)
        self.retry_after = retry_after


class NotFoundError(APIError):
    """404 — resource not found."""


class ValidationError(EODHDError):
    """A parameter failed local (client-side) validation."""


class ConnectionError(EODHDError):  # noqa: A001
    """Network-level connection failure."""


class TimeoutError(EODHDError):  # noqa: A001
    """Request timed out."""
