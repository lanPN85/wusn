import gc
import math


class Parameters:
    """This class is used for setting up parameters
    This class is set as default for transmitting signals between soil and air

    Do not invoke the object directly -> use the get_instance() function instead
    """
    def __init__(self, burial_depth=1, height_of_relay=10, radio_freq=300,
                 volumetric_moisture_content=0.1, bulk_density=1.3,
                 density_of_particles=2.66, sand_mass_fractions=0.5,
                 clay_mass_fractions=0.15, attenuation_coef=3, refractive_index_n1=1.55,
                 refractive_index_n2=1, number_of_sensors=200, number_of_relays=20,
                 possible_locations=200):
        self.burial_depth = burial_depth  # d_sn
        self.height_of_relay = height_of_relay  # h_rn
        self.radio_freq = radio_freq  # f
        self.volumetric_moisture_content = volumetric_moisture_content  # m_v
        self.bulk_density = bulk_density  # p_b
        self.density_of_particles = density_of_particles  # p_s
        self.sand_mass_fractions = sand_mass_fractions  # S
        self.clay_mass_fractions = clay_mass_fractions  # C
        self.attenuation_coef = attenuation_coef  # nuy
        self.refractive_index_n1 = refractive_index_n1  # n1
        self.refractive_index_n2 = refractive_index_n2  # n2
        self.number_of_sensors = number_of_sensors  # N
        self.number_of_relays = number_of_relays  # Y
        self.possible_locations = possible_locations  # M
        # constant
        self.alpha_1 = 0.65
        self.muy = 12.57 * math.pow(10, -7)
        self.water_relax_time = 2  # 2 - 4
        self.temperature = 20  # in c
        self.high_frequency_limit = -1.0  # e from w to infinity
        self.static_dielectric_water = 80.36  # e from w to 0
        # Calculated items
        self.real_dcs = -1.0
        self.imaginary_dcs = -1.0
        self.alpha = -1.0
        self.beta = -1.0
        self.beta1 = -1.0
        self.beta2 = -1.0
        self.real_dcfw = -1.0
        self.imaginary_dcfw = -1.0
        self.effective_conductivity = -1.0
        self.relative_permittivity = -1.0

    parameter = None

    @staticmethod
    def get_instance():
        if Parameters.parameter is None:
            Parameters.parameter = Parameters()
        return Parameters.parameter

    @staticmethod
    def clear_instance():
        if Parameters.parameter is None:
            return
        Parameters.parameter = None
        gc.collect()

    m0 = 1.256 * 1e-7

    def get_alpha(self):
        if self.alpha == -1.0:
            self.alpha = 2 * math.pi * self.radio_freq * math.sqrt(self.muy * self.m0 *
                                                                   self.get_real_dcs() * 1/2 * (
                                                                        math.sqrt(1 + math.pow(self.get_imaginary_dcs()
                                                                                               /
                                                                                               self.get_real_dcs(), 2) -
                                                                                  1)
                                                                   ))
        return self.alpha

    def get_beta(self):
        if self.beta == -1.0:
            self.beta = 2 * math.pi * self.radio_freq * math.sqrt(self.muy * self.m0 *
                                                                  self.get_real_dcs() * 1/2 * (
                                                                        math.sqrt(1 + math.pow(self.get_imaginary_dcs()
                                                                                               /
                                                                                               self.get_real_dcs(), 2) +
                                                                                  1)
                                                                   ))
        return self.beta

    def get_real_dcs(self):
        if self.real_dcs == -1.0:
            self.real_dcs = 1.15 * math.pow(1 + (self.bulk_density/self.density_of_particles)
                                            * math.pow(self.get_relative_permittivity(), self.alpha_1) +
                                            math.pow(self.volumetric_moisture_content, self.get_beta1()) *
                                            math.pow(self.get_real_dcfw(), self.alpha_1) -
                                            self.volumetric_moisture_content, 1/self.alpha_1) - 0.68
        return self.real_dcs

    def get_imaginary_dcs(self):
        if self.imaginary_dcs == -1.0:
            self.imaginary_dcs = math.pow(math.pow(self.volumetric_moisture_content,
                                                   self.get_beta2()) * math.pow(self.get_imaginary_dcfw(),
                                                                                self.alpha_1), 1/self.alpha_1)
        return self.imaginary_dcs

    def get_relative_permittivity(self):
        if self.relative_permittivity == -1.0:
            self.relative_permittivity = math.pow(1.01 + 0.44 * self.bulk_density, 2) - 0.062
        return self.relative_permittivity

    def get_beta1(self):  # beta'
        if self.beta1 == -1.0:
            self.beta1 = 1.2748 - 0.519 * self.sand_mass_fractions - 0.152 * self.clay_mass_fractions
        return self.beta1

    def get_beta2(self):  # beta''
        if self.beta2 == -1.0:
            self.beta2 = 1.33797 - 0.603 * self.sand_mass_fractions - 0.166 * self.clay_mass_fractions
        return self.beta2

    def get_real_dcfw(self):  # formulation 6 in paper
        if self.real_dcfw == -1.0:
            self.real_dcfw = self.get_high_frequency_limit() + \
                             (self.static_dielectric_water - self.get_high_frequency_limit()) / \
                             (1 + math.pow(2 * math.pi * self.radio_freq * self.get_effective_conductivity(),
                                           2))
        return self.real_dcfw

    def get_imaginary_dcfw(self):  # formulation 7 in paper
        if self.imaginary_dcfw == -1.0:
            first = (2 * math.pi * self.radio_freq * self.water_relax_time *
                     (self.static_dielectric_water - self.get_high_frequency_limit())) / \
                    (1 + math.pow(2 * math.pi * self.radio_freq * self.water_relax_time,2))

            second = self.get_effective_conductivity() * (self.density_of_particles - self.bulk_density) / (2 * math.pi * self.static_dielectric_water * self.radio_freq *
             self.density_of_particles * self.volumetric_moisture_content)

            self.imaginary_dcfw = first + second
        return self.imaginary_dcfw

    def get_high_frequency_limit(self):
        if self.high_frequency_limit == -1.0:
            self.high_frequency_limit = 38 - 5 * (self.temperature + 273)/300
        return self.high_frequency_limit

    def get_effective_conductivity(self):
        if self.effective_conductivity == -1.0:
            self.effective_conductivity = 0.0467 + 0.2204*self.bulk_density - \
                self.sand_mass_fractions * 0.411 + self.clay_mass_fractions * 0.6614
        return self.effective_conductivity

#
# parameters = Parameters.get_instance()
# print("high frequency limit of relative dielectric constant of free water : " + str(parameters.get_high_frequency_limit()))
# print("effective conductivity : " + str(parameters.get_effective_conductivity()))
# print("real dcfw : " + str(parameters.get_real_dcfw()))
# print("imm dcfw : " + str(parameters.get_imaginary_dcfw()))
# print("beta' : " + str(parameters.get_beta1()))
# print("beta'': " + str(parameters.get_beta2()))
# print("relative permittivity of sol solid : " + str(parameters.get_relative_permittivity()))
# print("real dcs", parameters.get_real_dcs())
# print("imm dcs : ", parameters.get_imaginary_dcfw())
# print("get alpha : " , parameters.get_alpha())
# print("get beta : ", parameters.get_beta())