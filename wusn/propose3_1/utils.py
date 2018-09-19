from wusn.commons import WusnOutput, WusnInput
from wusn.yuan.lbsna import lbsna3
from wusn.propose3_1.model import Individual

from deap import tools

import numpy as np
import random


class Evaluator:
    def __init__(self, inp: WusnInput):
        self.input = inp

    def evaluate(self, ind):
        out = ind_to_output(ind, self.input)
        mloss = out.max_loss

        return mloss,

    def best_indv(self, pop):
        best = None
        best_loss = float('inf')

        for indv in pop:
            ls = indv.fitness.values[0]

            if ls < best_loss:
                best_loss = ls
                best = indv
        return best


def greedy_assign(out: WusnOutput):
    for rn in out.relays:
        out.relay_to_sensors[rn] = []

    for sn in out.sensors:
        best_rn = None
        best_loss = float('inf')
        for rn in out.relays:
            if out.input.loss[(sn, rn)] < best_loss:
                best_rn = rn
                best_loss = out.input.loss[(sn, rn)]
        out.relay_to_sensors[best_rn].append(sn)


def ind_to_output(ind, inp: WusnInput, delegate=lbsna3.lbsna3):
    # relays = list(ind)
    relays = []
    for i, v in enumerate(ind):
        if v > 0:
            relays.append(inp.relays[i])

    out = WusnOutput(inp, sensors=inp.sensors, relays=relays)
    greedy_assign(out)
    out = delegate(out, verbose=False)
    return out


def crossover(ind1, ind2, relays_num=None, all_relays=None):
    _ind1, _ind2 = ind1.clone(), ind2.clone()

    n1, n2 = tools.cxTwoPoint(_ind1, _ind2)
    n1 = normalize(n1, relays_num, all_relays)
    n2 = normalize(n2, relays_num, all_relays)

    return n1, n2


def normalize(ind, relays_num, all_relays):
    count = ind.count(1)
    ni = np.asarray(ind, dtype=int)
    while count > relays_num:
        elist = np.where(ni == 1)[0]
        ei = np.random.choice(elist)
        ind[ei], ni[ei] = 0, 0
        count -= 1
    while count < relays_num:
        elist = np.where(ni == 0)[0]
        ei = np.random.choice(elist)
        ind[ei], ni[ei] = 1, 1
        count += 1
    return ind


def mutate(ind, all_relays=None):
    _ind = ind.clone()
    return tools.mutShuffleIndexes(_ind, 0.2)[0]
