class Strategies:
    """
    This class contains all strategies that will be used for performing the backtest.
    """

    @staticmethod
    def moving_average_strategy(candlestick_df, quantity=1):
        """
        Moving average strategy.

        This strategy includes the usage of 2 simple moving average: A fast moving average which will follow the price
        closely and a slow moving average which follows the ups and downs of the course not as closely.

        The strategy is defined by the following conditions:
            - If the price is 3% below the slow simple moving average, we will buy.
            - If the price is 2% above the buying price, we will sell.

        It creates two lists that will hold our buy and sell signals. Then, it will go through all of the data within
        the passed candlestick data frame and check for every entry whether our buy condition is met. If so, it will
        place a buy signal containing the buying price, the desired selling price and the exact moment in which the coin
        would have been bought. After collecting the buy signals we will go a second time through all of the market data
        in the data frame looking for potential selling points of our bought coins.

        Parameter:
            - candlestick_df: DataFrame - The candlestick market data we will perform the strategy on
            - quantity: int - The number of coins we will buy when our buy condition is met

        Return:
            - buy_signals: list - List of buy signals
            - sell_signals: list - List of sell signals
        """

        df = candlestick_df
        buy_signals = list()  # List that contains information on the buying point (time and buying price)
        sell_signals = list()  # List that contains information on the selling point (time and buying price)

        # For every row of the candlestick data frame, check, if the value of the slow simple moving average
        # (that is present on this exact time) is higher than the lowest price of the candlestick
        # (that is present on this exact time) AND if the slow simple moving average minus the lowest price of the
        # candlestick (that is present on this exact time) is bigger than the lowest price of the candlestick
        # (that is present to this exact time) multiplied with 0,03. ONLY then, we want to buy.
        # Every time this condition is true, append the time and buying price to the list of buy signals.
        for i in range(1, len(df["close"])):
            if df["slow_sma"][i] > df["low"][i] and (df["slow_sma"][i] - df["low"][i]) > 0.03 * df["low"][i]:
                time = df["datetime"][i]  # Time of buy
                buying_price = df["low"][i]
                selling_price = buying_price * 1.02  # The selling price must be 2% over the buying price
                index = i

                # Append buy signal to list of buy signals
                buy_signals.append([time, buying_price, selling_price, index, quantity])

        # Check where we would actually sell: for every buy signal that we got, check the candlestick data for a point
        # in time where the actual price meets our desired selling price. If the price is met, we create our sell signal
        for signal in buy_signals:
            buying_price = signal[1]
            selling_price = signal[2]
            index = signal[3]

            for i in range(index, len(df["close"])):
                if df["high"][i] >= selling_price:
                    time = df["datetime"][i]  # Time of sell
                    # Append sell signal to list of sell signals
                    sell_signals.append([time, buying_price, selling_price, index, quantity])
                    break  # Break the loop

        # Return list of buy and sell signals
        return buy_signals, sell_signals
