import os
import sys

import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import spline
# noinspection PyUnresolvedReferences
from analyze_log import read_stats, read_yuan_stats


def get_scenario(path):
    fname = os.path.split(path)[-1]
    tname = fname.split('.')[0]
    return tname.split('-')[0]


def merge_stats(stats, keys=('avg_loss',)):
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


def plot(stats, olb, out_path):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Dataset Size')
    ax.set_ylabel('Average %OPT (%LB)')
    ax.set_ylim(0, 70)

    x = np.asarray([4000, 9000, 14000])
    x += 30
    ax.set_xticks(x)
    ax.set_xticklabels(['Small set', 'Medium set', 'Full set'])

    WIDTH = 500

    for i, sc in enumerate(SCENARIOS):
        pcs = []
        for j, s in enumerate(SETS):
            ls = stats[s][sc]['avg_loss']
            opt = olb[s][sc]
            pc = (ls - opt) / opt * 100
            pcs.append(pc)
        pos = x - (3 - i) * WIDTH
        ax.bar(pos, pcs, WIDTH, color=COLORS[i], label=sc, edgecolor='k')
        # for p, v in zip(pos, pcs):
        #     ax.text(p - WIDTH, v + 1, '%.2f' % v, size='smaller')

    ax.legend(loc='upper left')
    plt.savefig(out_path, dpi=600)


if __name__ == '__main__':
    ROOT_DIR = '.'
    SETS = ['small', 'medium', 'full']
    # COLS = ('yuan', 'kmxf', 'mxf_k')
    COL = sys.argv[1]

    OLB = {
        'small': {
            'br': 90.92, 'cer': 70.71, 'fcr': 89.89,
            'mcr': 81.05, 'rfc': 89.29, 'rmc': 97.66,
            'rr': 86.00
        },
        'medium': {
            'br': 101.54, 'cer': 86.42, 'fcr': 103.34,
            'mcr': 104.36, 'rfc': 125.57, 'rmc': 110.28,
            'rr': 81.77
        },
        'full': {
            'br': 106.36, 'cer': 89.33, 'fcr': 102.56,
            'mcr': 96.79, 'rfc': 147.09, 'rmc': 132.61,
            'rr': 98.63
        }
    }

    SCENARIOS = ('br', 'cer', 'fcr', 'mcr', 'rfc', 'rmc', 'rr')
    # COLORS = ['lightcoral', 'dodgerblue', 'yellowgreen', 'gold', 'darkslategray', 'orangered', 'slateblue']
    # COLORS = ['gray', 'sienna', 'olive', 'k', 'lightslategray', 'maroon', 'indigo']
    COLORS = ['sienna', 'midnightblue', 'darkgray', 'khaki', 'darkolivegreen', 'brown', 'slategrey']
    ALL_STATS = {}

    odir = os.path.join(ROOT_DIR, COL)
    ALL_STATS[COL] = {}
    for st in SETS:
        sdir = os.path.join(odir, st)
        stats_ = read_stats(os.path.join(sdir, 'log.txt'))
        ALL_STATS[COL][st] = merge_stats(stats_)

    plot(ALL_STATS[COL], OLB, '%s_opt.png' % COL)
