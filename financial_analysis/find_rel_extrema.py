# coding=utf-8
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
import numpy as np


def smoothing():
    pass


def find_rel_extrema(f):
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
    plt.plot(x, y)
    if use_circles_for_identification:
        plt.scatter(maxmin['local_flex_minus'], y.take(maxmin['local_flex_minus']))
        plt.scatter(maxmin['local_flex_major'], y.take(maxmin['local_flex_major']))
    plt.plot(maxmin['peaks_min'], y[maxmin['peaks_min']], "_")
    # plt.plot(maxmin['peaks_max'], y[maxmin['peaks_max']], "_")
    plt.show()


if __name__ == '__main__':
    test_sin = False
    test_random = True

    N = 10000
    x = np.arange(0, N, 1)

    if test_sin:
        # test with sinusoidal increasing function
        y = x * np.sin(x * np.pi / 180)
    elif test_random:
        # test with random smooth function
        r = np.random.randn(N)
        y = np.cumsum(r)
    else:
        y = x
    stats = find_rel_extrema(y)
    plot_rel_extrema(stats, use_circles_for_identification=False)
