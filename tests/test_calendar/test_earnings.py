"""Tests for EarningsAPI."""
import responses
import pytest

from eodhd._http import HTTPClient
from eodhd.apis.calendar.earnings import EarningsAPI


@pytest.fixture()
def api():
    http = HTTPClient("0" * 20, max_retries=0)
    return EarningsAPI(http)


class TestEarnings:
    @responses.activate
    def test_get(self, api):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/calendar/earnings",
            json={"earnings": []},
            status=200,
        )
        result = api.get(from_date="2024-01-01", to_date="2024-01-31")
        assert isinstance(result, dict)
