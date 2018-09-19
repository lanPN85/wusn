import os
import sys
import pickle
import matplotlib.pyplot as plt

from tqdm import tqdm
from mpl_toolkits.mplot3d import Axes3D

from wusn.commons.point import RelayPosition, SensorNode
from wusn.commons.config import get_trans_loss
from wusn.commons.point import t_distances


# Cache related
CACHE_DIR = os.path.join(os.path.expanduser('~'), '.wusn_cache')
os.makedirs(CACHE_DIR, exist_ok=True)


class WusnInput:
    def __init__(self, sensors=None, relays=None,
                 relay_num=0, width=1000., height=1000.,
                 ignore_cache=False):
        if sensors is None:
            sensors = []
        if relays is None:
            relays = []

        self.sensors = sensors
        self.relays = relays
        self.relay_num = relay_num
        self.width = width
        self.height = height
        self._loss = None
        self._loss_index = None

        assert len(self.sensors) == len(set(self.sensors))
        assert len(self.relays) == len(set(self.relays))

        if not ignore_cache:
            self.load_cache()

    @property
    def loss_index(self):
        """
        Calculates the loss index matrix (if neccessary)
        :return: A 2-dimensional list containing
        """
        if self._loss_index is None:
            # if self._loss is None:
            #     self.__get_loss()
            # else:
            #     self.__index_from_loss()
            self.__get_loss()

        return self._loss_index

    @property
    def loss(self):
        """
        Calculates the loss dictionary (if neccessary)
        :return: A dictionary with keys (SN, RN) and the transmission loss as value.
        """
        if self._loss is None:
            self.__get_loss()

        return self._loss

    def __index_from_loss(self):
        self._loss_index = []
        for i, sn in enumerate(self.sensors):
            tmp = []
            for j, rn in enumerate(self.relays):
                l = self._loss[(sn, rn)]
                tmp.append(l)
            self._loss_index.append(tmp)

    def __get_loss(self):
        self._loss_index = []
        self._loss = {}
        print('Calculating transmission loss...')
        tsensors = tqdm(self.sensors, desc='Sensor', ncols=100, file=sys.stdout)
        for i, sn in enumerate(tsensors):
            tmp = []
            for j, rn in enumerate(self.relays):
                d_ug, d_ag = t_distances(sn, rn)
                l = get_trans_loss(d_ug, d_ag)
                tmp.append(l)
                self._loss[(sn, rn)] = l
            self._loss_index.append(tmp)

    @property
    def burial_depth(self):
        if len(self.sensors) < 1:
            return None
        else:
            return self.sensors[0].depth

    @property
    def relay_height(self):
        if len(self.relays) < 1:
            return None
        else:
            return self.relays[0].height

    @classmethod
    def from_file(cls, path, ignore_cache=False):
        with open(path, 'rt') as f:
            lines = f.readlines()
            lines = list(map(lambda l: l.strip(), lines))

            # W H
            width = float(lines[0].split(' ')[0])
            height = float(lines[0].split(' ')[1])

            # BD HR
            depth = float(lines[1].split(' ')[0])
            rheight = float(lines[1].split(' ')[1])

            # N M Y
            n = int(lines[2].split(' ')[0])
            m = int(lines[2].split(' ')[1])
            relay_num = int(lines[2].split(' ')[2])

            sensors = []
            for ln in lines[3:3+n]:
                x, y = ln.split(' ')
                sensors.append(SensorNode(float(x), float(y), depth=depth))

            relays = []
            for ln in lines[3+n:3+n+m]:
                x, y = ln.split(' ')
                relays.append(RelayPosition(float(x), float(y), height=rheight))

            return WusnInput(sensors=sensors, relays=relays, ignore_cache=ignore_cache,
                             relay_num=relay_num, width=width, height=height)

    def __hash__(self):
        return hash((self.width, self.height, self.relay_num,
                     tuple(self.sensors), tuple(self.relays)))

    def cache_losses(self):
        fname = '%s.loss' % hash(self)
        save_path = os.path.join(CACHE_DIR, fname)
        with open(save_path, 'wb') as f:
            pickle.dump(self.loss, f)
        print('Loss matrix saved to %s' % save_path)

    def load_cache(self):
        fname = '%s.loss' % hash(self)
        save_path = os.path.join(CACHE_DIR, fname)
        if os.path.exists(save_path):
            with open(save_path, 'rb') as f:
                self._loss = pickle.load(f)
                print('Loss matrix loaded from %s' % save_path)
        else:
            print('Cache not found')

    def plot(self, axes: Axes3D, **kwargs):
        # Plot all sensors
        sx = list(map(lambda s: s.x, self.sensors))
        sy = list(map(lambda s: s.y, self.sensors))
        sz = list(map(lambda s: -s.depth, self.sensors))
        axes.scatter(sx, sy, sz, c='r', label='Sensors')

        # Plot all relays
        rx = list(map(lambda r: r.x, self.relays))
        ry = list(map(lambda r: r.y, self.relays))
        rz = list(map(lambda r: r.height, self.relays))
        axes.scatter(rx, ry, rz, c='b', label='Relays')

    def to_file(self, path):
        with open(path, 'wt') as f:
            f.write('%f %f\n' % (self.width, self.height))
            f.write('%f %f\n' % (self.burial_depth, self.relay_height))
            f.write('%d %d %d\n' % (len(self.sensors), len(self.relays), self.relay_num))

            for s in self.sensors:
                f.write('%f %f\n' % (s.x, s.y))
            for r in self.relays:
                f.write('%f %f\n' % (r.x, r.y))
