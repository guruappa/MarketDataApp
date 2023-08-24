"""

Author : Guruppa Padsali

Purpose :
This file contains the functions that get data for options.

"""

import datetime
import marketdata.utilities as utilities
import marketdata.api_interface as api


def lookup_option_symbol(underlying, expiry_date, option_type, strike_price):
    """
    Generate a properly formatted OCC option symbol based on the user's human-readable description of an option.

    :param underlying    : Symbol of the underlying asset
    :param expiry_date   : Expiry date of the option in the format 'YYYY-MM-DD'
    :param option_type   : Option type, either 'C' (Call) or 'P' (Put)
    :param strike_price  : Strike price of the option

    :return:               option symbol in string format
    """
    url = utilities.get_marketdata_url('option_lookup')
    # TODO: The lookup url is giving wonky results.  Need to raise it with the MarketDataApp guys about its behaviour.
    pass


def get_option_symbol(underlying, expiry_date, option_type, strike_price):
    """
    Gets the option symbol given underlying, expiry_date, option_type, strike_price

    :param underlying    : Symbol of the underlying asset
    :param expiry_date   : Expiry date of the option in the format 'YYYY-MM-DD'
    :param option_type   : Option type, either 'C' (Call) or 'P' (Put)
    :param strike_price  : Strike price of the option

    :return:               option symbol in string format
    """
    expiry_date = datetime.datetime.strptime(expiry_date, '%Y-%m-%d')
    expiry_date = expiry_date.strftime('%y%m%d')
    strike_price = '{:0>8}'.format(int(strike_price * 1000))
    option_symbol = f'{underlying}{expiry_date}{option_type}{strike_price}'
    return option_symbol


def get_option_quote_by_symbol(option_symbol, ason_date=None, from_date=None, to_date=None):
    """
    Get a current or historical end of day quote for a single options contract.

    :param option_symbol     :  The option symbol (as defined by the OCC) for the option you wish to lookup. Use the
                                current OCC option symbol format, even for historic options that quoted before the
                                format change in 2010.
    :param ason_date        :   Use to lookup a historical end of day quote from a specific trading day. If no date is
                                specified the quote will be the most current price available during market hours. When
                                the market is closed the quote will be from the last trading day.
    :param from_date        :   Use to lookup a series of end of day quotes. from_date is the oldest (leftmost) date to
                                return (inclusive). If from_date/to_date is not specified the quote will be the most
                                current price available during market hours. When the market is closed the quote will
                                be from the last trading day.
    :param to_date          :   Use to lookup a series of end of day quotes. to_date is the newest (rightmost) date to
                                return (exclusive). If from_date/to_date is not specified the quote will be the most
                                current price available during market hours. When the market is closed the quote will
                                be from the last trading day.
    :return:                    pandas DataFrame object with the historical data
    """
    params = {}

    if option_symbol:
        url = utilities.get_marketdata_url('option_quote')
        base_url = f'{url}{option_symbol}/?format=json&dateformat=timestamp'  # get the base url

        if ason_date:
            params['date'] = ason_date
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date

        final_url = api.get_final_url(base_url, params)
        return api.get_quote(final_url)
    else:
        raise Exception("Parameters option_symbol is required")


def get_option_quote(underlying, expiry_date, option_type, strike_price):
    """
    Get Live quotes of an option.
    example       : options_quote_live('IBM', '2023-02-10', 'C', 140)

    :param underlying    : Symbol of the underlying asset
    :param expiry_date   : Expiry date of the option in the format 'YYYY-MM-DD'
    :param option_type   : Option type, either 'C' (Call) or 'P' (Put)
    :param strike_price  : Strike price of the option

    :return:               pandas DataFrame object with the quote data
    """
    if underlying and expiry_date and option_type and strike_price:
        option_symbol = get_option_symbol(underlying, expiry_date, option_type, strike_price)
        return get_option_quote_by_symbol(option_symbol)
    else:
        raise Exception("Parameters underlying, expiry_date, option_type and strike_price are required")


def get_option_quote_on_date(underlying, expiry_date, option_type, strike_price, ason_date):
    """
    Get quotes of an option on a date.

    :param underlying       :   Symbol of the underlying asset
    :param expiry_date      :   Expiry date of the option in the format 'YYYY-MM-DD'
    :param option_type      :   Option type, either 'C' (Call) or 'P' (Put)
    :param strike_price     :   Strike price of the option
    :param ason_date        :   Use to lookup a historical end of day quote from a specific trading day. If no date is
                                specified the quote will be the most current price available during market hours. When
                                the market is closed the quote will be from the last trading day.
    :return:                    pandas DataFrame object with the historical data
    """
    if underlying and expiry_date and option_type and strike_price and ason_date:
        option_symbol = get_option_symbol(underlying, expiry_date, option_type, strike_price)
        return get_option_quote_by_symbol(option_symbol, ason_date=ason_date)
    else:
        raise Exception("Parameters underlying, expiry_date, option_type, strike_price and ason_date are required")


def get_option_quote_history(underlying, expiry_date, option_type, strike_price, from_date, to_date):
    """
    Get quotes of an option for a range of dates.

    :param underlying       :   Symbol of the underlying asset
    :param expiry_date      :   Expiry date of the option in the format 'YYYY-MM-DD'
    :param option_type      :   Option type, either 'C' (Call) or 'P' (Put)
    :param strike_price     :   Strike price of the option
    :param from_date        :   Use to lookup a series of end of day quotes. from_date is the oldest (leftmost) date to
                                return (inclusive). If from_date/to_date is not specified the quote will be the most
                                current price available during market hours. When the market is closed the quote will
                                be from the last trading day.
    :param to_date          :   Use to lookup a series of end of day quotes. to_date is the newest (rightmost) date to
                                return (exclusive). If from_date/to_date is not specified the quote will be the most
                                current price available during market hours. When the market is closed the quote will
                                be from the last trading day.
    :return:                    pandas DataFrame object with the historical data
    """
    if underlying and expiry_date and option_type and strike_price and from_date and to_date:
        option_symbol = get_option_symbol(underlying, expiry_date, option_type, strike_price)
        return get_option_quote_by_symbol(option_symbol, from_date=from_date, to_date=to_date)
    else:
        raise Exception("Parameters underlying, expiry_date, option_type, strike_price, from_date and to_date are required")


def get_option_expiries(underlying, strike_price=None, from_date=None):
    """
    Get a list of current or historical option expiration dates for an underlying symbol. If no optional parameters are
    used, the function returns all expiration dates in the option chain.

    :param underlying   :   The underlying ticker symbol for the options chain you wish to lookup. A company or
                            securities identifier can also be used instead of a ticker symbol.
                                Ticker Formats: (TICKER, TICKER.EX, EXCHANGE:TICKER)
                                Company Identifiers: (CIK, LEI)
                                Securities Identifiers: (CUSIP, SEDOL, ISIN, FIGI)
    :param strike_price :   Limit the lookup of expiration dates to the strike provided.
    :param from_date    :   Use to lookup a historical list of expiration dates from a specific previous trading day.
                            If date is omitted the expiration dates will be from the current trading day during market
                            hours or from the last trading day when the market is closed.
                            Date to be in YYYY-MM-DD format
    :return             :   List of expiry dates in YYYY-MM-DD format
    """
    params = {}

    if underlying:
        url = utilities.get_marketdata_url('option_expirations')
        base_url = f'{url}{underlying}/?format=json&dateformat=timestamp'  # get the base url

        if strike_price:
            params['strike'] = strike_price
        if from_date:
            params['date'] = from_date

        final_url = api.get_final_url(base_url, params)
        return api.get_expirations(final_url)
    else:
        raise Exception("Parameters underlying is required")


def get_option_strikes(underlying, expiry_date=None, from_date=None):
    """
    Get a list of current or historical option expiration dates for an underlying symbol. If no optional parameters are
    used, the function returns all expiration dates in the option chain.

    :param underlying   :   The underlying ticker symbol for the options chain you wish to lookup. A company or
                            securities identifier can also be used instead of a ticker symbol.
                                Ticker Formats: (TICKER, TICKER.EX, EXCHANGE:TICKER)
                                Company Identifiers: (CIK, LEI)
                                Securities Identifiers: (CUSIP, SEDOL, ISIN, FIGI)
    :param expiry_date  :   Limit the lookup of strikes to options that expire on a specific expiration date. Date to
                            be in YYYY-MM-DD format
    :param from_date    :   Use to lookup a historical list of expiration dates from a specific previous trading day.
                            If date is omitted the expiration dates will be from the current trading day during market
                            hours or from the last trading day when the market is closed.
                            Date to be in YYYY-MM-DD format
    :return             :   List of expiry dates in YYYY-MM-DD format
    """
    params = {}

    if underlying:
        url = utilities.get_marketdata_url('option_strikes')
        base_url = f'{url}{underlying}/?format=json&dateformat=timestamp'  # get the base url

        if expiry_date:
            params['expiration'] = expiry_date
        if from_date:
            params['date'] = from_date

        final_url = api.get_final_url(base_url, params)
        return api.get_strikes(final_url)
    else:
        raise Exception("Parameters underlying is required")
