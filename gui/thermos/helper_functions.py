def scheduled_task_list():
    return ['Select', 'Rebalancer', 'PreRun', 'Full Rebalance', 'Roll Positions', 'Run Strategy Only', 'Run Eda Only',
            'Manual Run', 'Run Checks', 'Send Latest Positions To Live', 'Run Scheduled Jobs', 'Run Hedge Report']


def pricing_source():
    return ['Database', 'Backtest', 'File']


def jobs_list():
    return ['Send Reconciliation Signal', 'Run Cantab Execution', 'Load Intraday Data', 'Run Min Var Execution',
            'Run Roll Advisor', 'Send Constraints To Compliance', 'Send Rebalance Weights', 'Send Positions',
            'Paper Trading Results', 'Run Min Var Esg Execution', 'Run Variance Swap Execution',
            'Run Position Aggregates']


def account_types():
    return [('Select', 'Select'), ('sbdi', 'Sbdi'), ('cmwba', 'Cmwba'), ('cmlaa', 'Cmlaa')]


def momentum_strategies():
    return [('Select', 'Select'), ('Gtaa', 'Gtaa'), ('Bond Trend', 'Bond Trend'),
            ('Commodity Trend', 'Commodity Trend'),
            ('FX Trend', 'FX Trend')]


def value_strategies():
    return [('Select', 'Select'), ('FX Value', 'FX Value'), ('Equity Value', 'Equity Value Swap'),
            ('Merger Arbitrage Swap', 'Merger Arbitrage Swap'), ('Equity Minimum Variance', 'Equity Minimum Variance')]


def carry_strategies():
    return [('Select', 'Select'), ('CreditCarry', 'Credit Carry'), ('CommodityCarry', 'Commodity Carry'),
            ('Bond Carry', 'Bond Carry'), ('FX Carry', 'FX Carry'), ('UsShortVarianceSwap', 'Short Volatility')]


def execution_steps():
    return [('Select', 'Select'), ('thinkfolio', 'Run thinkfolio execution'), ('eda', 'Run expected drawdown analysis'),
            ('constraints', 'Run constraints'), ('signal_review', 'Send signal for review')]


def checks_to_run():
    return [('Select', 'Select'), ('constraints', 'Constraints'), ('instrument', 'Instrument Check'),
            ('database', 'Database Check'), ('minimizer', 'Allocation Minimizer')]


def plot_types():
    return [('line_plot', 'Line Plot'), ('multi_line_plot', 'Multi Line Plot'), ('pie_chart', 'Pie Chart'),
            ('table', 'Table'), ('line_plot', 'Line Plot')]


def task_definitions():
    return {'Main Rebalance': "This is the main monthly rebalance which runs all prerun checks and main rebalance "
                              "strategies. Also runs constraints, expected drawdown analysis and thinkfolio execution "
                              "before sending signals for review. Strategies run are: FxValue, EquityMinimumVarianceUs,"
                              "EquityMinimumVarianceEu, EquityMinimumVarianceJp, EquityMinimumVarianceUk, "
                              "EquityValueUs, EquityValueEu, EquityValueJp, Gtaa, BondTrend, FxTrend, CommodityTrend, "
                              "CreditCarry, CommodityCarry, BondCarry ",
            'Mid Month Rebalance': "This runs all the same processes run for main monthly rebalance but with a "
                                   "strategy list. Strategies run are: MergerArbitrageSwap, EquityMinimumVariance, "
                                   "EquityValue, MacquarieCommodityTrend, UsShortVarianceSwap",
            'Single Strategy Rebalance': "This runs all the same processes run for main monthly rebalance but no "
                                         "strategy list is supplied by default. Strategies need to be chosen from the UI "
                                         "which are then used",
            'Single Fund Rebalance': "Runs all prerun checks and constraints. Also runs chosen strategy, "
                                     "thinkfolio execution and sends signal for review"}
