import numpy as np
from FiniteElementModel import *
from utils import * 

class HeatBalanceEquation:
    def __init__(self, fe_model: FiniteElementModel) -> None:
        self.fe_model = fe_model

    def equation(self, t, y, a=0.1):
        Q_TC = np.zeros((self.fe_model.n_elem, self.fe_model.n_elem))

        y_i = np.tile(y, (5, 1))
        y_j = y_i.T

        k_ij = self.fe_model.thermal_conductivity_matrix * self.fe_model.intersection_matrix

        Q_TC += k_ij * (y_i - y_j)

        c0 = 5.67
        Q_E = - self.fe_model.emissivity * self.fe_model.surfaces * c0 * ((y / 100) ** 4)
        Q_R = np.array([string_to_function(str_fun, a) 
                        for str_fun in self.fe_model.heat_fluxes])

        eq = (np.sum(Q_TC, axis=1) + Q_E + 
              np.array([Q_R_i(t) for Q_R_i in Q_R])) / self.fe_model.coeffs

        return eq