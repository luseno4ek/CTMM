from utils import *
from ObjParser import *

# ------ BEGIN CONSTANTS ------

model_path = "model2.obj"
params_path = "parameters.json"

# ------ END CONSTANTS ------


# ------ BEGIN MAIN ------

# parse obj-file to FiniteElementModel
fe_model = ObjFileParser.parse_obj_to_finite_element_model(model_path)
# read parameters from json-file
fe_model.read_params_from_file(params_path)

# ------ END MAIN ------
