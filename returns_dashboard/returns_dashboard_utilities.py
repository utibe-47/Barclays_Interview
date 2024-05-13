from os import getcwd
from os.path import join
from functools import wraps
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, TableColumn, DataTable, Select
from bokeh.plotting import figure


def process_data(func):
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        data = func(*args, **kwargs)
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        data.sort_values(by='date', ascending=False, inplace=True)
        return data
    return wrapper_timer


@process_data
def read_data(filename):
    cwd = getcwd()
    filepath = join(cwd, filename)
    data = pd.read_csv(filepath)
    return data


def read_stock_data(filename):
    data = read_data(filename)
    data = data[['date', 'Name', 'close']]
    data = data.sort_values(['Name', 'date'])
    data = pd.pivot_table(data, values='close', index=['date'], columns=['Name'])
    data = data.dropna(axis='columns')
    return data.dropna()


def create_table(data):
    stats = round(data.describe().reset_index(), 2)
    stats_source = ColumnDataSource(data=stats)
    stat_columns = [TableColumn(field=col, title=col) for col in stats.columns]
    data_table = DataTable(source=stats_source, columns=stat_columns, width=400, height=350, index_position=None)
    return data_table, stats_source


def create_plots(source):
    corr_tools = 'pan,wheel_zoom,box_select,reset'
    tools = 'pan,wheel_zoom,xbox_select,reset'

    corr = figure(width=350, height=350, tools=corr_tools)
    corr.circle('t1_returns', 't2_returns', size=2, source=source,
                selection_color="firebrick", alpha=0.6, nonselection_alpha=0.1, selection_alpha=0.4)

    ts1 = figure(width=900, height=250, tools=tools, x_axis_type='datetime', active_drag="xbox_select")
    ts1.line('date', 't1', source=source)
    ts1.circle('date', 't1', size=1, source=source, color=None, selection_color="firebrick")

    ts2 = figure(width=900, height=250, tools=tools, x_axis_type='datetime', active_drag="xbox_select")
    ts2.x_range = ts1.x_range
    ts2.line('date', 't2', source=source)
    ts2.circle('date', 't2', size=1, source=source, color=None, selection_color="firebrick")
    return corr_tools, corr, ts1, ts2, tools


def get_returns_data(data, t1, t2):
    df = data[[t1, t2]]
    returns = df.pct_change().add_suffix("_returns")
    df = pd.concat([df, returns], axis=1)
    df.rename(columns={t1: 't1', t2: 't2', t1 + "_returns": "t1_returns", t2 + "_returns": "t2_returns"}, inplace=True)
    return df.dropna()


def find_other_values(value, collection):
    return [val for val in collection if val != value]


def update_widgets(ticker1, ticker2, data_table, corr, ts1, ts2):
    widgets = column(ticker1, ticker2, data_table)
    main_row = row(corr, widgets)
    series = column(ts1, ts2)
    layout = column(main_row, series)
    return layout


def set_up(filename):
    static_data = read_stock_data(filename)
    tickers = list(pd.unique(static_data.columns))

    ticker1 = Select(value='BAC', options=find_other_values('MSFT', tickers))
    ticker2 = Select(value='MSFT', options=find_other_values('BAC', tickers))

    data = get_returns_data(static_data, ticker1.value, ticker2.value)
    source = ColumnDataSource(data=data)
    data_table, stats_source = create_table(data)
    corr_tools, corr, ts1, ts2, tools = create_plots(source)
    return static_data, tickers, ticker1, ticker2, source, stats_source, data_table, corr, corr_tools, ts1, ts2
