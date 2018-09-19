from argparse import ArgumentParser

import os
import time
import sys

from wusn.commons import WusnInput
from wusn.propose3_1 import init, utils
from wusn.yuan.lbsna import lbsna1, lbsna2, lbsna3
from wusn import propose2


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default='out/kmh/')
    parser.add_argument('--lb', type=int, default=3)

    return parser.parse_args()


LB = [lbsna1.lbsna1, lbsna2.lbsna2, lbsna3.lbsna3]

if __name__ == '__main__':
    args = parse_arguments()

    os.makedirs(args.output, exist_ok=True)

    print('File: %s' % args.input, file=sys.stderr)
    inp = WusnInput.from_file(args.input)
    _ = inp.loss

    start_time = time.time()
    if args.lb > 0:
        out = init.kmeans_greedy(inp)
        out = utils.ind_to_output(out, inp, delegate=LB[args.lb - 1])
    else:
        out = propose2.init.kmeans_greedy(inp, km_runs=1)
        out = propose2.utils.ind_to_output(out, inp)

    elapsed = time.time() - start_time

    print('Elapsed time: %4fms' % (elapsed * 1000.), file=sys.stderr)
    print('Max loss: %.4f' % out.max_loss, file=sys.stderr)
    print('Max pair: %s' % str(out.max_loss_pair), file=sys.stderr)
    print(file=sys.stderr)

    test_name = os.path.split(args.input)[-1].split('.')[0]
    save_dir = os.path.join(args.output, test_name)
    os.makedirs(save_dir, exist_ok=True)

    print('Saving results to %s' % save_dir)
    out.to_text_file(args.input, os.path.join(save_dir, 'best.out'))
    out.plot_to_file(os.path.join(save_dir, 'best.png'))

    assert out.valid

    print('Done.')
