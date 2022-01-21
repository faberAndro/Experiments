import quandl
import os
import pandas as pd
import matplotlib.pyplot as plt
from local_settings import QUANDL_APL_KEY


# The adjusted close accounts for stock splits: so, that is just what we should make a graph of
def show_and_plot():
    plt.plot(stock.index, stock['Adj. Close'])
    plt.title('Stock Price')
    plt.ylabel('Price ($)')
    plt.show()


# CONFIG PARAMS
quandl.ApiConfig.api_key = QUANDL_APL_KEY
storage_dir = r'C:\04. IT Projects\PROJECTS\0. AI Projects\NEWS_ANALYTICS\SA_machine\Stocks_list_QDL'
stock_acronym = 'TSLA'

if __name__ == '__main__':
    stock_file_stored = ''.join([storage_dir, '/', stock_acronym, '.csv'])
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
