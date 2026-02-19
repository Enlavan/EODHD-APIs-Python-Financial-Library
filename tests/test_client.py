"""Tests for the APIClient facade."""

import pytest
import responses

from eodhd import APIClient
from eodhd._utils import validate_api_key


def test_invalid_api_key():
    with pytest.raises(ValueError, match="API key is invalid"):
        APIClient("bad")


def test_demo_key_accepted():
    client = APIClient("demo")
    assert client._api_key == "demo"


def test_namespaces_exist():
    client = APIClient("demo")
    assert hasattr(client, "market_data")
    assert hasattr(client, "fundamentals")
    assert hasattr(client, "calendar")
    assert hasattr(client, "exchanges")
    assert hasattr(client, "macro")
    assert hasattr(client, "user")
    assert hasattr(client, "marketplace")


def test_market_data_sub_apis():
    client = APIClient("demo")
    assert hasattr(client.market_data, "historical_eod")
    assert hasattr(client.market_data, "intraday")
    assert hasattr(client.market_data, "live_prices")
    assert hasattr(client.market_data, "technical_indicators")
    assert hasattr(client.market_data, "screener")
    assert hasattr(client.market_data, "search")
    assert hasattr(client.market_data, "logos")
    assert hasattr(client.market_data, "historical_market_cap")
    assert hasattr(client.market_data, "symbol_change_history")
    assert hasattr(client.market_data, "bulk_eod")
    assert hasattr(client.market_data, "historical_dividends")
    assert hasattr(client.market_data, "historical_splits")


def test_marketplace_sub_apis():
    client = APIClient("demo")
    assert hasattr(client.marketplace, "options")
    assert hasattr(client.marketplace, "tick_data")
    assert hasattr(client.marketplace, "trading_hours")
    assert hasattr(client.marketplace, "illio")
    assert hasattr(client.marketplace, "esg")
    assert hasattr(client.marketplace, "praams")


class TestBackwardCompatMethods:
    @responses.activate
    def test_get_historical_dividends_data(self):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/div/AAPL.US",
            json=[{"date": "2024-01-01", "value": 0.24}],
            status=200,
        )
        client = APIClient("0" * 20)
        result = client.get_historical_dividends_data(ticker="AAPL.US")
        assert isinstance(result, list)
        assert result[0]["value"] == 0.24

    @responses.activate
    def test_get_fundamentals_data(self):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/fundamentals/AAPL.US",
            json={"General": {"Code": "AAPL"}},
            status=200,
        )
        client = APIClient("0" * 20)
        result = client.get_fundamentals_data(ticker="AAPL.US")
        assert result["General"]["Code"] == "AAPL"

    @responses.activate
    def test_financial_news(self):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/news",
            json=[{"title": "Test news"}],
            status=200,
        )
        client = APIClient("0" * 20)
        result = client.financial_news(s="AAPL.US")
        assert isinstance(result, list)

    @responses.activate
    def test_get_list_of_exchanges(self):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/exchanges-list",
            json=[{"Name": "NYSE", "Code": "US"}],
            status=200,
        )
        client = APIClient("0" * 20)
        result = client.get_list_of_exchanges()
        assert isinstance(result, list)

    @responses.activate
    def test_get_eod_historical_stock_market_data(self):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/eod/AAPL.US",
            json=[{"date": "2024-01-01", "close": 150}],
            status=200,
        )
        client = APIClient("0" * 20)
        result = client.get_eod_historical_stock_market_data(symbol="AAPL.US")
        assert isinstance(result, list)
