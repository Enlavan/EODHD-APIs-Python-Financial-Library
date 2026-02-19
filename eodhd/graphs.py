"""Fibonacci extension / retracement charting.

Refactored from the original ``eodhdgraphs.py``.  pandas and
matplotlib are lazy-imported so they remain optional dependencies.
"""

from typing import Any

__all__ = ["EODHDGraphs"]


class EODHDGraphs:
    """Static helper methods for Fibonacci visualizations."""

    @staticmethod
    def fibonacci_extension(
        df: Any = None,
        trend_direction: str = "uptrend",
        price_field: str = "close",
        save_file: str = "",
        quiet: bool = False,
    ) -> None:
        """Plot Fibonacci extension levels on a price chart."""
        import matplotlib.pyplot as plt

        if trend_direction not in ("uptrend", "downtrend"):
            raise ValueError("trend_direction must be either uptrend or downtrend")
        if price_field not in ("close", "adjusted_close"):
            raise ValueError("price_field must be either close or adjusted_close")

        low = df[price_field].min()
        high = df[price_field].max()
        diff = high - low

        if trend_direction == "uptrend":
            fib2618 = high + diff * 2.618
            fib2000 = high + diff * 2
            fib1618 = high + diff * 1.618
            fib1382 = high + diff * 1.382
            fib1000 = high + diff * 1
            fib618 = high + diff * 0.618
        else:
            fib2618 = low - diff * 2.618
            fib2000 = low - diff * 2
            fib1618 = low - diff * 1.618
            fib1382 = low - diff * 1.382
            fib1000 = low - diff * 1
            fib618 = low - diff * 0.618

        plt.figure(figsize=(30, 10))
        plt.plot(df["adjusted_close"], color="black", label="Price")
        plt.axhline(y=fib2618, color="limegreen", linestyle="-", label="261.8%")
        plt.axhline(y=fib2000, color="slateblue", linestyle="-", label="200%")
        plt.axhline(y=fib1618, color="mediumvioletred", linestyle="-", label="161.8%")
        plt.axhline(y=fib1382, color="gold", linestyle="-", label="138.2%")
        plt.axhline(y=fib1000, color="dodgerblue", linestyle="-", label="100%")
        plt.axhline(y=fib618, color="darkturquoise", linestyle="-", label="61.8%")
        plt.ylabel("Price")
        plt.xticks(rotation=90)
        plt.title(f"Fibonacci Extension ({trend_direction})")
        plt.legend()
        if save_file:
            plt.savefig(save_file)
        if not quiet:
            plt.show()

    @staticmethod
    def fibonacci_retracement(
        df: Any = None,
        trend_direction: str = "uptrend",
        price_field: str = "close",
        save_file: str = "",
        quiet: bool = False,
    ) -> None:
        """Plot Fibonacci retracement levels on a price chart."""
        import matplotlib.pyplot as plt

        if trend_direction not in ("uptrend", "downtrend"):
            raise ValueError("trend_direction must be either uptrend or downtrend")
        if price_field not in ("close", "adjusted_close"):
            raise ValueError("price_field must be either close or adjusted_close")

        low = df[price_field].min()
        high = df[price_field].max()
        diff = high - low

        if trend_direction == "uptrend":
            fib0 = high
            fib236 = high - diff * 0.236
            fib382 = high - diff * 0.382
            fib50 = high - diff * 0.5
            fib618 = high - diff * 0.618
            fib764 = high - diff * 0.764
            fib100 = low
        else:
            fib100 = high
            fib764 = low + diff * 0.764
            fib618 = low + diff * 0.618
            fib50 = low + diff * 0.5
            fib382 = low + diff * 0.382
            fib236 = low + diff * 0.236
            fib0 = low

        plt.figure(figsize=(30, 10))
        plt.plot(df["adjusted_close"], color="black", label="Price")
        plt.axhline(y=fib100, color="limegreen", linestyle="-", label="100%")
        plt.axhline(y=fib764, color="slateblue", linestyle="-", label="76.4%")
        plt.axhline(y=fib618, color="mediumvioletred", linestyle="-", label="61.8%")
        plt.axhline(y=fib50, color="gold", linestyle="-", label="50%")
        plt.axhline(y=fib382, color="dodgerblue", linestyle="-", label="38.2%")
        plt.axhline(y=fib236, color="darkturquoise", linestyle="-", label="23.6%")
        plt.axhline(y=fib0, color="lightcoral", linestyle="-", label="0%")
        plt.ylabel("Price")
        plt.xticks(rotation=90)
        plt.title(f"Fibonacci Retracement ({trend_direction})")
        plt.legend()
        if save_file:
            plt.savefig(save_file)
        if not quiet:
            plt.show()
