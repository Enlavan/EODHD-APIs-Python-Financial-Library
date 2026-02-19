"""Tests for the exception hierarchy."""
from eodhd.exceptions import (
    EODHDError,
    APIError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ConnectionError,
    TimeoutError,
)


def test_hierarchy():
    assert issubclass(APIError, EODHDError)
    assert issubclass(AuthenticationError, APIError)
    assert issubclass(RateLimitError, APIError)
    assert issubclass(NotFoundError, APIError)
    assert issubclass(ValidationError, EODHDError)
    assert issubclass(ConnectionError, EODHDError)
    assert issubclass(TimeoutError, EODHDError)


def test_api_error_attributes():
    err = APIError(404, "Not found", '{"message":"Not found"}')
    assert err.status_code == 404
    assert err.message == "Not found"
    assert err.response_body == '{"message":"Not found"}'
    assert "(404)" in str(err)


def test_rate_limit_retry_after():
    err = RateLimitError(retry_after=30.0)
    assert err.retry_after == 30.0
    assert err.status_code == 429
