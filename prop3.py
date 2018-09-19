from argparse import ArgumentParser
from tqdm import tqdm

import os
import time
import sys

from wusn.commons import WusnInput
from wusn.propose2.init import kmeans_greedy
from wusn.propose2.utils import Evaluator, ind_to_output


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default='out/prop3/')
    parser.add_argument('--km-runs', type=int, default=3)
    parser.add_argument('--runs', type=int, default=200)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    os.makedirs(args.output, exist_ok=True)

    print('File: %s' % args.input, file=sys.stderr)
    inp = WusnInput.from_file(args.input)
    _ = inp.loss

    start_time = time.time()
    ev = Evaluator(inp)
    best_loss = float('inf')
    out = None

    for it in tqdm(range(args.runs), file=sys.stdout):
        indv = kmeans_greedy(inp, heuristic=True, km_runs=args.km_runs)
        ls = ev.evaluate(indv)[0]
        if ls < best_loss:
            best_loss = ls
            out = ind_to_output(indv, inp)
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

    assert out.valid

    print('Done.')
