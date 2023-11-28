import plotly.graph_objects as go
import numpy as np
import trimesh

def stl2mesh3d(tri_mesh):
    # Extract vertices and faces for Plotly Mesh3D
    vertices = np.array(tri_mesh.vertices)
    faces = np.array(tri_mesh.faces)
    x, y, z = vertices.T
    I, J, K = faces.T
    return x, y, z, I, J, K

my_mesh = trimesh.load("model1.stl")

# Extract vertices and faces for Plotly Mesh3D
x, y, z, I, J, K = stl2mesh3d(my_mesh)

# Define colorscale
colorscale = [[0, '#e5dee5'], [1, '#e5dee5']]

# Create Mesh3D object
mesh3D = go.Mesh3d(
    x=x,
    y=y,
    z=z, 
    i=I, 
    j=J, 
    k=K, 
    flatshading=True,
    colorscale=colorscale, 
    intensity=z, 
    name='Mesh3D',
    showscale=False
)

# Create Figure object
fig = go.Figure(data=[mesh3D])

# Update layout
fig.update_layout(
    paper_bgcolor='rgb(1,1,1)',
    title_text="html_title", title_x=0.5,
    font_color='white',
    width=1200,
    height=1200,
    scene_camera=dict(eye=dict(x=1.25, y=-1.25, z=1)),
    scene_xaxis_visible=False,
    scene_yaxis_visible=False,
    scene_zaxis_visible=False
)

# Show the figure
fig.show()