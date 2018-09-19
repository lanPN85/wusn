from argparse import ArgumentParser
# from deap import base, tools
#
# import numpy as np
# import random
from deap import base, tools
import numpy as np
import random
from wusn.propose.r_graph import *
from wusn.commons import WusnInput
from wusn.propose3_1 import utils, init
import os
import time
import sys
from wusn.propose.ecosys import *
from wusn.commons import WusnInput
from wusn.propose3_1 import ga, init


def mxf_eval(ind, ec: EcoSys):
    mcf = solve_maximum_flow(eco_sys=ec, individual=ind)
    output_temp = get_output(mcf, ec)
    ls = output_temp.max_loss
    return ls,


def start(inp: WusnInput, pop_size=100, max_iters=10000, patience=100,
          cross_rate=0.8, mut_rate=0.1, init_fn=init.kmeans_greedy_init, eco_sys=EcoSys.get_instance()):
    evaluator = utils.Evaluator(inp)
    toolbox = base.Toolbox()

    toolbox.register('select_tour', tools.selTournament, tournsize=5)
    # toolbox.register('select_random', tools.selRandom)
    toolbox.register('select', tools.selBest)
    # toolbox.register('select', tools.selRoulette)
    toolbox.register('initialize', init_fn)
    toolbox.register('crossover', utils.crossover, relays_num=inp.relay_num, all_relays=inp.relays)
    toolbox.register('mutate', utils.mutate, all_relays=inp.relays)
    toolbox.register('evaluate', mxf_eval)

    logbook = tools.Logbook()
    logbook.header = 'Gen', 'Nic', 'Min', 'PrevMut', 'PrevCross', 'Best', 'StdDev'

    population = toolbox.initialize(inp, pop_size)
    for indv in population:
        indv.fitness.values = toolbox.evaluate(indv, eco_sys)

    nic = 0
    best_loss = float('inf')
    best_indv = None
    prev_mutates = 0
    prev_cross = 0

    stats = tools.Statistics(key=lambda _ind: _ind.fitness.values[0])
    stats.register("Min", np.min)
    stats.register("StdDev", np.std)

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
                        nc.fitness.values = toolbox.evaluate(nc, eco_sys)
                        population.append(nc)
                    else:
                        mutant.fitness.values = toolbox.evaluate(mutant, eco_sys)
                        population.append(mutant)
        a = int(pop_size/10)
        b = pop_size - a
        population1 = toolbox.select(population, a)
        population2 = toolbox.select_tour(population, b)
        population = population1 + population2
        # population = toolbox.select_tour(population, pop_size)
    mcf = solve_maximum_flow(eco_sys=ec, individual=best_indv)
    output_temp = get_output(mcf, ec)
    return output_temp, logbook
    # return utils.ind_to_output(best_indv, inp), logbook
    # return best_indv, logbook


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default='out/prop3_1/')
    parser.add_argument('--pop-size', default=100, type=int)
    parser.add_argument('--iters', default=1000, type=int)
    parser.add_argument('--patience', default=30, type=int)
    parser.add_argument('--cross-rate', default=0.7, type=float)
    parser.add_argument('--mut-rate', default=0.1, type=float)
    parser.add_argument('--init', default='kmeans', help='kmeans | random')

    return parser.parse_args()


INIT_FN = {
    'kmeans': init.kmeans_greedy_init,
    'random': init.random_init
}


if __name__ == '__main__':
    args = parse_arguments()
    os.makedirs(args.output, exist_ok=True)

    print('File: %s' % args.input, file=sys.stderr)
    ec = EcoSys.get_instance()
    ec.set_input(args.input)
    inp = ec.wusn_input
    _ = ec.wusn_input.loss
    # inp = WusnInput.from_file(args.input)
    # _ = inp.loss

    start_time = time.time()
    out, logs = start(inp, pop_size=args.pop_size, max_iters=args.iters,
                         patience=args.patience, cross_rate=args.cross_rate,
                         mut_rate=args.mut_rate, init_fn=INIT_FN[args.init], eco_sys=ec)
    elapsed = time.time() - start_time

    print('Elapsed time: %4fms' % (elapsed * 1000.), file=sys.stderr)
    print('Max loss: %.4f' % out.max_loss, file=sys.stderr)
    print('Max pair: %s' % str(out.max_loss_pair), file=sys.stderr)

    test_name = os.path.split(args.input)[-1].split('.')[0]
    save_dir = os.path.join(args.output, test_name)
    os.makedirs(save_dir, exist_ok=True)

    print('Saving results to %s' % save_dir)
    out.to_text_file(args.input, os.path.join(save_dir, 'best.out'))
    out.plot_to_file(os.path.join(save_dir, 'best.png'))
    with open(os.path.join(save_dir, 'log.txt'), 'wt') as f:
        f.write(str(logs))
    #assert out.valid
    print('Done.')
