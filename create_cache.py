from argparse import ArgumentParser

import os

from wusn.commons import WusnInput


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument(dest='data_dir')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    files = os.listdir(args.data_dir)
    files = list(filter(lambda f: f.endswith('.test'), files))

    for fn in files:
        full_path = os.path.join(args.data_dir, fn)
        print(full_path)
        inp = WusnInput.from_file(full_path, ignore_cache=True)
        inp.cache_losses()
