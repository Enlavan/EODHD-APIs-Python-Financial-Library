"""Technical indicators.

Endpoint: ``GET /technical/{SYMBOL}``
Docs: https://eodhd.com/financial-apis/technical-indicators-api
"""

from typing import Any

from eodhd.apis._base import BaseAPI

__all__ = ["TechnicalIndicatorsAPI"]

POSSIBLE_FUNCTIONS = frozenset({
    "splitadjusted",
    "avgvol",
    "avgvolccy",
    "sma",
    "ema",
    "wma",
    "volatility",
    "stochastic",
    "rsi",
    "stddev",
    "stochrsi",
    "slope",
    "dmi",
    "dx",       # alias -- normalized to dmi
    "adx",
    "macd",
    "atr",
    "cci",
    "sar",
    "beta",
    "bbands",
    "format_amibroker",
})

_SPLITADJUSTED_ONLY_SUPPORTED = frozenset({
    "sma", "ema", "wma", "volatility", "rsi", "slope", "macd",
})


class TechnicalIndicatorsAPI(BaseAPI):
    """Fetch technical indicator data for a given ticker."""

    def get(
        self,
        ticker: str,
        function: str,
        *,
        period: int | None = 50,
        date_from: str | None = None,
        date_to: str | None = None,
        order: str | None = None,
        splitadjusted_only: str | bool = "0",
        agg_period: str | None = None,
        fast_kperiod: int | None = None,
        slow_kperiod: int | None = None,
        slow_dperiod: int | None = None,
        fast_dperiod: int | None = None,
        fast_period: int | None = None,
        slow_period: int | None = None,
        signal_period: int | None = None,
        acceleration: float | None = None,
        maximum: float | None = None,
        code2: str | None = None,
        fmt: str | None = None,
        filter_field: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Return technical indicator values.

        Parameters
        ----------
        ticker:
            Ticker with exchange suffix, e.g. ``"AAPL.US"``.
        function:
            Indicator function name. See ``POSSIBLE_FUNCTIONS`` for the full
            list.  ``"dx"`` is accepted as an alias for ``"dmi"``.
        period:
            Look-back period (2 -- 100 000, default 50).  Ignored for
            ``splitadjusted`` and ``format_amibroker``.
        date_from:
            Start date (``YYYY-MM-DD``).  Mapped to the ``from`` query param.
        date_to:
            End date (``YYYY-MM-DD``).  Mapped to the ``to`` query param.
        order:
            Sort order -- ``"a"`` (ascending) or ``"d"`` (descending).
        splitadjusted_only:
            ``"0"`` or ``"1"`` (or a bool).  Only sent for functions that
            support it.
        agg_period:
            Aggregation period for ``splitadjusted`` -- ``"d"``/``"w"``/``"m"``.
        fast_kperiod:
            Fast %K period (``stochastic``, ``stochrsi``).
        slow_kperiod:
            Slow %K period (``stochastic``).
        slow_dperiod:
            Slow %D period (``stochastic``).
        fast_dperiod:
            Fast %D period (``stochrsi``).
        fast_period:
            Fast EMA period (``macd``).
        slow_period:
            Slow EMA period (``macd``).
        signal_period:
            Signal period (``macd``).
        acceleration:
            Acceleration factor (``sar``).
        maximum:
            Maximum acceleration (``sar``).
        code2:
            Benchmark ticker for ``beta`` (server default is ``GSPC.INDX``).
        fmt:
            Response format -- ``"json"`` or ``"csv"``.
        filter_field:
            Filter specific fields in the response, e.g. ``"last_ema"``.
            Mapped to the ``filter`` query param.
        """
        # --- basic validation ---
        if not ticker or not str(ticker).strip():
            raise ValueError("ticker is required")
        if not function or not str(function).strip():
            raise ValueError("function is required")

        fn = str(function).strip().lower()
        # normalize dx -> dmi
        if fn == "dx":
            fn = "dmi"

        if fn not in POSSIBLE_FUNCTIONS and fn != "dmi":
            raise ValueError(
                f"Unknown function '{fn}'. Must be one of {sorted(POSSIBLE_FUNCTIONS)}"
            )

        if order is not None:
            order = str(order).lower()
            if order not in ("a", "d"):
                raise ValueError("order must be 'a' or 'd'")

        if fmt is not None:
            fmt = str(fmt).lower()
            if fmt not in ("json", "csv"):
                raise ValueError("fmt must be 'json' or 'csv'")

        # normalize splitadjusted_only
        if isinstance(splitadjusted_only, bool):
            splitadjusted_only = "1" if splitadjusted_only else "0"
        else:
            splitadjusted_only = str(splitadjusted_only)

        # validate period
        if period is not None:
            period = int(period)
            if period < 2 or period > 100_000:
                raise ValueError("period must be in range 2..100000")

        # --- build params ---
        params: dict[str, Any] = {"function": fn}

        if order is not None:
            params["order"] = order
        if date_from is not None:
            params["from"] = date_from
        if date_to is not None:
            params["to"] = date_to
        if fmt is not None:
            params["fmt"] = fmt
        if filter_field is not None and str(filter_field).strip():
            params["filter"] = str(filter_field).strip()

        # period: skip for format_amibroker and splitadjusted
        if fn not in ("format_amibroker", "splitadjusted") and period is not None:
            params["period"] = period

        # splitadjusted_only -- only for supported functions
        if fn in _SPLITADJUSTED_ONLY_SUPPORTED:
            params["splitadjusted_only"] = splitadjusted_only

        # splitadjusted function options
        if fn == "splitadjusted" and agg_period is not None:
            agg_period = str(agg_period).lower()
            if agg_period not in ("d", "w", "m"):
                raise ValueError("agg_period must be 'd', 'w', or 'm'")
            params["agg_period"] = agg_period

        # stochastic
        if fn == "stochastic":
            if fast_kperiod is not None:
                params["fast_kperiod"] = int(fast_kperiod)
            if slow_kperiod is not None:
                params["slow_kperiod"] = int(slow_kperiod)
            if slow_dperiod is not None:
                params["slow_dperiod"] = int(slow_dperiod)

        # stochrsi
        if fn == "stochrsi":
            if fast_kperiod is not None:
                params["fast_kperiod"] = int(fast_kperiod)
            if fast_dperiod is not None:
                params["fast_dperiod"] = int(fast_dperiod)

        # macd
        if fn == "macd":
            if fast_period is not None:
                params["fast_period"] = int(fast_period)
            if slow_period is not None:
                params["slow_period"] = int(slow_period)
            if signal_period is not None:
                params["signal_period"] = int(signal_period)

        # sar
        if fn == "sar":
            if acceleration is not None:
                params["acceleration"] = acceleration
            if maximum is not None:
                params["maximum"] = maximum

        # beta
        if fn == "beta":
            if code2 is not None and str(code2).strip():
                params["code2"] = str(code2).strip()
            if period is not None:
                params["period"] = period

        return self._get("technical", str(ticker).strip(), params=params)
