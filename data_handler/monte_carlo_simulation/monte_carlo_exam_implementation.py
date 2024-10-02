import numpy as np
import pandas as pd
from pydantic import ValidationError

from exercises.cqf.monte_carlo_simulation.monte_carlo_option_pricing import MonteCarloOptionPricing

prices_vary_rate = {}


def run():
    stock = 100
    strike = 100
    dte = 1
    rate = 0.05
    sigma = 0.2

    prices_vary_stock = varying_stock_price(dte, rate, sigma, strike)
    prices_vary_strike = varying_strike_price(stock, dte, rate, sigma)
    prices_vary_rates = varying_rates(stock, strike, dte, sigma)
    prices_vary_vol = varying_vol(stock, strike, dte, rate)
    return prices_vary_rates, prices_vary_vol, prices_vary_strike, prices_vary_stock


def varying_stock_price(dte, rate, sigma, strike):
    prices_vary_stock = {'call': [], 'put': [], 'asian_call': [], 'asian_put': [], 'lookback_fixed_call': [],
                         'lookback_fixed_put': [], 'lookback_floating_call': [], 'lookback_floating_put': []}
    for stock in np.arange(50, 150, 5):
        (call, put, asian_call, asian_put, lb_fixed_call,
         lb_fixed_put, lb_float_call, lb_float_put) = run_option_pricer(stock, strike, rate, sigma, dte)
        prices_vary_stock['call'].append(call)
        prices_vary_stock['put'].append(put)
        prices_vary_stock['asian_call'].append(asian_call)
        prices_vary_stock['asian_put'].append(asian_put)
        prices_vary_stock['lookback_fixed_call'].append(lb_fixed_call)
        prices_vary_stock['lookback_fixed_put'].append(lb_fixed_put)
        prices_vary_stock['lookback_floating_call'].append(lb_float_call)
        prices_vary_stock['lookback_floating_put'].append(lb_float_put)
    return prices_vary_stock


def varying_strike_price(stock, dte, rate, sigma):
    prices_vary_strike = {'call': [], 'put': [], 'asian_call': [], 'asian_put': [], 'lookback_fixed_call': [],
                          'lookback_fixed_put': [], 'lookback_floating_call': [], 'lookback_floating_put': []}
    for strike in np.arange(50, 150, 5):
        (call, put, asian_call, asian_put, lb_fixed_call,
         lb_fixed_put, lb_float_call, lb_float_put) = run_option_pricer(stock, strike, rate, sigma, dte)
        prices_vary_strike['call'].append(call)
        prices_vary_strike['put'].append(put)
        prices_vary_strike['asian_call'].append(asian_call)
        prices_vary_strike['asian_put'].append(asian_put)
        prices_vary_strike['lookback_fixed_call'].append(lb_fixed_call)
        prices_vary_strike['lookback_fixed_put'].append(lb_fixed_put)
        prices_vary_strike['lookback_floating_call'].append(lb_float_call)
        prices_vary_strike['lookback_floating_put'].append(lb_float_put)
    return prices_vary_strike


def varying_rates(stock, strike, dte, sigma):
    prices_vary_rates = {'call': [], 'put': [], 'asian_call': [], 'asian_put': [], 'lookback_fixed_call': [],
                         'lookback_fixed_put': [], 'lookback_floating_call': [], 'lookback_floating_put': []}
    for rate in np.arange(0.001, 0.1, 0.005):
        (call, put, asian_call, asian_put, lb_fixed_call,
         lb_fixed_put, lb_float_call, lb_float_put) = run_option_pricer(stock, strike, rate, sigma, dte)
        prices_vary_rates['call'].append(call)
        prices_vary_rates['put'].append(put)
        prices_vary_rates['asian_call'].append(asian_call)
        prices_vary_rates['asian_put'].append(asian_put)
        prices_vary_rates['lookback_fixed_call'].append(lb_fixed_call)
        prices_vary_rates['lookback_fixed_put'].append(lb_fixed_put)
        prices_vary_rates['lookback_floating_call'].append(lb_float_call)
        prices_vary_rates['lookback_floating_put'].append(lb_float_put)
    return prices_vary_rates


def varying_vol(stock, strike, dte, rate):
    prices_vary_vol = {'call': [], 'put': [], 'asian_call': [], 'asian_put': [], 'lookback_fixed_call': [],
                       'lookback_fixed_put': [], 'lookback_floating_call': [], 'lookback_floating_put': []}
    for sigma in np.arange(0.01, 0.2, 0.01):
        (call, put, asian_call, asian_put, lb_fixed_call,
         lb_fixed_put, lb_float_call, lb_float_put) = run_option_pricer(stock, strike, rate, sigma, dte)
        prices_vary_vol['call'].append(call)
        prices_vary_vol['put'].append(put)
        prices_vary_vol['asian_call'].append(asian_call)
        prices_vary_vol['asian_put'].append(asian_put)
        prices_vary_vol['lookback_fixed_call'].append(lb_fixed_call)
        prices_vary_vol['lookback_fixed_put'].append(lb_fixed_put)
        prices_vary_vol['lookback_floating_call'].append(lb_float_call)
        prices_vary_vol['lookback_floating_put'].append(lb_float_put)
    return prices_vary_vol


def run_option_pricer(s0, strike, rate, sigma, dte):
    try:
        option = MonteCarloOptionPricing(S0=s0, strike=strike, rate=rate, sigma=sigma, dte=dte, nsim=100000,
                                         timesteps=252)
    except ValidationError as e:
        print(f"\nValidation error: {e}")
        raise ValueError(f"\nValidation error: {e}")

    simulation_paths = pd.DataFrame(option.simulatepath)
    pseudorandom = option.pseudorandomnumber
    mean = pseudorandom.mean()
    std = pseudorandom.std()

    call_price = option.vanillaoption[0]
    put_price = option.vanillaoption[1]

    asian_call_price = option.asianoption[0]
    asian_put_price = option.asianoption[1]

    lookback_fixed_call_price = option.lookback_option[0]
    lookback_fixed_put_price = option.lookback_option[1]

    lookback_floating_call_price = option.lookback_floating_option[0]
    lookback_floating_put_price = option.lookback_floating_option[1]
    return (call_price, put_price, asian_call_price, asian_put_price, lookback_fixed_call_price,
            lookback_fixed_put_price, lookback_floating_call_price, lookback_floating_put_price)


if __name__ == '__main__':
    run()
