from argparse import ArgumentParser

import sys
import os

from wusn.commons import WusnInput
from wusn.exact import solve


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default='out/exact')
    parser.add_argument('--lax', action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    print('File: %s' % args.input)

    inp = WusnInput.from_file(args.input)
    print('Modeling...')
    prob = solve.model_lp(inp, lax=args.lax)

    print('Solving LP...')
    out = solve.solve_lp(prob, inp)

    test_name = os.path.split(args.input)[-1].split('.')[0]
    if not args.lax:
        save_dir = os.path.join(args.output, test_name)
        print('Saving results to %s ...' % save_dir)
        os.makedirs(save_dir, exist_ok=True)

        out.to_text_file(args.input, os.path.join(save_dir, 'opt.out'))
        out.plot_to_file(os.path.join(save_dir, 'opt.png'))

        print('Optimal loss [%s]: %.4f' % (test_name, out.max_loss), file=sys.stderr)
    else:
        print('Optimal non-integral loss [%s]: %.4f' % (test_name, out.value()), file=sys.stderr)
