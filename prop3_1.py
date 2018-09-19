from argparse import ArgumentParser

import os
import time
import sys

from wusn.commons import WusnInput
from wusn.propose3_1 import ga, init


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
    inp = WusnInput.from_file(args.input)
    _ = inp.loss

    start_time = time.time()
    out, logs = ga.start(inp, pop_size=args.pop_size, max_iters=args.iters,
                         patience=args.patience, cross_rate=args.cross_rate,
                         mut_rate=args.mut_rate, init_fn=INIT_FN[args.init])
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

    assert out.valid

    print('Done.')
