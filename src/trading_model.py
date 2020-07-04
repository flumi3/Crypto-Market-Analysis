import pandas as pd  # Library for data analyzing
import plotly.graph_objs as go  # Library for data visualizing

from pyti.smoothed_moving_average import smoothed_moving_average as sma  # Technical indicator library
from plotly.offline import plot  # Library for visualizing data
from binance import BinanceOperations
from strategies import Strategies


# This class holds all the properties and methods needed for the trading bot
class TradingModel:
    # Constructor
    def __init__(self, symbol):
        self.symbol = symbol

    # This method processes the candlestick data
    @staticmethod
    def process_data(candlestick_data):
        df = candlestick_data
        df = df.drop(range(6, 12), axis=1)  # Drop the last six columns as they are not needed

        # Rename the columns
        col_names = [
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]
        df.columns = col_names

        # Cast values from strings to floats
        for col in col_names:
            df[col] = df[col].astype(float)

        # Add the moving averages to the data frame
        df["fast_sma"] = sma(df["close"].tolist(), 10)  # fast simple moving average follows prices closely
        df["slow_sma"] = sma(df["close"].tolist(), 30)  # slow simple moving average follows prices less closely

        # Add date in datetime format to the data frame so we can se real dates on the plot and not just timestamps
        df["datetime"] = pd.to_datetime(df["time"] * 1000000, infer_datetime_format=True)

        # Return result
        return df

    # This method visualizes the candlestick data in form of a candlestick chart
    def plot_data(self, candlestick_df, buy_signals, sell_signals):
        df = candlestick_df

        # Plot candlestick chart
        candle = go.Candlestick(
            x=df["datetime"],
            open=df["open"],
            close=df["close"],
            high=df["high"],
            low=df["low"],
            name="Candlesticks"
        )

        # Plot fast simple moving average
        fast_sma = go.Scatter(
            x=df["datetime"],
            y=df["fast_sma"],
            name="Fast SMA",
            line=dict(color="rgba(102, 207, 255, 50)")
        )

        # Plot slow moving average
        slow_sma = go.Scatter(
            x=df["datetime"],
            y=df["slow_sma"],
            name="Slow SMA",
            line=dict(color="rgba(255, 207, 102, 50)")
        )

        # Plot buy signals
        buys = go.Scatter(
            x=[time[0] for time in buy_signals],
            y=[price[1] for price in buy_signals],
            name="Buy Signals",
            mode="markers"
        )

        # Plot desired selling prices
        desired_prices = go.Scatter(
            x=[time[0] for time in buy_signals],
            y=[price[1] * 1.02 for price in buy_signals],
            name="Desired Sell Prices",
            mode="markers"
        )

        # Plot selling signals
        sells = go.Scatter(
            x=[time[0] for time in sell_signals],
            y=[price[2] for price in sell_signals],
            name="Sell Signals",
            mode="markers",
            marker=dict(
                color="rgb(139,69,19)"
            )
        )

        # List of objects that shall be plotted
        data = [candle, slow_sma, fast_sma, buys, desired_prices, sells]

        # Style and display
        layout = go.Layout(
            title=self.symbol,
            xaxis_title="Time",
            yaxis_title="Euro"
        )

        # Create figure and plot it
        figure = go.Figure(data=data, layout=layout)
        plot(figure, filename=self.symbol + ".html")

    # This method backtests the strategy
    def backtest_strategy(self, buy_signals, sell_signals):
        money_spent = 0
        money_earned = 0

        # Add all buying and selling prices
        for signal in sell_signals:
            # [time, buying_price, selling_price, index, quantity]
            quantity = signal[4]
            buying_price = signal[1] * quantity
            selling_price = signal[2] * quantity

            # Calculate spent and earned money
            money_spent = money_spent + buying_price
            money_earned = money_earned + selling_price

        # Calculate some other stats
        profit = money_earned - money_spent
        coins_bought = len(buy_signals) * quantity
        coins_sold = len(sell_signals) * quantity
        average_buying_price = money_spent / coins_bought
        average_selling_price = money_earned / coins_bought

        # Output
        print(f"Symbol: {self.symbol}")
        print("")

        print(f"Coins bought: {coins_bought}")
        print(f"Coins sold: {coins_sold}")
        print("")

        print(f"Average buying price: {round(average_buying_price, 2)}€")
        print(f"Average selling price: {round(average_selling_price, 2)}€")
        print("")

        print(f"Total money spent: {round(money_spent, 2)}€")
        print(f"Total money earned: {round(money_earned, 2)}€")
        print("")

        print(f"Profit: {round(profit, 2)}€")

    # This method executes the actual operations of the bot
    def run_moving_average_strategy(self):
        binance = BinanceOperations()  # Create instance of binance operations class
        strategies = Strategies()  # Create instance of strategies class

        candlestick_data = binance.get_candlestick_data(self.symbol)  # Get the candlestick data
        candlestick_df = self.process_data(candlestick_data)  # Process the candlestick data

        # Compute buy and sell signals:
        signals = strategies.moving_average_strategy(candlestick_df, quantity=1)
        buy_signals = signals[0]
        sell_signals = signals[1]

        # Backtest the strategy
        self.backtest_strategy(buy_signals, sell_signals)

        # Plot the candlestick data as candlestick chart
        self.plot_data(candlestick_df, buy_signals, sell_signals)
