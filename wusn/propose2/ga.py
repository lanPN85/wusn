from deap import base, tools

import numpy as np
import random

from wusn.commons import WusnInput
from wusn.propose2 import utils, init


def start(inp: WusnInput, pop_size=30, max_iters=10000, patience=100,
          cross_rate=0.5, mut_rate=0.1, use_heuristic=False, init_fn=init.kmeans_greedy_init):
    evaluator = utils.Evaluator(inp)
    toolbox = base.Toolbox()

    toolbox.register('select', tools.selTournament, tournsize=10)
    # toolbox.register('select', tools.selBest)
    # toolbox.register('select', tools.selRoulette)
    toolbox.register('select1', tools.selBest)
    toolbox.register('select2', tools.selRandom)
    toolbox.register('initialize', init_fn, heuristic=use_heuristic)
    toolbox.register('crossover', utils.crossover, all_relays=inp.relays)
    toolbox.register('mutate', utils.mutate, all_relays=inp.relays)
    toolbox.register('evaluate', evaluator.evaluate)

    stats = tools.Statistics(key=lambda _ind: _ind.fitness.values[0])
    stats.register("Min", np.min)
    stats.register("StdDev", np.std)

    logbook = tools.Logbook()
    logbook.header = 'Gen', 'Nic', 'Min', 'PrevMut', 'PrevCross', 'Best', 'StdDev'

    population = toolbox.initialize(inp, pop_size)
    for indv in population:
        indv.fitness.values = toolbox.evaluate(indv)

    nic = 0
    best_loss = float('inf')
    best_indv = None
    prev_mutates = 0
    prev_cross = 0

    for it in range(max_iters):
        if nic > patience:
            print('No improvement after %d generations. Stopping.' % nic)
            break

        # Compile statistics
        records = stats.compile(population)
        min_loss = records['Min']
        if min_loss < best_loss:
            nic = 0
            best_loss = min_loss
            best_indv = evaluator.best_indv(population)
        else:
            nic += 1
        logbook.record(Gen=it, Nic=nic, Best=best_loss, PrevMut=prev_mutates,
                       PrevCross=prev_cross, **records)
        print(logbook.stream)

        current_pop = list(map(lambda x: x.clone(), population))

        prev_mutates, prev_cross = 0, 0
        for i, c1 in enumerate(current_pop):
            if random.random() < cross_rate:
                cand = list(filter(lambda x: x != c1, current_pop))
                if len(cand) < 1:
                    c2 = c1
                else:
                    c2 = random.choice(cand)

                prev_cross += 1
                n1, n2 = toolbox.crossover(c1, c2)
                # next_pop.extend([n1, n2])

                for mutant in [n1, n2]:
                    if random.random() < mut_rate:
                        prev_mutates += 1
                        nc = toolbox.mutate(mutant)
                        nc.fitness.values = toolbox.evaluate(nc)
                        population.append(nc)
                    else:
                        mutant.fitness.values = toolbox.evaluate(mutant)
                        population.append(mutant)

        population = toolbox.select(population, pop_size)

    return utils.ind_to_output(best_indv, inp), logbook
