"""
WORK IN PROGRESS!!

This V1 file introduces an enhanced feature:
a step-function generator based on partial linear regression.
This replaces the one in V0, based instead on a simple rel max and min connection.
Also, it attempts to use a new moving average rather than the V0 trend line.
"""
from . import stock_manipulator_V0 as sa
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plot_regressions = True


def moving_average(xa, w):
    return np.convolve(xa, np.ones(w), 'valid') / w


def make_step_function(serie_x, serie_y, day_interval):
    # compute linear regression segments?
    # divide initial series in N/M intervals of M days?
    edges = []
    m_giorni = len(serie_x) // day_interval + 1
    x_chunks = np.array_split(serie_x, m_giorni)
    y_chunks = np.array_split(serie_y, m_giorni)
    for i in range(m_giorni):
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_chunks[i], y_chunks[i])
        x1, x2 = x_chunks[i][0], x_chunks[i][-1]
        y1, y2 = intercept + slope*x1, intercept + slope*x2
        edges.append(((x1, x2), (y1, y2)))
    # finally, plot x_arr vs. y_all_regression on top of the original graph.
    # try to vectorise
    return edges


if __name__ == '__main__':
    # previously explored what happens changing the number of days (n_days) when building the trend.
    y_ma_1 = moving_average(y, 2)
    plt.plot(x[:-1], y_ma_1, c='red', label='moving av 1', linestyle='-.')
    # y_ma_2 = moving_average(y_ma_1, 2)            # cascade moving average
    # plt.plot(x[:-2], y_ma_2, c='orange', label='moving av 2')
    minimi, massimi = find_local_max_and_min(y_ma_1)
    if False:
        filtered_x_max = [x[0]]
        min_dist = 15
        taken_x = filtered_x_max[0]
        for i in range(1, len(massimi[0])):
            try:
                if massimi[0][i] - taken_x >= min_dist:
                    filtered_x_max.append(massimi[0][i])
                    taken_x = massimi[0][i]
            except IndexError:
                print(i, len(massimi[0]))
        plt.plot(filtered_x_max, y[filtered_x_max], c='green')
    plt.plot(massimi[0], y_ma_1[massimi], c='purple')
    plt.plot(minimi[0], y_ma_1[minimi], c='green')
    xt = np.arange(x[0], x[-1] + thick_interval, thick_interval)
    plt.grid(which='both', axis='both')
    plt.xticks(xt, rotation=90)
    plt.legend()
    plt.show()
    if False:
        intervallo = 60
        peso = 5
        spezzate = crea_spezzate(x, y, day_interval=intervallo)
        n_spezzate = len(spezzate)
        for spezzata in spezzate:
            x_su_spezzata = np.arange(spezzata[0][0], spezzata[0][1])
            y_su_spezzata = y[spezzata[0][0]: spezzata[0][1]]
            andamento_su_spezzata, delta_1 = trend_with_exp_weighted_av(y_su_spezzata, n_giorni=5)
            flex_bottom, flex_top = find_local_max_and_min(andamento_su_spezzata)

            plt.plot(delta_1 + x_su_spezzata, andamento_su_spezzata[:-delta_1], c='red')
            plt.plot(spezzata[0], spezzata[1], c='green')
            # plt.scatter(x_su_spezzata[0] + flex_at_min, y_su_spezzata[flex_at_min], s=1000, c='green', marker='_')
            # plt.scatter(x_su_spezzata[0] + flex_at_max, y_su_spezzata[flex_at_max], s=1000, c='red', marker='_')

        plot_analysis()                                                             # plot
# INDIRIZZARE CON IN NUMERI NATURALI E KEEP ONLY THE DATE EXTREMES IN EXTRACT DATA INTERVAL
