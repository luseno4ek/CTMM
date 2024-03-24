import numpy as np
import json

class FiniteElementModel:
    """
    Class to store finite element model
    """

    def __init__(self, 
                 full_surfaces, 
                 intersection_matrix,  
                 emissivity = None,
                 thermal_conductivity_matrix = None,
                 heat_fluxes = None,
                 coeffs = None) -> None:
        """
        Initialization of the finite element (FE) model

        Args:
            full_surfaces (np.array of shape (n_obj,)): array of full surfaces of FE
            intersection_matrix (np.array of shape (n_obj, n_obj)): matrix of surfaces of FE intersections
            emissivity (np.array of shape (n_obj,), optional): array of emissivity values of FE. Defaults to None.
            thermal_conductivity_matrix (np.array of shape (n_obj, n_obj), optional): matrix of thermal . Defaults to None.
            heat_fluxes (np.array of shape (n_obj,), optional): array of heat flux functions for FE. Defaults to None.
            coeffs (np.array of shape (n_obj,), optional): array of coefficients for the heat balance equation for FE. Defaults to None.
        """
        self.coeffs = coeffs
        self.emissivity = emissivity
        self.heat_fluxes = heat_fluxes
        self.intersection_matrix = intersection_matrix
        self.thermal_conductivity_matrix = thermal_conductivity_matrix
        self.surfaces = full_surfaces - np.sum(intersection_matrix, axis=0)
        
        
    def read_params_from_file(self, path) -> None:
        """
        Read FE parameters for the heat balance equation from json-file by given path

        Args:
            path (string): path to json-file
        """        
        f = open(path)
        data = json.load(f)
        self.coeffs = np.array(data["coeffs"])
        self.emissivity = np.array(data["emissivity"])
        self.heat_fluxes = np.array(data["heat_fluxes"])
        self.thermal_conductivity_matrix = np.array(data["thermal_conductivity"])
        f.close()