"""WebSocket client for real-time EODHD market data streams.

Refactored from the original ``websocketclient.py`` to use the new
exception types and validation utilities, while keeping the same
public API.
"""

import json
import signal
import threading
import time
from typing import Any

import websocket

from eodhd._utils import validate_api_key
from eodhd.exceptions import ValidationError

__all__ = ["WebSocketClient"]

_VALID_ENDPOINTS = {"us", "us-quote", "forex", "crypto"}


class WebSocketClient:
    """Stream real-time market data over a WebSocket connection.

    Parameters
    ----------
    api_key:
        EODHD API token.
    endpoint:
        One of ``"us"``, ``"us-quote"``, ``"forex"``, ``"crypto"``.
    symbols:
        List of ticker symbols to subscribe to (max 50).
    store_data:
        If *True*, append every message to an internal list retrievable
        via :meth:`get_data`.
    display_stream:
        Print each raw message to stdout.
    display_candle_1m / display_candle_5m / display_candle_1h:
        Print formed candles at the given interval.
    """

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        symbols: list[str],
        *,
        store_data: bool = False,
        display_stream: bool = False,
        display_candle_1m: bool = False,
        display_candle_5m: bool = False,
        display_candle_1h: bool = False,
    ) -> None:
        validate_api_key(api_key)

        if endpoint not in _VALID_ENDPOINTS:
            raise ValueError(f"Endpoint is invalid, must be one of {_VALID_ENDPOINTS}")

        if not symbols:
            raise ValueError("No symbol(s) provided")

        import re
        _sym_re = re.compile(r"^[A-Za-z0-9\-$]{1,48}$")
        for sym in symbols:
            if not _sym_re.match(sym):
                raise ValueError(f"Symbol is invalid: {sym}")

        if len(symbols) > 50:
            raise ValueError("Max symbol subscription count is 50!")

        self._api_key = api_key
        self._endpoint = endpoint
        self._symbols = symbols
        self._store_data = store_data
        self._display_stream = display_stream
        self._display_candle_1m = display_candle_1m
        self._display_candle_5m = display_candle_5m
        self._display_candle_1h = display_candle_1h

        self.running = True
        self.message: str | None = None
        self.stop_event = threading.Event()
        self.data_list: list[str] = []
        self.ws: websocket.WebSocket | None = None
        self.thread: threading.Thread | None = None
        self.keepalive_thread: threading.Thread | None = None

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum: int, frame: Any) -> None:
        print("Stopping websocket...")
        self.running = False
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()
        print("Websocket stopped.")

    @staticmethod
    def _floor_to_nearest_interval(timestamp_ms: int, interval: str) -> int:
        timestamp_s = timestamp_ms // 1000
        if interval == "1 minute":
            interval_seconds = 60
        elif interval == "5 minutes":
            interval_seconds = 300
        elif interval == "1 hour":
            interval_seconds = 3600
        else:
            raise ValueError(f"Unsupported interval: {interval}")
        return (timestamp_s // interval_seconds) * interval_seconds * 1000

    def _collect_data(self) -> None:
        self.ws = websocket.create_connection(
            f"wss://ws.eodhistoricaldata.com/ws/{self._endpoint}?api_token={self._api_key}"
        )
        payload = {"action": "subscribe", "symbols": ",".join(self._symbols)}
        self.ws.send(json.dumps(payload))

        candle_1m: dict[str, Any] = {}
        candle_5m: dict[str, Any] = {}
        candle_1h: dict[str, Any] = {}

        while not self.stop_event.is_set():
            self.message = self.ws.recv()
            message_json = json.loads(self.message)

            if self._store_data:
                self.data_list.append(self.message)
            if self._display_stream:
                print(self.message)
            if self._display_candle_1m:
                self._update_candle(message_json, candle_1m, "1 minute", 60)
            if self._display_candle_5m:
                self._update_candle(message_json, candle_5m, "5 minutes", 60)
            if self._display_candle_1h:
                self._update_candle(message_json, candle_1h, "1 hour", 60)

        self.ws.close()

    def _update_candle(
        self,
        msg: dict[str, Any],
        candle: dict[str, Any],
        interval: str,
        granularity: int,
    ) -> None:
        if "t" in msg:
            candle_date = self._floor_to_nearest_interval(msg["t"], interval)
            if "t" in candle and candle_date != candle["t"]:
                print(candle)
                candle.clear()
            candle["t"] = candle_date

        if "s" in msg:
            candle["m"] = msg["s"]
            candle["g"] = granularity

        if "p" in msg and "o" not in candle:
            candle["o"] = msg["p"]
            candle["h"] = msg["p"]
            candle["l"] = msg["p"]
            candle["c"] = msg["p"]
            if "q" in msg:
                candle["v"] = float(msg["q"])
        elif "p" in msg and "o" in candle:
            candle["c"] = msg["p"]
            if msg["p"] > candle["h"]:
                candle["h"] = msg["p"]
            if msg["p"] < candle["l"]:
                candle["l"] = msg["p"]
            candle["v"] = candle.get("v", 0) + float(msg.get("q", 0))

    def _keepalive(self, interval: int = 30) -> None:
        if self.ws is not None and hasattr(self.ws, "connected"):
            while self.ws.connected:
                self.ws.ping("keepalive")
                time.sleep(interval)

    def start(self) -> None:
        """Start streaming in background threads."""
        self.thread = threading.Thread(target=self._collect_data)
        self.keepalive_thread = threading.Thread(target=self._keepalive)
        self.thread.start()
        self.keepalive_thread.start()

    def stop(self) -> None:
        """Stop streaming and join threads."""
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()
        if self.keepalive_thread is not None:
            self.keepalive_thread.join()

    def get_data(self) -> list[str]:
        """Return all stored messages (requires ``store_data=True``)."""
        return self.data_list
