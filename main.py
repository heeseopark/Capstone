from meshclass import *

hand = Mesh('hand.stl')

scale_factor = 68 / (hand.width)

hand.scale(scale_factor).save('newhand.stl')

newhand = Mesh('newhand.stl')

newhand.print_values()

newhand.flip().save('translated.stl')

translatedhand = Mesh('translated.stl').print_values()

translatedhand.change_origin_to_wrist().save('changeorigin.stl')

changeorigin = Mesh('changeorigin.stl').smoothen().print_values()

# changeorigin.translate_z_direction()

import numpy as np
import trimesh
from scipy.spatial import KDTree

def find_overlapping_vertices(mesh1, mesh2, tolerance=1e-6):
    """
    Find vertices in mesh1 that overlap with any vertex in mesh2.
    """
    tree = KDTree(mesh2.vertices)
    overlapping = tree.query_ball_point(mesh1.vertices, r=tolerance)
    overlapping_indices = [i for i, points in enumerate(overlapping) if len(points) > 0]
    print(overlapping_indices)
    return overlapping_indices

def remove_above_points(mesh, reference_indices, axis='z'):
    """
    Remove vertices in 'mesh' that are 'above' vertices with indices in 'reference_indices'.
    'Above' is determined by the higher value along the specified axis.
    """
    if not reference_indices:  # Check if reference_indices is empty
        print("No overlapping vertices found. No points to remove.")
        return mesh

    reference_heights = mesh.vertices[reference_indices, {'x': 0, 'y': 1, 'z': 2}[axis]]
    max_height = np.max(reference_heights)
    to_keep = mesh.vertices[:, {'x': 0, 'y': 1, 'z': 2}[axis]] <= max_height
    return mesh.update_vertices(mesh.vertices[to_keep])

# Load STL files
finalhand = trimesh.load('changeorigin.stl')
base = trimesh.load('wristbase.stl')

# Find overlapping vertices
overlapping_indices = find_overlapping_vertices(finalhand, base)

print(f"Number of overlapping vertices found: {len(overlapping_indices)}")

# Remove points above the overlapping points
result_mesh = remove_above_points(finalhand, overlapping_indices)

# Show the resulting mesh
result_mesh.show()


# result_mesh = base.mesh.difference(finalhand.mesh, engine='blender')
