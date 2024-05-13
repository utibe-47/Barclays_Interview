from collections import namedtuple
from os import environ
from os.path import join

from bokeh.embed import components
from flask import render_template, flash, redirect, url_for, request

from data_handler.data_reader import DataReader
from . import results
from .figures import Plots
from .forms import ResultsForm, SelectionForm, PositionsForm
from .line_plots import create_histogram
from .selections_handler import get_positions, save_positions

PlotDataInputs = namedtuple('PlotDataInputs', ['file_path', 'file_names'])
file_selection_inputs_not_used = False


@results.route('/plot_data', methods=['GET', 'POST'])
def plot_data():
    form = ResultsForm()
    data_reader = DataReader()
    plotter = Plots()
    if request.method == 'POST':
        file_path = request.form.get('file_path', None)
        if file_path is not None:
            file_names = request.form.getlist('file_names')
            full_file_path = join(file_path, file_names[0])
            form.file_name.data = full_file_path

        full_file_path = form.file_name.data
        try:
            data_df = data_reader.read_csv_with_dt(full_file_path)
        except Exception:
            data_df = data_reader.read_csv_pd(full_file_path)
        feature_names = data_df.columns
    else:
        return redirect(url_for('results.select_file'))

    if form.validate_on_submit():
        y_feature_name = request.form.get("y_feature")
        x_feature_name = request.form.get("x_feature")
        plot_types = request.form.getlist('plot_type')
        title = form.title.data
        feature = request.form.get("h_feature")

        if len(plot_types) < 1:
            flash('You need to choose a plot type')
            return render_template('plot.html', form=form, feature_names=feature_names, data_df=data_df)
        elif len(plot_types) > 1:
            flash('You need to choose a single plot type')
            return render_template('plot.html', form=form, feature_names=feature_names)
        else:
            plot_type = plot_types[0]

        if plot_type == 'histogram':
            plot = create_histogram(data_df, feature, title=title)
            script, div = components(plot)
            return render_template("plot.html", script=script, feature_names=feature_names, form=form, div=div,
                                   data_df=data_df)
        elif plot_type == 'table':
            return render_template("plot.html", data_df=data_df, feature_names=feature_names, form=form)

        else:
            title_prop = {'align': 'center', 'text_font_size': '20pt'}
            xaxis_prop = {'axis_label_text_font_size': '20pt'}
            yaxis_prop = {'axis_label_text_font_size': '20pt'}
            plot = plotter.plot(plot_type, data_df, x_feature_name, y_feature_name, title_prop=title_prop,
                                xaxis_prop=xaxis_prop, yaxis_prop=yaxis_prop, title=title)
            script, div = components(plot)
        return render_template("plot.html", script=script, feature_names=feature_names, form=form, div=div,
                               data_df=data_df, column_names=data_df.columns.values,
                               row_data=list(data_df.values.tolist()), zip=zip)

    return render_template('plot.html', form=form, feature_names=feature_names, data_df=data_df,
                           column_names=data_df.columns.values, row_data=list(data_df.values.tolist()), zip=zip)


@results.route('/select_file', methods=['GET', 'POST'])
def select_file():
    file_selection_form = SelectionForm()
    if file_selection_form.validate_on_submit():
        file_path = file_selection_form.file_path.data
        file_names = request.form.getlist('file_names')
        return redirect(url_for('results.plot_data'))
    return render_template('load_data.html', file_selection_form=file_selection_form)


@results.route('/view_positions', methods=['GET', 'POST'])
def view_positions():
    form = PositionsForm()
    if form.validate_on_submit():
        run_model = request.form.get('rerun_models')
        use_today_model = request.form.get('use_today_model')
        save_file = request.form.get('save_file')
        load_file = request.form.get('load_file')

        rerun_models = False if run_model is None else True
        use_today_model = False if use_today_model is None else True
        save_file = False if save_file is None else True
        load_file = False if load_file is None else True
        environ["CONFIG_DIR_OVERRIDE"] = ''

        if load_file:
            return redirect(url_for('results.select_file'), code=307)

        if save_file:
            positions = get_positions(form, use_today_model)
            save_positions(positions, form.filename.data, form.table_format.data)
            return render_template('positions.html', form=form, column_names=positions.columns.values,
                                   row_data=list(positions.values.tolist()), zip=zip)

        if rerun_models:
            pass

        positions = get_positions(form, use_temp_models=use_today_model)
        return render_template('positions.html', form=form, column_names=positions.columns.values,
                               row_data=list(positions.values.tolist()), zip=zip)

    positions = get_positions(form)
    return render_template('positions.html', form=form, column_names=positions.columns.values,
                           row_data=list(positions.values.tolist()), zip=zip)
