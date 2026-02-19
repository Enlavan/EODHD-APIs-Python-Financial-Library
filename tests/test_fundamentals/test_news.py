"""Tests for NewsAPI."""
import pytest
import responses

from eodhd._http import HTTPClient
from eodhd.apis.fundamentals.news import NewsAPI


@pytest.fixture()
def api():
    http = HTTPClient("0" * 20, max_retries=0)
    return NewsAPI(http)


class TestNews:
    @responses.activate
    def test_get_by_symbol(self, api):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/news",
            json=[{"title": "News"}],
            status=200,
        )
        result = api.get(s="AAPL.US")
        assert isinstance(result, list)

    @responses.activate
    def test_get_by_tag(self, api):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/news",
            json=[{"title": "Tech news"}],
            status=200,
        )
        result = api.get(t="technology")
        assert isinstance(result, list)

    def test_no_s_or_t_raises(self, api):
        with pytest.raises(ValueError):
            api.get()
