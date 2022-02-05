import pandas as pd
from sys import exit
from settings import MTD_STOCK_STORAGE_DIR, QDL_STOCK_STORAGE_DIR


def load_equity(source: str,
                equity_acronym: str) -> pd.DataFrame:
    """
    loads up an equity, from the local storage to a pandas dataframe

    :param source: can be 'MTD' or 'QDL' (Macrotrends or Quandl)
    :param equity_acronym: the acronym (for example: TSLA = Tesla. It is source dependent)
    :return: a dataframe with the equity timeseries
    """
    # todo: consider checking time zones and maybe include them in the date format
    # todo: turn date to be the index (this affects the other files)
    if source == 'MTD':
        file_path = MTD_STOCK_STORAGE_DIR / f'MacroTrends_Data_Download_{equity_acronym}.csv'
        equity = pd.read_csv(file_path, header=9,
                             parse_dates=['date'])
        new_columns = {i: (i[0].upper() + i[1:]) for i in equity.columns}  # raise to uppercase first letter of column names
        equity.rename(new_columns, axis=1, inplace=True)
    elif source == 'QDL':
        file_path = QDL_STOCK_STORAGE_DIR / f'{equity_acronym}.csv'
        equity = pd.read_csv(file_path,
                             parse_dates=['Date'])
    else:
        print(f'SOURCE {source} NOT RECOGNIZED: THIS EQUITY OBJECT IS EMPTY.')
        equity = None
    if equity is not None:
        equity.set_index('Date', inplace=True)
    return equity
