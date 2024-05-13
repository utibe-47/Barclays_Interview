from functools import partial

from bokeh.layouts import layout
from bokeh.plotting import curdoc

from stock_dashboard_utilities import (read_data, create_sliders, create_filter_source, create_table, plot_function,
                                       create_widgets, filter_function, create_change_function)


def set_up(filename):
    data = read_data(filename)
    tickers, month, year, ticker_button, year_slider, month_slider = create_sliders(data)
    source = create_filter_source(data, ticker_button, month_slider, year_slider)
    table, columns = create_table(source)

    plot = plot_function(tickers, source)
    _filter_function = partial(filter_function, data, source, ticker_button, month_slider, year_slider)
    change_function = create_change_function(_filter_function)

    title, widgets_row = create_widgets(change_function, ticker_button, month_slider, year_slider)
    return title, widgets_row, table, plot


_filename = 'all_stocks_5yr.csv'
_title, _widgets_row, _table, _plot = set_up(_filename)
layout = layout([[_title], [_widgets_row], [_plot, _table]])
curdoc().title = 'Stock Analysis Dashboard'
curdoc().add_root(layout)
