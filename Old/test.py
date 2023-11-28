import trimesh
import numpy as np
import plotly.graph_objects as go
import pyvista as pv

def stl2mesh3d(tri_mesh):
    # Extract vertices and faces for Plotly Mesh3D
    vertices = np.array(tri_mesh.vertices)
    faces = np.array(tri_mesh.faces)
    x, y, z = vertices.T
    I, J, K = faces.T
    return x, y, z, I, J, K

def render_stl_to_html(stl_file_path, html_file_name, html_title):
    # Load STL file using trimesh
    my_mesh = trimesh.load(stl_file_path)

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

    # Define layout
    layout = go.Layout(
        paper_bgcolor='rgb(1,1,1)',
        title_text=html_title, title_x=0.5,
        font_color='white',
        width=1200,
        height=1200,
        scene_camera=dict(eye=dict(x=1.25, y=-1.25, z=1)),
        scene_xaxis_visible=False,
        scene_yaxis_visible=False,
        scene_zaxis_visible=False
    )

    # Create figure
    fig = go.Figure(data=[mesh3D], layout=layout)

    # Update lighting
    fig.data[0].update(lighting=dict(ambient=0.18, diffuse=1, fresnel=0.1, specular=1, roughness=0.1, facenormalsepsilon=0))
    fig.data[0].update(lightposition=dict(x=3000, y=3000, z=10000))

    # Save to HTML
    fig.write_html(html_file_name + '.html', auto_open=True)



# Example usage:
base = 'Low-Poly Bulbasaur - Remastered - 6231486/files/bulbasaur_lowpoly_remastered_flowalistik.stl'
cylinder = 'cylinder.stl'



import pyvista as pv

# Read the STL files
mesh1 = pv.read(base)
mesh2 = pv.read(cylinder).scale([0.5,0.5,0.5])

# Perform boolean subtraction
result = mesh1.boolean_difference(mesh2)

# Save the resulting mesh
result.save('subtracted.stl')

