"""Shared test fixtures."""

import pytest
import responses

from eodhd._http import HTTPClient
from eodhd.client import APIClient

_TEST_API_KEY = "0" * 20  # 20-char key passes validation
_BASE_URL = "https://eodhd.com/api"


@pytest.fixture()
def http() -> HTTPClient:
    """Return an HTTPClient with a test API key."""
    return HTTPClient(_TEST_API_KEY, base_url=_BASE_URL, max_retries=0)


@pytest.fixture()
def client() -> APIClient:
    """Return an APIClient with a test API key."""
    return APIClient(_TEST_API_KEY)


@pytest.fixture()
def mocked_responses():
    """Activate the ``responses`` mock for HTTP calls."""
    with responses.RequestsMock() as rsps:
        yield rsps
