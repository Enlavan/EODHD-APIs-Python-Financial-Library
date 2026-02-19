"""Market scanner with technical analysis overlays.

Refactored from the ``ScannerClient`` in the original ``apiclient.py``.
Requires the ``[scanner]`` extra (pandas, numpy, rich).
"""
from typing import Any, TYPE_CHECKING

from eodhd._utils import validate_api_key

if TYPE_CHECKING:
    import pandas as pd

__all__ = ["ScannerClient"]


class ScannerClient:
    """Scan exchange symbols and compute basic technical indicators.

    Parameters
    ----------
    api_key:
        EODHD API token.
    """

    def __init__(self, api_key: str) -> None:
        validate_api_key(api_key)

        # Import here so the rest of the library works without pandas
        from eodhd.client import APIClient

        self.api = APIClient(api_key)

    def scan_markets(
        self,
        market_type: str = "CC",
        interval: str = "d",
        quote_currency: str = "USD",
        request_limit: int = 5000,
    ) -> "pd.DataFrame":
        """Scan a market for symbols with SMA/EMA crossover signals.

        Returns a DataFrame sorted by bull/bear market status, next
        action, volume, and ATR percentage.
        """
        import numpy as np
        import pandas as pd
        from rich.progress import track

        if request_limit < 0 or request_limit > 100000:
            raise ValueError("request limit is out of bounds!")

        df_dataset = pd.DataFrame()

        resp = self.api.get_exchange_symbols(uri=market_type)
        symbol_list = resp[
            resp.Code.str.endswith(f"-{quote_currency}", na=False)
        ].Code.to_numpy()

        if request_limit > 0:
            symbol_list = symbol_list[: request_limit - 1]

        for symbol in track(symbol_list, description="Processing..."):
            df_data = self.api.get_historical_data(f"{symbol}.{market_type}", interval)
            if len(df_data) >= 200:
                df_data["sma50"] = df_data.adjusted_close.rolling(50, min_periods=1).mean()
                df_data["sma200"] = df_data.adjusted_close.rolling(200, min_periods=1).mean()
                df_data["bull_market"] = df_data.sma50 >= df_data.sma200

                df_data["ema12"] = df_data.adjusted_close.ewm(span=12, adjust=False).mean()
                df_data["ema26"] = df_data.adjusted_close.ewm(span=26, adjust=False).mean()
                df_data.loc[df_data["ema12"] > df_data["ema26"], "next_action"] = "sell"
                df_data["next_action"] = df_data["next_action"].fillna("buy")

                high_low = df_data["high"] - df_data["low"]
                high_close = abs(df_data["high"] - df_data["adjusted_close"].shift())
                low_close = abs(df_data["low"] - df_data["adjusted_close"].shift())
                ranges = pd.concat([high_low, high_close, low_close], axis=1)
                true_range = np.max(ranges, axis=1)
                df_data["atr14"] = true_range.rolling(14).sum() / 14
                df_data["atr14_pcnt"] = (
                    df_data["atr14"] / df_data["adjusted_close"] * 100
                ).round(2)

                df_dataset = pd.concat([df_dataset, df_data.tail(1)])

        df_dataset.replace([np.inf, -np.inf], np.nan, inplace=True)
        df_dataset.dropna(subset=["atr14_pcnt"], inplace=True)

        df_dataset.sort_values(
            by=["bull_market", "next_action", "volume", "atr14_pcnt"],
            ascending=[False, True, False, False],
            inplace=True,
        )
        df_dataset.to_csv("dataset.csv")

        return df_dataset
