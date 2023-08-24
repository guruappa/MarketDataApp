"""

Author : Guruppa Padsali

Purpose :
This file contains the functions that get option chain data for underlying symbol.

"""

import marketdata.utilities as utilities
import marketdata.api_interface as api


def get_option_chain(underlying, ason_date=None, expiry_date=None, from_date=None, to_date=None, month=None, year=None,
                     include_weekly=False, include_monthly=False, include_quarterly=False, dte=None, delta=None,
                     option_type=None, moneyness='all', strike_price=None, strike_price_count=None, minimum_oi=None,
                     minimum_volume=None, minimum_liquidity=None, max_bid_ask_spread=None, max_bid_ask_spread_pct=None):
    """
    Get a current or historical end of day options chain for an underlying ticker symbol. Optional parameters allow
    for extensive filtering of the chain.

    :param underlying               :   The underlying ticker symbol for the options chain you wish to lookup. A
                                        company or securities identifier can also be used instead of a ticker symbol.
                                            Ticker Formats: (TICKER, TICKER.EX, EXCHANGE:TICKER)
                                            Company Identifiers: (CIK, LEI)
                                            Securities Identifiers: (CUSIP, SEDOL, ISIN, FIGI)
    :param ason_date                :   Use to lookup a historical end of day options chain from a specific trading day.
                                        If no ason_date is specified the chain will be the most current chain available
                                        during market hours. When the market is closed the chain will be from the last
                                        trading day.  Date to be in YYYY-MM-DD format
    :param expiry_date              :   Limits the option chain to a specific expiration date. This parameter can be
                                        used to request a quote along with the chain. If omitted all expirations will
                                        be returned.  Date to be in YYYY-MM-DD format
    :param from_date                :   Limit the option chain to expiration dates after from (inclusive). Should be
                                        combined with to_date to create a range. If omitted all expirations will be
                                        returned. Date to be in YYYY-MM-DD format
    :param to_date                  :   Limit the option chain to expiration dates before to (not inclusive). Should be
                                        combined with from_date to create a range. If omitted all expirations will be
                                        returned. Date to be in YYYY-MM-DD format
    :param month                    :   Limit the option chain to options that expire in a specific month (1-12).
    :param year                     :   Limit the option chain to options that expire in a specific year. Year to be in
                                        YYYY format
    :param include_weekly           :   Limit the option chain to weekly expirations by setting weekly to True and
                                        omitting the monthly and quarterly parameters. If set to False, no weekly
                                        expirations will be returned. Defaults to False
    :param include_monthly          :   Limit the option chain to standard monthly expirations by setting monthly to
                                        True and omitting the weekly and quarterly parameters. If set to False, no
                                        monthly expirations will be returned. Defaults to True
    :param include_quarterly        :   Limit the option chain to quarterly expirations by setting quarterly to True
                                        and omitting the weekly and monthly parameters. If set to False, no quarterly
                                        expirations will be returned. Defaults to False
    :param dte                      :   Days to expiry. Limit the option chain to a single expiration date closest to
                                        the dte provided. Should not be used together with from and to. Take care
                                        before combining with include_weekly, include_monthly, include_quarterly, since
                                        that will limit the expirations dte can return. If you are using the ason_date
                                        parameter, dte is relative to the date provided.
    :param delta                    :   Limit the option chain to a single strike closest to the delta provided.
    :param option_type              :   Limit the option chain to either call or put. If omitted, both sides will be
                                        returned.
    :param moneyness                :   Limit the option chain to strikes that are in the money, out of the money,
                                        at the money, or include all. If omitted all options will be returned.
                                        Valid inputs: itm, otm, all.
    :param strike_price             :   Limit the option chain to options with the specific strike price specified.
    :param strike_price_count       :   Limit the number of total strikes returned by the option chain. For example, if
                                        a complete chain included 30 strikes and the limit was set to 10, the 20 strikes
                                        furthest from the money will be excluded from the response.

                                        If strike_price_count is combined with the moneyness or option_type parameter,
                                        those parameters will be applied first. In the above example, if the moneyness
                                        were set to itm (in the money) and option_type set to call, all puts and
                                        out of the money calls would be first excluded by the moneyness parameter and
                                        then strike_price_count will return a maximum of 10 in the money calls that are
                                        closest to the money. If the option_type parameter has not been used but
                                        moneyness has been specified, then strike_price_count will return the requested
                                        number of calls and puts for each side of the chain, but duplicating the number
                                        of strikes that are received.
    :param minimum_oi               :   Limit the option chain to options with an open interest greater than or equal
                                        to the number provided. Can be combined with minimum_volume and
                                        minimum_liquidity to further filter.
    :param minimum_volume           :   Limit the option chain to options with a volume transacted greater than or
                                        equal to the number provided.
    :param minimum_liquidity        :   Limit the option chain to options with liquidity greater than or equal to the
                                        number provided.
    :param max_bid_ask_spread       :   Limit the option chain to options with a bid-ask spread less than or equal to
                                        the number provided.
    :param max_bid_ask_spread_pct   :   Limit the option chain to options with a bid-ask spread less than or equal to
                                        the percent provided (relative to the underlying). For example, a value of 0.5%
                                        would exclude all options trading with a bid-ask spread greater than $1.00 in
                                        an underlying that trades at $200.

                                        Value of 0.5 will be considered as 0.5%, value of 1 will be considered as 1%


    :return:                            pandas DataFrame object containing the option chain
    """
    params = {}

    if underlying:
        url = utilities.get_marketdata_url('option_chain')
        base_url = f'{url}{underlying}/?format=json&dateformat=timestamp'  # get the base url
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

        final_url = api.get_final_url(base_url, params)
        return api.get_option_chain(final_url)
    else:
        raise Exception("Parameters underlying is required")
