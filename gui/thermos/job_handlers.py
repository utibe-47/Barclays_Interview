from os import getcwd
from os.path import join, dirname

from data_handler.data_reader import DataReader


def read_data(filename):
    folder_path = dirname(dirname(dirname(__file__)))
    filepath = join(folder_path, filename)
    datareader = DataReader()
    data = datareader.read_csv_pd(filepath)
    return data


def get_pricing_data(date=None):
    filename = 'all_stocks_5yr.csv'
    prices = read_data(filename)
    return prices
