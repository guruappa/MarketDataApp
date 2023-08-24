"""

Author : Guruppa Padsali

Purpose :
This file contains the functions that perform utility functions to read the configuration file

"""

import configparser


def load_configs(resource):   # type could be api, database
    try:
        config_file = "config.properties"           # Change the properties file
        configs = configparser.ConfigParser()
        configs.read(config_file)
        configs_data = dict(configs.items(resource))
        return configs_data
    except Exception as e:
        print(f'{e}')


def get_api_key(host):
    keys = load_configs('api')
    return keys[host]


def get_marketdata_url(function_name):
    urls = load_configs('marketdata_urls')
    return urls[function_name]


