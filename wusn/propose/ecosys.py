from wusn.commons.input import WusnInput
from wusn.propose.python_datastructure.graph import *
from wusn.propose.peripheral import *


class EcoSys:
    def __init__(self):
        self.sensors = []
        self.relays = []
        self.poss_locations = []
        self.relays_num = 0
        self.file_path = ""
        self.wusn_input = WusnInput()
        self.graph = Graph()
        self.poss_num = 0
        self.sensors_num = 0

    eco_sys = None

    @classmethod
    def get_instance(cls):
        if EcoSys.eco_sys is None:
            EcoSys.eco_sys = EcoSys()
        return EcoSys.eco_sys

    @classmethod
    def clear_instance(cls):
        EcoSys.eco_sys = None

    def set_up(self):
        self.sensors = self.wusn_input.sensors[:]
        self.poss_locations = self.wusn_input.relays[:]
        self.relays_num = self.wusn_input.relay_num
        self.sensors_num = len(self.sensors)
        self.poss_num = len(self.poss_locations)

    def set_input(self, file_path: str):
        self.wusn_input = WusnInput.from_file(file_path)
        self.set_up()
        self.set_graph()

    def set_graph(self):
        self.graph = set_graph(self.sensors, self.poss_locations, self.relays_num, self.wusn_input.loss)




# test setup
# if __name__ == '__main__':
#     eco = EcoSys.get_instance()
#     eco.set_input("data/001.test")
