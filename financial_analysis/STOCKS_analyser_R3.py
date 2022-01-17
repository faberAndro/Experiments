# coding=utf-8
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf, acf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
from statsmodels.tsa.arima_process import ArmaProcess
import numpy as np
import pandas as pd
from itertools import product
import warnings

warnings.filterwarnings('ignore')

# CARICA I DATI STORICI DI UN AZIONE
file_name = r'C:\04. IT Projects\PROJECTS\0. AI Projects/NEWS_ANALYTICS/SA_machine/Stocks_list_MTD/MacroTrends_Data_Download_A.csv'
time_series = pd.read_csv(file_name, header=9)
data = time_series[['date', 'open']]  # in questo caso il valore è il prezzo di apertura, ma si può scegliere anche come media dei 4 prezzi
ts = time_series[time_series.columns.to_list()[1:-1]]

# simulating random walk
steps = np.random.standard_normal(100)
steps[0] = 0
random_walk = np.cumsum(steps)
plot_pacf(data.open.to_numpy())
plot_acf(data.open.to_numpy())

# simulating moving average (MA)
ar2 = np.array([2])
ma2 = np.array([1, 0.3, 0.9])
MA2_process = ArmaProcess(ar2, ma2).generate_sample(nsample=1000)

plt.figure(figsize=[10, 7.5]) # Set dimensions for figure
plt.plot(MA2_process)
plt.title('Moving Average Process of Order 2')
plt.show()
plot_acf(MA2_process, lags=20)
