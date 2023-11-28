import trimesh
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

def matplotlib_3d_ptcloud(data, k = None):
    xdata = data[:,0].squeeze()
    ydata = data[:,1].squeeze()
    zdata = data[:,2].squeeze()

    fig = plt.figure(figsize=(15, 15))
    ax = plt.axes(projection='3d')
    plt.axis('scaled')
    
    ax.scatter3D(xdata, ydata, zdata, marker='o')
    if k != None:
        ax.scatter3D([k[0]/10 for i in range(10)], [k[1]/10+i/10.0 for i in range(10)], [k[2]/10 for i in range(10)], marker='^')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_ylabel('Z')
    plt.show()

def get_centroid(vertices):

    th = (vertices[:,1].max())*0.5+(vertices[:,1].min())*0.5
    vertices = vertices[vertices[:,1]>th]
    length = vertices[:,2].max()-vertices[:,2].min()
    var_min = 100000000
    var_mini = 0
    width = 0
    for i in range(20,80):

        tmp_vertices = vertices[vertices[:,2].min()+length*(i-0.5)/100<=vertices[:,2]]
        tmp_vertices = tmp_vertices[tmp_vertices[:,2]<=vertices[:,2].min()+length*(i+0.5)/100]
        tmp = (tmp_vertices[:,0].max()-tmp_vertices[:,0].min())
        print(i,tmp,tmp_vertices[:,0].std(),tmp_vertices[:,1].std())


        tmp_vertices_ = vertices[vertices[:,2].min()+length*(i-1.5)/100<=vertices[:,2]]
        tmp_vertices_ = tmp_vertices_[tmp_vertices_[:,2]<=vertices[:,2].min()+length*(i-0.5)/100]
        tmp_ = (tmp_vertices_[:,0].max()-tmp_vertices_[:,0].min())

        if tmp < var_min and tmp*1.08 < tmp_:
            var_min = tmp
            var_mini = i
            x = (tmp_vertices[:,0].max()+tmp_vertices[:,0].min()) / 2
            y = tmp_vertices[:,1].max()
            width = (tmp_vertices[:,1].max()-tmp_vertices[:,1].min())

    print(var_mini)

    z = vertices[:,2].min() + var_mini * length / 100

    return (x,y,z), width

# load mesh
mesh = trimesh.load('3DModel.stl')

# smooth mesh
smoothed_mesh = trimesh.smoothing.filter_laplacian(mesh)

# create scene
scene = smoothed_mesh.scene()

# get vertices
vertices = np.array(smoothed_mesh.vertices)
# matplotlib_3d_ptcloud(vertices/10)

# compute PCA
pca = PCA(n_components=3) # 주성분을 몇개로 할지 결정
pca.fit_transform(vertices)

# create cylinders
cylinder_x = trimesh.creation.cylinder(radius=0.1, height=10.0)
cylinder_x.visual.face_colors = [1, 0, 0, 0.5]
cylinder_y = trimesh.creation.cylinder(radius=0.1, height=10.0)
cylinder_y.visual.face_colors = [0, 1, 0, 0.5]
cylinder_z = trimesh.creation.cylinder(radius=0.1, height=10.0)
cylinder_z.visual.face_colors = [0, 0, 1, 0.5]

# align cylinders with axis
rotation_matrix_y = trimesh.transformations.rotation_matrix(angle= np.pi/2, direction=[1, 0, 0])
cylinder_y.apply_transform(rotation_matrix_y)
rotation_matrix_x = trimesh.transformations.rotation_matrix(angle= np.pi/2, direction=[0, 1, 0])
cylinder_x.apply_transform(rotation_matrix_x)

# align mesh model with axis
angle_0 = np.arccos(np.dot([0, 0, 1], pca.components_[0]))
direction_0 = np.cross(pca.components_[0], [0, 0, 1])
rotation_matrix_0 = trimesh.transformations.rotation_matrix(angle=angle_0, direction=direction_0)
smoothed_mesh.apply_transform(rotation_matrix_0)

axis_1 = pca.components_[1]
axis_1 = np.array([axis_1[0], axis_1[1], axis_1[2], 0])
axis_1 = np.dot(rotation_matrix_0, axis_1)
axis_1 = axis_1[:3]
angle_1 = np.arccos(np.dot([1, 0, 0], axis_1))
direction_1 = np.cross([1, 0, 0], axis_1)
rotation_matrix_1 = trimesh.transformations.rotation_matrix(angle=angle_1, direction=direction_1)
smoothed_mesh.apply_transform(rotation_matrix_1)



#100 25

# add geometry to scene
scene.add_geometry(cylinder_x)
scene.add_geometry(cylinder_y)
scene.add_geometry(cylinder_z)



vertices = np.array(smoothed_mesh.vertices)
(x,y,z),w = get_centroid(vertices)

smoothed_mesh.apply_translation([-x,-y,-z])

scale = 68/w

smoothed_mesh.apply_transform(trimesh.transformations.scale_matrix(scale))

scene.show()
