"""
This moudule tests a first rel. maxima and minima discovery performed on a time-series
"""

import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
import numpy as np


def smoothing():
    pass


def find_rel_extrema(f: np.array) -> dict:

    local_flex_minus_ = argrelextrema(f, np.less)
    local_flex_major_ = argrelextrema(f, np.greater)
    peaks_max_, _ = find_peaks(f, height=0)
    peaks_min_, _ = find_peaks(-f + max(f), height=0)
    result = {'local_flex_minus': local_flex_minus_,
              'local_flex_major': local_flex_major_,
              'peaks_min': peaks_min_,
              'peaks_max': peaks_max_}
    return result


def plot_rel_extrema(maxmin: dict, use_circles_for_identification=True):

    if use_circles_for_identification:
        plt.scatter(maxmin['local_flex_minus'], y.take(maxmin['local_flex_minus']))
        plt.scatter(maxmin['local_flex_major'], y.take(maxmin['local_flex_major']))
    plt.plot(maxmin['peaks_min'], y[maxmin['peaks_min']], "_")
    # plt.plot(maxmin['peaks_max'], y[maxmin['peaks_max']], "_")


if __name__ == '__main__':

    # GENERATES SAMPLE FUNCTIONS
    test_sin = False
    test_random = True
    N = 10000
    x = np.arange(0, N, 1)
    # test with sinusoidal increasing function
    if test_sin:
        y = x * np.sin(x * np.pi / 180)
    # test with random smooth function
    elif test_random:
        r = np.random.randn(N)
        y = np.cumsum(r)
    else:
        y = x

    # FINDS REL. EXTREMA
    extrema = find_rel_extrema(y)

    # PLOTS RESULTS
    plt.plot(x, y)
    plot_rel_extrema(extrema, use_circles_for_identification=False)
    plt.show()
