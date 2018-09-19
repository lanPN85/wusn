from typing import Dict, List, Any, Union

import sys
import re
import os
import numpy as np


def read_yuan_stats(logf):
    stats = {}

    current_t = ''
    with open(logf, 'rt') as f:
        for ln in f:
            if ln.startswith('File'):
                current_t = ln.split(' ')[-1].strip()
                current_t = os.path.split(current_t)[-1]

                stats[current_t] = {
                    'time': 0,
                    'loss': 0
                }
            elif ln.startswith('Best loss'):
                stats[current_t]['loss'] = float(ln.split(' ')[-1].strip())
            elif ln.startswith('Total running time'):
                stats[current_t]['time'] = float(ln.split(' ')[-1].strip()[:-2]) / 1000.
    return stats


def read_stats(file):
    stats = {}

    with open(file, 'rt') as f:
        lines = f.readlines()
        current_test = None

        # Gather time and losses
        for ln in lines:
            if ln.startswith('File: '):
                current_test = ln.split(': ')[-1].strip()
                current_test = os.path.split(current_test)[-1]
                if current_test not in stats.keys():
                    stats[current_test] = {
                        'times': [],
                        'losses': []
                    }
            elif ln.startswith('Elapsed time: '):
                time = float(ln.split(': ')[-1].strip()[:-3]) / 1000
                stats[current_test]['times'].append(time)
            elif ln.startswith('Max loss: '):
                loss = float(ln.split(': ')[-1].strip())
                stats[current_test]['losses'].append(loss)

        # Calculate metrics
        for test, values in stats.items():
            stats[test]['avg_time'] = np.mean(values['times'])
            stats[test]['min_time'] = min(values['times'])
            stats[test]['max_time'] = max(values['times'])
            stats[test]['avg_loss'] = np.mean(values['losses'])
            stats[test]['min_loss'] = min(values['losses'])
            stats[test]['max_loss'] = max(values['losses'])
            stats[test]['std_loss'] = np.std(values['losses'])
    return stats


def read_opts(file):
    opts = {}
    with open(file, 'rt') as f:
        for line in f:
            try:
                line = line.strip()
                val = float(line.split(': ')[-1])
                test = re.search('\[.*\]', line).group()[1:-1]
                opts[test] = val
            except Exception as e:
                continue
    return opts


if __name__ == '__main__':
    TARGET_FILE = sys.argv[1]

    stats_ = read_stats(TARGET_FILE)
    kv = sorted(list(stats_.items()), key=lambda x: x[0])

    for k, v in kv:  # type: (str, Dict[str, Union[List, Any], float])
        print('[%s]' % k)
        print(' Runs: %d' % len(v['times']))
        print(' Avg time: %.4fms (%.2fs)' % (v['avg_time'], v['avg_time'] / 1000.))
        print(' Min time: %.4fms (%.2fs)' % (v['min_time'], v['min_time'] / 1000.))
        print(' Max time: %.4fms (%.2fs)' % (v['max_time'], v['max_time'] / 1000.))
        print(' Avg loss: %.4f' % (v['avg_loss']))
        print(' Min loss: %.4f' % (v['min_loss']))
        print(' Max loss: %.4f' % (v['max_loss']))
        print(' Loss StdDev: %.4f' % (v['std_loss']))
