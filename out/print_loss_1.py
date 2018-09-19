import sys
import os
import numpy as np

# noinspection PyUnresolvedReferences
from analyze_log import read_stats, read_yuan_stats


def get_scenario(path):
    fname = os.path.split(path)[-1]
    tname = fname.split('.')[0]
    return tname.split('-')[0]


def merge_stats(stats, keys=('avg_loss', 'min_loss')):
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


def print_stats(stats):
    for i, sc in enumerate(SCENARIOS):
        row = '& %s' % sc
        row += ' & %.2f' % stats['yuan'][sc]['loss']
        for col in COLS[1:-1]:
            row += ' & %.2f' % stats[col][sc]['min_loss']

        for pr in PRIORITY:
            row += ' & %.2f' % stats[COLS[-1]][sc][pr]

        lne = '' if i < len(SCENARIOS) - 1 \
            else '\\hline'
        # else '\Xhline{3\\arrayrulewidth}'
        row += ' \\\\ %s' % lne
        print(row)


if __name__ == '__main__':
    ROOT_DIR = '.'
    SET = sys.argv[1]
    COLS = ('yuan', 'hxf/lu1', 'hxf/lu2', 'kmxf')

    SCENARIOS = ('br', 'cer', 'fcr', 'mcr', 'rfc', 'rmc', 'rr')
    PRIORITY = ('min_loss', 'avg_loss')

    ALL_STATS = {}

    # Get Yuan stats
    if 'yuan' in COLS:
        odir = os.path.join(ROOT_DIR, 'yuan', 'best')
        sdir = os.path.join(odir, SET)
        stats_ = read_yuan_stats(os.path.join(sdir, 'log.txt'))
        ALL_STATS['yuan'] = merge_stats(stats_, keys=('loss',))

    # Get remaining stats
    for cl in COLS[1:]:
        odir = os.path.join(ROOT_DIR, cl)
        sdir = os.path.join(odir, SET)
        stats_ = read_stats(os.path.join(sdir, 'log.txt'))
        ALL_STATS[cl] = merge_stats(stats_)

    print_stats(ALL_STATS)

