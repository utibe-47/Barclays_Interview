import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show


def change_date_format(x):
    return np.array(x, dtype=np.datetime64)


def create_single_line_plot(data_df, x_label, y_label, title, title_prop, xaxis_prop, yaxis_prop, x_axis_type='datetime',
                            legend='', legend_location='top_left', **kwargs):

    plot = figure(x_axis_type=x_axis_type, title=title, plot_width=800, plot_height=800)
    plot.grid.grid_line_alpha = 0.3
    plot.xaxis.axis_label = x_label
    plot.yaxis.axis_label = y_label
    for key, value in title_prop.items():
        setattr(plot.title, key, value)

    for key, value in xaxis_prop.items():
        setattr(plot.xaxis, key, value)

    for key, value in yaxis_prop.items():
        setattr(plot.yaxis, key, value)

    x_values, y_values = data_df[x_label], data_df[y_label]

    if len(x_values) != len(y_values):
        raise AttributeError('x_values and y_values need to be of the same size')

    if x_axis_type == 'datetime':
        plot.diamond(change_date_format(x_values), y_values, color='#A6CEE3', legend_label=legend, **kwargs)
    else:
        plot.line(x_values, y_values, color='#A6CEE3', legend_label=legend, **kwargs)

    if legend is not None:
        plot.legend.location = legend_location
    return plot


def create_multi_line_plot(x_values: tuple, y_values: tuple, x_label, y_label, title, x_axis_type='datetime',
                           legend=None, legend_location='top_left'):
    plot = figure(x_axis_type=x_axis_type, title=title)
    plot.grid.grid_line_alpha = 0.3
    plot.xaxis.axis_label = x_label
    plot.yaxis.axis_label = y_label

    if not isinstance(x_values, (tuple, list)) or not isinstance(y_values, (tuple, list)):
        raise TypeError("x_values and y_values needs to be a list or tuple")
    if len(x_values) != len(y_values):
        raise AttributeError('x_values and y_values need to be of the same size')

    for x_val, y_val, leg in zip(x_values, y_values, legend):
        if x_axis_type == 'datetime':
            plot.line(change_date_format(x_val), y_val, color='#A6CEE3', legend_label=leg)
        else:
            plot.line(x_val, y_val, color='#A6CEE3', legend_label=leg)

    if legend is not None:
        plot.legend.location = legend_location
    return plot


def create_histogram(data_df, feature, title=None):
    feature_data = np.isfinite(data_df[feature].values)
    hist, edges = np.histogram(feature_data, density=True, bins=50)
    plot = figure(title=title, tools='', background_fill_color="#fafafa")
    plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.5)
    return plot


def make_histogram_plot(title, hist, edges, x, pdf, cdf):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.line(x, pdf, line_color="#ff8888", line_width=4, alpha=0.7, legend_label="PDF")
    p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend_label="CDF")

    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color="white"
    return p

