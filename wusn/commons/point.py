from wusn.commons.config import Config

from scipy.optimize import least_squares

import math


class Point:
    """
    An immutable 2D point.
    """
    def __init__(self, x=0., y=0.):
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def clone(self):
        return self.__class__(self.x, self.y)

    def distance(self, other):
        """
        :param other: Other point
        :return: Euclidean distance between self & other
        """
        return distance(self, other)

    def __add__(self, other):
        res = self.clone()
        if isinstance(other, Point):
            res._x += other.x
            res._y += other.y
        else:
            res._x += other
            res._y += other
        return res

    def __sub__(self, other):
        res = self.clone()
        if isinstance(other, Point):
            res._x -= other.x
            res._y -= other.y
        else:
            res._x -= other
            res._y -= other
        return res

    def __mul__(self, other):
        res = self.clone()
        if isinstance(other, Point):
            res._x *= other.x
            res._y *= other.y
        else:
            res._x *= other
            res._y *= other
        return res

    def __floordiv__(self, other):
        res = self.clone()
        if isinstance(other, Point):
            res._x //= other.x
            res._y //= other.y
        else:
            res._x //= other
            res._y //= other
        return res

    def __truediv__(self, other):
        res = self.clone()
        if isinstance(other, Point):
            res._x /= other.x
            res._y /= other.y
        else:
            res._x /= other
            res._y /= other
        return res

    def __mod__(self, other):
        res = self.clone()
        if isinstance(other, Point):
            res._x %= other.x
            res._y %= other.y
        else:
            res._x %= other
            res._y %= other
        return res

    def __neg__(self):
        res = self.clone()
        res._x = -res.x
        res._y = -res.y
        return res

    def __abs__(self):
        res = self.clone()
        res._x = abs(res.x)
        res._y = abs(res.y)
        return res

    def __repr__(self):
        return '%s(%f %f)' % (self.__class__.__name__, self.x, self.y)


class SensorNode(Point):
    """
    A sensor node
    """
    def __init__(self, x=0., y=0., depth=1., hval=None):
        super().__init__(x, y)
        self._depth = depth
        if hval is None:
            self.__hash = hash((self.x, self.y, self.depth))
        else:
            self.__hash = hval

    @property
    def depth(self) -> float:
        return self._depth

    def clone(self):
        return self.__class__(self.x, self.y, self.depth, hval=self.__hash)

    def t_distances(self, relay, n1, n2):
        return t_distances(self, relay, n1, n2)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y and other.depth == self.depth

    def __hash__(self):
        return self.__hash


class RelayPosition(Point):
    """
    A potential position for a relay
    """
    def __init__(self, x=0., y=0., height=10., hval=None, chosen=False):
        super().__init__(x, y)
        self._height = height
        self.chosen = chosen
        if hval is None:
            self.__hash = hash((self.x, self.y, self.height))
        else:
            self.__hash = hval

    @property
    def height(self) -> float:
        return self._height

    def clone(self):
        return self.__class__(self.x, self.y, self.height, self.chosen)

    def t_distances(self, sensor, n1, n2):
        return t_distances(sensor, self, n1, n2)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y and other.height == self.height

    def __hash__(self):
        return self.__hash


def distance(p1: Point, p2: Point):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


__config = Config.get_instance()


def t_angles(sensor: SensorNode, relay: RelayPosition,
                n1=__config.get_air_refractive_index(), n2=__config.get_soil_refractive_index()):
    h_ug, h_ag = sensor.depth, relay.height
    dh = distance(sensor, relay)

    def equations(p):
        st = p[0]
        d1 = math.sqrt(1 - st ** 2)
        d2 = math.sqrt((n1 / n2) ** 2 - st ** 2)
        if d1 == 0.:
            d1 = 1e-5
        if d2 == 0.:
            d2 = 1e-5
        return h_ag * st / d1 + h_ug * st / d2 - dh

    results = least_squares(equations, 0.1, bounds=(0., 1.), ftol=1e-4, verbose=0)
    sin_t = results.x[0]
    sin_i = n2 / n1 * sin_t
    t_i, t_r = math.asin(sin_i), math.asin(sin_t)

    return t_i, t_r


def t_distances(sensor: SensorNode, relay: RelayPosition,
                n1=__config.get_air_refractive_index(), n2=__config.get_soil_refractive_index()):
    """
    Calculates EM wave transmission distances in soil & air between sensor and relay.
    Uses scipy.optimize.least_squares for root estimation.
    :param sensor: Selected sensor
    :param relay: Selected relay
    :param n1: Air refractive index
    :param n2: Soil refractive index
    :return: (d_ug, d_ag)
    """
    h_ug, h_ag = sensor.depth, relay.height
    t_i, t_r = t_angles(sensor, relay, n1, n2)

    d_ug = h_ug / math.cos(t_i)
    d_ag = h_ag / math.cos(t_r)
    return d_ug, d_ag


if __name__ == '__main__':
    s = SensorNode(722.721, 136.402)
    r = RelayPosition(159.405, 422.529)
    d1_, d2_ = t_distances(s, r, 1.55, 1.)
    print(d1_, d2_)
