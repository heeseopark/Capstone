import pyvista as pv
from meshclass import *

def subtract_stl(file1, file2, result_file):
    # Load the STL files
    mesh1 = pv.read(file1)
    mesh2 = pv.read(file2)

    # Perform the Boolean subtraction
    result_mesh = mesh1.boolean_difference(mesh2)

    # Save the result
    result_mesh.save(result_file)


hand = Mesh('hand.stl').scale(20).smoothen().run_pca().rotate('x',-90).rotate('z',180).print_values().render().scale(1/20)

scale_factor = 68 / float(hand.width)

print("scale factor: " + str(scale_factor))

hand.scale(scale_factor).translate('z', -hand.min_z_value).save('new3DModel.stl')

newhand = Mesh('newhand.stl').translate('z', 10).print_values()

readyforsubtraction = newhand.save('readyforsubtraction.stl')

base = Mesh('circlebase.stl').print_values()

subtract_stl('circlebase.stl', 'readyforsubtraction.stl', 'testresult.stl')

testresult = Mesh('testresult.stl').render()