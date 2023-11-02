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

Output:
```
         date status
0  2023-08-25   open
```

You can get the market status for a range of dates
```python
from_date = datetime(year=2023, month=8, day=1)
to_date = datetime(year=2023, month=8, day=31)

market_status = api_object.get_market_status(from_date=from_date, to_date=to_date)
print(market_status)
```

Output:
```
         date status
          date  status
0   2023-08-01    open
1   2023-08-02    open
2   2023-08-03    open
3   2023-08-04    open
4   2023-08-05  closed
..         ...     ...
26  2023-08-27  closed
27  2023-08-28    open
28  2023-08-29    open
29  2023-08-30    open
30  2023-08-31    open
```

Say you'd want to get the candles for an DJI index:
```python
dji_index = Index(symbol='DJI', auth_token=auth_token)
dji_candle_data = dji_index.get_candles(resolution='D', from_date=from_date, to_date=to_date)
print(dji_candle_data)
```

Output:
```
   symbol        date     close      high       low      open  volume
0     DJI  2023-08-01  35630.68  35679.13  35526.61  35585.99     NaN
1     DJI  2023-08-02  35282.52  35551.92  35226.26  35551.92     NaN
2     DJI  2023-08-03  35215.89  35348.20  35122.32  35194.56     NaN
3     DJI  2023-08-04  35065.62  35506.88  35033.76  35230.13     NaN
4     DJI  2023-08-07  35473.13  35497.38  35125.60  35125.60     NaN
..    ...         ...       ...       ...       ...       ...     ...
18    DJI  2023-08-25  34346.90  34441.91  34029.22  34217.06     NaN
19    DJI  2023-08-28  34559.98  34652.91  34441.64  34441.64     NaN
20    DJI  2023-08-29  34852.67  34864.42  34531.12  34531.12     NaN
21    DJI  2023-08-30  34890.24  35025.57  34811.74  34847.80     NaN
22    DJI  2023-08-31  34721.91  35070.21  34719.77  34909.09     NaN
```

Or, Apple stock...
```python
aapl_stock = Stock(symbol='AAPL', auth_token=auth_token)
candle_data = aapl_stock.get_candles(resolution='D', from_date=from_date, to_date=to_date)
print(candle_data)
```

Output:
```
   symbol        date    close      high       low     open     volume
0    AAPL  2023-08-01  195.605  196.7300  195.2800  196.235   35281426
1    AAPL  2023-08-02  192.580  195.1800  191.8507  195.040   50389327
2    AAPL  2023-08-03  191.170  192.3700  190.6900  191.570   62243282
3    AAPL  2023-08-04  181.990  187.3800  181.9200  185.520  115956841
4    AAPL  2023-08-07  178.850  183.1300  177.3500  182.130   97576069
..    ...         ...      ...       ...       ...      ...        ...
18   AAPL  2023-08-25  178.610  179.1500  175.8200  177.380   51449594
19   AAPL  2023-08-28  180.190  180.5900  178.5450  180.090   43820697
20   AAPL  2023-08-29  184.120  184.9000  179.5000  179.695   53003948
21   AAPL  2023-08-30  187.650  187.8500  184.7400  184.940   60813888
22   AAPL  2023-08-31  187.870  189.1200  187.4800  187.840   60794467
```

You can also get the quote for Apple
```python
aapl_quote = aapl_stock.get_quote()
print(aapl_quote)
```

Output:
```
                      updated symbol     bid  bid_size     mid     ask  ask_size    last  volume
0  2023-11-02 08:08:10 -04:00   AAPL  175.69         1  175.72  175.75         3  175.75       0
```

Or DJI
```python
dji_quote = dji_index.get_quote()
print(dji_quote)
```

Output:
```
                      updated symbol      last
0  2023-11-01 17:02:47 -04:00    DJI  33274.58
```

You want the option chain for the current month for Apple
```python
option_chain = aapl_stock.get_option_chain()
print(option_chain)
```

Output:
```
                        updated        option_symbol underlying                 expiry_date option_type  strike_price  \
0    2023-11-01 16:00:00 -04:00  AAPL231117C00050000       AAPL  2023-11-17 16:00:00 -05:00        call          50.0
1    2023-11-01 16:00:00 -04:00  AAPL231117C00055000       AAPL  2023-11-17 16:00:00 -05:00        call          55.0
2    2023-11-01 16:00:00 -04:00  AAPL231117C00060000       AAPL  2023-11-17 16:00:00 -05:00        call          60.0
3    2023-11-01 16:00:00 -04:00  AAPL231117C00065000       AAPL  2023-11-17 16:00:00 -05:00        call          65.0
4    2023-11-01 16:00:00 -04:00  AAPL231117C00070000       AAPL  2023-11-17 16:00:00 -05:00        call          70.0
..                          ...                  ...        ...                         ...         ...           ...
197  2023-11-01 16:00:00 -04:00  AAPL231117P00275000       AAPL  2023-11-17 16:00:00 -05:00         put         275.0
198  2023-11-01 16:00:00 -04:00  AAPL231117P00280000       AAPL  2023-11-17 16:00:00 -05:00         put         280.0
199  2023-11-01 16:00:00 -04:00  AAPL231117P00285000       AAPL  2023-11-17 16:00:00 -05:00         put         285.0
200  2023-11-01 16:00:00 -04:00  AAPL231117P00290000       AAPL  2023-11-17 16:00:00 -05:00         put         290.0
201  2023-11-01 16:00:00 -04:00  AAPL231117P00300000       AAPL  2023-11-17 16:00:00 -05:00         put         300.0

              first_traded_date  dte     bid  bid_size     mid     ask  ask_size  last_price  open_interest  volume  \
0    2023-03-14 09:30:00 -04:00   15  123.75         0  124.00  124.25         0      116.44            118       0
1    2023-03-14 09:30:00 -04:00   15  118.80         0  119.05  119.30         0      117.55             82       0
2    2023-03-14 09:30:00 -04:00   15  113.80         0  114.05  114.30         0      106.10             32       0
3    2023-03-14 09:30:00 -04:00   15  108.80         0  109.05  109.30         0      107.05             67       0
4    2023-03-14 09:30:00 -04:00   15  103.80         0  104.05  104.30         0      102.10             69       0
..                          ...  ...     ...       ...     ...     ...       ...         ...            ...     ...
197  2023-03-14 09:30:00 -04:00   15  100.90         0  101.08  101.25         0         NaN              0       0
198  2023-03-14 09:30:00 -04:00   15  105.80         0  106.05  106.30         0         NaN              0       0
199  2023-03-14 09:30:00 -04:00   15  110.90         0  111.08  111.25         0         NaN              0       0
200  2023-03-14 09:30:00 -04:00   15  115.80         0  116.00  116.20         0      115.63              0       0
201  2023-03-14 09:30:00 -04:00   15  125.80         0  126.05  126.30         0      126.70              0       0

     in_the_money  intrinsic_value extrnisic_value  underlying_price      iv  delta  gamma   theta  vega  rho
0            True         123.97            None            173.97   2.858    1.0   -0.0     0.0   0.0  0.0
1            True         118.97            None            173.97   2.581    1.0   -0.0     0.0   0.0  0.0
2            True         113.97            None            173.97   2.497    1.0   -0.0     0.0   0.0  0.0
3            True         108.97            None            173.97   2.315    1.0   -0.0     0.0   0.0  0.0
4            True         103.97            None            173.97   2.148    1.0   -0.0     0.0   0.0  0.0
..            ...            ...             ...               ...     ...    ...    ...     ...   ...  ...
197          True         101.03            None            173.97   1.055   -1.0    0.0    -0.0   0.0  0.0
198          True         106.03            None            173.97   1.166   -1.0    0.0    -0.0   0.0  0.0
199          True         111.03            None            173.97   1.202   -1.0    0.0    -0.0   0.0  0.0
200          True         116.03            None            173.97   1.122   -1.0    0.0    -0.0   0.0  0.0
201          True         126.03            None            173.97   1.257   -1.0    0.0     0.0   0.0  0.0
```
