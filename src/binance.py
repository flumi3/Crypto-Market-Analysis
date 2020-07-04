import pandas as pd  # Library for data analysing
import requests  # HTTP-Library for making HTTP requests easier
import json  # Library to work with JSON


class BinanceOperations:

    @staticmethod
    def get_candlestick_data(symbol):
        """
            This is how the candlestick data that we want to process looks:

            [
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
            ]
        """

        # Create URL
        base = "https://api.binance.com"  # Website of Binance
        endpoint = "/api/v3/klines"  # Endpoint for the candlestick data
        params = "?&symbol=" + symbol + "&interval=1h"  # Symbol (e.g. BTC/EUR) and interval of the candlesticks
        url = base + endpoint + params

        # Download the data
        data = requests.get(url)

        # Put json data into dictionary and generate a data frame from it
        data_dict = json.loads(data.text)
        df = pd.DataFrame.from_dict(data_dict)

        # Cast values from strings to floats
        for col in range(11):
            df[col] = df[col].astype(float)

        # Return the result
        return df
