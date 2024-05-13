from bokeh.io import curdoc

from returns_dashboard_utilities import get_returns_data, find_other_values, update_widgets, set_up

filename = '../stocks_dashboard/all_stocks_5yr.csv'
static_data, tickers, ticker1, ticker2, source, stats_source, data_table, corr, corr_tools, ts1, ts2 = set_up(filename)


def ticker1_change(attr, old, new):
    ticker2.options = find_other_values(new, tickers)
    update()


def ticker2_change(attr, old, new):
    ticker1.options = find_other_values(new, tickers)
    update()


def update(data=static_data):
    t1, t2 = ticker1.value, ticker2.value
    df = get_returns_data(data, t1, t2)
    source.data = df
    stats_source.data = round(df.describe().reset_index(), 2)
    corr.title.text = '%s returns vs. %s returns' % (t1, t2)
    ts1.title.text, ts2.title.text = t1, t2


ticker1.on_change('value', ticker1_change)
ticker2.on_change('value', ticker2_change)

layout = update_widgets(ticker1, ticker2, data_table, corr, ts1, ts2)
curdoc().add_root(layout)
curdoc().title = "Stock Returns"
