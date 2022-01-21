"""
This computes first indicators:
1. kurtosis
2. CCI
"""

import stock_manipulator_V0 as Sm0

# LOAD EQUITY DATA
file_name = r'C:\04. IT Projects\PROJECTS\0. AI Projects/NEWS_ANALYTICS/SA_machine/Stocks_list_MTD/MacroTrends_Data_Download_A.csv'
data = Sm0.load_data(file_name=file_name, load_all=True)

# INDICATORS:

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
    MA = 0
    for t in range(P):
        MA += tp(ts, time - t)
    return MA/P


def MD(ts, time):
    MD = 0
    for t in range(P):
        MD += abs(tp(ts, time - t) - MA(ts, time - t))
    return MD/P


def CCI(ts, time):
    return (tp(ts, time) - MA(ts, time)) / (0.015 * MD(ts, time))
