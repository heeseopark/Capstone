import FreeCAD as App
import Part
import Mesh

# Load FreeCAD and set up a document
App.newDocument("Unnamed")

# Load STL file
mesh = App.ActiveDocument.addObject("Mesh::Feature", "Mesh")
mesh_path = "C:/Users/heeseopark/Desktop/Capstone Project/Low-Poly Bulbasaur - Remastered - 6231486/files/bulbasaur_lowpoly_remastered_flowalistik.STL"
mesh.Mesh = Mesh.read(mesh_path)

# Create a shape from the mesh
shape = Part.Shape()
shape.makeShapeFromMesh(mesh.Mesh.Topology, 0.1)  # Tolerance

# Create a solid from the shape
solid = Part.makeSolid(shape)

# Export to STEP
Part.export([solid], "C:/Users/heeseopark/Desktop/Capstone Project/file.step")
