class Strategies:

    @staticmethod
    def moving_average_strategy(candlestick_df, quantity):
        """
        If the price is 3% below the slow simple moving average, we will buy.
        If the price is 2% above the buying price, we will sell.
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
