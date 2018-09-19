from argparse import ArgumentParser

import os
import time
import sys

from wusn.commons import WusnInput
from wusn.yuan.lbsna import lbsna1, lbsna2, lbsna3
from wusn.yuan.lurns import lurns1, lurns2

LU = [lurns1.lurns1, lurns2.lurns2]
LB = [lbsna1.lbsna1, lbsna2.lbsna2, lbsna3.lbsna3]


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--lu', type=int, required=True, help='1 | 2')
    parser.add_argument('--lb', type=int, required=True, help='1 | 2 | 3')
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default='out/text')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    lu = LU[args.lu - 1]
    lb = LB[args.lb - 1]
    print('File: %s' % args.input, file=sys.stderr)
    print('Using LU%d...' % args.lu, file=sys.stderr)
    print('Using LB%d...' % args.lb, file=sys.stderr)

    loss_start = time.time()
    inp = WusnInput.from_file(args.input)
    _ = inp.loss
    loss_time = time.time() - loss_start

    lu_start = time.time()
    out_lu = lu(inp)
    lu_time = time.time() - lu_start
    print('LURNS running time: %.4fms' % (lu_time * 1000.), file=sys.stderr)

    lb_start = time.time()
    out_lb = lb(out_lu)
    lb_time = time.time() - lb_start
    print('LBSNA running time: %.4fms' % (lb_time * 1000.), file=sys.stderr)

    print('Total running time: %.4fms' % ((lb_time + lu_time) * 1000.), file=sys.stderr)
    print('W/ loss calculation: %.4fms' % ((lb_time + lu_time + loss_time) * 1000.), file=sys.stderr)

    test_name = os.path.split(args.input)[-1].split('.')[0]
    save_dir = os.path.join(args.output, test_name)
    print('Saving results to %s ...' % save_dir)
    os.makedirs(save_dir, exist_ok=True)
    out_lu.to_text_file(args.input, os.path.join(save_dir, 'lu.out'))
    out_lu.plot_to_file(os.path.join(save_dir, 'lu_plot.png'))
    out_lb.to_text_file(args.input, os.path.join(save_dir, 'lb.out'))
    out_lb.plot_to_file(os.path.join(save_dir, 'lb_plot.png'))

    print('Max loss @LURNS: %.4f %s' % (out_lu.max_loss, out_lu.max_loss_pair), file=sys.stderr)
    print('Max loss @LBSNA: %.4f %s' % (out_lb.max_loss, out_lb.max_loss_pair), file=sys.stderr)
    print(file=sys.stderr)

    print('Done.')
