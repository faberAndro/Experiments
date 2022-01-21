"""
This module aims to explore the equity data using SARIMAX:
it compute autocorrelation and looks for seasonality
"""

from local_settings import FINANCIAL_WORKING_FOLDER
import numpy as np
import matplotlib.pyplot as plt
# from tqdm import tqdm_notebook
# from itertools import product
from stock_loader import load_equity

from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from statsmodels.tsa.arima_process import ArmaProcess
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# from statsmodels.tsa.holtwinters import ExponentialSmoothing
# from statsmodels.tsa.stattools import adfuller


# loading equity data
data = load_equity(source='MTD', equity_acronym='A')

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

plt.figure(figsize=[10, 7.5])  # Set dimensions for figure
plt.plot(MA2_process)
plt.title('Moving Average Process of Order 2')
plt.show()
plot_acf(MA2_process, lags=20)
