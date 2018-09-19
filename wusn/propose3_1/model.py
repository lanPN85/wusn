from deap import base, creator

from wusn.propose2.model import FitnessMin


class Individual(list):
    def __init__(self, other=None, fitness=None):
        if other is None:
            super().__init__()
        else:
            super().__init__(other)
        if fitness is None:
            fitness = FitnessMin()

        self.fitness = fitness

    def __add__(self, other):
        return Individual(super().__add__(other))

    def __mul__(self, other):
        return Individual(super().__mul__(other))

    def __hash__(self):
        return hash(tuple(self))

    def clone(self):
        ret = Individual(self)
        ret.fitness.values = self.fitness.values
        return ret

    def __getitem__(self, item):
        if isinstance(item, slice):
            ls = super().__getitem__(item)
            return Individual(ls)
        return super().__getitem__(item)


# For testing only
if __name__ == '__main__':
    ind = Individual([1, 2, 3, 4])
