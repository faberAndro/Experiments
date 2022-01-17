# coding=utf-8
import os
import pandas as pd
import talib
import yfinance
import datetime
from matplotlib import pyplot as plt

# SELECTING THE WORKING FOLDERS
CURRENT_FOLDER = r'C:\experiments\financial_analysis'
EQUITY_FOLDER = CURRENT_FOLDER + '/Stocks_list_QDL'
os.chdir(CURRENT_FOLDER)


def load_equity(equity_acronym: str):
    # needs to convert the date to a datetime object
    equity = pd.read_csv(f'{EQUITY_FOLDER}/{equity_acronym}.csv',
                         infer_datetime_format=True,
                         parse_dates=['Date'])
    return equity


def f1_average_return(equity, start_year, end_year, method='arithmetic_average'):
    investment_day = equity[equity['Date'].dt.year == start_year].Date.min()
    initial_value = equity['Open'][equity['Date'] == investment_day].values[0]
    returns = {}
    for y in range(start_year + 1, end_year + 1):
        last_day_in_year = equity[equity['Date'].dt.year == y].Date.max()
        returns[y] = (equity['Close'][equity['Date'] == last_day_in_year].values[0] - initial_value)/initial_value
        print(y, returns[y])
    print(returns)
    return sum(returns.values())/len(returns)


def plot(*args):
    plt.plot(close_prices, label='equity')
    plt.legend()
    for a in args:
        plt.plot(eval(a), label=a)
        plt.legend()
    plt.show()


equity = load_equity('GM')
close_prices = equity.Close
SMA = talib.SMA(close_prices)

plt.plot(close_prices)
plt.plot(SMA)
plt.show()

BB = talib.BBANDS(close_prices)
EMA = talib.EMA(close_prices)
DEMA = talib.DEMA(close_prices)
HT = talib.HT_TRENDLINE(close_prices)
SAR = talib.SAR(equity.High, equity.Low)