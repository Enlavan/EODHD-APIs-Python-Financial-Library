"""APIClient facade — single entry point for the EODHD API.

Usage (new namespaced style)::

    from eodhd import APIClient

    client = APIClient("YOUR_API_KEY")
    data = client.market_data.historical_eod.get("AAPL.US")

All legacy flat methods (``client.get_historical_dividends_data(…)``)
are preserved as thin delegates to the namespaced APIs so existing
code keeps working without changes.
"""
import json
import re
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, TYPE_CHECKING

from eodhd._http import HTTPClient
from eodhd._utils import validate_api_key
from eodhd._types import Interval, Order

# -- Market data --
from eodhd.apis.market_data.historical_eod import HistoricalEodAPI
from eodhd.apis.market_data.intraday import IntradayAPI
from eodhd.apis.market_data.live_prices import LivePricesAPI
from eodhd.apis.market_data.extended_quotes import ExtendedQuotesAPI
from eodhd.apis.market_data.technical_indicators import TechnicalIndicatorsAPI
from eodhd.apis.market_data.screener import ScreenerAPI
from eodhd.apis.market_data.search import SearchAPI
from eodhd.apis.market_data.logos import LogosAPI
from eodhd.apis.market_data.historical_market_cap import HistoricalMarketCapAPI
from eodhd.apis.market_data.symbol_change_history import SymbolChangeHistoryAPI
from eodhd.apis.market_data.bulk_eod import BulkEodAPI
from eodhd.apis.market_data.historical_dividends import HistoricalDividendsAPI
from eodhd.apis.market_data.historical_splits import HistoricalSplitsAPI

# -- Fundamentals --
from eodhd.apis.fundamentals.fundamentals import FundamentalsAPI
from eodhd.apis.fundamentals.bulk_fundamentals import BulkFundamentalsAPI
from eodhd.apis.fundamentals.news import NewsAPI
from eodhd.apis.fundamentals.sentiment import SentimentAPI
from eodhd.apis.fundamentals.news_word_weights import NewsWordWeightsAPI
from eodhd.apis.fundamentals.insider_transactions import InsiderTransactionsAPI

# -- Calendar --
from eodhd.apis.calendar.earnings import EarningsAPI
from eodhd.apis.calendar.trends import TrendsAPI
from eodhd.apis.calendar.dividends import DividendsAPI as CalendarDividendsAPI
from eodhd.apis.calendar.splits import SplitsAPI as CalendarSplitsAPI
from eodhd.apis.calendar.ipos import IposAPI
from eodhd.apis.calendar.economic_events import EconomicEventsAPI

# -- Exchanges --
from eodhd.apis.exchanges.exchanges_list import ExchangesListAPI
from eodhd.apis.exchanges.exchange_details import ExchangeDetailsAPI
from eodhd.apis.exchanges.exchange_tickers import ExchangeTickersAPI
from eodhd.apis.exchanges.index_components import IndexComponentsAPI
from eodhd.apis.exchanges.indices_list import IndicesListAPI
from eodhd.apis.exchanges.cboe_index import CboeIndexAPI
from eodhd.apis.exchanges.cboe_indices import CboeIndicesAPI

# -- Macro --
from eodhd.apis.macro.macro_indicator import MacroIndicatorAPI
from eodhd.apis.macro.treasury_bill_rates import TreasuryBillRatesAPI
from eodhd.apis.macro.treasury_long_term import TreasuryLongTermAPI
from eodhd.apis.macro.treasury_yield import TreasuryYieldAPI
from eodhd.apis.macro.treasury_real_yield import TreasuryRealYieldAPI

# -- User --
from eodhd.apis.user.user_details import UserDetailsAPI

# -- Marketplace --
from eodhd.apis.marketplace.options.eod import EodAPI as OptionsEodAPI
from eodhd.apis.marketplace.options.contracts import ContractsAPI as OptionsContractsAPI
from eodhd.apis.marketplace.options.underlyings import UnderlyingsAPI as OptionsUnderlyingsAPI

from eodhd.apis.marketplace.tick_data.us_tick_data import USTickDataAPI
from eodhd.apis.marketplace.tick_data.marketplace_tick_data import MarketplaceTickDataAPI

from eodhd.apis.marketplace.trading_hours.list_markets import ListMarketsAPI
from eodhd.apis.marketplace.trading_hours.lookup import LookupAPI
from eodhd.apis.marketplace.trading_hours.market_details import MarketDetailsAPI
from eodhd.apis.marketplace.trading_hours.market_status import MarketStatusAPI

from eodhd.apis.marketplace.illio.best_worst import BestWorstAPI
from eodhd.apis.marketplace.illio.beta_bands import BetaBandsAPI
from eodhd.apis.marketplace.illio.largest_volatility import LargestVolatilityAPI
from eodhd.apis.marketplace.illio.performance import PerformanceAPI
from eodhd.apis.marketplace.illio.risk_return import RiskReturnAPI
from eodhd.apis.marketplace.illio.volatility import VolatilityAPI
from eodhd.apis.marketplace.illio.performance_insights import PerformanceInsightsAPI
from eodhd.apis.marketplace.illio.risk_insights import RiskInsightsAPI

from eodhd.apis.marketplace.esg.companies import CompaniesAPI as EsgCompaniesAPI
from eodhd.apis.marketplace.esg.countries import CountriesAPI as EsgCountriesAPI
from eodhd.apis.marketplace.esg.sectors import SectorsAPI as EsgSectorsAPI
from eodhd.apis.marketplace.esg.view_company import ViewCompanyAPI
from eodhd.apis.marketplace.esg.view_country import ViewCountryAPI
from eodhd.apis.marketplace.esg.view_sector import ViewSectorAPI

from eodhd.apis.marketplace.praams.bank_balance_sheet import BankBalanceSheetAPI
from eodhd.apis.marketplace.praams.bank_income_statement import BankIncomeStatementAPI
from eodhd.apis.marketplace.praams.bond_analyze import BondAnalyzeAPI
from eodhd.apis.marketplace.praams.report_bond import ReportBondAPI
from eodhd.apis.marketplace.praams.report_equity import ReportEquityAPI
from eodhd.apis.marketplace.praams.risk_scoring import RiskScoringAPI
from eodhd.apis.marketplace.praams.screener_bond import ScreenerBondAPI
from eodhd.apis.marketplace.praams.screener_equity import ScreenerEquityAPI

if TYPE_CHECKING:
    import pandas as pd

__all__ = ["APIClient"]


# ------------------------------------------------------------------ #
# Namespace helpers                                                    #
# ------------------------------------------------------------------ #

class _MarketDataNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.historical_eod = HistoricalEodAPI(http)
        self.intraday = IntradayAPI(http)
        self.live_prices = LivePricesAPI(http)
        self.extended_quotes = ExtendedQuotesAPI(http)
        self.technical_indicators = TechnicalIndicatorsAPI(http)
        self.screener = ScreenerAPI(http)
        self.search = SearchAPI(http)
        self.logos = LogosAPI(http)
        self.historical_market_cap = HistoricalMarketCapAPI(http)
        self.symbol_change_history = SymbolChangeHistoryAPI(http)
        self.bulk_eod = BulkEodAPI(http)
        self.historical_dividends = HistoricalDividendsAPI(http)
        self.historical_splits = HistoricalSplitsAPI(http)


class _FundamentalsNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.fundamentals = FundamentalsAPI(http)
        self.bulk_fundamentals = BulkFundamentalsAPI(http)
        self.news = NewsAPI(http)
        self.sentiment = SentimentAPI(http)
        self.news_word_weights = NewsWordWeightsAPI(http)
        self.insider_transactions = InsiderTransactionsAPI(http)


class _CalendarNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.earnings = EarningsAPI(http)
        self.trends = TrendsAPI(http)
        self.dividends = CalendarDividendsAPI(http)
        self.splits = CalendarSplitsAPI(http)
        self.ipos = IposAPI(http)
        self.economic_events = EconomicEventsAPI(http)


class _ExchangesNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.exchanges_list = ExchangesListAPI(http)
        self.exchange_details = ExchangeDetailsAPI(http)
        self.exchange_tickers = ExchangeTickersAPI(http)
        self.index_components = IndexComponentsAPI(http)
        self.indices_list = IndicesListAPI(http)
        self.cboe_index = CboeIndexAPI(http)
        self.cboe_indices = CboeIndicesAPI(http)


class _MacroNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.macro_indicator = MacroIndicatorAPI(http)
        self.treasury_bill_rates = TreasuryBillRatesAPI(http)
        self.treasury_long_term = TreasuryLongTermAPI(http)
        self.treasury_yield = TreasuryYieldAPI(http)
        self.treasury_real_yield = TreasuryRealYieldAPI(http)


class _UserNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.user_details = UserDetailsAPI(http)


class _OptionsNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.eod = OptionsEodAPI(http)
        self.contracts = OptionsContractsAPI(http)
        self.underlyings = OptionsUnderlyingsAPI(http)


class _TickDataNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.us_tick_data = USTickDataAPI(http)
        self.marketplace_tick_data = MarketplaceTickDataAPI(http)


class _TradingHoursNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.list_markets = ListMarketsAPI(http)
        self.lookup = LookupAPI(http)
        self.market_details = MarketDetailsAPI(http)
        self.market_status = MarketStatusAPI(http)


class _IllioNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.best_worst = BestWorstAPI(http)
        self.beta_bands = BetaBandsAPI(http)
        self.largest_volatility = LargestVolatilityAPI(http)
        self.performance = PerformanceAPI(http)
        self.risk_return = RiskReturnAPI(http)
        self.volatility = VolatilityAPI(http)
        self.performance_insights = PerformanceInsightsAPI(http)
        self.risk_insights = RiskInsightsAPI(http)


class _EsgNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.companies = EsgCompaniesAPI(http)
        self.countries = EsgCountriesAPI(http)
        self.sectors = EsgSectorsAPI(http)
        self.view_company = ViewCompanyAPI(http)
        self.view_country = ViewCountryAPI(http)
        self.view_sector = ViewSectorAPI(http)


class _PraamsNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.bank_balance_sheet = BankBalanceSheetAPI(http)
        self.bank_income_statement = BankIncomeStatementAPI(http)
        self.bond_analyze = BondAnalyzeAPI(http)
        self.report_bond = ReportBondAPI(http)
        self.report_equity = ReportEquityAPI(http)
        self.risk_scoring = RiskScoringAPI(http)
        self.screener_bond = ScreenerBondAPI(http)
        self.screener_equity = ScreenerEquityAPI(http)


class _MarketplaceNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self.options = _OptionsNamespace(http)
        self.tick_data = _TickDataNamespace(http)
        self.trading_hours = _TradingHoursNamespace(http)
        self.illio = _IllioNamespace(http)
        self.esg = _EsgNamespace(http)
        self.praams = _PraamsNamespace(http)


# ------------------------------------------------------------------ #
# Main client                                                          #
# ------------------------------------------------------------------ #

class APIClient:
    """Unified EODHD API client.

    Parameters
    ----------
    api_key:
        Your EODHD API token (or ``"demo"`` for the free demo key).
    base_url:
        Override the API root URL.
    timeout:
        HTTP request timeout in seconds.
    max_retries:
        Number of retries on transient failures.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://eodhd.com/api",
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        validate_api_key(api_key)

        self._api_key = api_key
        self._http = HTTPClient(
            api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        # Namespaces
        self.market_data = _MarketDataNamespace(self._http)
        self.fundamentals = _FundamentalsNamespace(self._http)
        self.calendar = _CalendarNamespace(self._http)
        self.exchanges = _ExchangesNamespace(self._http)
        self.macro = _MacroNamespace(self._http)
        self.user = _UserNamespace(self._http)
        self.marketplace = _MarketplaceNamespace(self._http)

    # ================================================================ #
    # Backward-compatible flat methods                                   #
    # ================================================================ #
    # These delegate to the namespaced API instances so old code like
    #   client.get_historical_dividends_data(ticker="AAPL.US")
    # keeps working without changes.

    # -- convenience kept for ScannerClient --
    @property
    def _api_url(self) -> str:
        return self._http._base_url

    def _rest_get(self, endpoint: str = "", uri: str = "", querystring: str = "") -> "pd.DataFrame":
        """Legacy REST GET that returns a pandas DataFrame.

        Kept for backward compatibility with ``get_historical_data``
        and ``get_exchanges`` / ``get_exchange_symbols``.
        """
        import pandas as _pd

        if not endpoint.strip():
            raise ValueError("endpoint is empty!")

        data = self._http.get(endpoint, uri)

        if isinstance(data, list):
            return _pd.DataFrame.from_dict(data)
        else:
            return _pd.DataFrame(data, index=[0])

    def get_exchanges(self) -> "pd.DataFrame":
        """Get supported exchanges (returns DataFrame for backward compat)."""
        import pandas as _pd

        data = self.exchanges.exchanges_list.get()
        return _pd.DataFrame.from_dict(data)

    def get_exchange_symbols(self, uri: str = "", delisted: bool = False) -> "pd.DataFrame":
        """Get exchange symbols (returns DataFrame for backward compat)."""
        import pandas as _pd

        if not uri.strip():
            raise ValueError("endpoint uri is empty!")
        data = self.exchanges.exchange_tickers.get(uri, delisted=1 if delisted else 0)
        return _pd.DataFrame.from_dict(data)

    def get_historical_data(
        self,
        symbol: str,
        interval: str = "d",
        iso8601_start: str = "",
        iso8601_end: str = "",
        results: int = 300,
    ) -> "pd.DataFrame":
        """Fetch OHLCV data and return a pandas DataFrame.

        This is the legacy method with full pandas processing. For the
        raw JSON equivalent, use ``client.market_data.historical_eod.get()``
        or ``client.market_data.intraday.get()``.
        """
        import pandas as _pd
        import numpy as _np

        prog = re.compile(r"^[A-Za-z0-9\-$\.+]{1,48}$")
        if not prog.match(symbol):
            raise ValueError(f"Symbol is invalid: {symbol}")

        if symbol.count(".") == 2:
            symbol = symbol.replace(".", "-", 1)

        try:
            Interval(interval)
        except ValueError:
            return _pd.DataFrame()

        df_data = _pd.DataFrame()
        re_date_only = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        re_iso8601 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

        if interval in ("d", "w", "m"):
            if iso8601_end == "" or (
                not re_iso8601.match(iso8601_end) and not re_date_only.match(iso8601_end)
            ):
                date_to = datetime.today().date()
            else:
                if re_date_only.match(iso8601_end):
                    date_to = datetime.strptime(iso8601_end, "%Y-%m-%d").date()
                elif re_iso8601.match(iso8601_end):
                    date_to = datetime.strptime(iso8601_end, "%Y-%m-%dT%H:%M:%S").date()
                else:
                    date_to = datetime.today().date()

            if iso8601_start == "" or (
                not re_iso8601.match(iso8601_start) and not re_date_only.match(iso8601_start)
            ):
                date_from = date_to - timedelta(days=(results - 1))
            else:
                if re_date_only.match(iso8601_start):
                    date_from = datetime.strptime(iso8601_start, "%Y-%m-%d").date()
                elif re_iso8601.match(iso8601_start):
                    date_from = datetime.strptime(iso8601_start, "%Y-%m-%dT%H:%M:%S").date()
                else:
                    date_from = datetime.today().date()

            data = self.market_data.historical_eod.get(
                symbol,
                period=interval,
                from_date=str(date_from),
                to_date=str(date_to),
            )
            if not data:
                return _pd.DataFrame(
                    columns=["symbol", "interval", "open", "high", "low", "close", "adjusted_close", "volume"]
                )

            df_data = _pd.DataFrame.from_dict(data) if isinstance(data, list) else _pd.DataFrame(data, index=[0])

            if len(df_data) == 0:
                return _pd.DataFrame(
                    columns=["symbol", "interval", "open", "high", "low", "close", "adjusted_close", "volume"]
                )

            if iso8601_start == "" and iso8601_end == "":
                df_data = df_data.tail(results)
            elif iso8601_start != "" and iso8601_end == "":
                df_data = df_data.head(results)

            df_data["symbol"] = symbol
            df_data["interval"] = interval

            tsidx = _pd.DatetimeIndex(_pd.to_datetime(df_data["date"]).dt.strftime("%Y-%m-%d"))
            df_data.set_index(tsidx, inplace=True)
            df_data = df_data.drop(columns=["date"])

            df_data.columns = ["open", "high", "low", "close", "adjusted_close", "volume", "symbol", "interval"]
            df_data.fillna(0, inplace=True)
            for col in ["open", "high", "low", "close", "adjusted_close", "volume"]:
                df_data[col] = df_data[col].astype(object)

            return df_data[["symbol", "interval", "open", "high", "low", "close", "adjusted_close", "volume"]]

        elif interval in ("1m", "5m", "1h"):
            re_epoch = re.compile(r"^\d{10}$")

            if iso8601_end == "" or (
                not re_iso8601.match(iso8601_end) and not re_date_only.match(iso8601_end)
            ):
                date_to = str(int(datetime.today().timestamp()))
            else:
                if re_date_only.match(iso8601_end):
                    date_to = str(int(datetime.strptime(iso8601_end, "%Y-%m-%d").timestamp()))
                elif re_iso8601.match(iso8601_end):
                    date_to = str(int(datetime.strptime(iso8601_end, "%Y-%m-%dT%H:%M:%S").timestamp()))
                elif re_epoch.match(iso8601_end):
                    date_to = str(iso8601_end)
                else:
                    date_to = str(int(datetime.today().timestamp()))

            if iso8601_start == "" or (
                not re_iso8601.match(iso8601_start) and not re_date_only.match(iso8601_start)
            ):
                date_from = str(
                    int((datetime.fromtimestamp(int(date_to)) - timedelta(days=120)).timestamp())
                )
            else:
                if re_date_only.match(iso8601_start):
                    date_from = str(int(datetime.strptime(iso8601_start, "%Y-%m-%d").timestamp()))
                elif re_iso8601.match(iso8601_start):
                    date_from = str(int(datetime.strptime(iso8601_start, "%Y-%m-%dT%H:%M:%S").timestamp()))
                else:
                    date_from = str(int(datetime.today().timestamp()))

            data = self.market_data.intraday.get(
                symbol,
                interval=interval,
                from_unix_time=date_from,
                to_unix_time=date_to,
            )
            if not data:
                return _pd.DataFrame(
                    columns=["symbol", "interval", "open", "high", "low", "close", "adjusted_close", "volume"]
                )

            df_data = _pd.DataFrame.from_dict(data) if isinstance(data, list) else _pd.DataFrame(data, index=[0])

            if len(df_data) == 0:
                return _pd.DataFrame(
                    columns=["symbol", "interval", "open", "high", "low", "close", "adjusted_close", "volume"]
                )

            if iso8601_start == "" and iso8601_end == "":
                df_data = df_data.tail(results)
            elif iso8601_start != "" and iso8601_end == "":
                df_data = df_data.head(results)

            df_data["symbol"] = symbol
            df_data["interval"] = interval

            if "datetime" in df_data.columns:
                tsidx = _pd.DatetimeIndex(
                    _pd.to_datetime(df_data["datetime"]).dt.strftime("%Y-%m-%d %H:%M:%S")
                )
                df_data.set_index(tsidx, inplace=True)
                df_data = df_data.drop(columns=["datetime"])

            df_data.columns = ["epoch", "gmtoffset", "open", "high", "low", "close", "volume", "symbol", "interval"]
            df_data.fillna(0, inplace=True)
            for col in ["gmtoffset", "epoch", "open", "high", "low", "close", "volume"]:
                df_data[col] = df_data[col].astype(object)

            return df_data[["epoch", "gmtoffset", "symbol", "interval", "open", "high", "low", "close", "volume"]]

        else:
            raise ValueError(f"invalid interval: {interval}")

    # -- direct delegates --

    def get_historical_dividends_data(
        self, ticker: str, date_to: str | None = None, date_from: str | None = None
    ) -> list[dict[str, Any]]:
        return self.market_data.historical_dividends.get(ticker, date_from=date_from, date_to=date_to)

    def get_historical_splits_data(
        self, ticker: str, date_to: str | None = None, date_from: str | None = None
    ) -> list[dict[str, Any]]:
        return self.market_data.historical_splits.get(ticker, date_from=date_from, date_to=date_to)

    def get_technical_indicator_data(
        self,
        ticker: str,
        function: str,
        period: int = 50,
        date_from: str | None = None,
        date_to: str | None = None,
        order: str = "a",
        splitadjusted_only: str = "0",
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
    ) -> list[dict[str, Any]]:
        return self.market_data.technical_indicators.get(
            ticker=ticker,
            function=function,
            period=period,
            date_from=date_from,
            date_to=date_to,
            order=order,
            splitadjusted_only=splitadjusted_only,
            agg_period=agg_period,
            fast_kperiod=fast_kperiod,
            slow_kperiod=slow_kperiod,
            slow_dperiod=slow_dperiod,
            fast_dperiod=fast_dperiod,
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
            acceleration=acceleration,
            maximum=maximum,
        )

    def get_live_stock_prices(
        self, ticker: str, date_to: str | None = None, date_from: str | None = None, s: str | None = None
    ) -> list[dict[str, Any]] | dict[str, Any]:
        return self.market_data.live_prices.get(ticker, s=s)

    def get_economic_events_data(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        country: str | None = None,
        comparison: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        return self.calendar.economic_events.get(
            date_from=date_from,
            date_to=date_to,
            country=country,
            comparison=comparison,
            offset=offset,
            limit=limit,
        )

    def get_insider_transactions_data(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        code: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        return self.fundamentals.insider_transactions.get(
            date_from=date_from,
            date_to=date_to,
            code=code,
            limit=limit,
        )

    def get_fundamentals_data(self, ticker: str) -> dict[str, Any]:
        return self.fundamentals.fundamentals.get(ticker)

    def get_eod_splits_dividends_data(
        self,
        country: str = "US",
        type: str | None = None,
        date: str | None = None,
        symbols: str | None = None,
        filter: str | None = None,
    ) -> list[dict[str, Any]]:
        return self.market_data.bulk_eod.get(
            country,
            type=type,
            date=date,
            symbols=symbols,
            filter=filter,
        )

    def get_upcoming_earnings_data(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        symbols: str | None = None,
    ) -> dict[str, Any]:
        return self.calendar.earnings.get(from_date=from_date, to_date=to_date, symbols=symbols)

    def get_earning_trends_data(self, symbols: str) -> dict[str, Any]:
        return self.calendar.trends.get(symbols=symbols)

    def get_upcoming_IPOs_data(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> dict[str, Any]:
        return self.calendar.ipos.get(from_date=from_date, to_date=to_date)

    def get_upcoming_splits_data(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> dict[str, Any]:
        return self.calendar.splits.get(from_date=from_date, to_date=to_date)

    def get_upcoming_dividends_data(
        self,
        symbol: str | None = None,
        date_eq: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        page_limit: int | None = None,
        page_offset: int | None = None,
    ) -> dict[str, Any]:
        return self.calendar.dividends.get(
            symbol=symbol,
            date_eq=date_eq,
            date_from=date_from,
            date_to=date_to,
            page_limit=page_limit,
            page_offset=page_offset,
        )

    def get_macro_indicators_data(
        self, country: str, indicator: str | None = None
    ) -> list[dict[str, Any]]:
        return self.macro.macro_indicator.get(country, indicator=indicator)

    def get_list_of_exchanges(self) -> list[dict[str, Any]]:
        return self.exchanges.exchanges_list.get()

    def get_list_of_tickers(self, code: str, delisted: int = 0) -> list[dict[str, Any]]:
        return self.exchanges.exchange_tickers.get(code, delisted=delisted)

    def get_details_trading_hours_stock_market_holidays(
        self, code: str, from_date: str | None = None, to_date: str | None = None
    ) -> dict[str, Any]:
        return self.exchanges.exchange_details.get(code, from_date=from_date, to_date=to_date)

    def symbol_change_history(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        return self.market_data.symbol_change_history.get(from_date=from_date, to_date=to_date)

    def stock_market_screener(
        self,
        sort: str | None = None,
        filters: list | None = None,
        limit: int | None = None,
        signals: str | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        return self.market_data.screener.get(
            sort=sort,
            filters=filters,
            limit=limit,
            signals=signals,
            offset=offset,
        )

    def get_intraday_historical_data(
        self,
        symbol: str,
        interval: str = "5m",
        from_unix_time: str | None = None,
        to_unix_time: str | None = None,
    ) -> list[dict[str, Any]]:
        return self.market_data.intraday.get(
            symbol,
            interval=interval,
            from_unix_time=from_unix_time,
            to_unix_time=to_unix_time,
        )

    def get_eod_historical_stock_market_data(
        self,
        symbol: str,
        period: str = "d",
        from_date: str | None = None,
        to_date: str | None = None,
        order: str | None = None,
    ) -> list[dict[str, Any]]:
        return self.market_data.historical_eod.get(
            symbol,
            period=period,
            from_date=from_date,
            to_date=to_date,
            order=order,
        )

    def get_stock_market_tick_data(
        self,
        symbol: str,
        from_timestamp: str,
        to_timestamp: str,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        return self.marketplace.tick_data.us_tick_data.get(
            symbol,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
            limit=limit,
        )

    def financial_news(
        self,
        s: str | None = None,
        t: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        return self.fundamentals.news.get(
            s=s,
            t=t,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            offset=offset,
        )

    def get_sentiment(
        self,
        s: str,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        return self.fundamentals.sentiment.get(s=s, from_date=from_date, to_date=to_date)

    def news_word_weights(
        self,
        s: str,
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        return self.fundamentals.news_word_weights.get(
            s=s,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
        )

    def get_historical_market_capitalization_data(
        self,
        ticker: str,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict[str, Any]]:
        return self.market_data.historical_market_cap.get(
            ticker, from_date=from_date, to_date=to_date
        )

    def get_cboe_index_data(
        self,
        index_code: str,
        feed_type: str,
        date: str,
        fmt: str | None = None,
    ) -> dict[str, Any]:
        return self.exchanges.cboe_index.get(
            index_code=index_code,
            feed_type=feed_type,
            date=date,
            fmt=fmt,
        )

    def get_cboe_indices_list(self, fmt: str | None = None) -> dict[str, Any]:
        return self.exchanges.cboe_indices.get(fmt=fmt)

    def get_id_mapping(
        self,
        symbol: str | None = None,
        ex: str | None = None,
        isin: str | None = None,
        figi: str | None = None,
        lei: str | None = None,
        cusip: str | None = None,
        cik: str | None = None,
        page_limit: int | None = None,
        page_offset: int | None = None,
        fmt: str | None = None,
    ) -> dict[str, Any]:
        # ID mapping doesn't have a dedicated namespace module in the plan,
        # use the HTTP client directly.
        params: dict[str, Any] = {}
        if symbol is not None:
            params["filter[symbol]"] = symbol
        if ex is not None:
            params["filter[ex]"] = ex
        if isin is not None:
            params["filter[isin]"] = isin
        if figi is not None:
            params["filter[figi]"] = figi
        if lei is not None:
            params["filter[lei]"] = lei
        if cusip is not None:
            params["filter[cusip]"] = cusip
        if cik is not None:
            params["filter[cik]"] = cik
        if page_limit is not None:
            params["page[limit]"] = page_limit
        if page_offset is not None:
            params["page[offset]"] = page_offset
        if fmt is not None:
            params["fmt"] = fmt
        return self._http.get("id-mapping", params=params)

    def mp_indices_list(self) -> list[dict[str, Any]]:
        return self.exchanges.indices_list.get()

    def mp_index_components(
        self,
        symbol: str,
        historical: bool | int | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        return self.exchanges.index_components.get(
            symbol,
            historical=historical,
            from_date=from_date,
            to_date=to_date,
        )

    def get_us_options_contracts(
        self,
        underlying_symbol: str | None = None,
        contract: str | None = None,
        exp_date_eq: str | None = None,
        exp_date_from: str | None = None,
        exp_date_to: str | None = None,
        tradetime_eq: str | None = None,
        tradetime_from: str | None = None,
        tradetime_to: str | None = None,
        type: str | None = None,
        strike_eq: float | None = None,
        strike_from: float | None = None,
        strike_to: float | None = None,
        sort: str | None = None,
        page_offset: int = 0,
        page_limit: int = 1000,
        fields: Any = None,
        fmt: str = "json",
    ) -> dict[str, Any]:
        return self.marketplace.options.contracts.get(
            underlying_symbol=underlying_symbol,
            contract=contract,
            exp_date_eq=exp_date_eq,
            exp_date_from=exp_date_from,
            exp_date_to=exp_date_to,
            tradetime_eq=tradetime_eq,
            tradetime_from=tradetime_from,
            tradetime_to=tradetime_to,
            type=type,
            strike_eq=strike_eq,
            strike_from=strike_from,
            strike_to=strike_to,
            sort=sort,
            page_offset=page_offset,
            page_limit=page_limit,
            fields=fields,
            fmt=fmt,
        )

    def get_us_options_eod(
        self,
        underlying_symbol: str | None = None,
        contract: str | None = None,
        exp_date_eq: str | None = None,
        exp_date_from: str | None = None,
        exp_date_to: str | None = None,
        tradetime_eq: str | None = None,
        tradetime_from: str | None = None,
        tradetime_to: str | None = None,
        type: str | None = None,
        strike_eq: float | None = None,
        strike_from: float | None = None,
        strike_to: float | None = None,
        sort: str | None = None,
        page_offset: int = 0,
        page_limit: int = 1000,
        fields: Any = None,
        compact: int | None = None,
        fmt: str = "json",
    ) -> dict[str, Any]:
        return self.marketplace.options.eod.get(
            underlying_symbol=underlying_symbol,
            contract=contract,
            exp_date_eq=exp_date_eq,
            exp_date_from=exp_date_from,
            exp_date_to=exp_date_to,
            tradetime_eq=tradetime_eq,
            tradetime_from=tradetime_from,
            tradetime_to=tradetime_to,
            type=type,
            strike_eq=strike_eq,
            strike_from=strike_from,
            strike_to=strike_to,
            sort=sort,
            page_offset=page_offset,
            page_limit=page_limit,
            fields=fields,
            compact=compact,
            fmt=fmt,
        )

    def get_us_options_underlyings(
        self,
        page_offset: int | None = None,
        page_limit: int | None = None,
        fmt: str = "json",
    ) -> dict[str, Any]:
        return self.marketplace.options.underlyings.get(
            page_offset=page_offset,
            page_limit=page_limit,
            fmt=fmt,
        )
