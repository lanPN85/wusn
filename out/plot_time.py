import sys
import os
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import spline
# noinspection PyUnresolvedReferences
from analyze_log import read_stats, read_yuan_stats


def extract_avg(stats, key='avg_time'):
    values = []
    for k, v in stats.items():
        values.append(v[key])
    return np.mean(values)


def plot(stats, out_path):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Dataset Size')
    ax.set_ylabel('Average Runtime (s)')

    x = [40*40, 100*100, 200*200]
    xs = np.linspace(40 * 40, 200 * 200, 300)
    ax.set_xticks(x)
    ax.set_xticklabels(['Small set', 'Medium set', 'Full set'])
    # targs = dict(verticalalignment='bottom')
    # ax.text(40*40, 0, 'Small set', **targs)
    # ax.text(100*100, 0, 'Medium set', **targs)
    # ax.text(200*200, 0, 'Full set', **targs)

    for color, name, cl in zip(COLORS, NAMES, COLS):
        y = stats[cl]
        ys = spline(x, y, xs)
        ax.plot(x, y, color=color, label=name)
        ax.scatter(x, y, color=color)

    ax.legend()
    plt.savefig(out_path, dpi=800)


if __name__ == '__main__':
    ROOT_DIR = '.'
    SETS = ['small', 'medium', 'full']
    COLS = ('yuan', 'kmxf', 'mxf_k')
    # COLS = ['yuan', 'kmxf']

    COLORS = ['orangered', 'mediumslateblue', 'darkslategrey']
    NAMES = ['Yuan\'s heuristics', 'k-LURNS + MXF-LBSNA', 'MXFGA']

    SCENARIOS = ('br', 'cer', 'fcr', 'mcr', 'rfc', 'rmc', 'rr')
    ALL_STATS = {}

    if 'yuan' in COLS:
        odir = os.path.join(ROOT_DIR, 'yuan', 'best')
        ALL_STATS['yuan'] = []
        for st in SETS:
            sdir = os.path.join(odir, st)
            stats_ = read_yuan_stats(os.path.join(sdir, 'log.txt'))
            ALL_STATS['yuan'].append(extract_avg(stats_, key='time'))

    for col in COLS[1:]:
        odir = os.path.join(ROOT_DIR, col)
        ALL_STATS[col] = []
        for st in SETS:
            sdir = os.path.join(odir, st)
            stats_ = read_stats(os.path.join(sdir, 'log.txt'))
            ALL_STATS[col].append(extract_avg(stats_))

    plot(ALL_STATS, 'runtime.png')
