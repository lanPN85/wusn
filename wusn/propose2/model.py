from deap import base, creator

creator.create('FitnessMin', base.Fitness, weights=(-1.,))

# creator.create("Individual", list, fitness=creator.FitnessMin,
#                sensor_count=None, relay_count=None, max_loss=int, max_pair=tuple)

FitnessMin = creator.FitnessMin


class Individual(list):
    def __init__(self, other=None, sensor_count=None, relay_count=None, fitness=None):
        if other is None:
            super().__init__()
        else:
            super().__init__(other)
        if fitness is None:
            fitness = FitnessMin()

        self.fitness = fitness
        self.sensor_count = sensor_count
        self.relay_count = relay_count

    def clone(self):
        ret = Individual(self, sensor_count=self.sensor_count, relay_count=self.relay_count)
        ret.fitness.values = self.fitness.values
        return ret

    def __add__(self, other):
        return Individual(super().__add__(other), self.sensor_count, self.relay_count)

    def __mul__(self, other):
        return Individual(super().__mul__(other), self.sensor_count, self.relay_count)

    def __getitem__(self, item):
        if isinstance(item, slice):
            ls = super().__getitem__(item)
            return Individual(ls, self.sensor_count, self.relay_count)
        return super().__getitem__(item)


# For testing only
if __name__ == '__main__':
    ind = Individual([1, 2, 3, 4])
