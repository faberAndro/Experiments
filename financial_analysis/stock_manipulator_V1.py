"""
WORK IN PROGRESS!!

This V1 file introduces an enhanced feature:
a step-function generator based on partial linear regression.
This replaces the one in V0, based instead on a simple rel max and min connection.
Also, it attempts to use a new moving average rather than the V0 trend line.
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from stock_loader import load_equity
import stock_manipulator_V0 as Smo

plot_regressions = True


# ALTERNATIVE: use pandas rolling functions
def moving_average(xa, order):
    """

    :param xa: array of values from the timeseries
    :param order: order of the moving averages (= number of previous days it's computed over)
    :return: a numpy array of the moving average
    """
    return np.convolve(xa, np.ones(order), 'valid') / order


def regression_edges(f: np.array) -> (tuple, tuple):
    n = len(f)
    x = list(range(n))
    r = stats.linregress(x, f)
    return (0, r.intercept), (n-1, r.intercept + r.slope*(n-1))


def compute_regr(m: int, mm: np.array, y: np.array) -> (np.array, np.array):
    value_chunk = y[mm[m]: mm[m+1] + 1]
    p0, p1 = regression_edges(f=value_chunk)
    return np.array([p0[0] + mm[m], p0[1]]), np.array([p1[0] + mm[m], p1[1]])


if __name__ == '__main__':
    # TESTING A 'CASCADE' MOVING AVERAGE:
    ORDER = 14
    equity = load_equity(source='MTD', equity_acronym='A')
    values = equity.Close.to_numpy()
    y_ma_1 = moving_average(values, ORDER)
    y_ma_1 = np.append(np.zeros(ORDER-1), y_ma_1)     # shifts the ma forward, to superpose better the data
    y_ma_2 = moving_average(y_ma_1, ORDER+1)            # cascade moving average
    y_ma_2b = moving_average(y_ma_1, ORDER)            # cascade moving average
    # FINDING MAXIMA AND MINIMA ONTO THE SMOOTHED FUNCTION:
    minima, maxima = Smo.find_local_max_and_min(y_ma_2b)
    y_max = y_ma_2b.take(maxima)
    y_min = y_ma_2b.take(minima)

    # SEARCH FOR THE BETTER FIT OF THE REAL FUNCTION MAX AND MIN, IN THE NEIGHBORHOOD OF THE SMOOTHED MAX AND MIN
    span = int(ORDER/2)
    better_minima, better_maxima = [], []
    for m in minima[0]:
        neighbourhood = np.arange(max(m-span, 0), min(m+span, len(values)))
        y_interval = values.take(neighbourhood)
        x_real_min = y_interval.argmin()
        y_real_min = y_interval[x_real_min]
        better_minima.append(neighbourhood[x_real_min])
    better_y_min = values.take(better_minima)
    for m in maxima[0]:
        neighbourhood = np.arange(max(m-span, 0), min(m+span, len(values)))
        y_interval = values.take(neighbourhood)
        x_real_max = y_interval.argmax()
        y_real_max = y_interval[x_real_max]
        better_maxima.append(neighbourhood[x_real_max])
    better_y_max = values.take(better_maxima)

    # CONNECTING SIMPLY BETTER MAXIMA AND MINIMA
    x_mm = np.sort(np.concatenate((np.array([ORDER-1]), better_minima, better_maxima)), axis=0)     # reordering maxima and minima:
    y_mm = values.take(x_mm)

    # CONNECTING BETTER MAXIMA AND MINIMA THROUGH REGRESSION LINES
    # todo: get rid of oscillations shorted than 1 week, amending the better max and min arrays
    #  doing that will aslo ensure the  high-variability but static-on-the-average intervals captured can be still used for investment
    regression_extrema = []
    for m in range(len(x_mm) - 1):
        regression_extrema.append(compute_regr(m, x_mm, values))

    def plot_regression(r_array: list):
        for p in r_array:
            plt.plot((p[0][0], p[1][0]), (p[0][1], p[1][1]), c='red')

    # PLOTTING THE RESULTS
    plt.plot(values, label='equity', c='blue', linestyle='--')
    plt.plot(y_ma_2b, c='red', label='moving av 2b')
    plt.scatter(maxima, y_max, s=50, edgecolor='red', facecolor='none')
    plt.scatter(minima, y_min, s=50, edgecolor='black', facecolor='none')
    plt.scatter(better_minima, better_y_min, s=50, edgecolor='none', facecolor='green')
    plt.scatter(better_maxima, better_y_max, s=50, edgecolor='none', facecolor='grey')
    plt.plot(x_mm, y_mm, c='green')
    plot_regression(regression_extrema)
    plt.grid(True)
    plt.legend()
    plt.show()

# todo: refactor to work with pandas series rather than numpy?
