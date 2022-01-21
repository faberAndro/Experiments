"""
The main purpose of the stock_manipulator class is to
This module creates a first attempt of step-function, starting for a real world equity time-series
"""
# !/usr/bin/env python

# todo: transform the graph in a class! The main object of the class will be the equity.
import ctypes
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

from stock_loader import load_data

data_folder = r'C:\experiments\financial_analysis\Stocks_list_MTD'
file_name_x = data_folder + '/MacroTrends_Data_Download_A.csv'
first_date = '2013-01-03'
last_date = '2016-12-29'
thick_interval = 15
plot_trendline = True


def extract_data_interval(data, x_arr, date_1=None, date_2=None):
    # TODO: check if date_1 < date_2
    # TODO: WARNING: Not all days are included! (ex.: bank holidays and stock exchange closure days))
    date_arr = data['date'].to_numpy()
    if not date_1:
        date_1 = date_arr[0]
    index_1 = np.where(date_arr == date_1)
    if not date_2:
        date_2 = date_arr[-1]
    index_2 = np.where(date_arr == date_2)
    data.set_index('date', inplace=True)
    serie = pd.Series(data['open'])
    y_arr = serie.to_numpy()
    x = x_arr[index_1[0][0]:index_2[0][0]]
    y = y_arr[index_1[0][0]:index_2[0][0]]
    return x, y


def trend_with_exp_weighted_av(values, n_days):
    b = 1 - 1 / n_days
    lv = len(values)
    vt = np.zeros(lv)
    # vt[0] = (1-b)*values[0]
    for t in range(1, lv):
        vt[t] = b * vt[t-1] + (1-b) * values[t]
    vt[1:] = vt[1:] * 1/(1-b**np.arange(1, lv))
    shift = round(n_days / 2)
    vt_adjusted = np.roll(vt, -shift)
    vt_adjusted[-shift:] = 0
    return vt_adjusted, shift


def find_local_max_and_min(values):
    local_flex_minus = argrelextrema(values, np.less)
    local_flex_major = argrelextrema(values, np.greater)
    return local_flex_minus, local_flex_major


def plot_analysis(x, y, delta, y_trend, step_curve_x, step_curve_y):
    plt.plot(x, y, label='values')
    if plot_trendline:
        plt.plot(x[:-delta], y_trend[:-delta], label='trend line')
    xt = np.arange(x[0], x[-1]+thick_interval, thick_interval)
    plt.grid(which='both', axis='both')
    plt.xticks(xt, rotation=90)
    plt.plot(step_curve_x, step_curve_y)
    plt.scatter(step_curve_x, step_curve_y, s=100, facecolors='none', edgecolors='r')
    plt.legend()
    plt.show()


def generate_main_sequence():
    window_min_lim = 0
    window_max_lim = -1
    ctypes.windll.shcore.SetProcessDpiAwareness(1) if 'win' in sys.platform else None
    whole_data = load_data(file_name_x)                                         # load stock graph
    data = whole_data[window_min_lim: window_max_lim]                           # select a window of data
    x_arr = np.arange(len(data))                                                # maps dates to integers
    # todo: refactor all this to work with "date" objects
    x, y = extract_data_interval(data, x_arr, date_1=first_date, date_2=last_date)     # extract stock data subset
    # todo: the following function can be replaced using TA-lib
    y_trend, delta = trend_with_exp_weighted_av(y, n_days=40)                   # compute trend_line
    flex_at_min, flex_at_max = find_local_max_and_min(y_trend)                  # compute flex points
    # todo: we can replace the trend line with min and max Bollinger band.
    #  Then compute the min's on the BB-min and max's on the BB-max.
    step_curve_x = np.sort(np.concatenate((flex_at_min[0], flex_at_max[0]), axis=0))[:-10]    # build step_approx_curve
    step_curve_y = y_trend.take(step_curve_x)
    step_curve_x += x[0]
    plot_analysis(x, y, delta, y_trend, step_curve_x, step_curve_y)                                                             # plot
    # need to find a better plot: from human visual analysis to automatic analsys... possibly re-introducing the
    # idea of regression on single segments.
    return x, y, y_trend, step_curve_x, step_curve_x


if __name__ == '__main__':
    generate_main_sequence()
