import pathlib
from os.path import join

import pandas as pd
from xbbg import blp

from src.utilities.directory_manipulation.directory_manipulators import get_latest_folder_date
from src.utilities.email_sender.production_email_sender import get_latest_file
from src.utilities.helper_functions.read_files import ReadFiles


def get_exclusion_list(exclusion_list_path, file_name, extension=None, **kwargs):
    if extension is None:
        extension = '.xlsx'
    file_ext = pathlib.Path(file_name).suffix
    file_reader = ReadFiles()
    if bool(file_ext) and file_ext in file_name:
        file_df = file_reader.read(join(exclusion_list_path, file_name), **kwargs)
    else:
        file_df = file_reader.read(join(exclusion_list_path, file_name + extension), **kwargs)
    return file_df


def get_merger_arb_list(exclusion_list_path):
    exclusion_list_path = join(exclusion_list_path, get_latest_folder_date(exclusion_list_path))
    filename = get_latest_file(exclusion_list_path, 'positions')
    merger_arb_pd = get_exclusion_list(exclusion_list_path, filename, extension='xlsb', engine='pyxlsb')
    merger_arb_list = list(set(merger_arb_pd['contractidentifier'].to_list() +
                               merger_arb_pd['contractidentifier.1'].to_list()))
    merger_arb_list = [marb for marb in merger_arb_list if str(marb) != 'nan']
    return pd.DataFrame(data=merger_arb_list, columns=['Manual Ticker'])


def filter_by_global_id(excluded_global_id_pd, filtered_tickers):
    ticker_global_id_pd = blp.bdp(list(filtered_tickers), 'ID_BB_GLOBAL')
    excluded_ids = excluded_global_id_pd['BBG Global ID Clean'].tolist()
    excluded_global_id_pd = ticker_global_id_pd[ticker_global_id_pd['id_bb_global'].isin(excluded_ids)]
    if excluded_global_id_pd.shape[0] > 0:
        excluded_global_ids = set(excluded_global_id_pd.index)
        filtered_tickers = filtered_tickers - excluded_global_ids
    return filtered_tickers


def filter_exclusion_list(tickers, excluded_tickers_pd, excluded_global_id_pd):
    excluded_tickers = excluded_tickers_pd[excluded_tickers_pd['Manual Ticker'].isin(tickers)]
    filtered_tickers = set(tickers) - set(excluded_tickers['Manual Ticker'].to_list())
    filtered_tickers = filter_by_global_id(excluded_global_id_pd, filtered_tickers)
    return list(filtered_tickers)


def compile_exclusion_list(exclusion_path):
    primary_exclusion_pd = get_exclusion_list(exclusion_path, 'gam_exclusion_list', header=None)
    primary_exclusion_pd.columns = ['Manual Ticker']
    primary_exclusion_pd = primary_exclusion_pd.apply(lambda x: x + ' Equity')

    excluded_global_id_pd = get_exclusion_list(exclusion_path, 'AIA_restricted_list', sheetname='Sheet1')
    merger_arb_exclusion_pd = get_merger_arb_list(join(exclusion_path, 'merger_arb'))
    tickers = merger_arb_exclusion_pd['Manual Ticker'].tolist()
    is_complete = list(map(lambda x: 'Equity' in x, tickers))
    if any(val is False for val in is_complete):
        merger_arb_exclusion_pd['Manual Ticker'] = merger_arb_exclusion_pd['Manual Ticker'].apply(
            lambda x: x + ' Equity')
    excluded_tickers = pd.concat([primary_exclusion_pd, merger_arb_exclusion_pd])
    return excluded_tickers, excluded_global_id_pd
