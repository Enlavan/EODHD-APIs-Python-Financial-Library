"""Tests for Treasury API modules."""
import responses
import pytest

from eodhd._http import HTTPClient
from eodhd.apis.macro.treasury_bill_rates import TreasuryBillRatesAPI
from eodhd.apis.macro.treasury_yield import TreasuryYieldAPI


@pytest.fixture()
def http():
    return HTTPClient("0" * 20, max_retries=0)


class TestTreasuryBillRates:
    @responses.activate
    def test_get(self, http):
        api = TreasuryBillRatesAPI(http)
        responses.add(
            responses.GET,
            "https://eodhd.com/api/ust/bill-rates",
            json={"data": []},
            status=200,
        )
        result = api.get(year=2024)
        assert isinstance(result, dict)


class TestTreasuryYield:
    @responses.activate
    def test_get(self, http):
        api = TreasuryYieldAPI(http)
        responses.add(
            responses.GET,
            "https://eodhd.com/api/ust/yield-rates",
            json={"data": []},
            status=200,
        )
        result = api.get()
        assert isinstance(result, dict)
