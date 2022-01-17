#!/usr/bin/env python
# coding: utf-8
import ctypes, sys
from io import StringIO
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.signal import argrelextrema
from scipy.signal import find_peaks

file_name_x = r'C:\04. IT Projects\PROJECTS\0. AI Projects/NEWS_ANALYTICS/SA_machine/Stocks_list/MacroTrends_Data_Download_A.csv'
first_date = '2013-01-03'
last_date = '2016-12-29'
thick_interval = 15
plot_trendline = True
plot_max_min = False


def carica_dati_da_file___old___(file_name):
    """

    Args:
        file_name: path del file azionario

    Returns: un DataFrame Pandas,
             ridotto a soli data e valore,
             pulito dai commenti in testata

    """
    with open(file_name) as f:
        text = f.read()
    f.close()
    # pulizia commenti di intestazione
    testata = re.search('date', text)
    inizio = testata.span()[0]
    cleaned_data = text[inizio:]
    cleaned_dataset = StringIO(cleaned_data)
    time_series = pd.read_csv(cleaned_dataset)
    data_frame = time_series[['date', 'open']]    # in questo caso il valore è il prezzo di apertura, ma si può scegliere anche come media dei 4 prezzi
    return data_frame


def carica_dati_da_file(file_name):
    """

    Args:
        file_name: path del file azionario

    Returns: un DataFrame Pandas,
             ridotto a soli data e valore,
             pulito dai commenti in testata

    """
    time_series = pd.read_csv(file_name, header=9)
    data_frame = time_series[['date', 'open']]    # in questo caso il valore è il prezzo di apertura, ma si può scegliere anche come media dei 4 prezzi
    print(data_frame.head()), input()
    return data_frame


def extract_data_interval(data, data_1=None, data_2=None):
    # TODO: controllare se data_1 < data_2
    # TODO: WARNING: Nono sono presenti tutti i giorni! (Per esempio quelli festivi e/o quelli di chiusura della borsa)
    date_arr = data['date'].to_numpy()
    if not data_1:
        data_1 = date_arr[0]
    index_1 = np.where(date_arr == data_1)
    if not data_2:
        data_2 = date_arr[-1]
    index_2 = np.where(date_arr == data_2)
    # tutte_le_date = data['date'].to_numpy()
    # sotto_intervallo_date = pd.date_range(data_1, periods=30, freq='D')
    # data_ridotti = data['date' in sotto_intervallo_date]
    data.set_index('date', inplace=True)
    serie = pd.Series(data['open'])
    y_arr = serie.to_numpy()
    # data_ridotti.set_index('date', inplace=True)
    serie_ridotta = pd.Series(data['open'])
    x = x_arr[index_1[0][0]:index_2[0][0]]
    y = y_arr[index_1[0][0]:index_2[0][0]]
    return x, y


def trend_with_exp_weighted_av(valori, n_giorni):
    b = 1 - 1/n_giorni
    lv = len(valori)
    vt = np.zeros(lv)
    # vt[0] = (1-b)*valori[0]
    for t in range(1, lv):
        vt[t] = b*vt[t-1] + (1-b)*valori[t]
    vt[1:] = vt[1:] * 1/(1-b**np.arange(1, lv))
    shift = round(n_giorni/2)
    vt_adjusted = np.roll(vt, -shift)
    vt_adjusted[-shift:] = 0
    return vt_adjusted, shift
    # trend = pd.Series(vt_adjusted)
    # trend.index = serie_ridotta.index
    # x_labels = trend.index.to_numpy()
    # valori = serie_ridotta.to_numpy()


def crea_spezzate(serie):
    # CALCOLO DELLA SPEZZATA DI LINEAR REGRESSIONS
    # dividiamo la serie iniziale in N/M intervalli di M giorni
    m_giorni = 15
    y_all_regression = []
    value_chunks = np.array_split(serie, m_giorni)
    for subset_of_m_values in value_chunks:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_arr, subset_of_m_values)
        y_regr = intercept + slope*(x_arr - x_arr[0])
        y_all_regression.append(y_regr)
    # finally, plot x_arr vs. y_all_regression on top of the original graph.
    # cerchiamo di vettorizzare


def find_local_max_and_min(values):
    local_flex_minus = argrelextrema(values, np.less)
    local_flex_major = argrelextrema(values, np.greater)
    return local_flex_minus, local_flex_major


def plot_analysis():
    plt.plot(x, y, label='valori')

    if plot_trendline:
        plt.plot(x[:-delta], y_trend[:-delta], label='trend line')
    if plot_max_min:
        plt.scatter(x[0] + flex_at_min, y[flex_at_min], s=1000, c='green', marker='_')
        plt.scatter(x[0] + flex_at_max, y[flex_at_max], s=1000, c='red', marker='_')

    xt = np.arange(x[0], x[-1]+thick_interval, thick_interval)
    plt.grid(which='both', axis='both')
    plt.xticks(xt, rotation=90)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    window_min_lim = 0
    window_max_lim = -1
    ctypes.windll.shcore.SetProcessDpiAwareness(1) if 'win' in sys.platform else None
    whole_data = carica_dati_da_file(file_name_x)                               # load stock graph
    data = whole_data[window_min_lim: window_max_lim]
    x_arr = np.arange(len(data))                                                # maps dates to integers
    x, y = extract_data_interval(data, data_1=first_date, data_2=last_date)     # extract stock data subset
    y_trend, delta = trend_with_exp_weighted_av(y, n_giorni=180)                # compute trend_line
    flex_at_min, flex_at_max = find_local_max_and_min(y_trend)                  # compute flex points
    plot_analysis()                                                             # plot

