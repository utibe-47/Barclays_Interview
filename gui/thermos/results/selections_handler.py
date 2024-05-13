from os.path import dirname

from data_handler.write_data import WriteData
from gui.thermos.job_handlers import get_pricing_data

POSITIONS_OUTPUT_PATH = dirname(dirname(__file__))


def extract_inputs_for_job(form):
    strategies = form.strategy.data
    table_format = form.table_format.data
    accounts = form.accounts.data
    execution = form.execution.data
    checks = form.checks.data
    aum = form.account_aum.data
    date = form.date.data
    return accounts, date, table_format, strategies, execution, checks, aum


def get_positions(form, use_temp_models=False):
    accounts, date, table_format, strategies, execution, checks, aum = extract_inputs_for_job(form)
    positions = get_pricing_data(date=date)
    return positions


def save_positions(positions, filename, table_type):
    if filename is None or not bool(filename):
        filename = 'positions'

    filename = filename + '_' + table_type.lower()
    write_data = WriteData(save_path=POSITIONS_OUTPUT_PATH, extension='csv')
    write_data.write(filename, positions=positions)
