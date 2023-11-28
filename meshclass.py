import trimesh
from sklearn.decomposition import PCA
import numpy as np

class Mesh:
    def __init__(self, meshfile):
        self.meshfile = meshfile
        self.mesh = trimesh.load(meshfile)
        self.max_z_value = self.get_max_z_value()  # Initialize max Z value
        self.width = 0
        self.origin = 0
    
    def update_max_z_value(self):
        # Update the maximum Z value
        self.max_z_value = self.get_max_z_value()
    
    def flip_z_axis(self):
        transformation_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ])
        self.mesh.apply_transform(transformation_matrix)
        self.update_max_z_value()  # Update max Z value after transformation
        return self
    
    def save(self, filename=None):
        # If no filename is provided, use the original file name
        if filename is None:
            filename = self.meshfile
        self.mesh.export(filename)

    def render(self):
            # Get vertices
            vertices = np.array(self.mesh.vertices)

            # Compute PCA
            pca = PCA(n_components=3)
            pca.fit_transform(vertices)

            # Align mesh model with axis
            angle_0 = np.arccos(np.clip(np.dot([0, 0, 1], pca.components_[0]), -1.0, 1.0))
            direction_0 = np.cross(pca.components_[0], [0, 0, 1])
            rotation_matrix_0 = trimesh.transformations.rotation_matrix(angle=angle_0, direction=direction_0)
            self.mesh.apply_transform(rotation_matrix_0)

            axis_1 = pca.components_[1]
            axis_1 = np.array([axis_1[0], axis_1[1], axis_1[2], 0])
            axis_1 = np.dot(rotation_matrix_0, axis_1)
            axis_1 = axis_1[:3]
            angle_1 = np.arccos(np.clip(np.dot([1, 0, 0], axis_1), -1.0, 1.0))
            direction_1 = np.cross([1, 0, 0], axis_1)
            rotation_matrix_1 = trimesh.transformations.rotation_matrix(angle=angle_1, direction=direction_1)
            self.mesh.apply_transform(rotation_matrix_1)

            # Add axes to the scene
            axes = trimesh.creation.axis(transform=trimesh.transformations.identity_matrix(), axis_length=200, axis_radius=2)
            scene = self.mesh.scene()
            scene.add_geometry(axes)

            # Show scene
            scene.show()

    def get_max_z_value(self):
        # Return the maximum Z value from the mesh vertices
        return np.max(self.mesh.vertices[:, 2])

    def translate_z_direction(self, translation_amount):
        translation_matrix = trimesh.transformations.translation_matrix([0, 0, translation_amount])
        self.mesh.apply_transform(translation_matrix)
        self.update_max_z_value()
        return self

    def scale(self, scale_factor):
        # Apply the scaling to the mesh
        self.mesh.apply_scale(scale_factor)
        self.update_max_z_value()  # Update max Z value after scaling

        # Return self for method chaining if needed
        return self

    def get_wrist(self):

        vertices = self.mesh.vertices
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

            tmp_vertices_ = vertices[vertices[:,2].min()+length*(i-1.5)/100<=vertices[:,2]]
            tmp_vertices_ = tmp_vertices_[tmp_vertices_[:,2]<=vertices[:,2].min()+length*(i-0.5)/100]
            tmp_ = (tmp_vertices_[:,0].max()-tmp_vertices_[:,0].min())

            if tmp < var_min and tmp*1.08 < tmp_:
                var_min = tmp
                var_mini = i
                x = (tmp_vertices[:,0].max()+tmp_vertices[:,0].min()) / 2
                y = tmp_vertices[:,1].max()
                width = (tmp_vertices[:,0].max()-tmp_vertices[:,0].min())

        z = vertices[:,2].min() + var_mini * length / 100
        self.origin = (x,y,z)
        self.width = width

        return self


    
    def change_origin_to_wrist(self,ori):
        self.mesh.apply_translation([-ori[0],-ori[1],-ori[2]])
        return self
