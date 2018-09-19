from sklearn.cluster import KMeans
from tqdm import tqdm

import numpy as np
import random
import sys

from wusn.commons import WusnInput, WusnOutput, Point
from wusn.yuan.lbsna import lbsna3
from wusn.propose2.model import Individual


def kmeans_random_init(inp: WusnInput, pop_size):
    pop = []
    print('Creating population...')
    for _ in tqdm(range(pop_size), file=sys.stdout):
        pop.append(kmeans_random(inp))

    return pop


# noinspection PyTypeChecker
def kmeans_random(inp: WusnInput):
    X = list(map(lambda s: [s.x, s.y], inp.sensors))
    X = np.asarray(X)

    km = KMeans(n_clusters=inp.relay_num, n_init=1, max_iter=3000, verbose=0)
    km.fit(X)

    clusters = [[] for _ in range(inp.relay_num)]
    pairs = [None] * inp.relay_num
    for i, c in enumerate(km.labels_):
        clusters[c].append(inp.sensors[i])
        centroid = Point(*km.cluster_centers_[c])
        pairs[c] = (clusters[c], centroid)

    selected = random.sample(inp.relays, inp.relay_num)
    indv = Individual(sensor_count=len(inp.sensors), relay_count=inp.relay_num)

    # Sort clusters by centroid distance to an anchor point
    anchor = Point(0., 0.)
    # print(list(map(lambda x: x[1].distance(anchor), pairs)))
    pairs.sort(key=lambda x: x[1].distance(anchor))
    # print(list(map(lambda x: x[1].distance(anchor), pairs)))
    clusters = list(map(lambda x: x[0], pairs))

    # Flatten clusters
    for cl in clusters:
        indv.extend(cl)
    indv.extend(selected)

    return indv


def random_init(inp: WusnInput, pop_size, **kwargs):
    pop = []
    print('Creating population...')
    for _ in tqdm(range(pop_size), file=sys.stdout):
        sensors = inp.sensors[:]
        random.shuffle(sensors)
        relays = random.sample(inp.relays[:], inp.relay_num)
        random.shuffle(relays)
        indv = Individual(sensors + relays, sensor_count=len(sensors), relay_count=len(relays))
        pop.append(indv)

    return pop


def kmeans_greedy_init(inp: WusnInput, pop_size, heuristic=False):
    pop = []
    print('Creating population...')
    for _ in tqdm(range(pop_size), file=sys.stdout):
        pop.append(kmeans_greedy(inp, heuristic=heuristic))

    return pop


# noinspection PyTypeChecker
def kmeans_greedy(inp: WusnInput, heuristic=False, km_runs=1):
    X = list(map(lambda s: [s.x, s.y], inp.sensors))
    X = np.asarray(X)

    km = KMeans(n_clusters=inp.relay_num, n_init=km_runs, max_iter=3500, verbose=0)
    km.fit(X)

    clusters = [[] for _ in range(inp.relay_num)]
    pairs = [None] * inp.relay_num
    for i, c in enumerate(km.labels_):
        clusters[c].append(inp.sensors[i])
        centroid = Point(*km.cluster_centers_[c])
        pairs[c] = (clusters[c], centroid)

    # Sort clusters by centroid distance to an anchor point
    anchor = Point(0., 0.)
    pairs.sort(key=lambda x: x[1].distance(anchor))
    clusters = list(map(lambda x: x[0], pairs))

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

    if heuristic:
        out1 = WusnOutput(inp, sensors=inp.sensors.copy(),
                          relays=list(relay_to_sensors.keys()), relay_to_sensors=relay_to_sensors)
        out2 = lbsna3.lbsna3(out1, verbose=False)

        # Reorder selected and sensors
        selected, clusters = [], []
        for rn, sns in out2.relay_to_sensors.items():
            selected.append(rn)
            clusters.append(sns)

    indv = Individual(sensor_count=len(inp.sensors), relay_count=inp.relay_num)

    # Flatten clusters
    for cl in clusters:
        indv.extend(cl)
    indv.extend(selected)

    return indv
