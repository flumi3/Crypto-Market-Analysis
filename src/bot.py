from trading_model import TradingModel


def main():
    model = TradingModel("BTCEUR")
    model.run_moving_average_strategy()


if __name__ == "__main__":
    main()
