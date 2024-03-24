from utils import *
from FiniteElementModel import *
from pywavefront import Wavefront

class ObjFileParser:

    @staticmethod
    def parse_obj_to_finite_element_model(model_path, log_to_console=False) -> FiniteElementModel:
        # Specify the input and output file paths
        input_obj_file = model_path
        output_obj_file = model_path
        # Prepare .obj file for correct parse by Wavefront package
        replace_g_with_o(input_obj_file, output_obj_file)
        
        # Load the Wavefront object
        obj_file_path =  model_path
        wavefront = Wavefront(obj_file_path, collect_faces=True)

        n_obj = wavefront.mesh_list.__len__()

        intersection_matrix = np.zeros((n_obj, n_obj))
        full_surfaces = np.zeros(n_obj)

        # fix enumeration 
        mesh_list = np.array(wavefront.mesh_list)
        mesh_list[[2, 3]] = mesh_list[[3, 2]]

        # Iterate over each object in the mesh list
        for obj_idx, obj in enumerate(mesh_list):
            obj_vertices = wavefront.vertices
            obj_faces = obj.faces

            obj_surface_area = calculate_surface_area(obj_vertices, obj_faces)
            if log_to_console: print(f"Full surface area of Object {obj_idx + 1}: {obj_surface_area}")

            full_surfaces[obj_idx] = obj_surface_area

            # Calculate intersection area with other objects
            for other_obj_idx, other_obj in enumerate(mesh_list):
                other_obj_vertices = wavefront.vertices
                other_obj_faces = other_obj.faces

                if (obj_idx == other_obj_idx):
                    intersection_matrix[obj_idx, other_obj_idx] = 0
                    continue

                intersection_area = calculate_intersection_area(obj_vertices, obj_faces, other_obj_vertices, other_obj_faces)

                if intersection_matrix[obj_idx, other_obj_idx] == 0:
                    intersection_matrix[obj_idx, other_obj_idx] = intersection_area
                elif intersection_matrix[obj_idx, other_obj_idx] > intersection_area:
                    intersection_matrix[obj_idx, other_obj_idx] = intersection_area

                if intersection_matrix[other_obj_idx, obj_idx] == 0:
                    intersection_matrix[other_obj_idx, obj_idx] = intersection_area
                elif intersection_matrix[other_obj_idx, obj_idx] > intersection_area:
                    intersection_matrix[other_obj_idx, obj_idx] = intersection_area

                if log_to_console: 
                    print("== Intersection matrix ==")
                    for i in range(n_obj):
                        for j in range(n_obj):
                            print(f"{str(intersection_matrix[i, j])[:5]}", end=" ")
                        print('\n')

        return FiniteElementModel(full_surfaces, intersection_matrix)