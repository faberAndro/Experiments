"""
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


def plot_regression(r_array: list):
    for p in r_array:
        plt.plot((p[0][0], p[1][0]), (p[0][1], p[1][1]), c='red')


def compute_regression_extrema_directions(r):
    directions = []
    for points in r:
        x1, y1, x2, y2 = points[0][0], points[0][1], points[1][0], points[1][1]
        directions.append(np.sign((y2 - y1)/(x2 - x1)).astype(int))
    return directions


def zig_zag_test(y_test_directions):
    """

    :param y_test_directions:
    :return: True if the sequence of directions is a perfect zigzag
    """
    shifted_directions = np.roll(y_test_directions, -1)
    test = (y_test_directions + shifted_directions)[:-1]
    monotone_indexes = np.where(test != 0) + np.array(1)
    return not monotone_indexes.any()


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

    # REMOVING THE POINTS LESS THAN 'ORDER/2' CLOSE (EXAMPLE: IF ORDER=14, REMOVE POINTS THAT ARE LESS THAN 7 DAYS CLOSER TO THE PREVIOUS ONES)
    neighbourhood = int(ORDER/2)
    close_positions = np.where(np.diff(x_mm) <= 7) + np.array(1)
    x_distant = np.delete(x_mm, close_positions)
    y_distant = np.delete(y_mm, close_positions)

    # ENSURING THERE IS A PERFECT ALTERNANCE IN UPHILLS AND DOWNHILLS
    # todo: x and y can be vectorised to a single array
    y_mm_directions = np.sign(np.diff(y_distant))
    shifted_array = np.roll(y_mm_directions, -1)
    zig_zag_test = (y_mm_directions + shifted_array)[:-1]           # the sum of N.2 consecutive y directions should always be 0, so in theory this array should be made only of zeros
    monotone_spots = np.where(zig_zag_test != 0) + np.array(1)      # these are the indexes (in natural numbers) of the monotone points
    zigzag_x_mm = np.delete(x_distant, monotone_spots)
    zigzag_y_mm = np.delete(y_distant, monotone_spots)

    # CONNECTING BETTER MAXIMA AND MINIMA, NOW ALSO OPTIMISED, THROUGH REGRESSION LINES
    # todo: get rid of oscillations shorted than 1 week, amending the better max and min arrays
    #  doing that will aslo ensure the  high-variability but static-on-the-average intervals captured can be still used for investment
    regression_extrema = []
    for m in range(len(zigzag_x_mm) - 1):
        regression_extrema.append(compute_regr(m, zigzag_x_mm, values))

    # PLOTTING THE RESULTS
    plt.plot(values, label='equity', c='blue', linestyle='--')
    plt.plot(y_ma_2b, c='red', label='moving av 2b')
    plt.scatter(minima, y_min, s=50, edgecolor='black', facecolor='none')
    plt.scatter(maxima, y_max, s=50, edgecolor='red', facecolor='none')
    plt.scatter(better_minima, better_y_min, s=50, edgecolor='none', facecolor='green')
    plt.scatter(better_maxima, better_y_max, s=50, edgecolor='none', facecolor='grey')
    plt.plot(x_mm, y_mm, c='green')
    plt.plot(zigzag_x_mm, zigzag_y_mm, c='orange')
    plot_regression(regression_extrema)
    plt.grid(True)
    plt.legend()
    plt.show()

# todo: refactor to work with pandas series rather than numpy?
