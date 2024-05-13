from datetime import datetime
from os.path import dirname
import pandas as pd

from data_handler.database.connector import sqlite_db_session
from data_handler.database.models.thinkfolio_position import (ThinkfolioPositions, header, header_csv,
                                                              header_with_date, header_csv_with_date)
from data_handler.database.queries.position_handler_queries import query_latest_data
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


def _get_position_df(session, date=None):
    q_data = query_latest_data(session, date_limit=date)
    return q_data


def get_positions(sess, date, keep_date=False):
    run_time_func = decorate_function(_get_position_df, dataframe_creator)
    data = run_time_func(sess, date=date)
    return data


class ThinkfolioPositionHandler:

    def __init__(self, database_name='singularity.db'):
        self.basedir = dirname(__file__)
        self.database_name = database_name

    def save_position(self, thinkfolio_positions: DF, run_date=None):
        if run_date is None:
            run_date = datetime.now()
        thinkfolio_positions.columns = header
        with sqlite_db_session(self.basedir, self.database_name) as sess:
            for index, row in thinkfolio_positions.iterrows():
                positions = ThinkfolioPositions(Date=run_date, LeadDirection=row['LeadDirection'], Lead=row['Lead'],
                                                NonLead=row['NonLead'], Security=row['Security'], Tenor=row['Tenor'],
                                                PositionTarget=row['PositionTarget'], Protection=row['Protection'],
                                                Account=row['Account'], Strategy=row['Strategy'],
                                                DealingDesk=row['DealingDesk'], InstrumentType=row['InstrumentType'],
                                                Strike=row['Strike'], ReasonCode=row['ReasonCode'])

                sess.add(positions)
                sess.commit()

    def get_position_by_date(self, date):
        data = self.get_position(date)
        return data

    def get_position(self, date=None, keep_date=False):
        with sqlite_db_session(self.basedir, self.database_name) as sess:
            data = get_positions(sess, date, keep_date)
        return data

    @staticmethod
    def _get_latest_roll_data(latest_data, reason_code):
        latest_roll_data = latest_data[latest_data['ReasonCode'] == reason_code]
        return latest_roll_data


if __name__ == '__main__':
    strategies = ''
    position_handler = ThinkfolioPositionHandler()
    thinkfolio_position = position_handler.get_position()
    g = 5