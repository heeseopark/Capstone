import trimesh

# Load the STL file
mesh = trimesh.load('hand.stl')

# Define the scaling factor
scale_factor = 100

# Apply the scaling transformation to the mesh
# This will scale the mesh uniformly in all directions (X, Y, and Z)
mesh.apply_scale(scale_factor)

# Save the scaled mesh as a new STL file
mesh.export('scaledhand.stl')
