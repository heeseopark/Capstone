from meshclass import *

hand = Mesh('hand.stl').run_pca().smoothen().print_values().render()

scale_factor = 68 / float(hand.width)

print("scale factor: " + str(scale_factor))

hand.scale(scale_factor).save('newhand.stl')

newhand = Mesh('newhand.stl').print_values().render()

base = Mesh('wristbase.stl').rotate('z', 90).render()

import trimesh

def subtract_stl(file1, file2, output_file):
    # Load the STL files
    mesh1 = trimesh.load_mesh(file1)
    mesh2 = trimesh.load_mesh(file2)

    # Perform the subtraction
    subtracted_mesh = mesh1.difference(mesh2, engine='scad')

    # Save the resulting mesh
    subtracted_mesh.export(output_file)

# Example usage
subtract_stl('wristbase.stl', 'newhand.stl', 'product.stl')

product = Mesh('product.stl')