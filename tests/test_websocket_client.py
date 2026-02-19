"""Tests for the refactored WebSocketClient."""
import pytest

from eodhd import WebSocketClient


def test_api_key_invalid():
    with pytest.raises(ValueError, match="API key is invalid"):
        WebSocketClient(api_key="", endpoint="", symbols=[])


def test_endpoint_invalid():
    with pytest.raises(ValueError, match="Endpoint is invalid"):
        WebSocketClient(
            api_key="0" * 20,
            endpoint="invalid",
            symbols=["BTC-USD"],
        )


def test_symbols_empty():
    with pytest.raises(ValueError, match="No symbol"):
        WebSocketClient(
            api_key="0" * 20,
            endpoint="crypto",
            symbols=[],
        )


def test_symbols_invalid():
    with pytest.raises(ValueError, match="Symbol is invalid"):
        WebSocketClient(
            api_key="0" * 20,
            endpoint="crypto",
            symbols=[""],
        )


def test_max_symbols_exceeded():
    with pytest.raises(ValueError, match="Max symbol subscription"):
        WebSocketClient(
            api_key="0" * 20,
            endpoint="crypto",
            symbols=[f"SYM{i}" for i in range(51)],
        )


def test_instantiate_success():
    ws = WebSocketClient(
        api_key="0" * 20,
        endpoint="crypto",
        symbols=["BTC-USD"],
    )
    assert isinstance(ws, WebSocketClient)
    assert ws.data_list == []
