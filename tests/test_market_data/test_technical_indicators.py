"""Tests for TechnicalIndicatorsAPI."""
import pytest
import responses

from eodhd._http import HTTPClient
from eodhd.apis.market_data.technical_indicators import TechnicalIndicatorsAPI


@pytest.fixture()
def api():
    http = HTTPClient("0" * 20, max_retries=0)
    return TechnicalIndicatorsAPI(http)


class TestTechnicalIndicators:
    @responses.activate
    def test_get_sma(self, api):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/technical/AAPL.US",
            json=[{"date": "2024-01-01", "sma": 150}],
            status=200,
        )
        result = api.get("AAPL.US", "sma", period=50)
        assert isinstance(result, list)

    def test_empty_ticker_raises(self, api):
        with pytest.raises(ValueError):
            api.get("", "sma")

    def test_empty_function_raises(self, api):
        with pytest.raises(ValueError):
            api.get("AAPL.US", "")

    def test_invalid_function_raises(self, api):
        with pytest.raises(ValueError):
            api.get("AAPL.US", "nonexistent_function")
