import pandas as pd  # Library for data analysing
import requests  # HTTP-Library for making HTTP requests easier
import json  # Library to work with JSON


class BinanceOperations:
    """
    This class functions as interface for the Binance API in order to access or send data from and to the Binance API.
    """

    @staticmethod
    def get_candlestick_data(symbol, start_time=None, end_time=None):
        """
        Access candlestick market data from the Binance API.

        Creates a Binance URL to access the right endpoint at the Binance API. Then downloads candlestick market data
        looking like this:

            [
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "17928899.62484339" // Ignore.
            ]

        After getting the JSON formatted data, convert it into a pandas data frame - a excel table like data structure.

        Parameter:
            - symbol: string - Symbol for which we want to get the market data on (e.g. BTCEUR, ETHEUR, ...)
            - start_time: timestamp - Start time of the candlestick data we will access
            - end_time: timestamp - End time of the candlestick data we will access

        Return:
            - DataFrame - The created data frame containing the candlestick data
        """

        # Create the invidual URL parts
        base = "https://api.binance.com"  # Website of Binance
        endpoint = "/api/v3/klines"  # Endpoint for the candlestick data
        params = "?&symbol=" + symbol + "&interval=1h"  # Symbol (e.g. BTC/EUR) and interval of the candlesticks

        # Add start and end time to the url if it has been passed
        if start_time:
            params = params + "&startTime=" + str(start_time)
        if end_time:
            params = params + "&endTime=" + str(end_time)

        # Create complete url
        url = base + endpoint + params

        # Download the data
        data = requests.get(url)

        # Put json data into dictionary and generate a data frame from it
        data_dict = json.loads(data.text)
        df = pd.DataFrame.from_dict(data_dict)

        # Return the result
        return df
