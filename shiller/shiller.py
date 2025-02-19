#!/usr/bin/env python
"""

Import Robert Shiller's P,E,CPI,Interest rate data.

"""

import os

import pandas as pd
import numpy as np

mod_dir = os.path.dirname(__file__)
csv_file = os.path.join(mod_dir, 'shiller.csv')

if not os.path.exists(csv_file):
    xls_url = 'http://www.econ.yale.edu/~shiller/data/chapt26.xlsx'

    xls = pd.ExcelFile(xls_url)
    df = xls.parse('Data', skiprows=[0, 1, 3, 4, 5, 6, 7],
                   skip_footer=5, index_col=0)

    df.to_csv(csv_file)

else:
    df = pd.read_csv(csv_file, index_col=0)

cpi = df['CPI']
gs10 = df['RLONG'] / 100.  # convert from percent to fraction

stock_price = df['P']
stock_div = df['D']


## Computing annualized changes

def annualized_changes(x):
    return x.diff() / x


# Inflation rate
inflation = annualized_changes(cpi)
inflation = inflation[inflation.index.dropna()]

# Stock market rate of return
stock_increase = stock_price[stock_price.index.dropna()].astype('float64').diff() + stock_div.dropna()
stock_returns = stock_increase / stock_price[stock_price.index.dropna()].astype('float64')

interest_rates = gs10
interest_rates = interest_rates[interest_rates.index.dropna()]

dates = cpi.index.dropna()

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib import rcParams

    rcParams['figure.figsize'] = [7., 3.5]

    plt.figure()

    plt.plot(dates, 100 * stock_returns, label='stock returns',
             lw=0.7)

    plt.plot(dates, 100 * inflation, label='inflation', ls='--')

    plt.plot(dates, 100 * interest_rates, label='long term interest', ls=':')

    plt.ylabel('Annualized Rate (%)')
    plt.legend(loc='lower left', fontsize='small')

    plt.savefig('historical-trends.pdf')
