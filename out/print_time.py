import sys
import os
import numpy as np

# noinspection PyUnresolvedReferences
from analyze_log import read_stats, read_yuan_stats


def get_scenario(path):
    fname = os.path.split(path)[-1]
    tname = fname.split('.')[0]
    return tname.split('-')[0]


def merge_stats(stats, key_name='avg_time'):
    nstats = {}
    for k, v in stats.items():
        sc = get_scenario(k)
        if sc not in nstats.keys():
            nstats[sc] = [v[key_name]]
        else:
            nstats[sc].append(v[key_name])

    keys = list(nstats.keys())
    for k in keys:
        nstats[k] = np.mean(nstats[k])

    return nstats


def print_stats(stats):
    for i, sc in enumerate(SCENARIOS):
        row = '& %s' % sc
        for col in COLS:
            row += ' & %.2f' % stats[col][sc]
        lne = '\cline{2-%d}' % len(SCENARIOS) if i < len(SCENARIOS) - 1 \
            else '\Xhline{3\\arrayrulewidth}'
        row += ' \\\\ %s' % lne
        print(row)


if __name__ == '__main__':
    ROOT_DIR = '.'
    SET = sys.argv[1]
    COLS = ('yuan', 'prop2', 'prop2-random', 'prop3_1', 'prop3_1-random')
    SCENARIOS = ('br', 'cer', 'fcr', 'mcr', 'rfc', 'rmc', 'rr')
    ALL_STATS = {}

    # Get Yuan stats
    odir = os.path.join(ROOT_DIR, 'yuan', 'best')
    sdir = os.path.join(odir, SET)
    stats_ = read_yuan_stats(os.path.join(sdir, 'log.txt'))
    ALL_STATS['yuan'] = merge_stats(stats_, key_name='time')

    # Get other stats
    for cl in COLS[1:]:
        odir = os.path.join(ROOT_DIR, cl)
        sdir = os.path.join(odir, SET)
        stats_ = read_stats(os.path.join(sdir, 'log.txt'))
        ALL_STATS[cl] = merge_stats(stats_)

    print_stats(ALL_STATS)
