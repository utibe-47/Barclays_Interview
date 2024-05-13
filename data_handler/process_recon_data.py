import warnings
from copy import deepcopy
from functools import partial

import numpy as np
import pandas as pd

from utilities.generic_functions import futures_code_checker


def _find_missing_roll_data(latest_roll_data, missing_securities, rebalance_data):
    index_not_found = []
    for count, missing_security in enumerate(missing_securities):
        reb_data = deepcopy(rebalance_data[['Future/Security', 'Account', 'Strategy', 'Position Target']])
        security, account, strategy, ind = missing_security

        code_checker = partial(futures_code_checker, security)
        reb_data['Check'] = reb_data['Future/Security'].map(code_checker)

        index = np.where((reb_data['Account'] == account) & (reb_data['Strategy'] == strategy) &
                         (reb_data['Check'] == True))[0]

        if len(index) > 0:
            latest_roll_data.at[ind, 'Position Target'] = reb_data['Position Target'][index[0]]
        else:
            index_not_found.append(security)

        reb_data = pd.DataFrame()

    if len(index_not_found) > 0:
        message = "Could not find securities {} in latest rebalance data".format(', '.join(index_not_found))
        warnings.warn(message)

    return latest_roll_data


def _process_roll_data(latest_roll_data, latest_rebalance_data, rebalance_dates):
    missing_securities = []
    rebalance_dates.pop(0)
    for index, row in latest_roll_data.iterrows():
        security = row['Future/Security']
        account = row['Account']
        strategy = row['Strategy']

        ind = np.where((latest_rebalance_data['Future/Security'] == security) & (
                    latest_rebalance_data['Account'] == account) & (latest_rebalance_data['Strategy'] == strategy))[
            0]
        if len(ind) > 0:
            latest_roll_data.at[index, 'Position Target'] = latest_rebalance_data['Position Target'][ind[0]]
        else:
            missing_securities.append((security, account, row['Strategy'], index))

    if len(missing_securities) > 0:
        latest_roll_data = _find_missing_roll_data(latest_roll_data, missing_securities, latest_rebalance_data)

    return latest_roll_data