"""

Author : Guruppa Padsali

Purpose :
This file contains the functions that get data for markets.

"""

import json

import pandas as pd
import requests

import mdapi_functions.api_interface as api
import mdapi_functions.utilities as utilities


def get_market_status(country=None, ason_date=None, from_date=None, to_date=None, num_of_days=None):
    """
    Get the past, present, or future status for a stock market. The returning dataframe object will have status column
    with values as "open" for trading days or "closed" for weekends or market holidays.

    :param country:         Use to specify the country. Use the two digit ISO 3166 country code. If no country is
                            specified, US will be assumed. Only countries that Market Data supports for stock price
                            data are available (currently only the United States).
    :param ason_date:       Consult whether the market was open or closed on the specified date in the YYYY-MM-DD format
    :param from_date:       The earliest date (inclusive) in the YYYY-MM-DD format. If you use countback, from_date is
                            not required
    :param to_date:         The last date (inclusive) in the YYYY-MM-DD format
    :param num_of_days:     Countback will fetch a number of dates before to_date; if you use from, countback is not
                            required

    :return:                pandas dataframe object with the date and market status as on that date
    """
    params = {}
    url = utilities.get_marketdata_url('market_status')
    base_url = f'{url}?format=json&dateformat=timestamp'  # using the dateformat as timestamp

    if country:
        params['country'] = country
    else:
        params['country'] = 'US'

    if ason_date:
        params['date'] = ason_date

    if from_date:
        params['from'] = from_date

    if to_date:
        params['to'] = to_date

    if num_of_days:
        params['countback'] = num_of_days

    final_url = api.get_final_url(base_url, params)
    response = requests.get(final_url, headers=api.set_headers())

    if response.text:
        response_json = json.loads(response.text)
        status = response_json['s']

        if status == 'ok':
            columns = ['date', 'status']
            dates = response_json['date']
            status = response_json['status']
            status_df = pd.DataFrame(list(zip(dates, status)), columns=columns)
            return status_df
        else:
            return api.process_not_ok_response(response_json)
    else:
        raise Exception("Oops...  Looks like the server is acting up.  Please check back later")
