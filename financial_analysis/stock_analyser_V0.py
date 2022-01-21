"""
This computes the following indicators:
1. kurtosis
2. F1 average return
3. CCI
"""

from stock_loader import load_data

# LOAD EQUITY DATA
file_name = r'C:\04. IT Projects\PROJECTS\0. AI Projects/NEWS_ANALYTICS/SA_machine/Stocks_list_MTD/MacroTrends_Data_Download_A.csv'
data = load_data(file_name=file_name, load_all=True)

# INDICATORS:


# F1 average return
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


# kurtosis:
krt = data.Open.kurtosis()

# CCI:
# implementing ...
# to be vectorizes because not performant: each function is to be replaced with a new pd/np series/array
P = 20
start = 2*P


def tp(ts, time):
    return sum((ts.high + ts.low + ts.close)[time-P: time])/3/P


def MA(ts, time):
    MAV = 0
    for t in range(P):
        MAV += tp(ts, time - t)
    return MAV/P


def MD(ts, time):
    _MD = 0
    for t in range(P):
        _MD += abs(tp(ts, time - t) - MA(ts, time - t))
    return _MD/P


def CCI(ts, time):
    return (tp(ts, time) - MA(ts, time)) / (0.015 * MD(ts, time))
