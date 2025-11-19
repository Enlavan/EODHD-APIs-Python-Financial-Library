from .BaseAPI import BaseAPI


class LiveExtendedQuotesAPI(BaseAPI):
    """
    Wrapper for the /us-quote-delayed endpoint.

    Live v2 for US Stocks: Extended Quotes (delayed, exchange-compliant).
    """

    def get_us_extended_quotes(
        self,
        api_token: str,
        symbols,
        page_limit: int = None,
        page_offset: int = None,
    ):
        """
        Get delayed extended quotes for one or more US symbols.

        Parameters
        ----------
        api_token : str
            Your EODHD API access token.
        symbols : str | list | tuple | set
            One or more tickers. Examples:
            - "AAPL.US"
            - "AAPL.US,TSLA.US"
            - ["AAPL.US", "TSLA.US"]
        page_limit : int, optional
            Number of symbols per page (max 100).
        page_offset : int, optional
            Offset for pagination.

        Returns
        -------
        dict
            Parsed JSON response with keys: meta, data, links.
        """

        if not symbols:
            raise ValueError("Parameter 'symbols' is required (one or more tickers).")

        # Allow list/tuple/set of symbols as well as plain string
        if isinstance(symbols, (list, tuple, set)):
            symbols_param = ",".join(map(str, symbols))
        else:
            symbols_param = str(symbols)

        endpoint = "us-quote-delayed"
        query_string = f"&s={symbols_param}"

        if page_limit is not None:
            query_string += f"&page[limit]={page_limit}"
        if page_offset is not None:
            query_string += f"&page[offset]={page_offset}"

        return self._rest_get_method(
            api_key=api_token,
            endpoint=endpoint,
            querystring=query_string,
        )
