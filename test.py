import trimesh
from meshclass import *

hand = trimesh.load('hand.stl').scene().show()

print(Mesh('hand.stl').width)

Mesh('hand.stl').render()