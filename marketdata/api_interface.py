"""

Author : Guruppa Padsali

Purpose :
This file contains the functions that interface with the marketdata.app api urls.  The functions process the json in the
response object into formats that can be consumed in the downstream calls.

"""

import json
import urllib.parse

import numpy as np
import pandas as pd
import requests

import marketdata.utilities as utilities

DATA_SOURCE = 'marketdata'


def set_headers():
    """
    Set the header information for the request to the API
    :return: The header information
    """
    return {'Authorization': f'token {utilities.get_api_key(DATA_SOURCE)}'}


def get_final_url(base_url, params):
    """
    Builds the final url before making the request to marketdata.app APIs
    :param base_url:    The base url on which the parameters are to be added
    :param params:      The query parameters in dictionary that need to be encoded in the final url
    :return:            The final URL that can be sent as a request to the API
    """
    url_params = urllib.parse.urlencode(params)
    final_url = f"{base_url}&{url_params}"
    return final_url


def process_not_ok_response(response_json):
    """
    Utility function for processing the response that does not contain data

    :return: string containing the message
    """
    status = response_json['s']
    match status:
        case 'no_data':
            # when the server returned no data
            return 'No Data'
        case 'error':
            # when the server returned error
            return response_json['errmsg']


def get_history(final_url, symbol):
    """
    Get the history for the symbol, whether symbol is an index or stock.

    :param final_url:   The final url of the API to get the data, with all query parameters
    :param symbol:      The symbol for which the history is requested
    :return:            pandas DataFrame object with the historical price candles
    """
    response = requests.get(final_url, headers=set_headers())
    if response.text:
        response_json = json.loads(response.text)
        status = response_json['s']

        if status == 'ok':
            candles_pd = response_json
            candles_hist = pd.DataFrame(candles_pd)
            candles_hist['symbol'] = symbol

            # rename the columns
            columns = {'c': 'close', 'h': 'high', 'l': 'low', 'o': 'open', 'v': 'volume', 't': 'date'}
            candles_hist.rename(columns=columns, inplace=True)
            candles_hist.drop(['s'], axis=1, inplace=True)
            candles_hist = candles_hist.reindex(columns=['symbol', 'date', 'close', 'high', 'low', 'open', 'volume'])
            return candles_hist
        else:
            return process_not_ok_response(response_json)
    else:
        raise Exception


def get_quote(final_url):
    """
    Get the real-time price quote for the symbol, whether symbol is an index or stock.

    :param final_url:   The final url of the API to get the data, with all query parameters
    :return:            pandas DataFrame object with the historical price candles
    """
    response = requests.get(final_url, headers=set_headers())
    if response.text:
        response_json = json.loads(response.text)
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
            return process_not_ok_response(response_json)
    else:
        raise Exception


def get_expirations(final_url):
    """
    Get a list of current or historical option expiration dates from the final url

    :param final_url:   The final url of the API to get the data, with all query parameters
    :return:            List of expiry dates in YYYY-MM-DD format
    """
    response = requests.get(final_url, headers=set_headers())
    if response.text:
        response_json = json.loads(response.text)
        status = response_json['s']

        if status == 'ok':
            expirations = response_json['expirations']
            return expirations
        else:
            return process_not_ok_response(response_json)
    else:
        raise Exception


def get_strikes(final_url):
    """
    Get a list of current or historical option expiration dates from the final url

    :param final_url:   The final url of the API to get the data, with all query parameters
    :return:            pandas DataFrame with strikes for expiry dates
    """
    response = requests.get(final_url, headers=set_headers())
    if response.text:
        response_json = json.loads(response.text)
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
            return process_not_ok_response(response_json)
    else:
        raise Exception


def get_option_chain(final_url):
    response = requests.get(final_url, headers=set_headers())
    if response.text:
        response_json = json.loads(response.text)
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
            return process_not_ok_response(response_json)
    else:
        raise Exception
