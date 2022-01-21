import quandl
import os
import pandas as pd
import matplotlib.pyplot as plt
from local_settings import QUANDL_APL_KEY
from settings import QDL_STOCK_STORAGE_DIR

# CONFIG PARAMS
quandl.ApiConfig.api_key = QUANDL_APL_KEY
# stock_acronym example: 'TSLA' (Tesla)


def download_equity_timeseries(stock_acronym: str) -> pd.DataFrame:
    """
    download a stock from Quandl and saves it to the storage folder
    If the stock already exists, no downloaded is operated
    :param stock_acronym: the acronym of the equity
    :return: the dataframe of the timeseries downloaded (or from the storage folder if already existing)
    """
    stock_file_stored = ''.join([QDL_STOCK_STORAGE_DIR, '/', stock_acronym, '.csv'])
    if os.path.exists(stock_file_stored) is True:
        print(stock_acronym + ' Stock already downloaded.')
        stock = pd.read_csv(stock_file_stored)
        print(stock.head())
    else:
        stock_name = 'WIKI/' + stock_acronym
        print('downloading ' + stock_acronym + '...')
        stock = quandl.get(stock_name)
        stock.to_csv(stock_file_stored)
        print(stock.head())
        return stock


# The adjusted close accounts for stock splits: so, that is just what we should make a graph of
def show_and_plot(stock: pd.DataFrame):
    plt.plot(stock.index, stock['Adj. Close'])
    plt.title('Stock Price')
    plt.ylabel('Price ($)')
    plt.show()
