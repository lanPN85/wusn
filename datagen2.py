from argparse import ArgumentParser

import random
import os
import numpy as np

from wusn.commons import WusnInput, SensorNode, RelayPosition


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-o', '--output-dir', default='data')
    parser.add_argument('-c', '--count', type=int, default=5)
    parser.add_argument('-W', '--width', type=float, default=1000.)
    parser.add_argument('-H', '--height', type=float, default=1000.)
    parser.add_argument('--depth', type=float, default=1.)
    parser.add_argument('--rheight', type=float, default=10.)
    parser.add_argument('-N', '--sensors', type=int, default=200)
    parser.add_argument('-M', '--relays', type=int, default=200)
    parser.add_argument('-Y', type=int, default=20)

    return parser.parse_args()


def uniform_point(max_width, max_height):
    return random.uniform(0., max_width), random.uniform(0., max_height)


def uniform_sensors(width, height, depth, N, M, Y):
    sensors = []
    for _ in range(N):
        x, y = uniform_point(width, height)
        sn = SensorNode(x, y, depth=depth)
        while sn in sensors:
            x, y = uniform_point(width, height)
            sn = SensorNode(x, y, depth=depth)
        sensors.append(sn)
    return sensors


def uniform_half_sensors(width, height, depth, N, M, Y):
    return uniform_sensors(width, height, depth, N // 2, M, Y)


def uniform_relays(width, height, rheight, N, M, Y):
    relays = []
    for _ in range(M):
        x, y = uniform_point(width, height)
        rn = RelayPosition(x, y, height=rheight)
        while rn in relays:
            x, y = uniform_point(width, height)
            rn = RelayPosition(x, y, height=rheight)
        relays.append(rn)
    return relays


def uniform_half_relays(width, height, rheight, N, M, Y):
    return uniform_relays(width, height, rheight, N, M // 2, Y)


def clustered_sensors(width, height, depth, N, clusters):
    _w = 0.6
    cluster_size = N // clusters
    sensors = []

    for _ in range(clusters):
        center_x, center_y = uniform_point(width, height)
        for _ in range(cluster_size):
            sn = None
            while sn is None or sn in sensors:
                x = np.random.normal(loc=center_x, scale=width / clusters * _w)
                x = np.clip(x, 0, width)
                y = np.random.normal(loc=center_y, scale=height / clusters * _w)
                y = np.clip(y, 0, height)
                sn = SensorNode(x, y, depth=depth)
            sensors.append(sn)

    return sensors


def clustered_relays(width, height, rheight, M, clusters):
    _w = 0.6
    cluster_size = M // clusters
    relays = []

    for _ in range(clusters):
        center_x, center_y = uniform_point(width, height)
        for _ in range(cluster_size):
            rn = None
            while rn is None or rn in relays:
                x = np.random.normal(loc=center_x, scale=width / clusters * _w)
                x = np.clip(x, 0, width)
                y = np.random.normal(loc=center_y, scale=height / clusters * _w)
                y = np.clip(y, 0, height)
                rn = RelayPosition(x, y, height=rheight)
            relays.append(rn)

    return relays


def many_clustered_sensors(width, height, depth, N, M, Y):
    return clustered_sensors(width, height, depth, N, N // Y * 2)


def few_clustered_sensors(width, height, depth, N, M, Y):
    return clustered_sensors(width, height, depth, N, N // Y // 2)


def many_clustered_relays(width, height, rheight, N, M, Y):
    return clustered_relays(width, height, rheight, M, Y * 2)


def few_clustered_relays(width, height, rheight, N, M, Y):
    return clustered_relays(width, height, rheight, M, Y // 2)


def normal_point(max_width, max_height):
    x_ = np.random.normal(loc=max_width / 2, scale=max_width / 4)
    x_ = np.clip(x_, 0., max_width)
    y_ = np.random.normal(loc=max_height / 2, scale=max_height / 4)
    y_ = np.clip(y_, 0., max_height)
    return x_, y_


def bordered_relays(width, height, rheight, N, M, Y, thres=0.2):
    relays = []
    max_left, min_right = width * thres, width * (1-thres)
    max_bottom, min_top = height * thres, height * (1-thres)
    for _ in range(M):
        rn = None
        while rn is None or rn in relays:
            rnd = random.random()
            if rnd < 0.25:
                x, y = random.uniform(0., max_left), random.uniform(0., height)
            elif rnd < 0.5:
                x, y = random.uniform(min_right, width), random.uniform(0., height)
            elif rnd < 0.75:
                x, y = random.uniform(0., width), random.uniform(0., max_bottom)
            else:
                x, y = random.uniform(0., width), random.uniform(min_top, height)

            rn = RelayPosition(x, y, height=rheight)
        relays.append(rn)
    return relays


def bordered_sensors(width, height, depth, N, M, Y, thres=0.2):
    sensors = []
    max_left, min_right = width * thres, width * (1-thres)
    max_bottom, min_top = height * thres, height * (1-thres)
    for _ in range(M):
        sn = None
        while sn is None or sn in sensors:
            rnd = random.random()
            if rnd < 0.25:
                x, y = random.uniform(0., max_left), random.uniform(0., height)
            elif rnd < 0.5:
                x, y = random.uniform(min_right, width), random.uniform(0., height)
            elif rnd < 0.75:
                x, y = random.uniform(0., width), random.uniform(0., max_bottom)
            else:
                x, y = random.uniform(0., width), random.uniform(min_top, height)

            sn = SensorNode(x, y, depth=depth)
        sensors.append(sn)
    return sensors


def centered_relays(width, height, rheight, N, M, Y, thres=0.2):
    relays = []
    min_left, max_right = width * thres, width * (1 - thres)
    min_bottom, max_top = height * thres, height * (1 - thres)
    for _ in range(M):
        rn = None
        while rn is None or rn in relays:
            x = random.uniform(min_left, max_right)
            y = random.uniform(min_bottom, max_top)

            rn = RelayPosition(x, y, height=rheight)
        relays.append(rn)
    return relays


def centered_sensors(width, height, depth, N, M, Y, thres=0.2):
    sensors = []
    min_left, max_right = width * thres, width * (1 - thres)
    min_bottom, max_top = height * thres, height * (1 - thres)
    for _ in range(M):
        sn = None
        while sn is None or sn in sensors:
            x = random.uniform(min_left, max_right)
            y = random.uniform(min_bottom, max_top)

            sn = SensorNode(x, y, depth=depth)
        sensors.append(sn)
    return sensors


GENS = {
    'rr': (uniform_sensors, uniform_relays),
    # 'rhr': (uniform_sensors, uniform_half_relays),
    'mcr': (many_clustered_sensors, uniform_relays),
    'fcr': (few_clustered_sensors, uniform_relays),
    'rmc': (uniform_sensors, many_clustered_relays),
    'rfc': (uniform_sensors, few_clustered_relays),
    'br': (bordered_sensors, uniform_relays),
    'cer': (centered_sensors, uniform_relays)
    # 'rb': (uniform_sensors, bordered_relays),
    # 'rce': (uniform_sensors, centered_relays)
}


if __name__ == '__main__':
    args = parse_arguments()

    count = 1
    for name, (fn_s, fn_r) in GENS.items():
        for i in range(args.count):
            sensors_ = fn_s(args.width, args.height, args.depth, args.sensors, args.relays, args.Y)
            relays_ = fn_r(args.width, args.height, args.rheight, args.sensors, args.relays, args.Y)
            inp = WusnInput(sensors=sensors_, relays=relays_, relay_num=args.Y,
                            width=args.width, height=args.height, ignore_cache=True)

            fname = '%s-%03d.test' % (name, i + 1)
            path = os.path.join(args.output_dir, fname)
            print('Saving test case %d to %s' % (count, path))
            count += 1
            inp.to_file(path)
