import sys
sys.path.append(r'C:\Users\u49402\Repository\Singularity\gui\thermos\results')

from data_handler.data_reader import DataReader
from gui.thermos.results.line_plots import create_multi_line_plot, create_single_line_plot, create_histogram
from bokeh.plotting import show


class Plots:

    def __init__(self):
        self.plot_types = {'line_plot': self.plot_line, 'histogram': self.plot_histogram}

    def plot(self, plot_type, *args, **kwargs):
        try:
            plot_func = self.plot_types[plot_type]
        except KeyError:
            raise KeyError('{} - Not one of the allowed type of plots'.format(plot_type))
        else:
            plt = plot_func(*args, **kwargs)
        return plt

    @staticmethod
    def plot_histogram(self, *args, **kwargs):
        plot = create_histogram(*args, **kwargs)
        return plot

    @staticmethod
    def plot_line(*args, **kwargs):
        plot = create_single_line_plot(*args, **kwargs)
        return plot


if __name__ == '__main__':
    data_reader = DataReader()
    plotter = Plots()
    file_path = r'N:\multi_mg\LDN\ARP\execution\output_results\strategies\Bond Carry\2019-11-20\2019-11-20T13-47-28.552037_rebalancing_weights.csv'
    data_df = data_reader.read_csv_with_dt(file_path)
    feature_names = list(data_df.columns)
    x_feature_name = feature_names[0]
    y_feature_name = feature_names[1]
    plot_type = 'line_plot'
    title = 'test'

    plot = plotter.plot(plot_type, data_df, x_feature_name, y_feature_name, title=title, line_dash='dotdash', size=10)
    show(plot)
