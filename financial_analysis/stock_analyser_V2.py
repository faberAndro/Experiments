"""
This module experiments financial analysis through the functions
available within the TA-lib library
Note: all the indicator from this library are timeseries themselves
"""

import os
import talib
from matplotlib import pyplot as plt
from stock_loader import load_equity


def plot(*args):
    """
    plots the equity superposed with the indicators from *args
    :param args: a list of text values, matching the name of the variable for the desired indicators
    :return: None
    """
    plt.plot(close_prices, label='equity')
    plt.legend()
    for a in args:
        plt.plot(eval(a), label=a)
        plt.legend()
    plt.show()


equity_loaded = load_equity(source='QDL', equity_acronym='GM')
close_prices = equity_loaded.Close
SMA = talib.SMA(close_prices)

plt.plot(close_prices)
plt.plot(SMA)
plt.show()

BB = talib.BBANDS(close_prices)
EMA = talib.EMA(close_prices)
DEMA = talib.DEMA(close_prices)
HT = talib.HT_TRENDLINE(close_prices)
SAR = talib.SAR(equity_loaded.High, equity_loaded.Low)
