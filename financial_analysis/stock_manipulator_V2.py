"""
This V2 file refactors the V1 into a class, with clearer methods and properties to use:
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from financial_analysis.stock_loader import load_equity
from financial_analysis.stock_manipulator_V1 import moving_average, compute_regr, plot_regression
import financial_analysis.stock_manipulator_V0 as Smo


class Equity:
    def __init__(self, source, equity_acronym):
        # todo: provide the possibility to have a dictionary of series smoothed to different orders
        self.ORDER = 14
        self.source = source
        self.equity_acronym = equity_acronym
        self.timeseries = load_equity(source=self.source,
                                      equity_acronym=self.equity_acronym)
        # self.timeseries = self.timeseries.assign(history=self.timeseries.Close)   # this can be another option
        self.timeseries = self.timeseries.assign(History=(self.timeseries.High + self.timeseries.Low)/2)
        
        # SMOOTHING
        mav_l1 = moving_average(self.timeseries.History.values, self.ORDER)
        mav_l1 = np.append(np.zeros(self.ORDER - 1), mav_l1)
        mav_l2 = moving_average(mav_l1, self.ORDER)
        self.timeseries = self.timeseries.assign(Smoothed=np.append(mav_l2, np.zeros(self.ORDER - 1)))
        # IMPORTANT: smoothing and all calcs are to be done ignoring dates, but with consecutive values only
        # Cutting now head and tail of ORDER-size, as they are not properly captured by the smoothing algo
        self.analysis = self.timeseries.iloc[self.ORDER: -self.ORDER-1][
            ['Date', 'Volume', 'History', 'Smoothed']].reset_index(drop=True)
        
        # FINDING NOW LOCAL MAX AND MIN
        smoothed_array = self.analysis.Smoothed.values
        x_minima, x_maxima = Smo.find_local_max_and_min(smoothed_array)
        y_minima, y_maxima = smoothed_array.take(x_minima), smoothed_array.take(x_maxima)
        
        # CORRECTING LOCAL MAX AND MIN WITH BETTER NEIGHBOURS
        real_values = self.analysis.History
        span = int(self.ORDER / 2)
        adjusted_minima, adjusted_maxima = [], []
        for m in x_minima[0]:
            neighbourhood = np.arange(max(m - span, 0), min(m + span, len(real_values)))
            y_interval = real_values.take(neighbourhood)
            x_real_min = y_interval.argmin()
            # y_real_min = y_interval[x_real_min]
            adjusted_minima.append(neighbourhood[x_real_min])
        # adjusted_y_min = real_values.take(adjusted_minima)
        for m in x_maxima[0]:
            neighbourhood = np.arange(max(m - span, 0), min(m + span, len(real_values)))
            y_interval = real_values.take(neighbourhood)
            x_real_max = y_interval.argmax()
            # y_real_max = y_interval[x_real_max]
            adjusted_maxima.append(neighbourhood[x_real_max])
        # adjusted_y_max = real_values.take(adjusted_maxima)
        
        # MERGING TO ONE ARRAY ALL LOCAL ADJUSTED MAX AND MIN
        x_mm = np.sort(np.concatenate((adjusted_minima, adjusted_maxima),
                       axis=0))  # reordering maxima and minima
        y_mm = real_values.take(x_mm)

        # REMOVING THE POINTS LESS THAN 'ORDER/2' CLOSE (EXAMPLE: IF ORDER=14, REMOVE POINTS THAT ARE LESS THAN 7 DAYS CLOSER TO THE PREVIOUS ONES)
        neighbourhood = int(self.ORDER / 2)
        close_positions = np.where(np.diff(x_mm) <= neighbourhood) + np.array(1)
        x_distant = np.delete(x_mm, close_positions)
        y_distant = real_values.take(x_distant)

        # ENSURING THERE IS A PERFECT ALTERNANCE IN UPHILLS AND DOWNHILLS
        # todo: x and y can be vectorised to a single array
        y_mm_directions = np.sign(np.diff(y_distant))
        shifted_array = np.roll(y_mm_directions, -1)
        zig_zag_test = (y_mm_directions + shifted_array)[
                       :-1]  # the sum of N.2 consecutive y directions should always be 0, so in theory this array should be made only of zeros
        monotone_spots = np.where(zig_zag_test != 0) + np.array(1)  # these are the indexes (in natural numbers) of the monotone points
        zigzag_x_mm = np.delete(x_distant, monotone_spots)
        zigzag_y_mm = real_values.take(zigzag_x_mm)
        self.local_extrema = pd.DataFrame({'y': zigzag_y_mm}, index=zigzag_x_mm)

        # COMPUTING REGRESSION LINES FROM OPTIMISED MAXIMA AND MINIMA
        regression_points = []
        for m in range(len(zigzag_x_mm) - 1):
            regression_points.append(compute_regr(m, zigzag_x_mm, real_values))
        self.regression_lines = regression_points


if __name__ == '__main__':
    # CALLING THE CONSTRUCTOR
    equity_1 = Equity(source='MTD', equity_acronym='A')

    # PLOTTING RESULTS
    ax0 = plt.gca()
    equity_1.analysis.History.plot(ax=ax0)
    plot_regression(equity_1.regression_lines, ax=ax0)

    # ax = plt.gca()
    # equity_1.analysis.Smoothed.plot(ax=ax)
    # equity_1.local_extrema.plot(ax=ax, color='red')
    # plot_regression(equity_1.regression_lines, ax=ax)
