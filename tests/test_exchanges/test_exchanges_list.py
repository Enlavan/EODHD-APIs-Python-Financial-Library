"""Tests for ExchangesListAPI."""
import responses
import pytest

from eodhd._http import HTTPClient
from eodhd.apis.exchanges.exchanges_list import ExchangesListAPI


@pytest.fixture()
def api():
    http = HTTPClient("0" * 20, max_retries=0)
    return ExchangesListAPI(http)


class TestExchangesList:
    @responses.activate
    def test_get(self, api):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/exchanges-list",
            json=[{"Name": "NYSE", "Code": "US"}],
            status=200,
        )
        result = api.get()
        assert isinstance(result, list)
        assert result[0]["Code"] == "US"
