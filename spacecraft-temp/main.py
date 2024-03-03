from pywavefront import Wavefront
from utils import *

model_path = "model2.obj"

# Load the Wavefront object
obj_file_path =  model_path
wavefront = Wavefront(obj_file_path, collect_faces=True)

# Iterate over each object in the mesh list
for obj_idx, obj in enumerate(wavefront.mesh_list):
    obj_vertices = wavefront.vertices
    obj_faces = obj.faces

    obj_surface_area = calculate_surface_area(obj_vertices, obj_faces)
    print(f"Surface area of Object {obj_idx + 1}: {obj_surface_area}")

    # Calculate intersection area with other objects
    for other_obj_idx, other_obj in enumerate(wavefront.mesh_list[obj_idx + 1:]):
        other_obj_vertices = wavefront.vertices
        other_obj_faces = other_obj.faces

        intersection_area = calculate_intersection_area(obj_vertices, obj_faces, other_obj_vertices, other_obj_faces)
        print(f"Intersection area between Object {obj_idx + 1} and Object {obj_idx + 2 + other_obj_idx}: {intersection_area}")