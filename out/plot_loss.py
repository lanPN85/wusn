import sys
import os
import numpy as np
import matplotlib.pyplot as plt


def parse_table(path):
    with open(path, 'rt') as f:
        stats = {}
        mode = 0
        for line in f:
            line = line.strip()
            if mode == 0:
                if line == '':
                    mode = 1
                else:
                    line = line.replace('\\\\', '')\
                        .replace('\\hline', '').strip()
                    cols = line.split('&')
                    test_name = cols[0].strip()
                    if test_name not in stats.keys():
                        stats[test_name] = {}

                    stats[test_name]['YHB'] = float(cols[1].strip())
                    stats[test_name]['k-LU + MXF-LB'] = float(cols[5].strip())
                    try:
                        stats[test_name]['OPT'] = float(cols[7].strip())
                    except ValueError:
                        stats[test_name]['OPT'] = None
                        pass
                    stats[test_name]['LB'] = float(cols[8].strip())
            elif mode == 1:
                line = line.replace('\\\\', '') \
                    .replace('\\hline', '').strip()
                cols = line.split('&')
                test_name = cols[0].strip()
                stats[test_name]['MXFGA'] = float(cols[5].strip())

        return stats


GRAPH_GAP = 30


def linearize(stats, key_list, inner_key):
    x, y = [], []
    for i, k in enumerate(key_list):
        if stats[k][inner_key] is not None:
            x.append(i * GRAPH_GAP + 10)
            y.append(stats[k][inner_key])
    return x, y


def plot(stats, path):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.set_xlabel('Test case')
    ax.set_ylabel('Average loss value')

    key_list = sorted(list(stats.keys()))
    ticks = np.linspace(10, len(key_list) * GRAPH_GAP + 10, len(key_list))
    ax.set_xticks(ticks)
    # ax.set_xticklabels(key_list)
    ax.set_xticklabels([''] * len(key_list))
    ax.set_xlim(0, len(key_list) * GRAPH_GAP + 10)

    # inner_keys = ['YHB', 'k-LU + MXF-LB', 'OPT', 'LB', 'MXFGA']
    # colors = ['orangered', 'mediumslateblue', 'darkslategrey', 'maroon', 'k']
    inner_keys = ['YHB', 'k-LU + MXF-LB', 'LB', 'MXFGA']
    colors = ['orangered', 'k', 'mediumslateblue', 'maroon']

    for ik, cl in zip(inner_keys, colors):
        ax.plot(*linearize(stats, key_list, ik), '-', color=cl, label=ik)

    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=2,
              ncol=2, borderaxespad=0.)
    plt.savefig(path, dpi=800)


if __name__ == '__main__':
    ROOT_DIR = '.'
    TXT_FILE = sys.argv[1]
    OUT_FILE = sys.argv[2]

    stats_ = parse_table(TXT_FILE)
    plot(stats_, OUT_FILE)

