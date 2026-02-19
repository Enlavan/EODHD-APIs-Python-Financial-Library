"""Fundamentals-related API wrappers."""

from eodhd.apis.fundamentals.fundamentals import FundamentalsAPI
from eodhd.apis.fundamentals.bulk_fundamentals import BulkFundamentalsAPI
from eodhd.apis.fundamentals.news import NewsAPI
from eodhd.apis.fundamentals.sentiment import SentimentAPI
from eodhd.apis.fundamentals.news_word_weights import NewsWordWeightsAPI
from eodhd.apis.fundamentals.insider_transactions import InsiderTransactionsAPI

__all__ = [
    "FundamentalsAPI",
    "BulkFundamentalsAPI",
    "NewsAPI",
    "SentimentAPI",
    "NewsWordWeightsAPI",
    "InsiderTransactionsAPI",
]
