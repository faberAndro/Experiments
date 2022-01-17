import quandl
import os
import pandas as pd
import matplotlib.pyplot as plt
# import fbprophet    # Prophet requires columns ds (Date) and y (value)


# The adjusted close accounts for stock splits, so that is what we should graph
def show_and_plot():
    plt.plot(stock.index, stock['Adj. Close'])
    plt.title('Stock Price')
    plt.ylabel('Price ($)')
    plt.show()


# CONFIG PARAMS
quandl.ApiConfig.api_key = 'wySzzBoH_8sR8_zzcpPH'
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


# gm = gm.rename(columns={'Date': 'ds', 'cap': 'y'})      # Put market cap in billions
# gm['y'] = gm['y'] / 1e9     # Make the prophet model and fit on the data
# gm_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15)
# gm_prophet.fit(gm)
