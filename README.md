# MarketDataApp

This is a python SDK for accessing data with the MarketData APIs (available at https://www.marketdata.app).  To use the SDK, you will need to register and generate authentication token with the [MarketData](https://www.marketdata.app).

# Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install

```
pip install market-data-api
```

# Usage

Import the necessary packages
```python
from market_data_api.MarketDataAPI import MarketDataAPI, Stock, Index
import pandas as pd
from datetime import datetime
```

Once you set up authentication token, you can use the token for accessing the data
```python
auth_token = <<YOUR AUTHENTICAION TOKEN>>
api_object = MarketDataAPI(auth_token=auth_token)
```

Suppose you'd like to know the market status on a particular date:
```python
ason_date = datetime(year=2023, month=8, day=25).date()
market_status = api_object.get_market_status(ason_date=ason_date)
print(market_status)
```

