import numpy as np

def replace_g_with_o(input_file, output_file):
    with open(input_file, 'r') as file:
        obj_content = file.read()

    # Replace 'g' with 'o' in the OBJ content
    modified_content = obj_content.replace('g ', 'o ')

    with open(output_file, 'w') as file:
        file.write(modified_content)

def area_of_triangle(v1, v2, v3):
    return 0.5 * np.linalg.norm(np.cross(v2 - v1, v3 - v1))

def is_triangle_aligned_with_axs(triangle):
    vertex = triangle[0].reshape(1,3)
    return np.all((triangle == vertex), axis=0)


def axes_of_triangles_overlap(triangle1, triangle2):
    axs1 = is_triangle_aligned_with_axs(triangle1)
    if not np.any(axs1): return None

    axs2 = is_triangle_aligned_with_axs(triangle2)
    if not np.any(axs2): return None

    if np.any(axs1 == axs2) and np.all(triangle1[:, axs1] == triangle2[:, axs2]):
        return np.argmax(axs1), triangle1[:, axs1][0][0]
    else: 
        return None  # Triangles do not overlap
    
def find_common_axis_value(obj1_vertices, obj1_faces, obj2_vertices, obj2_faces):
    for face1 in obj1_faces:
        for face2 in obj2_faces:
            # Extract vertices of the triangles
            tri1 = np.array((
                    np.array(obj1_vertices[face1[0]]), 
                    np.array(obj1_vertices[face1[1]]), 
                    np.array(obj1_vertices[face1[2]])))
            tri2 = np.array((
                    np.array(obj2_vertices[face2[0]]), 
                    np.array(obj2_vertices[face2[1]]), 
                    np.array(obj2_vertices[face2[2]])))
            
            ax = axes_of_triangles_overlap(tri1, tri2)

            if ax is not None:
                    return ax
    return None

def calculate_surface_area(vertices, faces):
    total_area = 0.0

    for face in faces:
        p1 = np.array(vertices[face[0]])
        p2 = np.array(vertices[face[1]])
        p3 = np.array(vertices[face[2]])

        area = area_of_triangle(p1, p2, p3)
        total_area += area

    return total_area

def calculate_intersection_area(obj1_vertices, obj1_faces, obj2_vertices, obj2_faces):
    intersection_area = 0.0

    ax = find_common_axis_value(obj1_vertices, obj1_faces, obj2_vertices, obj2_faces)

    if ax is not None:
        for face1 in obj1_faces:
            tri1 = np.array((
                        np.array(obj1_vertices[face1[0]]), 
                        np.array(obj1_vertices[face1[1]]), 
                        np.array(obj1_vertices[face1[2]])))
            if (np.all(tri1[:, ax[0]] == ax[1])):
                intersection_area += area_of_triangle(*tri1)

    return intersection_area