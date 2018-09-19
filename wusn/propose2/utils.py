from deap import tools

import random

from wusn.commons import WusnInput, WusnOutput
from wusn.propose2.model import Individual


class Evaluator:
    def __init__(self, inp: WusnInput):
        self.input = inp

    def evaluate(self, ind):
        mloss = -float('inf')

        sensors = ind[:ind.sensor_count]
        relays = ind[ind.sensor_count:]
        chunk_size = ind.sensor_count // ind.relay_count
        for i, rn in enumerate(relays):
            sns = sensors[i * chunk_size: (i + 1) * chunk_size]
            for sn in sns:
                ls = self.input.loss[(sn, rn)]
                if ls > mloss:
                    mloss = ls

        return mloss,

    def best_indv(self, pop):
        best = None
        best_loss = float('inf')

        for indv in pop:
            if not indv.fitness.valid:
                ls = self.evaluate(indv)[0]
            else:
                ls = indv.fitness.values[0]

            if ls < best_loss:
                best_loss = ls
                best = indv
        best.fitness.values = best_loss,
        return best


def ind_to_output(ind, inp: WusnInput) -> WusnOutput:
    out = WusnOutput(inp)
    sensors = ind[:ind.sensor_count]
    relays = ind[ind.sensor_count:]

    out.sensors = sensors
    out.relays = relays

    chunk_size = ind.sensor_count // ind.relay_count
    for i, rn in enumerate(relays):
        sns = sensors[i * chunk_size: (i + 1) * chunk_size]
        out.relay_to_sensors[rn] = []
        for sn in sns:
            out.relay_to_sensors[rn].append(sn)

    return out


def crossover(ind1, ind2, all_relays=tuple()):
    """
    Performs 2 two-point crossovers on the sensor and relay part of the genes.
    :param all_relays: List containing all possible relay positions
    :param ind1:
    :param ind2:
    :return:  A tuple of two individuals.
    """
    ind1, ind2 = ind1.clone(), ind2.clone()
    s1 = ind1[:ind1.sensor_count]
    s2 = ind2[:ind2.sensor_count]
    r1 = ind1[ind1.sensor_count:]
    r2 = ind2[ind2.sensor_count:]

    nr1, nr2 = tools.cxTwoPoint(r1[:], r2[:])
    nr1 = normalize_relays(nr1, all_relays)
    nr2 = normalize_relays(nr2, all_relays)
    ns1, ns2 = cxPartialyMatched(s1[:], s2[:])
    # nr1, nr2 = cxPartialyMatched(r1[:], r2[:])
    # assert len(set(nr1)) == len(set(r1)), '[%d %d]' % (len(set(nr1)), len(set(r1)))
    # assert len(set(nr2)) == len(set(r2)), '[%d %d]' % (len(set(nr2)), len(set(r2)))

    ni1 = ns1 + nr1
    ni2 = ns2 + nr2

    return ni1, ni2


def normalize_relays(nr, all_relays):
    ret = []
    for rn in nr:
        if rn in ret:
            cand = list(filter(lambda r: (r not in ret) and (r not in nr), all_relays))
            rep = random.sample(cand, 1)[0]
            ret.append(rep)
        else:
            ret.append(rn)
    return ret


def cxPartialyMatched(ind1, ind2):
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place.

    Modified version based on deap's implementation. Uses a dict instead of list to support non-index data types.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.
    """
    size = min(len(ind1), len(ind2))
    p1, p2 = {}, {}

    # Initialize the position of each indices in the individuals
    for i in range(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i
    # Choose crossover points
    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Apply crossover between cx points
    for i in range(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return ind1, ind2


def mutate(ind, all_relays=tuple()):
    ind = ind.clone()
    sensors = ind[:ind.sensor_count]
    relays = ind[ind.sensor_count:]

    # Swap sensors
    chunk_size = ind.sensor_count / ind.relay_count
    indices = list(range(len(sensors)))
    i1 = random.sample(indices, 1)[0]
    indices = list(filter(lambda i: i // chunk_size != i1 // chunk_size, indices))
    i2 = random.sample(indices, 1)[0]
    sensors[i1], sensors[i2] = sensors[i2], sensors[i1]

    # Insert a random relay
    inr = random.sample(all_relays, 1)[0]
    indices = list(filter(lambda i: relays[i] != inr, list(range(len(relays)))))
    outi = random.sample(indices, 1)[0]

    if inr in relays:
        ini = relays.index(inr)
        relays[ini], relays[outi] = relays[outi], relays[ini]
    else:
        relays[outi] = inr

    # random.shuffle(sensors)
    # relays = random.sample(all_relays, ind.relay_count)
    # random.shuffle(relays)

    return sensors + relays

