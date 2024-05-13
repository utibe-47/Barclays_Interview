from datetime import datetime
from os.path import dirname
import pandas as pd
from functools import singledispatch

from data_handler.database.connector import sqlite_db_session
from data_handler.database.models.historical_prices import InstrumentPrices, header, header_csv, header_with_date, \
    header_csv_with_date
from data_handler.database.queries.pricing_queries import query_by_date, query_data, query_latest_data, \
    query_latest_data_with_contract

from utilities.datetime_helpers import DateHelpers
from utilities.decorator_functions import decorator_factory
from utilities.generic_functions import create_dataframe

DF = pd.DataFrame


def dataframe_creator(q_data):
    data = create_dataframe(q_data, *header)
    data.columns = header_csv
    return data


def dataframe_creator_with_date(q_data):
    data = create_dataframe(q_data, *header_with_date)
    data.columns = header_csv_with_date
    return data


def decorate_function(func, factory_func):
    decorator_func = decorator_factory(factory_func)
    run_time_func = decorator_func(func)
    return run_time_func


def _get_position_df(session, reason_code=None, date=None, by_security=False):
    if by_security:
        date_limit = DateHelpers.add_months(datetime.now(), -2)
        q_data = query_latest_data_with_contract(session, date_limit)
    else:
        if reason_code is not None:
            q_data = query_data(session, reason_code, date)
        else:
            if date is not None:
                q_data = query_latest_data(session)
            else:
                q_data = query_latest_data(session, date_limit=date)
    return q_data


@singledispatch
def query_prices(ticker, *args):
    raise TypeError('Do not know how to get prices from the database, the argument ticker should be of type '
                    'string or list and not {} provided'.format(type(ticker).__name__))


@query_prices.register(str)
def _(ticker, sess, date, *args):
    ordered_rebalance_dates = query_by_date(sess, date_limit=date)
    run_time_func = decorate_function(_get_position_df, dataframe_creator)
    latest_data = run_time_func(sess, date=date)

    return latest_data


@query_prices.register(list)
def _(ticker, sess, date, keep_date):
    if keep_date:
        run_time_func = decorate_function(_get_position_df, dataframe_creator_with_date)
        latest_data = run_time_func(sess, date=date, by_security=True)
    else:
        run_time_func = decorate_function(_get_position_df, dataframe_creator)
        latest_data = run_time_func(sess, date=date, by_security=True)

    latest_data.reset_index(drop=True, inplace=True)
    return latest_data


class HistoricalPricesHandler:

    def __init__(self, database_name='infinity.db'):
        self.basedir = dirname(__file__)
        self.database_name = database_name

    def save_prices(self, prices: DF):
        with sqlite_db_session(self.basedir, self.database_name) as sess:
            for index, row in prices.iterrows():
                prices = InstrumentPrices(CobDate=row['Date'], Ticker=row['ticker'], Name=row['name'],
                                          Price=row['price'], Volume=row['volume'])

                sess.add(prices)
                sess.commit()

    def get_prices_by_date(self, ticker, start_date=None, end_date=None):

        if end_date is None:
            end_date = datetime.now()
        data = self.get_prices(ticker, start_date, end_date)

        return data

    def get_prices(self, ticker, date=None, keep_date=False):
        with sqlite_db_session(self.basedir, self.database_name) as sess:
            data = query_prices(ticker, sess, date, keep_date)
        return data


if __name__ == '__main__':
    _ticker = ''
    position_handler = HistoricalPricesHandler()
    _prices = position_handler.get_prices(_ticker)
    g = 5
