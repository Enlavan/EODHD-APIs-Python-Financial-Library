"""Tests for the HTTPClient."""

import json

import pytest
import responses

from eodhd._http import HTTPClient
from eodhd.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)


@pytest.fixture()
def http():
    return HTTPClient("0" * 20, max_retries=0)


class TestGet:
    @responses.activate
    def test_get_json(self, http: HTTPClient):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/eod/AAPL.US",
            json=[{"date": "2024-01-01", "close": 150}],
            status=200,
        )
        result = http.get("eod", "AAPL.US")
        assert isinstance(result, list)
        assert result[0]["close"] == 150

    @responses.activate
    def test_get_injects_api_token(self, http: HTTPClient):
        responses.add(responses.GET, "https://eodhd.com/api/eod/AAPL.US", json=[], status=200)
        http.get("eod", "AAPL.US")
        assert "api_token=" + "0" * 20 in responses.calls[0].request.url

    @responses.activate
    def test_get_merges_params(self, http: HTTPClient):
        responses.add(responses.GET, "https://eodhd.com/api/eod/AAPL.US", json=[], status=200)
        http.get("eod", "AAPL.US", params={"period": "d", "from": "2024-01-01"})
        url = responses.calls[0].request.url
        assert "period=d" in url
        assert "from=2024-01-01" in url

    @responses.activate
    def test_get_raw_returns_response(self, http: HTTPClient):
        responses.add(responses.GET, "https://eodhd.com/api/logo/AAPL.US", body=b"\x89PNG", status=200)
        resp = http.get("logo", "AAPL.US", raw=True)
        assert resp.content == b"\x89PNG"


class TestErrorMapping:
    @responses.activate
    def test_401_raises_auth_error(self, http: HTTPClient):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/eod/AAPL.US",
            json={"message": "Unauthorized"},
            status=401,
        )
        with pytest.raises(AuthenticationError) as exc_info:
            http.get("eod", "AAPL.US")
        assert exc_info.value.status_code == 401

    @responses.activate
    def test_404_raises_not_found(self, http: HTTPClient):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/eod/INVALID",
            json={"message": "Not found"},
            status=404,
        )
        with pytest.raises(NotFoundError):
            http.get("eod", "INVALID")

    @responses.activate
    def test_429_raises_rate_limit(self, http: HTTPClient):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/eod/AAPL.US",
            json={"message": "Too many requests"},
            status=429,
            headers={"Retry-After": "60"},
        )
        with pytest.raises(RateLimitError) as exc_info:
            http.get("eod", "AAPL.US")
        assert exc_info.value.retry_after == 60.0

    @responses.activate
    def test_500_raises_api_error(self, http: HTTPClient):
        responses.add(
            responses.GET,
            "https://eodhd.com/api/eod/AAPL.US",
            json={"message": "Internal Server Error"},
            status=500,
        )
        with pytest.raises(APIError) as exc_info:
            http.get("eod", "AAPL.US")
        assert exc_info.value.status_code == 500


class TestPost:
    @responses.activate
    def test_post_with_json_body(self, http: HTTPClient):
        responses.add(
            responses.POST,
            "https://eodhd.com/api/mp/praams/explore/bond",
            json={"peers": [], "totalCount": 0},
            status=200,
        )
        result = http.post(
            "mp/praams/explore/bond",
            json_body={"mainRatioMin": 1},
        )
        assert result["totalCount"] == 0
        assert json.loads(responses.calls[0].request.body) == {"mainRatioMin": 1}
