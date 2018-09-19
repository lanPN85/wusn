import sys
import os
import numpy as np

# noinspection PyUnresolvedReferences
from analyze_log import read_stats, read_yuan_stats, read_opts


def get_scenario(path):
    fname = os.path.split(path)[-1]
    tname = fname.split('.')[0]
    return tname.split('-')[0]


def print_stats(stats, opts, lbs):
    for i, sc in enumerate(SCENARIOS):
        suffix = ['-001', '-002', '-003', '-004', '-005']
        ext = '.test'
        for j, sf in enumerate(suffix):
            test_name = sc + sf
            opt = opts.get(test_name, None)
            lb = lbs.get(test_name, None)
            opt = '%.2f' % opt if opt is not None else '-'
            lb = '%.2f' % lb if lb is not None else '-'
            row = '%s ' % test_name

            row += ' & %.2f' % stats['yuan'][test_name + ext]['loss']

            for col in COLS[1:-1]:
                row += ' & %.2f' % stats[col][test_name + ext]['min_loss']

            for pr in PRIORITY:
                row += '& %.2f ' % stats[COLS[-1]][test_name + ext][pr]
            row += '& %s & %s' % (opt, lb)
            line = '' if (j < len(suffix) - 1) else '\\hline'
            row += ' \\\\ %s ' % line
            print(row)


if __name__ == '__main__':
    ROOT_DIR = '.'
    SET = sys.argv[1]
    DATA_DIR = sys.argv[2]
    COLS = ('yuan', 'hxf/lu1', 'hxf/lu2', 'kmxf')

    SCENARIOS = ('br', 'fcr', 'mcr', 'rfc', 'rmc', 'rr')
    # SCENARIOS = ('br', 'cer', 'fcr', 'mcr', 'rmc', 'rr')
    PRIORITY = ('min_loss', 'avg_loss', 'std_loss')

    stats_ = {}

    # Get remaining stats
    for cl in COLS:
        if cl == 'yuan':
            odir = os.path.join(ROOT_DIR, 'yuan', 'best')
            sdir = os.path.join(odir, SET)
            stats_['yuan'] = read_yuan_stats(os.path.join(sdir, 'log.txt'))
        else:
            odir = os.path.join(ROOT_DIR, cl)
            sdir = os.path.join(odir, SET)
            stats_[cl] = read_stats(os.path.join(sdir, 'log.txt'))
    opts_ = read_opts(os.path.join(DATA_DIR, 'OPTIMAL'))
    lbs_ = read_opts(os.path.join(DATA_DIR, 'BOUND'))

    print_stats(stats_, opts_, lbs_)
