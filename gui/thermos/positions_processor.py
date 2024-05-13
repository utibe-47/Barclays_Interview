import pandas as pd
import re

from gui.thermos.enums import AccountNames


def capitalize_words(s):
    return re.sub(r'\w+', lambda m: m.group(0).capitalize(), s).replace(" ", "")


def filter_positions(positions, accounts=None, strategies=None, use_temp_models=False):
    if accounts is None and strategies is None:
        return positions

    if isinstance(accounts, list) and len(accounts) < 1 and isinstance(strategies, list) and len(strategies) < 1:
        return positions

    if accounts is not None:
        try:
            iter(accounts)
        except TypeError:
            accounts = [accounts]

        if len(accounts) > 0:
            accounts = list(map(lambda x: x.upper(), accounts))
            positions = positions[positions.Account.isin(accounts)]

    if strategies is not None and len(strategies) > 0:
        positions['Strategy'] = positions['Strategy'].apply(capitalize_words)
        try:
            iter(strategies)
        except TypeError:
            positions = positions[positions.Strategy.isin([strategies])]
        else:
            positions = positions[positions.Strategy.isin(strategies)]

    positions = positions.reset_index(drop=True)
    return positions


def filter_position_summary(positions_dict: dict, account):
    try:
        position = positions_dict[account]
    except KeyError:
        positions_list = []
        for acc in AccountNames.__members__.keys():
            positions_list.append(positions_dict[acc])
        position = pd.concat(positions_list, axis=0)
    return position
