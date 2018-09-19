import sys
import os
import numpy as np

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


def print_stats(stats, olb):
    for i, sc in enumerate(SCENARIOS):
        row = '& %s' % sc
        # row += ' & %.2f' % stats['yuan'][sc]['loss']
        for col in COLS:
            for pr in PRIORITY:
                row += ' & %.2f' % stats[col][sc][pr]
        row += ' & %.2f' % olb[sc]

        lne = '' if i < len(SCENARIOS) - 1 \
            else '\\hline'
        # else '\Xhline{3\\arrayrulewidth}'
        row += ' \\\\ %s' % lne
        print(row)


if __name__ == '__main__':
    ROOT_DIR = '.'
    SET = sys.argv[1]
    COLS = ('kmxf', 'mxf_k')
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
    # SCENARIOS = ('br', 'cer', 'fcr', 'mcr', 'rmc', 'rr')
    PRIORITY = ('min_loss', 'avg_loss', 'std_loss')

    ALL_STATS = {}

    # Get remaining stats
    for cl in COLS:
        odir = os.path.join(ROOT_DIR, cl)
        sdir = os.path.join(odir, SET)
        stats_ = read_stats(os.path.join(sdir, 'log.txt'))
        ALL_STATS[cl] = merge_stats(stats_)

    print_stats(ALL_STATS, OLB[SET])
