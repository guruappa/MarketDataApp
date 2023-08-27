import datetime

from Symbol import Symbol


class Option(Symbol):
    def __init__(self, underlying, strike_price, option_type, expiry_date, country=None):
        super().__init__(country, symbol_type='option')

        # Build the urls
        self.__quote_url = super().set_quote_url(self.__api_instance.get_api_url(api_name="option_quote"))
        self.__expirations_url = super().set_expirations_url(
            self.__api_instance.get_api_url(api_name="option_expirations"))
        self.__strikes_url = super().set_quote_url(self.__api_instance.get_api_url(api_name="option_strikes"))
        self.__option_chain_url = super().set_quote_url(self.__api_instance.get_api_url(api_name="option_chain"))

        self.underlying = underlying
        self.strike_price = strike_price

        # Check the option type and set up 1 letter type
        match option_type.upper():
            case 'CALL':
                self.option_type = 'C'
            case 'PUT':
                self.option_type = 'P'

        # Check if the expiry date is given as python datetime object or as string.  If string, check its format.  If datetime object, convert to string
        self.expiry_date = expiry_date

        # Build the option symbol given the ingredients
        self.option_symbol = None
        self._build_option_symbol()

    def _build_option_symbol(self):
        """
        Builds the option symbol after initiation
        """
        expiry_date = datetime.datetime.strptime(self.expiry_date, '%Y-%m-%d').strftime('%y%m%d')
        strike_price = '{:0>8}'.format(int(self.strike_price * 1000))
        option_symbol = f'{self.underlying}{expiry_date}{self.option_type}{strike_price}'
        self.set_option_symbol(option_symbol)

    def get_option_symbol(self):
        """
        Return the option symbol

        :return :   option symbol in string format
        """
        return self.option_symbol

    def set_option_symbol(self, option_symbol):
        """
        Sets the option symbol
        """
        self.option_symbol = option_symbol
