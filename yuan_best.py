from argparse import ArgumentParser

import os
import time
import sys

from wusn.commons import WusnInput
from wusn.yuan.lbsna import lbsna1, lbsna2, lbsna3
from wusn.yuan.lurns import lurns1, lurns2

LU = [lurns1.lurns1, lurns2.lurns2]
# LU = [lurns1.lurns1]
LB = [lbsna1.lbsna1, lbsna2.lbsna2, lbsna3.lbsna3]


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default='out/yuan/')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    print('File: %s' % args.input, file=sys.stderr)
    inp = WusnInput.from_file(args.input)
    _ = inp.loss
    best_out = None
    best_loss = float('inf')

    start = time.time()
    for i, lu in enumerate(LU):
        print('Using LU%d...' % (i + 1), file=sys.stderr)
        try:
            out_lu = lu(inp)
            for j, lb in enumerate(LB):
                print('Using LB%d...' % (j + 1), file=sys.stderr)

                out_lb = lb(out_lu)
                ls = out_lb.max_loss
                print('Loss value: %.4f' % ls, file=sys.stderr)
                if ls < best_loss:
                    best_loss = ls
                    best_out = out_lb
        except:
            print('LU2 error...', file=sys.stderr)
            continue

    elapsed = time.time() - start

    test_name = os.path.split(args.input)[-1].split('.')[0]
    save_dir = os.path.join(args.output, test_name)
    print('Saving results to %s ...' % save_dir)
    os.makedirs(save_dir, exist_ok=True)
    best_out.to_text_file(args.input, os.path.join(save_dir, 'best.out'))
    best_out.plot_to_file(os.path.join(save_dir, 'best.png'))

    print('Best loss: %.4f' % best_loss, file=sys.stderr)
    print('Total running time: %.4fms' % (elapsed * 1000.), file=sys.stderr)
    print(file=sys.stderr)
    print('Done.')
