from copy import deepcopy
from datetime import datetime
from functools import partial
from os.path import join

from xbbg import blp
from src.db_model.fetcher.bloomberg_fetcher import BEQS
from src.utilities.helper_functions.datetime_helpers import (DateHelpers, change_date,
                                                             get_nearest_preceding_working_day as nearest_wd)
from src.utilities.helper_functions.read_files import ReadFiles

date_converter = partial(DateHelpers.convert_dt_to_str, date_format='%d/%m/%Y')


def read_bloomberg_data(index):
    data = blp.bdh(tickers=index, start_date=DateHelpers.convert_dt_to_str(datetime.now()), flds=['market_cap',
                                                                                                  'market_status',
                                                                                                  'Px_last',
                                                                                                  'volume_avg_30d'])
    return data


def read_equity_value_bloomberg_data_from_file(folder_path, region):
    file_reader = ReadFiles()
    file_df = file_reader.read(join(folder_path, region + '.xlsx'), rows_skipped=2)
    bloomberg_tickers = file_df.loc[1:, 'Ticker'].tolist()
    return bloomberg_tickers


def single_bdh(sec, field, bbg_first_date='2020-01-01', bbg_end_date=None):
    return blp.bdh(sec, field, bbg_first_date, bbg_end_date)


def read_security_data(securities, field, calendar, months_of_data=10):
    end_date = nearest_wd(DateHelpers.convert_dt_to_str(datetime.now()), calendar,
                          date_formatter=DateHelpers.convert_dt_to_str)
    start_date = DateHelpers.convert_dt_to_str(change_date(datetime.now(), -months_of_data, month=True))
    start_date = nearest_wd(start_date, calendar, date_formatter=DateHelpers.convert_dt_to_str)
    data = single_bdh(deepcopy(securities), field, start_date, end_date)
    return data


def process_bloomberg_data(df):
    if df.isnull().values.any():
        df = df.dropna(how='all')
        df.fillna(method='ffill', inplace=True)

    df.reset_index(inplace=True)
    columns = list(df.columns)
    columns, _ = list(map(list, zip(*columns)))
    columns[0] = 'Date'
    df.columns = columns
    df['Date'] = df['Date'].astype(str)
    df['Date'] = df['Date'].apply(date_converter)
    # df = df.set_index('Date')
    return df


def read_min_var_bloomberg_data_from_file(folder_path, region):
    file_reader = ReadFiles()
    file_df = file_reader.read_csv_pd(join(folder_path, region + '.csv'))
    bloomberg_tickers = file_df.loc[3:, 'EQY_FUND_CRNCY'].tolist()
    bloomberg_tickers = [x for x in bloomberg_tickers if str(x) != 'nan']
    return bloomberg_tickers


def run_bloomberg_screen(screen_name: str, date: str):
    try:
        bloomberg_tickers = BEQS(screen_name, date)
    except Exception:
        raise NotImplementedError('EQS screen with name {} failed. Please check bloomberg to make sure '
                                  'screen still works'.format(screen_name))
    else:
        bloomberg_tickers = [x for x in bloomberg_tickers if str(x) != 'nan']
    return bloomberg_tickers
