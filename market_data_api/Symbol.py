"""
Base class for Stocks and Indices

"""
import json
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from MarketDataAPI import MarketDataAPI


class Symbol(ABC):
    def __init__(self, symbol, country="US", symbol_type=None):
        """
        Initialization method

        :param symbol       :   The company's or index ticker symbol. If no exchange is specified, by default a US
                                exchange will be assumed. You may embed the exchange in the ticker symbol using the
                                Yahoo Finance or TradingView formats. A company or securities identifier can also be
                                used instead of a ticker symbol.
                                - Ticker Formats: (TICKER, TICKER.EX, EXCHANGE:TICKER)
                                - Company Identifiers: (CIK, LEI)
                                - Securities Identifiers: (CUSIP, SEDOL, ISIN, FIGI)
        :param country      :   Use to specify the country of the exchange (not the country of the company) in
                                conjunction with the symbol argument. This argument is useful when you know the ticker
                                symbol and the country of the exchange, but not the exchange code. Use the two digit
                                ISO 3166 country code.  If no country is specified, US exchanges will be assumed.
        :param symbol_type  :   The type of the symbol, whether stock or index
        """
        self.symbol = symbol
        self.country = country
        self.symbol_type = symbol_type
        self.underlying = None
        self.__api_instance = MarketDataAPI(config_file="config.properties")
        self.__candle_url = None
        self.__quote_url = None
        self.__expirations_url = None
        self.__strikes_url = None
        self.__option_chain_url = None

    def __get_date_string(self, object):
        pass

    @abstractmethod
    def get_candles(self, resolution, **kwargs):
        """
        Get the price candles for the symbol.

        :param resolution   :   The duration of each candle.
                                Minutely Resolutions:   (1, 3, 5, 15, 30, 45, ...)
                                Hourly Resolutions:     (H, 1H, 2H, ...)
                                Daily Resolutions:      (D, 1D, 2D, ...)
                                Weekly Resolutions:     (W, 1W, 2W, ...)
                                Monthly Resolutions:    (M, 1M, 2M, ...)
                                Yearly Resolutions:     (Y, 1Y, 2Y, ...)
        :param **kwargs     :   The keyword arguments that fine-tunes the behavior of the results
        :return             :   pandas DataFrame object with the historical price candles
        """
        pass

    def get_quote(self, year_statistics=False):
        """
        Get a real-time price quote.

        :param year_statistics  :   Enable the output of 52-week high and 52-week low data in the quote output.
                                    By default, this parameter is false.
        :return                 :   pandas DataFrame object with the quote data
        """
        params = {}
        if year_statistics:
            params['52week'] = year_statistics

        # get the base url
        base_url = f'{self.__quote_url}{self.symbol}/?format=json&dateformat=timestamp'
        response = self.__api_instance.get_data_from_url(base_url, params)
        return self._format_quote_data(response)

    def get_candle_url(self):
        """
        Getter function for candle url

        :return             :   Candle url
        """
        return self.__candle_url

    def set_candle_url(self, url):
        """
        Setter function for candle url

        :param url  :   The candle API url
        """
        self.__candle_url = url

    def get_quote_url(self):
        """
        Getter function for quote url

        :return             :   Candle url
        """
        return self.__quote_url

    def set_quote_url(self, url):
        """
        Setter function for candle url

        :param url  :   The quote API url
        """
        self.__quote_url = url

    def get_expirations_url(self):
        """
        Getter function for expiration url

        :return             :   Expiration url
        """
        return self.__expirations_url

    def set_expirations_url(self, url):
        """
        Setter function for expiration url

        :param url  :   The expiration API url
        """
        self.__expirations_url = url

    def get_strikes_url(self):
        """
        Getter function for strike prices url

        :return             :   Expiration url
        """
        return self.__strikes_url

    def set_strikes_url(self, url):
        """
        Setter function for strike prices url

        :param url  :   The strike prices API url
        """
        self.__strikes_url = url

    def _format_candle_data(self, url_response):
        """
        Format the candle data from the response object into pandas DataFrame object

        :param url_response :   The response object containing the data
        :return             :   pandas DataFrame object
        """
        if url_response.text:
            response_json = json.loads(url_response.text)
            status = response_json['s']

            if status == 'ok':
                candles_pd = response_json
                candles_hist = pd.DataFrame(candles_pd)
                candles_hist['symbol'] = self.symbol

                # rename the columns
                columns = {'c': 'close', 'h': 'high', 'l': 'low', 'o': 'open', 'v': 'volume', 't': 'date'}
                candles_hist.rename(columns=columns, inplace=True)
                candles_hist.drop(['s'], axis=1, inplace=True)
                candles_hist = candles_hist.reindex(
                    columns=['symbol', 'date', 'close', 'high', 'low', 'open', 'volume'])
                return candles_hist
            else:
                return self.__api_instance.process_not_ok_response(response_json)
        else:
            # TODO: Log the exception
            raise Exception

    def _format_quote_data(self, url_response):
        """
        Format the quote data from the response object into pandas DataFrame object

        :param url_response :   The response object containing the data
        :return             :   pandas DataFrame object
        """
        if url_response.text:
            response_json = json.loads(url_response.text)
            status = response_json['s']

            if status == 'ok':
                quote_df = pd.DataFrame({
                    'updated': response_json.get('updated', np.nan),
                    'symbol': response_json.get('symbol', np.nan),
                    'bid': response_json.get('bid', np.nan),
                    'bid_size': response_json.get('bidSize', np.nan),
                    'mid': response_json.get('mid', np.nan),
                    'ask': response_json.get('ask', np.nan),
                    'ask_size': response_json.get('askSize', np.nan),
                    'last': response_json.get('last', np.nan),
                    'volume': response_json.get('volume', np.nan),
                    '52_week_high': response_json.get('52weekHigh', np.nan),
                    '52_week_low': response_json.get('52weekLow', np.nan),
                    'open_interest': response_json.get('openInterest', np.nan),
                    'underlying_price': response_json.get('underlyingPrice', np.nan),
                    'in_the_money': response_json.get('inTheMoney', np.nan),
                    'intrinsic_value': response_json.get('intrinsicValue', np.nan),
                    'extrinsic_value': response_json.get('extrinsicValue', np.nan),
                    'iv': response_json.get('iv', np.nan),
                    'delta': response_json.get('delta', np.nan),
                    'gamma': response_json.get('gamma', np.nan),
                    'theta': response_json.get('theta', np.nan),
                    'vega': response_json.get('vega', np.nan),
                    'rho': response_json.get('rho', np.nan),
                })
                quote_df = quote_df.dropna(axis=1)
                return quote_df
            else:
                return self.__api_instance.process_not_ok_response(response_json)
        else:
            # TODO: Log the exception
            raise Exception

    def __get_underlying(self):
        """
        Gets the underlying symbol for functions around options

        :return             :   Underlying Symbol
        """
        if self.symbol_type == 'option':
            underlying_symbol = self.underlying
        else:
            underlying_symbol = self.symbol

        return underlying_symbol

    def get_expirations(self, strike_price=None, ason_date=None):
        """
        Gets the expiration dates

        :param strike_price :    Limit the lookup of expiration dates to the strike price provided.
        :param ason_date    :   Use to lookup a historical list of expiration dates from a specific previous trading
                                day. If date is omitted the expiration dates will be from the current trading day
                                during market hours or from the last trading day when the market is closed.
                                Date to be in YYYY-MM-DD format
        :return             :   List of expiry dates in YYYY-MM-DD format
        """
        underlying_symbol = self.__get_underlying()

        params = {}
        if strike_price:
            params['strike'] = strike_price
        if ason_date:
            params['date'] = ason_date

        # get the base url
        base_url = f'{self.__expirations_url}{underlying_symbol}/?format=json&dateformat=timestamp'
        response = self.__api_instance.get_data_from_url(base_url, params)
        return self._format_expirations_data(response)

    def _format_expirations_data(self, url_response):
        """
        Format current or historical option expiration dates from the URL response object into list

        :param url_response :   The response object containing the data
        :return             :   List of expiry dates in YYYY-MM-DD format
        """
        if url_response.text:
            response_json = json.loads(url_response.text)
            status = response_json['s']

            if status == 'ok':
                expirations = response_json['expirations']
                return expirations
            else:
                return self.__api_instance.process_not_ok_response(response_json)
        else:
            # TODO: Log the exception
            raise Exception

    def get_strikes(self, strike_price=None, ason_date=None):
        """
        Gets the strike prices for Options

        :param strike_price :    Limit the lookup of expiration dates to the strike price provided.
        :param ason_date    :   Use to lookup a historical list of expiration dates from a specific previous trading
                                day. If date is omitted the expiration dates will be from the current trading day
                                during market hours or from the last trading day when the market is closed.
                                Date to be in YYYY-MM-DD format
        :return             :   List of expiry dates in YYYY-MM-DD format
        """
        underlying_symbol = self.__get_underlying()

        params = {}
        if strike_price:
            params['strike'] = strike_price
        if ason_date:
            params['date'] = ason_date

        # get the base url
        base_url = f'{self.__strikes_url}{underlying_symbol}/?format=json&dateformat=timestamp'
        response = self.__api_instance.get_data_from_url(base_url, params)
        return self._format_strikes_data(response)

    def _format_strikes_data(self, url_response):
        """
        Format strikes API URL response, in a pandas DataFrame with expiration dates and strike prices columns

        :param url_response :   The response object containing the data
        :return             :   pandas DataFrame with expiration dates and strike prices columns
        """
        if url_response.text:
            response_json = json.loads(url_response.text)
            status = response_json['s']

            if status == 'ok':
                keys = response_json.keys()
                expirations = [key for key in keys if key not in ["s", "updated"]]

                strike_price_df = pd.DataFrame()

                for expiration in expirations:
                    expiration_df = pd.DataFrame()
                    strike_prices = response_json[expiration]
                    strike_prices = pd.Series(strike_prices, index=range(len(strike_prices)))
                    expiration_dates = pd.Series(expiration, index=range(len(strike_prices)))
                    expiration_df['expiration'] = expiration_dates
                    expiration_df['strike_prices'] = strike_prices

                    strike_price_df = pd.concat([strike_price_df, expiration_df], ignore_index=True)
                    strike_price_df = strike_price_df.reindex()

                    del expiration_df

                return strike_price_df
            else:
                return self.__api_instance.process_not_ok_response(response_json)
        else:
            # TODO: Log the exception
            raise Exception

    def get_option_chain(self, ason_date=None, expiry_date=None, from_date=None, to_date=None, month=None, year=None,
                         include_weekly=False, include_monthly=False, include_quarterly=False, dte=None, delta=None,
                         option_type=None, moneyness='all', strike_price=None, strike_price_count=None, minimum_oi=None,
                         minimum_volume=None, minimum_liquidity=None, max_bid_ask_spread=None,
                         max_bid_ask_spread_pct=None):
        """
        Get a current or historical end of day options chain. Optional parameters allow for extensive filtering of the
        chain.

        :param ason_date                :   Use to lookup a historical end of day options chain from a specific trading
                                            day. If no ason_date is specified the chain will be the most current chain
                                            available during market hours. When the market is closed the chain will be
                                            from the last trading day.  Date to be in YYYY-MM-DD format
        :param expiry_date              :   Limits the option chain to a specific expiration date. This parameter can be
                                            used to request a quote along with the chain. If omitted all expirations
                                            will be returned.  Date to be in YYYY-MM-DD format
        :param from_date                :   Limit the option chain to expiration dates after from (inclusive). Should be
                                            combined with to_date to create a range. If omitted all expirations will be
                                            returned. Date to be in YYYY-MM-DD format
        :param to_date                  :   Limit the option chain to expiration dates before to (not inclusive).
                                            Should be combined with from_date to create a range. If omitted all
                                            expirations will be returned. Date to be in YYYY-MM-DD format
        :param month                    :   Limit the option chain to options that expire in a specific month (1-12).
        :param year                     :   Limit the option chain to options that expire in a specific year. Year to
                                            be in YYYY format
        :param include_weekly           :   Limit the option chain to weekly expirations by setting weekly to True and
                                            omitting the monthly and quarterly parameters. If set to False, no weekly
                                            expirations will be returned. Defaults to False
        :param include_monthly          :   Limit the option chain to standard monthly expirations by setting monthly to
                                            True and omitting the weekly and quarterly parameters. If set to False, no
                                            monthly expirations will be returned. Defaults to True
        :param include_quarterly        :   Limit the option chain to quarterly expirations by setting quarterly to True
                                            and omitting the weekly and monthly parameters. If set to False, no
                                            quarterly expirations will be returned. Defaults to False
        :param dte                      :   Days to expiry. Limit the option chain to a single expiration date closest
                                            to the dte provided. Should not be used together with from and to. Take care
                                            before combining with include_weekly, include_monthly, include_quarterly,
                                            since that will limit the expirations dte can return. If you are using the
                                            ason_date parameter, dte is relative to the date provided.
        :param delta                    :   Limit the option chain to a single strike closest to the delta provided.
        :param option_type              :   Limit the option chain to either call or put. If omitted, both sides will be
                                            returned.
        :param moneyness                :   Limit the option chain to strikes that are in the money, out of the money,
                                            at the money, or include all. If omitted all options will be returned.
                                            Valid inputs: itm, otm, all.
        :param strike_price             :   Limit the option chain to options with the specific strike price specified.
        :param strike_price_count       :   Limit the number of total strikes returned by the option chain. For example,
                                            if a complete chain included 30 strikes and the limit was set to 10, the
                                            20 strikes furthest from the money will be excluded from the response.

                                            If strike_price_count is combined with the moneyness or option_type
                                            parameter, those parameters will be applied first. In the above example, if
                                            the moneyness were set to itm (in the money) and option_type set to call,
                                            all puts and out of the money calls would be first excluded by the
                                            moneyness parameter and then strike_price_count will return a maximum of 10
                                            in the money calls that are closest to the money. If the option_type
                                            parameter has not been used but moneyness has been specified, then
                                            strike_price_count will return the requested number of calls and puts for
                                            each side of the chain, but duplicating the number of strikes that are
                                            received.
        :param minimum_oi               :   Limit the option chain to options with an open interest greater than or
                                            equal to the number provided. Can be combined with minimum_volume and
                                            minimum_liquidity to further filter.
        :param minimum_volume           :   Limit the option chain to options with a volume transacted greater than or
                                            equal to the number provided.
        :param minimum_liquidity        :   Limit the option chain to options with liquidity greater than or equal to
                                            the number provided.
        :param max_bid_ask_spread       :   Limit the option chain to options with a bid-ask spread less than or equal
                                            to the number provided.
        :param max_bid_ask_spread_pct   :   Limit the option chain to options with a bid-ask spread less than or equal
                                            to the percent provided (relative to the underlying). For example, a value
                                            of 0.5% would exclude all options trading with a bid-ask spread greater
                                            than $1.00 in an underlying that trades at $200.

                                            Value of 0.5 will be considered as 0.5%, value of 1 will be considered as 1%
        :return:                            pandas DataFrame object containing the option chain
        """
        params = {}
        underlying = self.__get_underlying()

        if underlying:
            # get the base url
            base_url = f'{self.__option_chain_url}{underlying}/?format=json&dateformat=timestamp'
            params['range'] = moneyness

            if ason_date:
                params['date'] = ason_date
            if expiry_date:
                params['expiration'] = expiry_date
            if from_date:
                params['from'] = from_date
            if to_date:
                params['to'] = to_date
            if month:
                params['month'] = month
            if year:
                params['year'] = year
            if include_weekly:
                params['weekly'] = include_weekly
            if include_monthly:
                params['monthly'] = include_monthly
            if include_quarterly:
                params['quarterly'] = include_quarterly
            if dte:
                params['dte'] = dte
            if delta:
                params['delta'] = delta
            if option_type:
                params['side'] = option_type
            if strike_price:
                params['strike'] = strike_price
            if strike_price_count:
                params['strikeLimit'] = strike_price_count
            if minimum_oi:
                params['minOpenInterest'] = minimum_oi
            if minimum_volume:
                params['minVolume'] = minimum_volume
            if minimum_liquidity:
                params['minLiquidity'] = minimum_liquidity
            if max_bid_ask_spread:
                params['maxBidAskSpread'] = max_bid_ask_spread
            if max_bid_ask_spread_pct:
                params['maxBidAskSpreadPct'] = max_bid_ask_spread_pct

            response = self.__api_instance.get_data_from_url(base_url, params)
            return self._format_option_chain_data(response)
        else:
            # TODO: Log the exception
            raise Exception

    def _format_option_chain_data(self, url_response):
        """
        Format option chain API URL response, in a pandas DataFrame

        :param url_response :   The response object containing the data
        :return             :   pandas DataFrame object containing the option chain
        """
        if url_response.text:
            response_json = json.loads(url_response.text)
            status = response_json['s']

            if status == 'ok':
                rename_columns = {"s": "status", "updated": "updated", "optionSymbol": "option_symbol",
                                  "underlying": "underlying",
                                  "expiration": "expiry_date", "side": "option_type", "strike": "strike_price",
                                  "firstTraded": "first_traded_date", "dte": "dte", "bid": "bid", "bidSize": "bid_size",
                                  "mid": "mid", "ask": "ask", "askSize": "ask_size", "last": "last_price",
                                  "openInterest": "open_interest", "volume": "volume", "inTheMoney": "in_the_money",
                                  "intrinsicValue": "intrinsic_value", "extrinsicValue": "extrnisic_value",
                                  "underlyingPrice": "underlying_price", "iv": "iv", "delta": "delta", "gamma": "gamma",
                                  "theta": "theta", "vega": "vega", "rho": "rho"}
                final_columns = ["updated", "option_symbol", "underlying", "expiry_date", "option_type", "strike_price",
                                 "first_traded_date", "dte", "bid", "bid_size", "mid", "ask", "ask_size",
                                 "last_price", "open_interest", "volume", "in_the_money", "intrinsic_value",
                                 "extrnisic_value", "underlying_price", "iv", "delta", "gamma", "theta", "vega", "rho"]
                option_chain_json = response_json
                option_chain_pd = pd.DataFrame(option_chain_json)

                option_chain_pd.rename(columns=rename_columns, inplace=True)
                option_chain_pd.drop(['status'], axis=1, inplace=True)
                option_chain_pd = option_chain_pd.reindex(columns=final_columns)
                return option_chain_pd
            else:
                return self.__api_instance.process_not_ok_response(response_json)
        else:
            # TODO: Log the exception
            raise Exception
