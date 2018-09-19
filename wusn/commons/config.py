from wusn.commons.parameters import Parameters
import math


class Config:
    def __init__(self):
        self.parameters = Parameters.get_instance()
        self.sensors = []
        self.relay_nodes = []

    config = None

    @staticmethod
    def get_instance():
        if Config.config is None:
            Config.config = Config()
        return Config.config

    @staticmethod
    def clear_instance():
        if Config.config is None:
            return
        Config.config = None

    def get_t_ug(self, d_ug):
        t_ug = 6.4 + 20 * math.log(d_ug, 2) + 20 * math.log(self.parameters.get_beta()) +\
            8.69 * self.parameters.get_alpha()*d_ug
        return t_ug

    def get_t_ag(self, d_ag):
        t_ag = -147.6 + 10 * self.parameters.attenuation_coef * math.log(d_ag, 2) +\
            20 * math.log(self.parameters.radio_freq, 2)
        return t_ag

    def get_trans_loss(self, d_ug, d_ag):
        return self.get_t_ug(d_ug) + self.get_t_ag(d_ag)

    def get_air_refractive_index(self):
        return self.parameters.refractive_index_n1

    def get_soil_refractive_index(self):
        return self.parameters.refractive_index_n2


def get_trans_loss(d_ug, d_ag):
    a_config = Config.get_instance()
    return a_config.get_trans_loss(d_ug, d_ag)


def get_air_refractive_index():
    return Config.get_instance().get_air_refractive_index()


def get_soil_refractive_index():
    return Config.get_instance().get_soil_refractive_index()