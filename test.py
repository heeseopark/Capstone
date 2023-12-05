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


newhand = Mesh('newhand.stl').translate('z',8).rotate('z', 90).print_values().render()

readyforsubtraction = newhand.save('readyforsubtraction.stl')

base = Mesh('wristbase.stl').scale(1/4).render()

subtract_stl('wristbase.stl', 'readyforsubtraction.stl', 'testresult.stl')

testresult = Mesh('testresult.stl').render()