import sys
import os
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import spline
# noinspection PyUnresolvedReferences
from analyze_log import read_stats, read_yuan_stats


def get_scenario(path):
    fname = os.path.split(path)[-1]
    tname = fname.split('.')[0]
    return tname.split('-')[0]


def merge_stats(stats, keys=('min_loss', 'avg_loss', 'std_loss')):
    nstats = {}
    for k, v in stats.items():
        sc = get_scenario(k)
        if sc not in nstats.keys():
            nstats[sc] = {}
        for ky in keys:
            if ky not in nstats[sc].keys():
                nstats[sc][ky] = []
            nstats[sc][ky].append(v[ky])

    keys_ = list(nstats.keys())
    for k in keys_:
        for ky in keys:
            nstats[k][ky] = np.mean(nstats[k][ky])

    return nstats


def plot(stats, out_path):
    # print(stats)

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

    hd = [None] * len(NAMES)
    for k, name in enumerate(NAMES):
        for i, sc in enumerate(SCENARIOS):
            y = []
            for j, s in enumerate(SETS):
                y.append(stats[COLS[k]][s][sc]['avg_time'])
            # ys = spline(x, y, xs)
            hd[k], = ax.plot(x, y, color=COLORS[i], linestyle=STYLES[k],
                    label='%s' % (NAMES[k],))
            ax.scatter(x, y, color=COLORS[i])

    ax.legend(hd, NAMES)
    plt.savefig(out_path, dpi=800)


if __name__ == '__main__':
    ROOT_DIR = '.'
    SETS = ['small', 'medium', 'full']
    COLS = ('kmxf', 'mxf_k')

    STYLES = ['-', '--']
    NAMES = ['k-LURNS + MXF-LBSNA', 'MXFGA']
    COLORS = ['k', 'midnightblue', 'darkgray', 'darkorange', 'indigo', 'brown', 'slategrey']
    SCENARIOS = ('br', 'cer', 'fcr', 'mcr', 'rfc', 'rmc', 'rr')
    ALL_STATS = {}

    for col in COLS:
        odir = os.path.join(ROOT_DIR, col)
        ALL_STATS[col] = {}
        for st in SETS:
            sdir = os.path.join(odir, st)
            stats_ = read_stats(os.path.join(sdir, 'log.txt'))
            ALL_STATS[col][st] = merge_stats(stats_, keys=('avg_time',))

    plot(ALL_STATS, 'runtime.png')
