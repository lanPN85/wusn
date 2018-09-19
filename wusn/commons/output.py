import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import Point, LineString

from wusn.commons.point import RelayPosition, t_distances
from wusn.commons.input import WusnInput, SensorNode


class WusnOutput:
    def __init__(self, inp: WusnInput, sensors=None, relays=None, relay_to_sensors=None):
        if sensors is None:
            sensors = []
        if relays is None:
            relays = []
        if relay_to_sensors is None:
            relay_to_sensors = {}

        self.input = inp
        self.sensors = sensors
        self.relays = relays
        self.relay_to_sensors = relay_to_sensors

    def get_relays(self, sensor):
        relays = []
        for r, ss in self.relay_to_sensors.items():
            if sensor in ss:
                relays.append(r)
        return relays

    @property
    def max_loss(self):
        losses = self.input.loss
        max_loss = -float('inf')
        for rn, sns in self.relay_to_sensors.items():
            for sn in sns:
                ls = losses[(sn, rn)]
                if ls > max_loss:
                    max_loss = ls

        return max_loss

    @property
    def max_loss_pair(self):
        losses = self.input.loss
        max_loss = -float('inf')
        max_pair = None

        for rn, sns in self.relay_to_sensors.items():
            for sn in sns:
                ls = losses[(sn, rn)]
                if ls > max_loss:
                    max_loss = ls
                    max_pair = (sn, rn)

        return max_pair

    @property
    def valid(self):
        assgn_counts = np.unique(list(map(lambda r: len(self.relay_to_sensors[r]), self.relays)))
        return len(set(self.sensors)) == len(self.input.sensors) \
               and len(set(self.relays)) == self.input.relay_num \
               and len(self.relay_to_sensors.keys()) == self.input.relay_num \
               and len(assgn_counts) == 1 \
               and assgn_counts[0] == len(self.sensors) // self.input.relay_num

    def clean_relays(self):
        k = list(self.relay_to_sensors.keys())
        for rn in k:
            if len(self.relay_to_sensors[rn]) < 1:
                self.relay_to_sensors.pop(rn)
                self.relays.remove(rn)

    def to_text_file(self, input_path, path):
        with open(path, 'wt') as f:
            f.write('%s\n' % input_path)
            f.write('%f\n' % self.max_loss)
            for relay, sensors in self.relay_to_sensors.items():
                f.write('%f,%f' % (relay.x, relay.y))
                for sn in sensors:
                    f.write(' %f,%f' % (sn.x, sn.y))
                f.write('\n')

    @classmethod
    def from_text_file(cls, path):
        with open(path, 'rt') as f:
            lines = f.readlines()
            inp_path = lines[0].strip()
            inp = WusnInput.from_file(inp_path)

            sensors, relays = [], []
            relay_to_sensors = {}
            for ln in lines[2:]:
                coords = ln.strip().split(' ')
                rn_x, rn_y = coords[0].split(',')
                rn = RelayPosition(float(rn_x), float(rn_y), inp.relay_height)
                relays.append(rn)
                relay_to_sensors[rn] = []
                for cd in coords[1:]:
                    sn_x, sn_y = cd.split(',')
                    sn = SensorNode(float(sn_x), float(sn_y), inp.burial_depth)
                    sensors.append(sn)
                    relay_to_sensors[rn].append(sn)

        return cls(inp, sensors=sensors, relays=relays, relay_to_sensors=relay_to_sensors)

    def plot(self, axes: Axes3D, highlight_max=True):
        # Plot all unpicked relay positions
        unpicked = list(filter(lambda x: x not in self.relays, self.input.relays))
        rx = list(map(lambda r: r.x, unpicked))
        ry = list(map(lambda r: r.y, unpicked))
        rz = list(map(lambda r: r.height, unpicked))
        axes.scatter(rx, ry, rz, c='#a5b6d3', label='Potential positions.')

        # Highlight ground
        gx = np.arange(0, self.input.width + 10)
        gy = np.arange(0, self.input.height + 10)
        gx, gy = np.meshgrid(gx, gy)
        gz = gx * 0
        axes.plot_surface(gx, gy, gz, alpha=0.2, color='brown')

        # Plot assignments
        for rn, sns in self.relay_to_sensors.items():
            for sn in sns:
                tx, ty = self.interm_point(sn, rn)
                x = [rn.x, tx, sn.x]
                y = [rn.y, ty, sn.y]
                z = [rn.height, 0, -sn.depth]
                axes.plot(x, y, z, linewidth=0.5, c='#000000')

        # Highlight max pair
        if highlight_max:
            ms, mr = self.max_loss_pair
            tx, ty = self.interm_point(ms, mr)
            mx = [ms.x, tx, mr.x]
            my = [ms.y, ty, mr.y]
            mz = [-ms.depth, 0, mr.height]
            axes.plot(mx, my, mz, c='tab:orange', label='Max assignment (%.2f)' % self.max_loss)

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

    def interm_point(self, sensor, relay):
        d_u, d_a = t_distances(sensor, relay)
        ox = LineString([(0, 0), (self.input.width, 0)])
        oy = LineString([(0, 0), (self.input.height, 0)])

        csx = Point(sensor.x, sensor.depth).buffer(d_u).boundary
        csy = Point(sensor.y, sensor.depth).buffer(d_u).boundary
        crx = Point(relay.x, relay.height).buffer(d_a).boundary
        cry = Point(relay.y, relay.height).buffer(d_a).boundary

        px = csx.intersection(ox)
        py = csy.intersection(oy)

        # print(px)
        try:
            tx = px.x
        except AttributeError:
            tx = px[0].x
        try:
            ty = py.x
        except AttributeError:
            ty = py[0].x
        return tx, ty

    def plot_to_file(self, path, dpi=200, highlight_max=True):
        fig = plt.figure(dpi=dpi)
        ax = Axes3D(fig)
        self.plot(ax, highlight_max=highlight_max)
        ax.legend()
        fig.savefig(path)
