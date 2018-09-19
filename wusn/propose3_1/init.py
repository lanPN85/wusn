from sklearn.cluster import KMeans
from tqdm import tqdm

import numpy as np
import sys

from wusn.commons import WusnInput, WusnOutput, Point
from wusn.propose3_1.model import Individual


def random_init(inp: WusnInput, pop_size):
    pop = []
    print('Creating population...')
    for _ in tqdm(range(pop_size), file=sys.stdout):
        indv = Individual([0] * len(inp.relays))
        for _ in range(inp.relay_num):
            alist = np.where(np.asarray(indv) == 0)[0]
            ai = np.random.choice(alist)
            indv[ai] = 1
        pop.append(indv)
    return pop


def kmeans_greedy_init(inp: WusnInput, pop_size):
    pop = []
    print('Creating population...')
    for _ in tqdm(range(pop_size), file=sys.stdout):
        pop.append(kmeans_greedy(inp))

    return pop


# noinspection PyTypeChecker
def kmeans_greedy(inp: WusnInput, km_runs=1):
    X = list(map(lambda s: [s.x, s.y], inp.sensors))
    X = np.asarray(X)

    km = KMeans(n_clusters=inp.relay_num, n_init=km_runs, max_iter=3500, verbose=0)
    km.fit(X)

    clusters = [[] for _ in range(inp.relay_num)]
    for i, c in enumerate(km.labels_):
        clusters[c].append(inp.sensors[i])

    # Greedily choose a relay for each cluster
    current_relays = inp.relays.copy()
    relay_to_sensors = {}
    selected = []

    for cl in clusters:
        best_rn = None
        best_loss = float('inf')
        for rn in current_relays:
            max_loss = -float('inf')
            for sn in cl:
                ls = inp.loss[(sn, rn)]
                if ls > max_loss:
                    max_loss = ls
            if max_loss < best_loss:
                best_loss = max_loss
                best_rn = rn

        current_relays.remove(best_rn)
        selected.append(best_rn)
        relay_to_sensors[best_rn] = cl

    # indv = Individual(selected)
    indv = Individual()
    for rn in inp.relays:
        if rn in selected:
            indv.append(1)
        else:
            indv.append(0)

    return indv

