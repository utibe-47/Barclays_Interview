import random
from functools import wraps
from os import getcwd
from os.path import join

import pandas as pd
from bokeh.models import (MultiChoice, Slider, RangeSlider, ColumnDataSource, TableColumn, DateFormatter, DataTable,
                          HoverTool, CDSView, GroupFilter, Div, Column, Row)
from bokeh.palettes import Category20
from bokeh.plotting import figure


def process_data(func):
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        data = func(*args, **kwargs)
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        data.sort_values(by='date', ascending=False, inplace=True)
        data['Month'] = pd.to_datetime(data['date']).dt.month
        data['Year'] = pd.to_datetime(data['date']).dt.year
        return data
    return wrapper_timer


@process_data
def read_data(filename):
    cwd = getcwd()
    filepath = join(cwd, filename)
    data = pd.read_csv(filepath)
    return data


def create_sliders(data):
    tickers = sorted(list(data.Name.unique()))
    month = sorted(list(data.Month.unique()))
    year = sorted(list(data.Year.unique()))
    ticker_button = MultiChoice(value=tickers[:2], options=tickers)
    year_slider = Slider(start=year[0], end=year[-1], value=year[1], step=1, title='Year')
    month_slider = RangeSlider(start=month[0], end=month[-1], value=month[:2], step=1, title='Month')
    return tickers, month, year, ticker_button, year_slider, month_slider


def create_filter_source(data, ticker_button, month_slider, year_slider):
    df = data[(data['Name'].isin(ticker_button.value)) & (data['Month'] >= month_slider.value[0]) & (
            data['Month'] <= month_slider.value[1]) & (data['Year'] == year_slider.value)]
    source = ColumnDataSource(data=df)
    return source


def create_table(source):
    columns = [TableColumn(field="date", title="Date", formatter=DateFormatter(format="%Y-%m-%d")),
               TableColumn(field="Name", title="Name"),
               TableColumn(field="close", title="Close"), ]

    table = DataTable(source=source, columns=columns, height=500)
    return table, columns


def plot_function(tickers, source):
    colors = list(Category20.values())[17]
    random_colors = []
    for c in range(len(tickers)):
        random_colors.append(random.choice(colors))

    hover = HoverTool(tooltips=[('date', '$x{%Y-%m-%d}'),
                                ('close', '$@{close}{0.0}'),
                                ('high', '$@{high}{0.0}'),
                                ('low', '$@{low}{0.0}'),
                                ('volume', '@volume{0.00 a}')],
                      formatters={'$x': 'datetime'})

    plot = figure(x_axis_type='datetime', width=1000, height=500)

    for t, rc in zip(tickers, random_colors):
        view = CDSView(source=source, filters=[GroupFilter(column_name='Name', group=t)])
        plot.scatter(x='date', y='close', source=source, view=view, line_color=rc, line_width=4)

    plot.add_tools(hover)
    return plot


def create_widgets(change_function, ticker_button, month_slider, year_slider):
    ticker_button.on_change('value', change_function)
    month_slider.on_change('value', change_function)
    year_slider.on_change('value', change_function)

    title = Div(text='<h1 style="text-align: center">Stock Dashboard</h1>')
    widgets_col = Column(month_slider, year_slider)
    widgets_row = Row(widgets_col, ticker_button)
    return title, widgets_row


def filter_function(data, source, ticker_button, month_slider, year_slider):
    new_src = data[(data['Name'].isin(ticker_button.value)) & (data['Month'] >= month_slider.value[0]) & (
            data['Month'] <= month_slider.value[1]) & (data['Year'] == year_slider.value)]
    source.data = new_src.to_dict('series')


def create_change_function(filter_function):
    def change_function(attr, old, new):
        filter_function()
    return change_function
