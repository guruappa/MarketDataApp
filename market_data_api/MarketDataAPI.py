import configparser
import os.path
import urllib.parse

import requests


class MarketDataAPI:
    def __init__(self, config_file=None):
        """
        Initialize an instance of the class

        :param config_file  :   The configuration file
        """
        self.config_file = config_file
        self.__configs_data = {}
        self.__load_configs()
        self.__no_data_str = 'No Data'

    def __check_config_file(self):
        """
        Check if the config file exists

        :return: True, if the file exists, else False
        """
        if os.path.isfile(self.config_file):
            return True
        else:
            return False

    def __load_configs(self):
        """
        Load the configuration settings from the config file into the instance variable
        """
        try:
            if self.__check_config_file():
                configs = configparser.ConfigParser()
                configs.read(self.config_file)

                for section in configs.sections():
                    self.__configs_data[section] = dict(configs.items("api"))
        except Exception as e:
            print(f'{e}')

    def get_header(self):
        """
        Get the header information for the request to the API

        :return: The header information
        """
        return {'Authorization': f'token {self.__configs_data["authentication"]["token"]}'}

    def get_api_url(self, api_name):
        """
        Gets the API URL from the config file

        :param api_name:  The name of the parameter
        :return:
        """
        return self.__configs_data["api_urls"][api_name]

    def process_not_ok_response(self, response_json):
        """
        Utility function for processing the response that does not contain data

        :return: string containing the message
        """
        # TODO: Log the status and error
        status = response_json['s']
        match status:
            case 'no_data':
                # when the server returned no data
                return self.__no_data_str
            case 'error':
                # when the server returned error
                return response_json['errmsg']

    def build_final_url(self, base_url, params):
        """
        Builds the final url before making the request to market_data_api.app APIs

        :param base_url :   The base url on which the parameters are to be added
        :param params   :   The query parameters in dictionary that need to be encoded in the final url
        :return         :   The final URL that can be sent as a request to the API
        """
        url_params = urllib.parse.urlencode(params)
        final_url = f"{base_url}&{url_params}"
        return final_url

    def get_data_from_url(self, url, params):
        """
        Get the data from the MarketData API

        :param url      : The url of the API
        :param params   :   The parameters for the API
        :return         : The response object of the API
        """
        if params:
            final_url = self.build_final_url(url, params)
        else:
            final_url = url

        response = requests.get(final_url, headers=self.get_header())
        return response
