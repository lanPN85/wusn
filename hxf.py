from argparse import ArgumentParser
from tqdm import tqdm

import os
import time
import sys

from wusn.yuan.lurns import lurns1, lurns2
from wusn.propose2.init import kmeans_greedy
from wusn.propose.ecosys import EcoSys
from wusn.propose.r_graph import *
import sys
sys.setrecursionlimit(10000)


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default='out/hxf/')
    parser.add_argument('--lu', type=int, default=1)
    parser.add_argument('--runs', type=int, default=1)

    return parser.parse_args()


def check_individual(eco_sys, individual: list):
    count = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            count += 1
    if count != eco_sys.relays_num:
        print("not available individual")
        return False
    return True


LU = [lurns1.lurns1, lurns2.lurns2]

if __name__ == '__main__':
    args = parse_arguments()
    os.makedirs(args.output, exist_ok=True)

    print('File: %s' % args.input, file=sys.stderr)
    ec = EcoSys.get_instance()
    ec.set_input(args.input)
    inp = ec.wusn_input
    _ = ec.wusn_input.loss

    start_time = time.time()
    best_loss = float('inf')
    out = None

    for it in tqdm(range(args.runs), file=sys.stdout):
        o1 = LU[args.lu - 1](inp)

        # Map relays to new indv
        relays = o1.relays
        ind2 = [0] * len(inp.relays)
        for i, r in enumerate(inp.relays):
            if r in relays:
                ind2[i] = 1
        if not check_individual(ec, ind2):
            print("error generating ind2")
            exit(1)
        # mcf = get_min_cost_flow(ind2, ec.graph, len(inp.relays), len(inp.sensors))
        # ls = get_fitness_value(ind2, ec, mcf)
        mcf = solve_maximum_flow(eco_sys=ec, individual=ind2)
        output_temp = get_output(mcf, ec)
        ls = output_temp.max_loss
        if ls < best_loss:
            best_loss = ls
            out = get_output(mcf, ec)
    elapsed = time.time() - start_time

    print('Elapsed time: %4fms' % (elapsed * 1000.), file=sys.stderr)
    print('Max loss: %.4f' % out.max_loss, file=sys.stderr)
    print('Max pair: %s' % str(out.max_loss_pair), file=sys.stderr)

    test_name = os.path.split(args.input)[-1].split('.')[0]
    save_dir = os.path.join(args.output, test_name)
    os.makedirs(save_dir, exist_ok=True)

    print('Saving results to %s' % save_dir)
    out.clean_relays()
    out.to_text_file(args.input, os.path.join(save_dir, 'best.out'))
    out.plot_to_file(os.path.join(save_dir, 'best.png'))

    # assert out.valid

    print('Done.')
