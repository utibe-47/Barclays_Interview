from yfinance import tickers as tks
from typing import Iterable

from utilities.run_date_check import RunDateChecker
from utilities.meta_helpers import DescriptorNamingMeta

CURRENCY_TICKERS = ['GBPUSD=X', 'GBPAUD=X', 'GBPCHF=X', 'GBPJPY=X', 'GBPCAD=X', 'GBPEUR=X']
STOCK_TICKERS = ['AAPL', 'GOOG', 'MSFT', 'LLOY', 'BARC']
COMMODITY_FUTURES = ['GC=F', 'CL=F', 'NG=F', 'ZC=F', 'BZ=F', 'HE=F', 'SI=F', 'HG=F', 'LE=F', 'CC=F']
STOCK_INDICES = ['^FTSE', '^GSPC', '^DJI', '^IXIC', '^FCHI']


def clean_ticker(ticker: str):
    ticker = ticker.replace('^', '').replace('=X', '').replace('=F', '')
    return ticker


class YahooDataReader(metaclass=DescriptorNamingMeta):

    def __init__(self, start_date=None, end_date=None):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker_list = CURRENCY_TICKERS + COMMODITY_FUTURES + STOCK_TICKERS + STOCK_INDICES

    def run(self):
        data = {}
        for ticker in self.ticker_list:
            data[clean_ticker(ticker)] = self.query_data(ticker)
        return data

    def query_data(self, ticker: str, start_date: str = None, end_date: str = None):
        start_date = self.start_date if start_date is None else start_date
        end_date = self.end_date if end_date is None else end_date
        ticker = tks.Ticker(ticker)
        data = ticker.history(start=start_date, end=end_date)
        # info = ticker.info
        return data

    start_date = RunDateChecker()
    end_date = RunDateChecker()


if __name__ == '__main__':
    _start = '2004-01-05'
    _reader = YahooDataReader(_start)
    _data = _reader.run()
