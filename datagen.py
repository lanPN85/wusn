from argparse import ArgumentParser

import random
import os
import numpy as np

from wusn.commons import WusnInput, SensorNode, RelayPosition


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-o', '--output-dir', default='data')
    parser.add_argument('-c', '--count', type=int, default=10)
    parser.add_argument('-W', '--width', type=float, default=1000.)
    parser.add_argument('-H', '--height', type=float, default=1000.)
    parser.add_argument('--depth', type=float, default=1.)
    parser.add_argument('--rheight', type=float, default=10.)
    parser.add_argument('-N', '--sensors', type=int, default=200)
    parser.add_argument('-M', '--relays', type=int, default=200)
    parser.add_argument('-Y', type=int, default=20)
    parser.add_argument('--sdist', default='uniform', help='uniform | normal | poisson')
    parser.add_argument('--rdist', default='uniform', help='uniform | normal | poisson')

    return parser.parse_args()


def uniform_point(max_width, max_height):
    return random.uniform(0., max_width), random.uniform(0., max_height)


def normal_point(max_width, max_height):
    x_ = np.random.normal(loc=max_width / 2, scale=max_width / 4)
    x_ = np.clip(x_, 0., max_width)
    y_ = np.random.normal(loc=max_height / 2, scale=max_height / 4)
    y_ = np.clip(y_, 0., max_height)
    return x_, y_


def poisson_point(max_width, max_height):
    x_ = np.random.poisson(lam=max_width / 4)
    x_ = np.clip(x_, 0., max_width)
    y_ = np.random.poisson(lam=max_height / 4)
    y_ = np.clip(y_, 0., max_height)
    return x_, y_


RAND_FUNCTIONS = {
    'uniform': uniform_point,
    'normal': normal_point,
    'poisson': poisson_point
}


if __name__ == '__main__':
    args = parse_arguments()

    inputs = []
    for i in range(args.count):
        inp = WusnInput(relay_num=args.Y, width=args.width, height=args.height,
                        ignore_cache=True)

        # Random sensors
        for j in range(args.sensors):
            x, y = RAND_FUNCTIONS[args.sdist](inp.width, inp.height)
            sn = SensorNode(x, y, depth=args.depth)
            while sn in inp.sensors:
                x, y = RAND_FUNCTIONS[args.sdist](inp.width, inp.height)
                sn = SensorNode(x, y, depth=args.depth)
            inp.sensors.append(sn)

        # Random relays
        for j in range(args.relays):
            x, y = RAND_FUNCTIONS[args.rdist](inp.width, inp.height)
            rn = RelayPosition(x, y, height=args.rheight)
            while rn in inp.relays:
                x, y = RAND_FUNCTIONS[args.rdist](inp.width, inp.height)
                rn = RelayPosition(x, y, height=args.rheight)
            inp.relays.append(rn)

        inputs.append(inp)

    for i, inp in enumerate(inputs):
        fname = '%03d.test' % (i + 1)
        path = os.path.join(args.output_dir, fname)
        print('Saving test case %d to %s' % (i+1, path))
        inp.to_file(path)
