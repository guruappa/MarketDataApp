"""

Author : Guruppa Padsali

Purpose :
This file contains the functions that get data for indices.

"""

import mdapi_functions.api_interface as api
import mdapi_functions.utilities as utilities


def get_index_candles(resolution, symbol, from_date=None, to_date=None, num_of_periods=None):
    """
    Get historical price candles for an index.
    :param resolution:      The duration of each candle.
                            Minutely Resolutions: (1, 3, 5, 15, 30, 45, ...)
                            Hourly Resolutions: (H, 1H, 2H, ...)
                            Daily Resolutions: (D, 1D, 2D, ...)
                            Weekly Resolutions: (W, 1W, 2W, ...)
                            Monthly Resolutions: (M, 1M, 2M, ...)
                            Yearly Resolutions:(Y, 1Y, 2Y, ...)')
    :param symbol:          The company's ticker symbol. If no exchange is specified, by default a US exchange will be
                            assumed. You may embed the exchange in the ticker symbol using the Yahoo Finance or
                            TradingView formats. A company or securities identifier can also be used instead of a ticker
                            symbol.
                            - Ticker Formats: (TICKER, TICKER.EX, EXCHANGE:TICKER)
                            - Company Identifiers: (CIK, LEI)
                            - Securities Identifiers: (CUSIP, SEDOL, ISIN, FIGI)
    :param from_date:       The leftmost candle on a chart (inclusive). If you use countback, to is not required.
    :param to_date:         The rightmost candle on a chart (not inclusive).
    :param num_of_periods:  Fetch a number of candles before (to the left of) to_date. If you use from, num_of_periods
                            is not required.

    :return:                pandas DataFrame object with historical stock price candles
    """
    params = {}

    if resolution and symbol:
        url = utilities.get_marketdata_url('index_history')
        base_url = f'{url}{resolution}/{symbol}/?format=json&dateformat=timestamp'  # get the base url

        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
        if num_of_periods:
            params['countback'] = num_of_periods

        final_url = api.get_final_url(base_url, params)
        return api.get_candles(final_url, symbol)
    else:
        raise Exception("Parameters resolution and symbol are required")


def get_index_quote(symbol, year_statistics=False):
    """
    Get a real-time quote for an index.

    :param symbol:          The index's ticker symbol. If no exchange is specified. You may embed the exchange in the
                            ticker symbol using the Yahoo Finance or TradingView formats.
    :param year_statistics: Enable the output of 52-week high and 52-week low data in the quote output. By default this
                            parameter is false if omitted.
    :return:                pandas DataFrame object with the quote data
    """
    params = {}

    if symbol:
        url = utilities.get_marketdata_url('index_quote')
        base_url = f'{url}{symbol}/?format=json&dateformat=timestamp'  # get the base url

        if year_statistics:
            params['52week'] = year_statistics
        final_url = api.get_final_url(base_url, params)
        return api.get_quote(final_url)
    else:
        raise Exception("Parameters symbol is required")


