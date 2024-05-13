from flask_wtf import Form, FlaskForm
from wtforms.fields import BooleanField, StringField, FormField, SelectField, SelectMultipleField, DateField

from gui.thermos.helper_functions import plot_types, value_strategies, carry_strategies, momentum_strategies, \
    account_types, execution_steps, checks_to_run


class AllocationOutputForm(FlaskForm):
    dates = SelectField(u'Dates', coerce=int)
    file_names = SelectField(u'Filenames', coerce=int)
    filename = StringField('Filename')


class StrategyForm(FlaskForm):
    strategy_list = SelectMultipleField(u'Strategy List', coerce=int)
    dates = SelectField(u'Dates', coerce=int)
    file_names = SelectField(u'Filenames', coerce=int)
    filename = StringField('Filename')


class InputDataForm(FlaskForm):
    input_data = SelectField('Input data', choices=[('allocation', 'Allocation'), ('strategy', 'Strategy')])
    file_names = SelectField(u'Filenames', coerce=int)
    filename = StringField('Filename')


class PlotTypeForm(FlaskForm):
    line_plot = BooleanField('Line?')
    multi_line = BooleanField('Multi Line?')
    histogram = BooleanField('Histogram?')
    pie_chart = BooleanField('Pie Chart?')
    table = BooleanField('Table?')


class SelectionForm(FlaskForm):
    file_path = StringField('Filepath')
    file_name = StringField('Filename')


class StrategyGroupForm(FlaskForm):
    value = SelectMultipleField('Value', choices=value_strategies(), default='')
    carry = SelectMultipleField('Carry', choices=carry_strategies(), default='')
    momentum = SelectMultipleField('Momentum', choices=momentum_strategies(), default='')


class AccountForm(FlaskForm):
    sbdi = StringField('SBDI')
    cmwba = StringField('CMWBA')
    cmlaa = StringField('CMLAA')


class AccountAum(FlaskForm):
    sbdi = StringField('SBDI', render_kw={"placeholder": "SBDI"})
    cmwba = StringField('CMWBA', render_kw={"placeholder": "CMWBA"})
    cmlaa = StringField('CMLAA', render_kw={"placeholder": "CMLAA"})


class PositionsForm(FlaskForm):
    table_format = SelectField(u'Table format', choices=[('full', 'Full table'), ('summary', 'Summary')])
    accounts = SelectMultipleField('Select account', choices=account_types(), coerce=str)
    strategy = FormField(StrategyGroupForm)
    execution = SelectMultipleField('Select processes to run', choices=execution_steps()[:2], coerce=str, default='')
    checks = SelectMultipleField('Select checks to run', choices=checks_to_run()[1:], coerce=str, default='')
    account_aum = FormField(AccountAum)
    date = StringField('Date', render_kw={"placeholder": "yyyy/mm/dd"}, default='')
    rerun_model = BooleanField('Rerun models')
    filename = StringField('filename', render_kw={"placeholder": "Filename"})


class ResultsForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super().__init__(*args, **kwargs)

    plot_type = FormField(PlotTypeForm)
    title = StringField('Title')
    file_name = StringField('File name')
