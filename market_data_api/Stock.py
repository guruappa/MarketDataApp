from Symbol import Symbol


class Stock(Symbol):
    def __init__(self, symbol, country=None):
        """
        Initialize an instance of Stock class.

        :param symbol:          The company's ticker symbol. If no exchange is specified, by default a US exchange will be
                                assumed. You may embed the exchange in the ticker symbol using the Yahoo Finance or
                                TradingView formats. A company or securities identifier can also be used instead of a ticker
                                symbol.
                                - Ticker Formats: (TICKER, TICKER.EX, EXCHANGE:TICKER)
                                - Company Identifiers: (CIK, LEI)
                                - Securities Identifiers: (CUSIP, SEDOL, ISIN, FIGI)
        :param country:         Use to specify the country of the exchange (not the country of the company) in conjunction
                                with the symbol argument. This argument is useful when you know the ticker symbol and the
                                country of the exchange, but not the exchange code. Use the two digit ISO 3166 country code.
                                If no country is specified, US exchanges will be assumed.
        """
        super().__init__(symbol, country, symbol_type='stock')
        self.__candle_url = super().set_candle_url(self.__api_instance.get_api_url(api_name="stock_candles"))
        self.__quote_url = super().set_quote_url(self.__api_instance.get_api_url(api_name="stock_quote"))

    def get_candles(self, resolution='D', from_date=None, to_date=None, num_of_periods=None, exchange=None,
                    extended=False, adjustSplits=True, adjustDividends=True):
        """
        Get historical price candles for a stock.

        :param resolution       :   The duration of each candle.
                                    Minutely Resolutions    :   (1, 3, 5, 15, 30, 45, ...)
                                    Hourly Resolutions      :   (H, 1H, 2H, ...)
                                    Daily Resolutions       :   (D, 1D, 2D, ...)
                                    Weekly Resolutions      :   (W, 1W, 2W, ...)
                                    Monthly Resolutions     :   (M, 1M, 2M, ...)
                                    Yearly Resolutions      :   (Y, 1Y, 2Y, ...)

                                    Default resolution is Daily (D)

        :param from_date        :   The leftmost candle on a chart (inclusive). If you use countback, to_date is not
                                    required.
        :param to_date          :   The rightmost candle on a chart (not inclusive).
        :param num_of_periods   :   Fetch a number of candles before (to the left of) to_date. If you use from_date,
                                    num_of_periods is not required.
        :param exchange         :   Use to specify the exchange of the ticker. This is useful when you need to specify
                                    stock that quotes on several exchanges with the same symbol. You may specify the
                                    exchange using the EXCHANGE ACRONYM, MIC CODE, or two digit YAHOO FINANCE EXCHANGE
                                    CODE. If no exchange is specified symbols will be matched to US exchanges first.
        :param extended         :   Include extended hours trading sessions when returning intraday candles. Daily
                                    resolutions never return extended hours candles. The default is false
        :param adjustSplits     :   Adjust historical data for historical splits and reverse splits. Market Data uses
                                    the CRSP methodology for adjustment.
                                    Daily candles default: true.
                                    Intraday candles default: false.
        :param adjustDividends  :   Adjust candles for dividends. Market Data uses the CRSP methodology for adjustment.
                                    Daily candles default: true.
                                    Intraday candles default: false.

        :return                 :   pandas DataFrame object with historical stock price candles
        """
        params = {}
        params['country'] = self.country

        if resolution and self.symbol:
            # get the base url
            base_url = f'{self.__candle_url}{resolution}/{self.symbol}/?format=json&dateformat=timestamp'

            if from_date:
                params['from'] = from_date
            if to_date:
                params['to'] = to_date
            if num_of_periods:
                params['countback'] = num_of_periods
            if exchange:
                params['exchange'] = exchange
            if extended:
                params['extended'] = extended
            if adjustSplits:
                params['adjustsplits'] = adjustSplits
            if adjustDividends:
                params['adjustdividends'] = adjustDividends

            # final_url = self.__api_instance.get_response(base_url, params)
            response = self.__api_instance.get_data_from_url(base_url, params)
            return self._format_candle_data(response)
        else:
            raise Exception("Parameters resolution and symbol are required")
