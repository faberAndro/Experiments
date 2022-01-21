import pandas as pd
from local_settings import FINANCIAL_WORKING_FOLDER


def load_data(file_name: str, load_all: bool = False) -> pd.DataFrame:
    """
    Args:
        file_name: filepath
    Returns: Pandas DataFrame,
             only with date and values,
             without header comments
             :param file_name:
             :param load_all:

    """
    # todo: parse dates correctly. Currently they are strings.
    time_series = pd.read_csv(file_name, header=9)
    if not load_all:
        return time_series[['date', 'open']]    # open price
    else:
        return time_series


def load_equity_from_QDL(equity_acronym: str):
    # needs to convert the date to a datetime object
    equity = pd.read_csv(f'{FINANCIAL_WORKING_FOLDER}/Stocks_list_QDL/{equity_acronym}.csv',
                         infer_datetime_format=True,
                         parse_dates=['Date'])
    return equity
