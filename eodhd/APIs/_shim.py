"""Backward-compatibility shim for the old eodhd.APIs package.

Importing from ``eodhd.APIs`` still works but emits deprecation warnings.
Old class names (including typos like ``UpcomgingEarningsAPI``) are preserved.
"""

import warnings

from eodhd.apis._base import BaseAPI as _NewBaseAPI

# We re-export the old class *names* as thin wrappers that warn on import.
# Each old class name maps to the new module + class.


def __getattr__(name: str):  # noqa: C901
    _MAP = {
        # Old class name -> (new module path, new class name)
        "BaseAPI": ("eodhd.apis._base", "BaseAPI"),
        "HistoricalDividendsAPI": ("eodhd.apis.market_data.historical_dividends", "HistoricalDividendsAPI"),
        "HistoricalSplitsAPI": ("eodhd.apis.market_data.historical_splits", "HistoricalSplitsAPI"),
        "TechnicalIndicatorAPI": ("eodhd.apis.market_data.technical_indicators", "TechnicalIndicatorsAPI"),
        "LiveStockPricesAPI": ("eodhd.apis.market_data.live_prices", "LivePricesAPI"),
        "LiveExtendedQuotesAPI": ("eodhd.apis.market_data.extended_quotes", "ExtendedQuotesAPI"),
        "EconomicEventsDataAPI": ("eodhd.apis.calendar.economic_events", "EconomicEventsAPI"),
        "InsiderTransactionsAPI": ("eodhd.apis.fundamentals.insider_transactions", "InsiderTransactionsAPI"),
        "FundamentalDataAPI": ("eodhd.apis.fundamentals.fundamentals", "FundamentalsAPI"),
        "BulkEodSplitsDividendsDataAPI": ("eodhd.apis.market_data.bulk_eod", "BulkEodAPI"),
        "UpcomgingEarningsAPI": ("eodhd.apis.calendar.earnings", "EarningsAPI"),  # typo preserved
        "UpcomingEarningsAPI": ("eodhd.apis.calendar.earnings", "EarningsAPI"),
        "EarningTrendsAPI": ("eodhd.apis.calendar.trends", "TrendsAPI"),
        "UpcomingIPOsAPI": ("eodhd.apis.calendar.ipos", "IposAPI"),
        "UpcomingDividendsAPI": ("eodhd.apis.calendar.dividends", "DividendsAPI"),
        "UpcomingSplitsAPI": ("eodhd.apis.calendar.splits", "SplitsAPI"),
        "MacroIndicatorsAPI": ("eodhd.apis.macro.macro_indicator", "MacroIndicatorAPI"),
        "ListOfExchangesAPI": ("eodhd.apis.exchanges.exchanges_list", "ExchangesListAPI"),
        "TradingHours_StockMarketHolidays_SymbolsChangeHistoryAPI": (
            "eodhd.apis.exchanges.exchange_details",
            "ExchangeDetailsAPI",
        ),
        "StockMarketScreenerAPI": ("eodhd.apis.market_data.screener", "ScreenerAPI"),
        "FinancialNewsAPI": ("eodhd.apis.fundamentals.news", "NewsAPI"),
        "IntradayDataAPI": ("eodhd.apis.market_data.intraday", "IntradayAPI"),
        "EodHistoricalStockMarketDataAPI": ("eodhd.apis.market_data.historical_eod", "HistoricalEodAPI"),
        "StockMarketTickDataAPI": ("eodhd.apis.marketplace.tick_data.us_tick_data", "USTickDataAPI"),
        "HistoricalMarketCapitalizationAPI": ("eodhd.apis.market_data.historical_market_cap", "HistoricalMarketCapAPI"),
        "CBOEIndexFeedAPI": ("eodhd.apis.exchanges.cboe_index", "CboeIndexAPI"),
        "IDMappingAPI": ("eodhd.apis.exchanges.cboe_index", "CboeIndexAPI"),
        "MPIndexComponentsAPI": ("eodhd.apis.exchanges.index_components", "IndexComponentsAPI"),
        "MPIndicesListAPI": ("eodhd.apis.exchanges.indices_list", "IndicesListAPI"),
        "MPUSOptionsContractsAPI": ("eodhd.apis.marketplace.options.contracts", "ContractsAPI"),
        "MPUSOptionsEODAPI": ("eodhd.apis.marketplace.options.eod", "EodAPI"),
        "MPUSOptionsUnderlyingSymbolsAPI": ("eodhd.apis.marketplace.options.underlyings", "UnderlyingsAPI"),
    }

    if name in _MAP:
        module_path, class_name = _MAP[name]
        warnings.warn(
            f"Importing {name} from eodhd.APIs is deprecated. "
            f"Use {module_path}.{class_name} instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        import importlib

        mod = importlib.import_module(module_path)
        return getattr(mod, class_name)

    raise AttributeError(f"module 'eodhd.APIs' has no attribute {name!r}")
