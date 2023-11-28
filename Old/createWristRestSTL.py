from stl import mesh
import numpy as np
import plotly.graph_objects as go

def find_reference_point(stl_mesh):
    # Calculate the centroid of the mesh
    return np.mean(stl_mesh.points.reshape(-1, 9).reshape(-1, 3), axis=0)

def calculate_rotation_matrix(from_direction, to_direction):
    # Calculate the rotation matrix required to align two vectors
    v = np.cross(from_direction, to_direction)
    c = np.dot(from_direction, to_direction)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

def apply_transform(stl_mesh, transform_matrix):
    # Apply a transformation matrix to the mesh
    for point in stl_mesh.points:
        for i in range(3):
            point[i*3:i*3+3] = np.dot(transform_matrix, point[i*3:i*3+3])

def stl2mesh3d(stl_mesh):
    p, q, r = stl_mesh.vectors.shape
    vertices, ixr = np.unique(stl_mesh.vectors.reshape(p*q, r), return_inverse=True, axis=0)
    I = np.take(ixr, [3*k for k in range(p)])
    J = np.take(ixr, [3*k+1 for k in range(p)])
    K = np.take(ixr, [3*k+2 for k in range(p)])
    return vertices, I, J, K

def render_stl_to_html(stl_file_path, html_file_name, html_title):
    # Load STL file
    my_mesh = mesh.Mesh.from_file(stl_file_path)

    # Extract vertices and faces for Plotly Mesh3D
    vertices, I, J, K = stl2mesh3d(my_mesh)
    x, y, z = vertices.T

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
    fig.write_html(html_file_name, auto_open=True)

# Load STL files
left_arm = mesh.Mesh.from_file('left_arm.stl')
right_arm = mesh.Mesh.from_file('right_arm.stl')
wrist_rest_base = mesh.Mesh.from_file('wrist_rest_base.stl')

render_stl_to_html('wrist_rest_base.stl', 'wrist_rest_base.html', 'wrist_rest_base')

# Assume you have a way to find the reference points for the cylinders on the wrist rest base
left_cylinder_ref_point = find_reference_point(...)  # Define this
right_cylinder_ref_point = find_reference_point(...) # Define this

# Align the Left Arm
left_arm_ref_point = find_reference_point(left_arm)
left_translation = left_cylinder_ref_point - left_arm_ref_point
left_translation_matrix = np.eye(4)
left_translation_matrix[:3, 3] = left_translation
apply_transform(left_arm, left_translation_matrix)

# Similarly for Right Arm
right_arm_ref_point = find_reference_point(right_arm)
right_translation = right_cylinder_ref_point - right_arm_ref_point
right_translation_matrix = np.eye(4)
right_translation_matrix[:3, 3] = right_translation
apply_transform(right_arm, right_translation_matrix)

# Export Aligned Models
left_arm.save('aligned_left_arm.stl')
right_arm.save('aligned_right_arm.stl')
