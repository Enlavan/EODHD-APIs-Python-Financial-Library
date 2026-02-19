"""Macroeconomic and treasury-related API wrappers."""

from eodhd.apis.macro.macro_indicator import MacroIndicatorAPI
from eodhd.apis.macro.treasury_bill_rates import TreasuryBillRatesAPI
from eodhd.apis.macro.treasury_long_term import TreasuryLongTermAPI
from eodhd.apis.macro.treasury_yield import TreasuryYieldAPI
from eodhd.apis.macro.treasury_real_yield import TreasuryRealYieldAPI

__all__ = [
    "MacroIndicatorAPI",
    "TreasuryBillRatesAPI",
    "TreasuryLongTermAPI",
    "TreasuryYieldAPI",
    "TreasuryRealYieldAPI",
]
