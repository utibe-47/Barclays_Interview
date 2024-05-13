from data_handler.historical_price_handler import HistoricalPricesHandler
from data_handler.pull_yahoo_data import YahooDataReader


class PopulateDatabase:

    def __init__(self):
        self.database_handler = HistoricalPricesHandler()
        self.datareader = YahooDataReader()

    def run(self):
        data = self.read_data()
        self.populate(data)

    def read_data(self):
        data = self.datareader.run()
        return data

    def populate(self, data: dict):
        for ticker, prices in data.items():
            self.database_handler.save_prices(prices)


if __name__ == '__main__':
    pd = PopulateDatabase()
    pd.run()
