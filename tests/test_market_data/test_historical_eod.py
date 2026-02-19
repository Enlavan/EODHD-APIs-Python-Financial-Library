"""Tests for HistoricalEodAPI."""
import pytest
import responses

from eodhd._http import HTTPClient
from eodhd.apis.market_data.historical_eod import HistoricalEodAPI


@pytest.fixture()
def api():
    http = HTTPClient("0" * 20, max_retries=0)
    return HistoricalEodAPI(http)


class TestHistoricalEod:
    @responses.activate
    def test_get_basic(self, api):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/eod/AAPL.US",
            json=[{"date": "2024-01-01", "close": 150}],
            status=200,
        )
        result = api.get("AAPL.US")
        assert isinstance(result, list)
        assert result[0]["close"] == 150

    @responses.activate
    def test_get_with_params(self, api):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/eod/AAPL.US",
            json=[],
            status=200,
        )
        api.get("AAPL.US", period="w", from_date="2024-01-01", to_date="2024-12-31", order="d")
        url = responses.calls[0].request.url
        assert "period=w" in url
        assert "from=2024-01-01" in url
        assert "to=2024-12-31" in url
        assert "order=d" in url

    def test_empty_symbol_raises(self, api):
        with pytest.raises(ValueError, match="symbol is required"):
            api.get("")
