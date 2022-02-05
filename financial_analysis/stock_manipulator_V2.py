"""
This V2 file refactors the V1 into a class, with clearer methods and properties to use:
"""
import numpy as np
from matplotlib import pyplot as plt
from financial_analysis.stock_loader import load_equity
from financial_analysis.stock_manipulator_V1 import moving_average


class Equity:
    def __init__(self, source, equity_acronym):
        # todo: provide the possibility to have a dictionary of series smoothed to different orders
        self.ORDER = 14
        self.source = source
        self.equity_acronym = equity_acronym
        self.timeseries = load_equity(source=self.source,
                                      equity_acronym=self.equity_acronym)
        # self.timeseries = self.timeseries.assign(history=self.timeseries.Close)   # this can be another option
        self.timeseries = self.timeseries.assign(history=(self.timeseries.High + self.timeseries.Low)/2)
        mav_l1 = moving_average(self.timeseries.history.values, self.ORDER)
        mav_l1 = np.append(np.zeros(self.ORDER - 1), mav_l1)
        mav_l2 = moving_average(mav_l1, self.ORDER)
        self.timeseries = self.timeseries.assign(smoothed=np.append(mav_l2, np.zeros(self.ORDER - 1)))
        # IMPORTANT: smoothing and all calcs are to be done ignoring dates, but with consecutive values only
        # FINDING NOW MAX AND MIN

if __name__ == '__main__':
    equity_1 = Equity(source='MTD', equity_acronym='A')
    plt.figure()
    # equity_1.timeseries.history.plot()
    equity_1.timeseries.smoothed.plot()
    plt.figure()
    plt.plot(equity_1.timeseries.smoothed.values)
