"""Tests for Options API modules."""
import responses
import pytest

from eodhd._http import HTTPClient
from eodhd.apis.marketplace.options.contracts import ContractsAPI
from eodhd.apis.marketplace.options.eod import EodAPI


@pytest.fixture()
def http():
    return HTTPClient("0" * 20, max_retries=0)


class TestContracts:
    @responses.activate
    def test_get(self, http):
        api = ContractsAPI(http)
        responses.add(
            responses.GET,
            "https://eodhd.com/api/mp/unicornbay/options/contracts",
            json={"meta": {}, "data": []},
            status=200,
        )
        result = api.get(underlying_symbol="AAPL")
        assert isinstance(result, dict)
        assert "data" in result


class TestEod:
    @responses.activate
    def test_get(self, http):
        api = EodAPI(http)
        responses.add(
            responses.GET,
            "https://eodhd.com/api/mp/unicornbay/options/eod",
            json={"meta": {}, "data": []},
            status=200,
        )
        result = api.get(underlying_symbol="AAPL")
        assert isinstance(result, dict)
